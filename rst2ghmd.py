import re
import argparse
import sys


def is_header_line(line):
    if len(line) > 1:
        l = line.split('\n')[0]
        return l == len(l) * l[0]
    else:
        return False


def convert_header_line(line, replacement):
    return line.replace(line[0], replacement)


def convert_issue(line):
    return re.sub(r':issue:`(.*?)`', '#\\1', line)


def remove_ref(line, ref):
    return line.replace(ref, '')


def parse_refs(line):
    line = remove_ref(line, ':class:')
    line = remove_ref(line, ':mod:')
    line = convert_issue(line)
    return line


release_reference_prefix = '_changes'
bullet_point_chars = ('*', '-')


def rst2ghmd(file, n_releases=1, min_header_level=1, exclude_min_header=False):
    parsed = -1
    headers = []
    new_lines = []
    print(exclude_min_header)
    with open(file, 'r') as fd:
        lines = [line for line in fd]

    for i in range(len(lines)):
        line = lines[i]

        if line.startswith('.. ' + release_reference_prefix):
            parsed += 1
            continue

        if parsed < 0:
            continue
        elif parsed < n_releases:
            if is_header_line(line):
                # if header symbol not seen yet, save symbol
                if line[0] not in headers:
                    headers.append(line[0])

                # modify previous line with corresponding md header style
                header_level = headers.index(line[0]) + min_header_level

                if exclude_min_header and header_level == min_header_level:
                    line = ''
                else:
                    line = "".join([header_level * '#', ' ', lines[i - 1]])

                # rst header symbol line not needed
                new_lines.pop()
            else:
                # convert any references
                line = parse_refs(line)

                # if the line is a continuation of previous line, join them
                if lines[i-1] != '\n' and line != '\n' \
                        and not line.startswith(bullet_point_chars):
                    line = "".join([new_lines.pop().strip(),
                                    ' ', line.strip() + '\n'])

            new_lines.append(line)
        else:
            break

    return new_lines


if __name__ == '__main__':
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
