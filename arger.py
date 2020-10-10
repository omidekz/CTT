import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(
        
)

group.add_argument(
    '-d', '--db', type=str,
    nargs='?',
    help='the name of db, default is last db that used'
)

group.add_argument(
    '-t', '--toggle', type=str,
    help='toggle a task'
)

group.add_argument(
    '-n', '--new', nargs='+', type=str,
    help='new lable(s)'
)

group.add_argument(
    '-u', '--update', help='update a lable. lable present the name of task\nthat must pass in first',
    nargs='+'
)

group.add_argument(
    '-a', '--all', action='store_true',
    help='status of all tasks[-a] or DBs[-ad]'
)

group.add_argument(
    '-s', '--status',
    type=str,
    help='status of task'
)

parser.add_argument(
    '-v', '--verbose', action='store_true'
)
