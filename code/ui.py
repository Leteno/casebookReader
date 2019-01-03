#!/usr/bin/env python3

import re, sys

def show(data, job):
    loopOne(data, job)

def loopOne(data, job):
    dictionary = {}
    for case in data:
        page = str(case['page'])
        dictionary[page] = case
    while True:
        print('\ncurrent List: (enter page num, such as 1, e for exit)')
        for case in data:
            name, page = case['name'], case['page']
            print('%s. %s' % (page, name) )
        command = readFromStd()
        if command == 'e':
            print('Are you sure?  (Yes or No)')
            cmd = readFromStd()
            if cmd == 'Yes' or cmd == 'yes':
                break
            continue
        elif command in dictionary:
            loopTwo(dictionary[command], job)
        else:
            print('invalid number %s is not in the list' % command)

def loopTwo(case, job):
    if 'prompt' not in case:
        print('invalid prompt: %s' % case)
        return
    numberRegex = re.compile('^([0-9]+)$')
    while True:
        print('\ncurrent Prompt: (enter prompt number, such as 1, e for go back)')
        for i in range(len(case['prompt'])):
            p = case['prompt'][i]
            print('%s. %s' % (i+1, p['name']))
        command = readFromStd()
        if command == 'e':
            break
        m = numberRegex.match(command)
        if m:
            number = int(m.group(1))
            if number > len(case['prompt']):
                print('invalid number: %s' % number)
                continue
            content = case['prompt'][number - 1]['content']
            job(content)

def readFromStd():
    line = sys.stdin.readline()
    line = line.replace('\n', '').replace('\r', '')
    return line
