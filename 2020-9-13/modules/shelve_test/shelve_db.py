#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : shelve_db.py
# @Author: Lizi
# @Date  : 2020/9/24

'''一个简单的数据库，通过用户输入的指令进行操作，
根据用户输入的PID号查找相关的用户信息，若PID不存在，则提示相应的信息'''

import shelve

def store_person(db):
    '''让用户输入数据并存储到shelf对象中'''
    person = {}
    pid = input('Please enter your PID:')
    person['name'] = input("Please Enter your name:")
    person['age'] = input("Please Enter your age:")
    person['phone'] = input('Please Enter your phone:')
    db[pid] = person

def look_up(db):
    '''让用户输入ID和所需的字段，并从shelf对象中获取相应的数据'''
    pid = input("Please Enter your PID ：")
    try:
        new_pid = db[pid]
        field = input('what would your like to know?(name, age, phone) ')
        field = field.strip().lower()
        try:
            infos = new_pid[field]
            print(field.capitalize() + ':', infos)
        except KeyError:
            print('{} not exits!'.format(field))
    except KeyError:
        print('PID not exits!')


def print_help():
    print('The avaliable commands are:')
    print('store:Stroe information about a person')
    print('lookup: Looks up a person from ID number')
    print("quit:Save changes and exit")
    print('?:Print this message')

def enter_number():
    cmd = input('Please Enter command (? for help) ')
    cmd = cmd.strip().lower()
    return cmd

def main():
    database = shelve.open('./database.dat')
    try:
        while True:
            cmd = enter_number()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'look_up':
                look_up(database)
            elif cmd == '?':
                print_help()
            elif cmd == 'quit':
                break
                # return
    finally:
        database.close()


if __name__ == '__main__':
    main()

