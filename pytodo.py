#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014,  Adrian Matejov

import sys
import pynotify
import os
import re

TASKS_PATH = os.path.join(os.path.dirname(__file__), "tasks.txt")


class Task:
    """
        @param string text
        @param int ID
        @param string priority (low - L/normal - N/critical - C)
    """
    def __init__(self, text, ID, priority):
        self.text = text
        self.ID = ID
        self.priority = priority


class Pytodo:
    def __init__(self, args):
        self.args = args
        self.f = None

        self.tasks = self._read_tasks()

        if not os.path.exists(os.path.dirname(TASKS_PATH)):
            os.mkdir(os.path.dirname(TASKS_PATH))

        if not os.path.isfile(TASKS_PATH):
            f = open(TASKS_PATH, 'w')
            f.close()

    def _read_tasks(self):
        """Reads tasks from .txt file and parse them"""
        self._open_file('r')
        lines = self.f.readlines()
        self._close_file()

        for i in range(len(lines)):
            lines[i] = lines[i].replace(" \n", "")

        tasks = []
        for i, line in enumerate(lines):
            if "@priorityL@" in line:
                priority = "L"
            elif "@priorityC@" in line:
                priority = "C"
            else:
                priority = "N"

            ID = i + 1
            text = re.sub("@priority[LCN]@", "", line)
            tasks.append(Task(text, ID, priority))
            
        return tasks

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
        self._close_file()

        for i in numbers:
            try:
                if lines[int(i) - 1]:
                    lines[int(i) - 1] = ''
            except IndexError:
                print "Could not remove task number %d. Task does not exist!" % int(i)
                return

        tasks = ''
        for task in lines:
            tasks += task

        self._open_file('w')
        self._write_file(tasks)
        self._close_file()

    def edit_task(self, number, task):
        """Edits current task"""
        self._open_file('r')
        lines = self.f.readlines()
        self._close_file()

        try:
            if lines[int(number) - 1]:
                lines[int(number) - 1] = ''
                for i in task:
                    lines[int(number) - 1] += i + ' '
                lines[int(number) - 1] += '\n'
        except IndexError:
            print "Could not edit task number %d. Task does not exist!" % int(number)
            return
        
        tasks = ''
        for t in lines:
            tasks += t

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
            elif cmd == 'edit':
                self.edit_task(self.args[1], self.args[2:])
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
