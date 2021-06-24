import models
import click


@click.group()
def cli(): pass


@click.command('create')
@click.option('-d', '--desc', 'desc', type=str, default='', help='description')
@click.option(
    '-pt',
    default=0,
    help='before payed time. 1h13m [d(ay), h(our), m(inute)]',
    type=int,
    show_default=True
)
@click.argument('label', required=True)
def create(label: str, desc: str, pt: int):
    t = models.Task(label=label, _total_time=pt, description=desc)
    click.echo(f'-- created and id is {t.id}')


@click.command('ls')
@click.argument('ids', nargs=-1, type=int)
def task_list(ids):
    print(models.Task.headline())
    for item in models.Task.tasks(ids):
        print(item.to_inline())


@click.command('rm')
@click.option('-a', '--all', '_all', default=False, prompt=True, confirmation_prompt=True)
@click.argument('ids', nargs=-1, type=int)
def remove_task(ids, _all: bool = True):
    print(_all)
    models.Task.remove(ids)


@click.command('track')
@click.argument('_id', type=int)
def track_tasks(_id: int):
    print(models.Task.toggle(_id))


cli.add_command(create)
cli.add_command(task_list)
cli.add_command(remove_task)
cli.add_command(track_tasks)


if __name__ == '__main__':
    cli()
