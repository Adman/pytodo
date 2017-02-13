#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2017,  Adrian Matejov

import pynotify
import os
import json
import datetime
import argparse
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

    def add_task(self, words, priority):
        """Add new task"""
        self.tasks.append(Task(' '.join(words), str(priority),
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

    def process(self):
        if res.edit and res.id > -1:
            self.edit_task(res.id, res.edit)

        if res.task_id_to_remove > -1:
            self.rm_task(res.task_id_to_remove)

        if res.new_task:
            self.add_task(res.new_task, res.priority)

        self.show_notification()

    def _write_file(self):
        """Write json dump to file"""
        self.data['tasks'] = [task.dump() for task in self.tasks]

        with open(TASKS_PATH, 'w') as f:
            json.dump(self.data, f)


if __name__ == '__main__':
    pynotify.init("Pytodo")

    argp = argparse.ArgumentParser()
    argp.add_argument('-a', '--add', help='Add a task into ToDo List',
                      dest='new_task', default=[], nargs='+')
    argp.add_argument('-p', '--priority', choices=[0, 1, 2], type=int,
                      default=1,
                      help='Optional argument when adding a task to set \
                            priority. Default 1. 0=low, 1=normal, 2=critical')
    argp.add_argument('-r', '--remove', help='Remove tasks with given IDs',
                      dest='task_id_to_remove', default=-1, type=int)
    argp.add_argument('-e', '--edit', help='Edit task with given ID',
                      default=[], nargs='+')
    argp.add_argument('-i', '--id', type=int, default=-1,
                      help='Provide this argument when you want to edit task \
                            with this ID')
    res = argp.parse_args()

    todo = Pytodo(res)
    todo.process()
