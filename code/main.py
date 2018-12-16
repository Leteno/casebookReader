#!/usr/bin/env python3

import json, os, re, sys

import audio, ui

def main():
    filename = getFileName()
    content = getContent(filename)
    d = parse(content)
    display(d)

def getFileName():
    return "casebook.json"

def getFamilarFileName(name):
    if os.path.exists(name):
        return name
    return None  # TODO

def getContent(filename):
    content = None
    with open(filename, 'r') as f:
        content = f.read()
    return content

def parse(content):
    d = json.loads(content)
    result = []
    def validCase(case):
        if 'prompt' not in case:
            return False
        if not case['prompt']:
            return False
        if not case['prompt'][0]:
            return False
        if 'page' not in case['prompt'][0]:
            return False
        if not case['prompt'][0]['page']:
            return False
        return True
    def casePage(case):
        if validCase(case):
            return int(case['prompt'][0]['page'])
        return -1
    for key in d:
        val = d[key]
        page = casePage(val)
        if validCase(val) > 0:
            val['page'] = page
            result.append(val)
    result.sort(key=lambda x: x['page'])
    return result

def display(data):
    # print(json.dumps(data, indent=4))
    def job(content):
        audio.speak(content)
    ui.show(data, job)

if __name__ == '__main__':
    main()
