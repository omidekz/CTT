import argparse

parser = argparse.ArgumentParser()

db_or_toggle = parser.add_mutually_exclusive_group(
        
)
db_or_toggle.add_argument(
    '-d', '--db', type=str,
    nargs='?',
    help='the name of db, default is last db that used'
)
db_or_toggle.add_argument(
    '-t', '--toggle', type=str,
    help='toggle a task'
)
db_or_toggle.add_argument(
    '-n', '--new', nargs='+', type=str,
    help='new lable(s)'
)
db_or_toggle.add_argument(
    '-u', '--update', help='update a lable. lable present the name of task\nthat must pass in first',
    nargs='+'
)

notice_commands = parser.add_mutually_exclusive_group(

)

notice_commands.add_argument(
    '-s', '--status',
    type=str,
    help='status of task'
)
notice_commands.add_argument(
    '-a', '--all', action='store_true',
    help='status of all tasks[-a] or DBs[-ad]'
)

parser.add_argument(
    '-v', '--verbose', action='store_true'
)
