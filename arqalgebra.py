#!/usr/bin/env python
import subprocess
import re

regex = re.compile(r'\n\s+')

class ARQAlgebraError(Exception):
    def __init__(self, expression):
        self.expression = expression
        self.message = "ARQ algebra error"

class QueryNotSupportedError(ARQAlgebraError):
    def __init__(self, expression):
        self.expression = expression
        self.message = "Query not supported error"

class SPARQLSyntaxError(ARQAlgebraError):
    def __init__(self, expression):
        self.expression = expression
        self.message = "SPARQL syntax error"

def parse(query, oneline=False):
    cmd = "java -cp jena-arq/* arq.qparse --print=op".split(' ')
    cmd.append(query)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('utf-8')
    err = result.stderr.decode('utf-8')
    if out.startswith('('):
        if out.startswith('(null') or out.startswith('(table'):
            raise QueryNotSupportedError(query)
        output = regex.sub(' ', out.strip()) if oneline else out.strip()
        return output
    if err.startswith('Encountered'):
        raise SPARQLSyntaxError(err.split('\n')[0])
    raise ARQAlgebraError(err)


if __name__ == '__main__':
    import sys
    print(parse(sys.argv[1]))
