#!/usr/bin/env python
import subprocess
from sexpdata import loads
import re

regex = re.compile(r'\n\s+')
CMD_BASE = "java -cp jena-arq/commons-compress-1.19.jar:jena-arq/jena-arq-3.14.0.jar:jena-arq/"\
    "jena-base-3.14.0.jar:jena-arq/jena-cmds-3.14.0.jar:jena-arq/jena-core-3.14.0.jar:jena-arq/"\
    "jena-dboe-base-3.14.0.jar:jena-arq/jena-iri-3.14.0.jar:jena-arq/jena-shaded-guava-3.14.0.jar:"\
    "jena-arq/jena-tdb2-3.14.0.jar:jena-arq/jsonld-java-0.12.5.jar:jena-arq/libthrift-0.13.0.jar:"\
    "jena-arq/log4j-1.2.17.jar:jena-arq/slf4j-api-1.7.26.jar:jena-arq/slf4j-log4j12-1.7.26.jar "\
    "arq.qparse --print=op"

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
    cmd = CMD_BASE.split(' ')
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

def parse_to_tree(query):
    s = parse(query, oneline=True)
    return loads(s)

def search(tree, term):
    queue = [ { 'node': tree, 'parent': None } ]
    while queue:
        x = queue.pop(0)
        if hasattr(x['node'], '_val'):
            if x['node']._val == term:
                return x['parent']['node']
        else:
            if isinstance(x['node'], list):
                queue += [{ 'node': child, 'parent': x } for child in x['node']]
    return None


if __name__ == '__main__':
    import sys
    print(parse(sys.argv[1]))
