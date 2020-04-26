# arq-algebra

🐍 A Python wrapper to transform SPARQL queries into [ARQ algebra](https://www.w3.org/2011/09/SparqlAlgebra/ARQalgebra) [S-expressions](https://en.wikipedia.org/wiki/S-expression).

## Requirements

* Java SDK 1.8+

## Supported queries

* `SELECT`
* `ASK`
* `CONSTRUCT` (unstable)

## Install

```bash
$ ./install.sh
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

From Python, one can also append `oneline=True`:

```python
import arqalgebra as aa

s_exp = aa.parse('select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)', oneline=True)
```

The expected output is the S-expression:

```
(project (?p ?c) (order ((desc ?c)) (extend ((?c ?.0)) (group (?p) ((?.0 (count))) (bgp (triple ?s ?p ?o))))))
```

## Tests

```bash
$ pip install -r requirements.txt
$ py.test
```
