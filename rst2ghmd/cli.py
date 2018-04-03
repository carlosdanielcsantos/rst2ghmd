import argparse
import sys
from rst2ghmd import rst2ghmd


def main():
    parser = argparse.\
        ArgumentParser(description='Convert rst to github md.',
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', help='rst file to be converted')
    parser.add_argument('-n', help='convert last n releases',
                        type=int, default=1)
    parser.add_argument('--min-header', '-H', help='minimum header level',
                        type=int, default=1)
    parser.add_argument('--exclude-min-header', '-e', action='store_true',
                        help='exclude minimum header level')

    args = parser.parse_args()

    for line in rst2ghmd(args.file, args.n, args.min_header,
                         args.exclude_min_header):
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
