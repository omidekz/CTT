import argparse
import typing

main_parser = argparse.ArgumentParser()

parser = main_parser

xor = parser.add_mutually_exclusive_group(required=True)

xor.add_argument('-c', '--create', help='-c new_task_name')
xor.add_argument('-t', '--toggle', help='toggle the task state. [todo -> in_progress <=> done]')
xor.add_argument('-ls', nargs='*', help='-ls task_name(s) or not')
xor.add_argument('-r', nargs='+', type=str)
