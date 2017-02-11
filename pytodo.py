#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2017,  Adrian Matejov

import sys
import pynotify
import os
import json
import datetime
from operator import attrgetter

TASKS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "tasks.json")


class Task(object):
    """
        @param string text
        @param string priority (low - 0/normal - 1/critical - 2)
        @param datetime date_added
    """
    def __init__(self, text, priority, date_added):
        self._text = text
        self._priority = priority
        self._date_added = date_added

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def date_added(self):
        return self._date_added

    @date_added.setter
    def date_added(self, value):
        self._date_added = value

    def dump(self):
        return {'priority': self._priority, 'text': self._text,
                'date_added': str(self._date_added)}

    def __repr__(self):
        return "[{1}] -> {2}".format(self._priority, self._text)

    def __str__(self):
        return self._text


class Pytodo:
    def __init__(self, args):
        self.args = args
        self.data = None
        self.tasks = []

        if not os.path.exists(os.path.dirname(TASKS_PATH)):
            os.mkdir(os.path.dirname(TASKS_PATH))

        if not os.path.isfile(TASKS_PATH):
            self._write_file()

        self.tasks = self._read_tasks()
        self._sort_tasks()

    def _sort_tasks(self):
        self.tasks.sort(key=attrgetter('priority', 'date_added'), reverse=True)

    def _read_tasks(self):
        """Parse json tasks file"""
        with open(TASKS_PATH) as data_file:
            self.data = json.load(data_file)

        tasks = []
        for task in self.data['tasks']:
            date_obj = datetime.datetime.strptime(task['date_added'],
                                                  '%Y-%m-%d %H:%M:%S.%f')
            tasks.append(Task(task['text'], task['priority'], date_obj))

        return tasks

    def add_task(self, words):
        """Add new task"""
        # TODO: add parameter for priority
        self.tasks.append(Task(' '.join(words), '1',
                               datetime.datetime.utcnow()))
        self._sort_tasks()
        self._write_file()

    def rm_task(self, num):
        """Remove a task from tasks list"""
        self.tasks.pop(int(num)-1)
        self._write_file()

    def edit_task(self, num, task):
        """Edit current task"""
        try:
            self.tasks[int(num)-1].text = ' '.join(task)
        except IndexError:
            print "Could not edit task number {0}. " \
                  "Task does not exist!".format(int(num))
            return

        self._write_file()

    def show_notification(self):
        """Show notification window"""
        tasklist = ''
        for i, task in enumerate(self.tasks):
            tasklist += "{0}. {1}\n".format(i+1, task.text)

        n = pynotify.Notification("ToDo Notes", tasklist[:-1])

        n.show()

    def print_help(self):
        """Print available commands on the screen"""
        print "ToDo Notes, (c) 2013-2016, Adman"
        print "Available arguments:"
        print "     help - show available commands"
        print "     add <task> - add a task to the todo list"
        print "     rm/remove/done <number> - remove a task from the todo list"
        print "     edit <number> <task> - edit a task from the todo list"

    def process(self):
        cmd = self.args[0].lower() if len(self.args) else 0

        if len(self.args):
            if cmd == 'help':
                self.print_help()
                sys.exit(1)
            elif cmd == 'add':
                self.add_task(self.args[1:])
            elif cmd == 'rm' or cmd == 'remove' or cmd == 'done':
                self.rm_task(self.args[1])
            elif cmd == 'edit':
                self.edit_task(int(self.args[1]), self.args[2:])
            else:
                self.print_help()
                sys.exit(1)

        self.show_notification()

    def _write_file(self):
        """Write json dump to file"""
        self.data['tasks'] = [task.dump() for task in self.tasks]

        with open(TASKS_PATH, 'w') as f:
            json.dump(self.data, f)


if __name__ == '__main__':
    pynotify.init("Pytodo")
    args = sys.argv[1:]

    todo = Pytodo(args)
    todo.process()
