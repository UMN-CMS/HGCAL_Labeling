import json
import argparse
from MajorTypes import majortypes


def main():
    parser = argparse.ArgumentParser(description='Export major types')
    parser.add_argument('-o', '--output', required=True, help="Outpath")
    args = parser.parse_args()
    with open(args.output , 'w') as f:
        json.dump(majortypes, f)

if __name__ == '__main__':
    main()
