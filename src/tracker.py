from parser import parser
import models


if __name__ == '__main__':
    args = parser.parse_args()
    if args.create:
        t = models.Task(
            label=args.create
        )
        print('-- created and id is', t.id)
    elif args.r:
        models.Task.remove(args.r)
    elif args.toggle:
        print(args.toggle)
    elif args.ls is not None:
        head = '{:<5} {:<10} {:<9} {:<4}'.format('id', 'name', 'state', 'total time')
        print(head)
        print('_' * len(head))
        for item in models.Task.tasks(args.ls):
            print("{:<5} {:<10} {:<9} {:<4}".format(item.id, item.label, item.state.value, item.total_time))
