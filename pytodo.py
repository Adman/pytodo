#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014,  Adrian Matejov

import sys
import pynotify
import os

TASKS_PATH = os.path.join(os.path.dirname(__file__), "tasks.txt")


class Task:
    def __init__(self, text, ID, priority):
        self.text = text
        self.ID = ID
        self.priority = priority


class Pytodo:
    def __init__(self, args):
        self.args = args
        self.f = None

        if not os.path.exists(os.path.dirname(TASKS_PATH)):
            os.mkdir(os.path.dirname(TASKS_PATH))

        if not os.path.isfile(TASKS_PATH):
            f = open(TASKS_PATH, 'w')
            f.close()

    def add_task(self, words):
        """Adds a task to the .txt file"""
        task = ''
        for i in words:
            task += i + ' '

        self._open_file('a')
        self._write_file(task + '\n')
        self._close_file()

    def rm_task(self, numbers):
        """Removes a task from .txt file"""
        self._open_file('r')
        lines = self.f.readlines()
        self.f.close()

        for i in numbers:
            try:
                if lines[int(i) - 1]:
                    lines[int(i) - 1] = ''
            except IndexError:
                print "Could not remove task number %d. Task does not exist!" % int(i)

        tasks = ''
        for task in lines:
            tasks += task

        self._open_file('w')
        self._write_file(tasks)
        self._close_file()


    def show_notification(self):
        """Shows notification window"""
        self._open_file('r+')
        tasks = self.f.read()
        self._close_file()

        tasks = tasks.split('\n')
        tasks.pop()

        tasklist = ''
        for i, j in enumerate(tasks):
            if i + 1 == len(tasks):
                tasklist += '%d. %s' % (i+1, j)
            else:
                tasklist += '%d. %s\n' % (i+1, j)

        n = pynotify.Notification ("ToDo Notes", tasklist)

        n.show()

    def print_help(self):
        """Prints available commands on the screen"""
        print "ToDo Notes, (c) 2013 Adman"
        print "Available arguments:"
        print "     help - show available commands"
        print "     add <task> - add a task to the todo list"
        print "     rm/remove/done <number> - remove a task from the todo list"


    def process(self):
        cmd = self.args[0].lower() if len(self.args) else 0

        if len(self.args):
            if cmd == 'help':
                self.print_help()
                sys.exit(1)
            elif cmd == 'add':
                self.add_task(self.args[1:])
            elif cmd == 'rm' or cmd == 'remove' or cmd == 'done':
                self.rm_task(self.args[1:])
            else:
                self.print_help()
                sys.exit(1)

        self.show_notification()

    def _open_file(self, mode="r"):
        self.f = open(TASKS_PATH, mode)

    def _write_file(self, text):
        self.f.write(text)

    def _close_file(self):
        self.f.close()

      
if __name__ == '__main__':
    pynotify.init("summary-only")
    args = sys.argv[1:]

    todo = Pytodo(args)
    todo.process()
