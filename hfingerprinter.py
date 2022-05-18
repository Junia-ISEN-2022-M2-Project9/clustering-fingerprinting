"""
ClI entry point. Init logger, treat args and process an output file
Returns:

"""
import argparse
import json
import logging
import os
import sys

from hfingerprinter.analysis import is_pcap_file, run_tshark, write_results_to_file, ensure_environment
from hfingerprinter.common import to_txt
from hfingerprinter.hfinger_exceptions import NotAPcap, TsharkTooOld, TsharkNotFound, PythonTooOld

my_parser = argparse.ArgumentParser(
    description="Hfingerprinter - fingerprinting malware HTTP requests stored in pcap files",
    allow_abbrev=False,
    prog="hfinger",
    formatter_class=argparse.RawTextHelpFormatter,
)
my_group = my_parser.add_mutually_exclusive_group(required=True)
my_group.add_argument(
    "-f", "--file", action="store", type=str, help="Read a single pcap file"
)
my_group.add_argument(
    "-d",
    "--directory",
    metavar="DIR",
    action="store",
    type=str,
    help="Read pcap files from the directory DIR",
)
my_parser.add_argument(
    "-oj",
    "--output-json-path",
    metavar="output_json_path",
    type=str,
    action="store",
    help="Path to the json output directory",
)

my_parser.add_argument(
    "-ot",
    "--output-txt-path",
    metavar="output_txt_path",
    action="store",
    type=str,
    help="Path to the txt output directory. Each line contains a fingerprint",
)

my_parser.add_argument(
    "-m",
    "--mode",
    type=int,
    default=2,
    choices=[0, 1, 2, 3, 4],
    help="Fingerprint report mode. "
         "\n0 - similar number of collisions and fingerprints as mode 2, but using fewer features, "
         "\n1 - representation of all designed features, but a little more collisions than modes 0, 2, and 4, "
         "\n2 - optimal (the default mode), "
         "\n3 - the lowest number of generated fingerprints, but the highest number of collisions, "
         "\n4 - the highest fingerprint entropy, but slightly more fingerprints than modes 0-2",
)
my_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Report information about non-standard values in the request "
         "\n(e.g., non-ASCII characters, no CRLF tags, values not present in the configuration list). "
         "\nWithout --logfile (-l) will print to the standard error.",
)
my_parser.add_argument(
    "-l",
    "--logfile",
    action="store",
    type=str,
    help="Output logfile in the verbose mode. Implies -v or --verbose switch.",
)

args = my_parser.parse_args()
tshark_exec = ""
tshark_ver = ""
try:
    tshark_exec, tshark_ver = ensure_environment()
except (PythonTooOld, TsharkNotFound, TsharkTooOld) as err:
    print(err)
    sys.exit(1)
logger = logging.getLogger('hfinger')
if args.logfile:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.FileHandler(args.logfile, encoding="utf-8"))
elif args.verbose:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
if args.file:
    logger.info("Logger initiated")
    try:
        is_pcap_file(args.file)
    except (FileNotFoundError, IsADirectoryError, PermissionError) as err:
        print("Problem with file access. " + str(err))
        sys.exit(1)
    except NotAPcap:
        print("The provided file is not a valid pcap file.")
        sys.exit(1)
    else:
        results = run_tshark(args.file, args.mode, tshark_exec, tshark_ver)
        if not results:
            logger.warning("No HTTP requests can be used")
            print("No HTTP requests can be used")
        if args.output_json_path is not None:
            write_results_to_file(args.file, args.output_json_path, results)
        if args.output_txt_path is not None:
            to_txt(results, args.output_txt_path)
        else:
            print(json.dumps(results))
else:
    no_pcaps_found_flag = True
    try:
        filelist = os.listdir(args.directory)
    except NotADirectoryError as err:
        print("The entered path is not a directory. " + str(err))
        sys.exit(1)
    for x in os.listdir(args.directory):
        cur_file = os.path.join(args.directory, x)
        try:
            is_pcap_file(cur_file)
        except IsADirectoryError:
            continue
        except (FileNotFoundError, PermissionError) as err:
            print("Problem with file access. " + str(err))
            sys.exit(1)
        except NotAPcap:
            continue
        else:
            no_pcaps_found_flag = False
            logger.info("Analyzing file: " + str(cur_file))
            results = run_tshark(cur_file, args.mode, tshark_exec, tshark_ver)
            if args.output_json_path is not None:
                write_results_to_file(cur_file, args.output_json_path, results)
            if args.output_txt_path is not None:
                to_txt(results, args.output_txt_path)
            else:
                print(json.dumps(results))
    if no_pcaps_found_flag:
        print("No valid pcap files found in the directory")
