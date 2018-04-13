#!/usr/bin/env python
"""Usage:
  draftable [options] <left> <right>

Options:
  -u UID, --user UID          : if (default: none) use $DRAFTABLE_API_UID
  -t TOK, --token TOK         : if (default: none) use $DRAFTABLE_API_TOK
  -i ID, --identifier ID      : existing identifier (default: auto)
  -l TYPE, --left-type TYPE   : filetype (default: auto)
  -r TYPE, --right-type TYPE  : filetype (default: auto)
  -e TIME, --expires TIME  : Time before comparison expires
      [default: 30:int] minutes.
  -d, --delete  : delete specified ID
  -g, --get     : get specified ID
  --log LEVEL  : (FAT|CRITIC)AL|ERROR|WARN(ING)|[default: INFO]|DEBUG|NOTSET

Arguments:
  <left>   : filename
  <right>  : filename
"""
import draftable
# import sys
import datetime as dt
from io import open as io_open
import re
from os import path, getenv
import logging
from argopt import argopt
__all__ = ["main", "run"]
__version__ = "0.0.0"
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__licence__ = "2018 [MPLv2.0](https://www.mozilla.org/MPL/2.0)"
__license__ = __licence__

RE_URL = re.compile("^[a-z]{3,5}://")


class Client(draftable.Client, object):
  def toSide(self, fpath, ftype=None, fname=None):
    file_type = ftype or fpath.rsplit('.', 1)[-1]
    display_name = fname or path.split(fpath)[-1]
    if RE_URL.match(fpath):
      return self.comparisons.side_from_url(
          fpath,
          file_type=file_type, display_name=display_name)
    return self.comparisons.side_from_file(
        io_open(fpath, mode="rb"),
        file_type=file_type, display_name=display_name)


def run(args):
  """@param args: RunArgs"""
  log = logging.getLogger(__name__)

  # CLIENT

  client = Client(
      args.user or getenv("DRAFTABLE_API_UID"),
      args.token or getenv("DRAFTABLE_API_TOK"))
  comparisons = client.comparisons
  log.info(comparisons)

  # CREATE

  identifier = args.identifier or comparisons.generate_identifier()
  log.info("ID:{}".format(identifier))

  # DELETE

  if args.delete:
    comparisons.delete(identifier)
    log.info("DEL:{}".format(identifier))

  # GET

  expires = dt.timedelta(minutes=args.expires)
  comparison = None
  if args.get:
    comparison = comparisons.get(identifier)
  else:
    comparison = comparisons.create(
        identifier=identifier,
        left=client.toSide(args.left, args.left_type),
        right=client.toSide(args.right, args.right_type),
        # 'public' omitted to only allow authenticated users
        expires=expires)

  log.debug("CMP:{}".format(comparison))
  log.info("VISIBILITY:" + ("public" if comparison.public else "private"))
  log.info("READY:" + ("True" if comparison.ready else "False"))

  if comparison.failed:
    log.error("failed:\n" + comparison.error_message)

  viewer_url = comparisons.signed_viewer_url(
      comparison.identifier, valid_until=expires, wait=True)

  # generate signed viewer URL to access the private comparison
  log.info("Viewer URL (expires in {expires:d} min):{url:s}".format(
      expires=args.expires, url=viewer_url))

  # oldest_comparisons = comparisons.all()[-10:]
  # for comparison in oldest_comparisons:
  #   comparisons.delete(comparison.identifier)


def main(argv=None):
  """argv  : list, optional (default: sys.argv[1:])"""
  args = argopt(__doc__, version=__version__).parse_args(args=argv)
  logging.basicConfig(
      level=getattr(logging, args.log, logging.INFO),
      format="%(levelname)s:%(module)s:%(lineno)d:%(message)s")
  log = logging.getLogger(__name__)
  log.debug(args)
  return run(args) or 0


if __name__ == "__main__":
  main()
