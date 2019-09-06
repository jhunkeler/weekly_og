#!/usr/bin/env python
import argparse
import os
import datetime
from subprocess import Popen
from . import __version__


def user_message(tm, status):
    banner = '=' * 80
    marker = '{0}\n{1}\n{2}\n{0}'.format(banner, tm, status)
    done = False
    lines = []

    while not done:
        msg = ''
        output = ''

        try:
            print('>>>', end='')
            msg = input()
        except EOFError:
            done = True

        if msg == '.' or msg == 'EOF':
            done = True

        if not done:
            if len(lines) < 1:
                lines.append(marker)
            lines.append(msg)

        if lines:
            output = '\n'.join([x for x in lines])
            output += '\n'

    return output


def show_messages(path):
    for root, dirs, files in os.walk(path):
        for f in sorted(files, reverse=False):
            ingest = os.path.join(root, f)
            with open(ingest, 'r') as fp:
                for line in fp:
                    print(line.rstrip())


def main():
    DATA = os.path.abspath(os.path.expanduser('~/.reports/data'))
    now = datetime.datetime.now()
    year, weekno, day = now.isocalendar()

    if not os.path.exists(DATA):
        os.makedirs(DATA)

    todays_path = os.path.join(DATA, str(year), str(weekno))
    todays_file = os.path.join(todays_path, str(day))

    if not os.path.exists(todays_path):
        os.makedirs(todays_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--important', action='store_true',
                        required=False)
    parser.add_argument('-r', '--retrieve', action='store_true')
    parser.add_argument('-e', '--edit', action='store_true')
    parser.add_argument('-V', '--version', action='store_true')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    if args.edit:
        editor = '/usr/bin/vim'
        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
        command = ' '.join([editor, todays_file])
        proc = Popen(command.split())
        proc.communicate()
        retval = proc.wait()
        if retval is None:
            retval = 1

        return retval

    if args.retrieve:
        show_messages(todays_path)
        return 0

    status = 'NOTE'
    if args.important:
        status = 'IMPORTANT'

    message = user_message(now, status)
    with open(todays_file, 'a') as fp:
        fp.write(message)
        fp.write(os.linesep)

    return 0


if __name__ == '__main__':
    sys.exit(main())
