import filer

Manager = filer.Manager('./task.dat')

def start(lable) -> int:
    # return time in secs
    return Manager.write(lable)

def has_task(lable) -> bool:
    return Manager.exists(lable)
