#!/usr/bin/env python3

import json, re

def parse(fd):
    '''
    return:
    {
        "Sardine Airline": {
            "title": 
            "page": "77",
            "prompt": [
                {
                    "name": "Prompt #1",
                    "content": "Sardine Airlines is an ultra low-cost"
                },
                ...
            ]
        }
    }
    '''
    result, stateStart = {}, True
    title = ""
    numToken = re.compile('^[\r ]*([0-9]+)[\r ]*$')
    promptToken = re.compile('^[\r ]*(Prompt #.*)[\r ]*$')
    firstLine, thirdPart, page = "", [], ""
    for line in fd:
        line = line.decode('utf-8', errors='ignore')[:-1]
        if not line or line == '\x0c' or line == '\n':
            # empty line
            stateStart = True
            firstLine, thirdPart, page = "", [], ""
            continue
        m = numToken.match(line)
        if m:
            page = m.group(1)
            continue
        m = promptToken.match(line)
        if m:
            content = ""
            for _x in thirdPart:
                content += _x
            prompt = {
                "name": m.group(1),
                "page": page,
                "content": content
            }
            title = firstLine
            if title not in result:
                result[title] = {
                    "name": title,
                    "prompt": []
                }
            result[title]['prompt'].append(prompt)
            firstLine, thirdPart, page = "", [], ""
            continue
        if stateStart:
            firstLine, thirdPart, page = line, [], ""
            if firstLine == 'YachtCo ':
                import pdb
                #pdb.set_trace()
            stateStart = False
            continue
        if page:
            thirdPart.append(line)

    return result

def fromCasebookToJsonFile(filename):
    with open(filename, 'rb') as f:
        d = parse(f)
        with open('casebook.json', 'w') as writer:
            writer.write(json.dumps(d, indent=4))

def testParse():
    import json
    with open('casebook.txt', 'rb') as f:
        d = parse(f)
        print(json.dumps(d, indent=4))

def testTraslate():
    filename = 'casebook.txt'
    fromCasebookToJsonFile(filename)


if __name__ == '__main__':
    testTraslate()
