#!/usr/bin/env python

import argparse
import configparser
import datetime
import os
import sys

from draftable import Client as DraftableClient
from draftable.endpoints.comparisons.sides import make_side
from draftable.endpoints.exceptions import InvalidArgument, InvalidPath, NotFound

DESCRIPTION = "Create and manage Draftable.com comparisons on the command line"

USAGE_TEMPLATE = """%(prog)s <command> [<command-args>]

COMMANDS:

{COMMANDS}

CONFIGURATION:

  Both account_id and auth_token must be set. They can be provided several ways:

  1. Environment variables (DR_ACCOUNT, DR_TOKEN)
  2. A named configuration group in file `~/.draftable`, for example:

      [cloud-testing]  # replace the following with your own credentials
      account: F91n2k-test
      token: d9c3b60dcb83a7bb87efc5c8e72a0599

     To use the above, either specify `-e cloud-testing` as flags to this script,
     or `DR_ENV=cloud-testing` as an environment variable.

  3. As command-line flags, for example:

       "-a <account> -t <token>"
     or
       "--account <account> --token <token>".

  The `base_url` is needed only for self-hosted or development purposes. It can be
  set from environment variable (DR_BASE_URL), preset in the configuration file,
  or a command-line flag (`-b <url>`).

  The `base_url` must always end with '/api' with no trailing slash.

EXAMPLES:

  The following assume credentials are in the environment.

  Create a comparison:

    $ dr-compare create ./left.pdf ./right.pdf

  Create a public comparison that expires in 15 minutes:

    $ dr-compare create -p -m 15 ./left.pdf ./right.pdf

  Provide the file types when not clear from the file extension:

    $ dr-compare create --left-type=pdf --right-type=rtf ./left-file ./right-file

  List all comparisons:

    $ dr-compare list
    $ dr-compare all

  Get a specific comparison:

    $ dr-compare get PCiIEXzW

  Get public URL:

    $ dr-compare url PCiIEXzW

  Get signed URL with 30 minute expiry:

    $ dr-compare signed PCiIEXzW

  Get signed URL with 75 minute expiry:

    $ dr-compare signed PCiIEXzW -m 75
    $ dr-compare signed PCiIEXzW --expiry-mins 75
"""


class SetupError(Exception):
    pass


def get_connection_args(name):
    ini_path = os.path.join(os.path.expanduser("~"), ".draftable")
    if not os.path.isfile(ini_path):
        raise SetupError(
            f"Requested environment '{name}' but missing config file: {ini_path}"
        )

    config = configparser.ConfigParser()
    config.read(ini_path)

    if name not in config:
        raise SetupError(
            f"Requested environment '{name}' but config file ({ini_path}) does not define that name."
        )

    base_url = config.get(name, "base_url", fallback=None)

    return (
        config.get(name, "account"),
        config.get(name, "token"),
        base_url,
    )


def create_client(args):
    # First, use any environment variables
    account = os.getenv("DR_ACCOUNT")
    token = os.getenv("DR_TOKEN")
    base_url = os.getenv("DR_BASE_URL")

    # Secondly, if provided, look up this name in the ~/.draftable file (if it exists)
    env_name = getattr(args, "env_name") or os.getenv(
        "DR_ENV"
    )  # getattr default value doesn't work with args object

    if env_name:
        account, token, base_url = get_connection_args(env_name)

    # Thirdly, allow the user to override both environment vars and predefined settings with command-line flags.
    account = args.account if args.account else account
    token = args.token if args.token else token
    base_url = args.base_url if args.base_url else base_url

    # Some sanity checks
    if not account or not token:
        raise SetupError("Both account and token must be set.")

    client = DraftableClient(account, token, base_url)
    if args.unverified_ssl:
        client.verify_ssl = False
    return client


def with_std_options(arg_parser):
    """Embellish the provided `arg_parser` with standard options."""
    arg_parser.add_argument(
        "-a",
        "--account",
        metavar="<ACCOUNT-ID>",
        action="store",
        help="For cloud, see https://api.draftable.com/account/credentials",
    )
    arg_parser.add_argument(
        "-b",
        "--base-url",
        metavar="<BASE-URL>",
        action="store",
        help="Only for Enterprise self-hosted",
    )
    arg_parser.add_argument(
        "-e",
        "--env-name",
        metavar="<ENV-NAME>",
        action="store",
        help="Name from file $HOME/.draftable",
    )
    arg_parser.add_argument(
        "-t",
        "--token",
        metavar="<TOKEN>",
        action="store",
        help="For cloud, see https://api.draftable.com/account/credentials",
    )
    arg_parser.add_argument(
        "-S",
        "--unverified-ssl",
        action="store_true",
        help="Don't verify SSL validity; useful for self-hosted self-signed SSL",
    )
    return arg_parser


def default_comparison_display(comp, out=sys.stdout, position=None):
    """Print a comparison to stdout"""
    out.write("Comparison")
    if position is not None:
        out.write(" f{position}")
    out.write(f" identifier: {comp.identifier}\n")
    out.write(f"  ready:       {comp.ready}\n")
    out.write(f"  failed:      {comp.failed}\n")
    out.write(f"  error:       {comp.error_message}\n")
    out.write(f"  public:      {comp.public}\n")
    out.write(f"  created:     {comp.creation_time}\n")
    out.write(f"  expires:     {comp.expiry_time}\n")
    out.write(f"  left:        {comp.left}\n")
    out.write(f"  right:       {comp.right}\n")


def create_comparison(system_args, prog, cmd_name):
    """Create a new comparison."""
    arg_parser = with_std_options(
        argparse.ArgumentParser(description=create_comparison.__doc__)
    )

    arg_parser.add_argument(
        "-p",
        "--public",
        action="store_true",
        default=False,
        help="Marks this comparison public",
    )
    arg_parser.add_argument(
        "-i", "--identifier", default=None, help="Provide your own comparison ID"
    )
    arg_parser.add_argument(
        "-m",
        "--expiry-mins",
        metavar="<MINS>",
        type=int,
        default=None,
        help="number of minutes this URL should be valid",
    )

    arg_parser.add_argument(
        "--left-type",
        default="guess",
        metavar="<EXT>",
        action="store",
        help="e.g. 'pdf', 'doc', 'docx', 'ppt', 'pptx'.",
    )
    arg_parser.add_argument(
        "--right-type", default="guess", metavar="<EXT>", action="store"
    )
    arg_parser.add_argument("left", metavar="left-file-path-or-url")
    arg_parser.add_argument("right", metavar="right-file-path-or-url")

    # arg_parser.add_argument('--amend', action='store_true')

    args = arg_parser.parse_args(system_args)
    # print('Running create, args:', args)

    client = create_client(args)
    # print("Client:", client)

    try:
        left = make_side(args.left, args.left_type)
        right = make_side(args.right, args.right_type)
    except InvalidArgument as ex:
        raise SetupError(
            f"{ex}. You may need to specify file type with --left-type or --right-type"
        )
    except InvalidPath as ex:
        raise SetupError(str(ex))

    identifier = args.identifier
    public = args.public
    expires = datetime.timedelta(minutes=args.expiry_mins) if args.expiry_mins else None

    print("Create:")
    print(f"  identifier: {identifier}")
    print(f"  public: {public}")
    print(f"  expires: {expires}")
    print(f"  left: {left}")
    print(f"  right: {right}")
    print("  ...")
    comp = client.comparisons.create(left, right, identifier, public, expires)

    display = default_comparison_display
    display(comp)
    print_basic_urls(client, comp)


def print_basic_urls(client, comp):
    url_expiry = datetime.timedelta(minutes=30)
    print("\nURLs:")
    print(f"  public URL:  {client.comparisons.public_viewer_url(comp.identifier)}")
    print(
        f"  signed URL:  {client.comparisons.signed_viewer_url(comp.identifier, url_expiry)}"
    )
    print(f"     expires:  {url_expiry}")


def list_all_comparisons(system_args, prog, cmd_name):
    """Retrieve and display all comparisons."""

    arg_parser = with_std_options(
        argparse.ArgumentParser(description=list_all_comparisons.__doc__)
    )

    args = arg_parser.parse_args(system_args)
    # print('Running list, args:', args)
    client = create_client(args)
    display = default_comparison_display
    # print("Client:", client)
    comparisons = client.comparisons.all()
    num_comparisons = len(comparisons)

    print(f"Account {client.account_id} has {num_comparisons:d} comparison(s):")
    for i, comp in enumerate(comparisons, 1):
        display(comp, position=f"{i:d} of {num_comparisons:d}")


def list_one_comparison(system_args, prog, cmd_name):
    """Retrieve and display specific comparison or comparisons."""
    arg_parser = with_std_options(
        argparse.ArgumentParser(
            prog=f"{prog} {cmd_name}",  # so "-h / --help" shows "dr-compare <cmd>"
            description=list_one_comparison.__doc__,
        )
    )
    arg_parser.add_argument(
        "identifiers", metavar="<ID>", nargs="+", help="a comparison identifier"
    )

    args = arg_parser.parse_args(system_args)
    client = create_client(args)
    display = default_comparison_display
    num_comparisons = len(args.identifiers)

    for i, identifier in enumerate(args.identifiers, 1):
        try:
            comp = client.comparisons.get(identifier)
            display(comp, position=f"{i:d} of {num_comparisons:d}")
            print_basic_urls(client, comp)
        except NotFound:
            print(f"Comparison not found with identifier: {identifier}")


def delete_comparison(system_args, prog, cmd_name):
    """Delete a specific comparison."""
    arg_parser = with_std_options(
        argparse.ArgumentParser(
            prog=f"{prog} {cmd_name}",  # so "-h / --help" shows "dr-compare <cmd>"
            description=list_one_comparison.__doc__,
        )
    )
    arg_parser.add_argument(
        "identifier", metavar="<ID>", help="a comparison identifier"
    )

    args = arg_parser.parse_args(system_args)
    client = create_client(args)
    identifier = args.identifier

    try:
        client.comparisons.delete(identifier)
    except NotFound:
        print(f"Comparison not found with identifier: {identifier}")


def show_public_url(system_args, prog, cmd_name):
    """Generate a public (unsigned) URL to view a specific comparison."""
    arg_parser = with_std_options(
        argparse.ArgumentParser(
            prog=f"{prog} {cmd_name}",  # so "-h / --help" shows "dr-compare <cmd>"
            description=list_one_comparison.__doc__,
        )
    )
    arg_parser.add_argument(
        "identifiers", metavar="<ID>", nargs="+", help="a comparison identifier"
    )

    args = arg_parser.parse_args(system_args)
    client = create_client(args)

    for _, identifier in enumerate(args.identifiers, 1):
        print(client.comparisons.public_viewer_url(identifier))


def show_signed_url(system_args, prog, cmd_name):
    """Generate a signed URL to view a specific comparison."""
    arg_parser = with_std_options(
        argparse.ArgumentParser(
            prog=f"{prog} {cmd_name}",  # so "-h / --help" shows "dr-compare <cmd>"
            description=list_one_comparison.__doc__,
        )
    )
    arg_parser.add_argument(
        "-m",
        "--expiry-mins",
        metavar="<MINS>",
        type=int,
        default=30,
        help="number of minutes this URL should be valid",
    )
    arg_parser.add_argument(
        "identifiers", metavar="<ID>", nargs="+", help="a comparison identifier"
    )

    args = arg_parser.parse_args(system_args)
    client = create_client(args)
    url_expiry = datetime.timedelta(minutes=args.expiry_mins)

    for _, identifier in enumerate(args.identifiers, 1):
        print(client.comparisons.signed_viewer_url(identifier, url_expiry))


COMMANDS = dict(
    create=create_comparison,
    all=list_all_comparisons,
    get=list_one_comparison,
    delete=delete_comparison,
    url=show_public_url,
    signed=show_signed_url,
)

ALIASES = {
    "new": "create",
    "post": "create",
    "add": "create",
    "list": "all",
    "getall": "all",
    "del": "delete",
    "rm": "delete",
    "public": "url",
    "public-url": "url",
    "public_url": "url",
    "signed-url": "signed",
    "signed_url": "signed",
}


def make_usage(template, command_map, alias_map):
    """Generate the usage doc based on configured commands and aliases"""

    def format_command_info(command_name):
        func = command_map[command_name]

        # Some commands (but not all) have aliases
        aliases = [k for k in alias_map.keys() if alias_map[k] == command_name]
        aliases = " ".join(sorted(aliases)) if aliases else ""
        aliases = f"\n           Aliases: {aliases}"

        return f"  {command_name:8s} {func.__doc__}{aliases}\n"

    command_info_parts = map(
        format_command_info, (name for name in sorted(command_map.keys()))
    )
    return template.format(COMMANDS="\n".join(command_info_parts))


def dr_compare_main(system_args=None):
    if system_args is None:
        system_args = sys.argv

    arg_parser = argparse.ArgumentParser(
        description=DESCRIPTION, usage=make_usage(USAGE_TEMPLATE, COMMANDS, ALIASES)
    )
    arg_parser.add_argument("command", help="Command to run")
    args = arg_parser.parse_args(system_args[1:2])  # just to select the command

    if args.command == "help":
        arg_parser.print_usage()
        sys.exit(0)

    command_name = ALIASES.get(args.command, args.command)
    command = COMMANDS.get(command_name)

    if not command:
        err = f"Invalid command '{command_name}'. For list of commands: {arg_parser.prog} -h\n"
        arg_parser.error(err)

    command(system_args[2:], arg_parser.prog, command_name)


if __name__ == "__main__":
    try:
        dr_compare_main(sys.argv)
    except SetupError as ex:
        sys.stderr.write(f"Error: {ex}\n")
        sys.exit(1)
