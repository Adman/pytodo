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

    def __repr__(self):
        return "[{0}] [{1}] -> {2}".format(self.ID, self.priority, self.text)


class Pytodo:
    def __init__(self, args):
        self.args = args
        self.f = None

        if not os.path.exists(os.path.dirname(TASKS_PATH)):
            os.mkdir(os.path.dirname(TASKS_PATH))

        if not os.path.isfile(TASKS_PATH):
            f = open(TASKS_PATH, 'w')
            f.close()

        self.tasks = self._read_tasks()
        #print self.tasks

    def _read_tasks(self):
        """Reads tasks from .txt file and parse them"""
        self._open_file('r')
        lines = self.f.readlines()
        self._close_file()

        lines = [line[:-1] for line in lines]

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
        self._open_file('a')
        self._write_file(' '.join(words) + '\n')
        self._close_file()
        # TODO: add parameter for priority
        self.tasks.append(Task(' '.join(words), len(self.tasks) + 1, 'N'))

    def rm_task(self, ids):
        """Removes a task from .txt file"""
        ids = [int(i) for i in ids]

        for i, t in enumerate(self.tasks):
            if t.ID in ids:
                self.tasks.pop(i)

        tasks = [x.text for x in self.tasks]

        self._open_file('w')
        self._write_file("\n".join(tasks))
        self._close_file()

    def edit_task(self, ID, task):
        """Edits current task"""
        try:
            self.tasks[int(ID)-1].text = ' '.join(task)
        except IndexError:
            print "Could not edit task number %d. Task does not exist!" % int(ID)
            return
        
        tasks = [x.text for x in self.tasks]

        self._open_file('w')
        self._write_file('\n'.join(tasks))
        self._close_file()
        
    def show_notification(self):
        """Shows notification window"""
        tasklist = ''
        for task in self.tasks:
            tasklist += "{0}. {1}\n".format(task.ID, task.text)

        n = pynotify.Notification ("ToDo Notes", tasklist[:-1])

        n.show()

    def print_help(self):
        """Prints available commands on the screen"""
        print "ToDo Notes, (c) 2013-2014 Adman"
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
                self.edit_task(int(self.args[1]), self.args[2:])
            else:
                self.print_help()
                sys.exit(1)

        self.show_notification()

    def _open_file(self, mode="r"):
        """Opens file with tasks in given mode"""
        self.f = open(TASKS_PATH, mode)

    def _write_file(self, text):
        """Write given text to the tasks file"""
        self.f.write(text)

    def _close_file(self):
        """Just close file object"""
        self.f.close()

      
if __name__ == '__main__':
    pynotify.init("summary-only")
    args = sys.argv[1:]

    todo = Pytodo(args)
    todo.process()
