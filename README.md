pyToDo
==========
Remember your tasks via terminal, show them and remove them when they are done!

Dependencies
------------
* Python 2.x+
* Pynotify
* If you have problem with old version of notity-send, follow
[this](http://www.webupd8.org/2014/04/configurable-notification-bubbles-for.html) tutorial.

## Usage

```bash
pytodo.py [-h] [-a NEW_TASK [NEW_TASK ...]] [-p {0,1,2}]
                 [-r TASK_ID_TO_REMOVE] [-e EDIT [EDIT ...]] [-i ID]

optional arguments:
  -h, --help            show this help message and exit
  -a NEW_TASK [NEW_TASK ...], --add NEW_TASK [NEW_TASK ...]
                        Add a task into ToDo List
  -p {0,1,2}, --priority {0,1,2}
                        Optional argument when adding a task to set priority.
                        Default 1. 0=low, 1=normal, 2=critical
  -r TASK_ID_TO_REMOVE, --remove TASK_ID_TO_REMOVE
                        Remove tasks with given IDs
  -e EDIT [EDIT ...], --edit EDIT [EDIT ...]
                        Edit task with given ID
  -i ID, --id ID        Provide this argument when you want to edit task with
                        this ID
```

## Examples:
* To add a task with priority
    `$ ./pytodo.py -a My Critical Priority Task -p 2`
* To remove task with given ID
    `$ ./pytodo.py -r 1`
* To edit task with specific ID
    `$ ./pytodo.py -e New Text Of Task -i 1`

or run just `./pytodo.py` and see all the tasks
