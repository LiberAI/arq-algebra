# 🐍 arq-algebra

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

A Python wrapper to transform SPARQL queries into [ARQ algebra](https://www.w3.org/2011/09/SparqlAlgebra/ARQalgebra) [S-expressions](https://en.wikipedia.org/wiki/S-expression).

## Requirements

* Java SDK 1.8+

## Supported queries

* `SELECT`
* `ASK`
* `CONSTRUCT` (unstable)

## Install

```bash
$ ./install.sh
$ pip install -r requirements.txt
```

## Usage

From command line:

```bash
$ python arqalgebra.py 'select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)'
```

The expected output is the S-expression:

```
(project (?p ?c)
  (order ((desc ?c))
    (extend ((?c ?.0))
      (group (?p) ((?.0 (count)))
        (bgp (triple ?s ?p ?o))))))
```

### Parse to string

From Python, one can also append `oneline=True`:

```python
import arqalgebra as aa

s_exp = aa.parse('select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)', oneline=True)
# (project (?p ?c) (order ((desc ?c)) (extend ((?c ?.0)) (group (?p) ((?.0 (count))) (bgp (triple ?s ?p ?o))))))
```

### Parse to tree

Return a SPARQL S-expression tree using the [sexpdata](https://github.com/jd-boyd/sexpdata) library.

```python
s_exp_tree = aa.parse_to_tree('select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)')
# [Symbol('project'), [Symbol('?p'), Symbol('?c')], [Symbol('order'), [[Symbol('desc'), Symbol('?c')]], [Symbol('extend'), [[Symbol('?c'), Symbol('?.0')]], [Symbol('group'), [Symbol('?p')], [[Symbol('?.0'), [Symbol('count')]]], [Symbol('bgp'), [Symbol('triple'), Symbol('?s'), Symbol('?p'), Symbol('?o')]]]]]]
```

### Search term

Search for a term in the parsed tree and return the parent object.

```python
aa.search(s_exp_tree, 'bgp')
# [Symbol('bgp'), [Symbol('triple'), Symbol('?s'), Symbol('?p'), Symbol('?o')]]
```

## Tests

```bash
$ py.test
```
