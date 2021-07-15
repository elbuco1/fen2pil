#!/usr/bin/env python

import argparse
import os
import re
import json



def version_increased(former_version, current_version):
    """Check that version in the package is greater than version_master
    and that only one int has increased of 1.

    Args:
        version_master (str): former version
    """
    current_version_int = int("".join(current_version.split(".")))
    former_version_int = int("".join(former_version.split(".")))

    assert current_version_int > former_version_int,  f"New version ({current_version}) should be greater than former version ({former_version})."

    version = [int(e) for e in current_version.split(".")]
    version_former = [int(e) for e in former_version.split(".")]

    diffs = []
    for new, old in zip(version, version_former):
        diffs.append(max(0, new - old))

    assert sum(
        diffs) == 1, f"Only one digit should be increased by one in version. Got {diffs}."

    print("Version increased validation passed!")



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    version_increased_parser = subparsers.add_parser(
        'version_increased', help="Validate that version is greater than former version")
    version_increased_parser.add_argument(
        '-f', '--former_version', type=str, required=True, help='Pass the content of VERSION file in master last commit.')
    version_increased_parser.add_argument(
        '-c', '--current_version', type=str, required=True, help='Pass the content of VERSION file in current commit.')
    version_increased_parser.set_defaults(func=version_increased)
   

    # parse
    args = parser.parse_args()
    func = vars(args).pop("func")
    func(**vars(args))


if __name__ == "__main__":
    main()
