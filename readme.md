# Command line Time Tracker

## Project is in developing


# Usage

  __it is not useable yet now. but you be able to use in below structure in the futur__

    tracker.py [-h] [-d [db name] | -t task lable | -n lable(s) [NEW ...] | -u tasl lable [UPDATE ...]] [-s lable | -a] [-v]

# Doc

- ## abstracts

  - BaseManager

    it's a interface that explain the relation of end user and core APIs.
    if you want to develop or make new Manager to take datas in DBs or ..., you have to
    extends you'r manager from this interface

  - ReadResponse

    it's an binder that bind cores data to actor(end user)

  - STATES

    an enum class that hold PROGRESS | END state of lables
