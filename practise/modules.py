# -*- coding:utf-8 -*-
# @Filename : modules.py 
# @Author : Lizi
# @Time : 2020/6/12 11:02 
# @Software: PyCharm

import sys, shelve

def store_person(db):
    '''让用户输入数据并将其存储到shelf对象中'''

    pid = input('enter unique ID number: ')
    person = {}
    person['name'] = input('Enter name: ')
    person['age'] = input('Enter age:')
    person['phone'] = input('Enter phone number:')
    db[pid] = person


def lookup_person(db):
    '''让用户输入ID和所需的字段，并从shelf对象中获取相应的值'''
    pid = input('Enter ID number:')
    filed = input('What would you like to know?(name,age,number)')
    filed = filed.strip().lower()

    print(filed.capitalize() + ':', db[pid][filed])

def print_help():
    print('The available commands are:')
    print('store : Stores informations about a person')
    print('lookup : Looks Up a person from ID number')
    print('quit: Save changes and exit')
    print('? : Print this messge')

def enter_command():
    cmd = input('Enter command (? for help):')
    cmd = cmd.strip().lower()
    return cmd


def main():
    database = shelve.open('D:\\database.dat')
    try:
        while True:
            cmd = enter_command()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == '?':
                print_help()
            elif cmd == 'quit':
                return
    finally:
        database.close()


if __name__ == '__main__':
    main()