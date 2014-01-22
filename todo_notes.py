#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014,  Adrian Matejov

import sys
import pynotify
import os

TASKS_PATH = os.path.join(os.path.dirname(__file__), "tasks.txt")

def add_task(args):
    """
        Adds task to the .txt file
    """
    f = open(TASKS_PATH, 'a')
    task = ''
    for i in args:
        task += i + ' '

    f.write(task + '\n')
    f.close()

def rm_task(args):
    """
        Removes task from .txt file
    """
    fr = open(TASKS_PATH, 'r')
    lines = fr.readlines()
    fr.close()

    fw = open(TASKS_PATH, 'w')
        
    for i in args:
        try:
            if lines[int(i) - 1]:
                lines[int(i) - 1] = '' 
        except IndexError:
            print "Could not remove task number %d. Task does not exist!" % int(i)
     
    tasks = ''
    for task in lines:
        tasks += task

    fw.write(tasks)
    fw.close()

def show_window():
    """
        Reads tasks from the .txt file and shows them on the screen.
    """
    f = open(TASKS_PATH, 'r')
    tasks = f.read()

    #print tasks into notification window
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
    f.close()

def print_help():
    """
        Prints available commands in the terminal
    """
    print "ToDo Notes, (c) 2013 Adman"
    print "Available arguments:"
    print "	help - show available commands"
    print "	add <task> - add a task to the todo list"
    print "	rm <number> - remove a task from the todo list"

def main(args):
    if not os.path.exists(os.path.dirname(TASKS_PATH)):
        os.mkdir(os.path.dirname(TASKS_PATH))

    if not os.path.isfile(TASKS_PATH):
        f = open(TASKS_PATH, 'w')
        f.close()

    if len(args):
        if args[0].lower() == 'help':
            print_help()
            sys.exit(1)
        elif args[0].lower() == 'add':
            add_task(args[1:])
        elif args[0].lower() == 'rm' or args[0].lower() == 'remove':
            rm_task(args[1:])
        else:
            print_help()
            sys.exit(1) 

    show_window()
   
if __name__ == '__main__':
    pynotify.init("summary-only")
    args = sys.argv[1:]

    main(args)
