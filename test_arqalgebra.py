#!/usr/bin/env python
import pytest
from arqalgebra import parse, parse_to_tree, search, SPARQLSyntaxError, QueryNotSupportedError


def test_count():
    assert parse('select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)') == \
            '(project (?p ?c)\n  (order ((desc ?c))\n    (extend ((?c ?.0))\n      (group (?p) ((?.0 (count)))\n        (bgp (triple ?s ?p ?o))))))'

def test_count_oneline():
    assert parse('select ?p (count(*) as ?c) where { ?s ?p ?o } group by ?p order by desc(?c)', oneline=True) == \
            '(project (?p ?c) (order ((desc ?c)) (extend ((?c ?.0)) (group (?p) ((?.0 (count))) (bgp (triple ?s ?p ?o))))))'

def test_filter():
    assert parse('select ?p where { ?s ?p ?o ; ?p2 "asd"@en . filter(regex(?o, "http://")) } limit 10') == \
            '(slice _ 10\n  (project (?p)\n    (filter (regex ?o "http://")\n      (bgp\n        (triple ?s ?p ?o)\n        (triple ?s ?p2 "asd"@en)\n      ))))'

def test_ask():
    assert parse('ask { ?s ?p ?o }') == \
            '(bgp (triple ?s ?p ?o))'

def test_table_unit():
    with pytest.raises(QueryNotSupportedError):
        parse('construct { ?s ?p ?o } where { }')

def test_describe():
    with pytest.raises(QueryNotSupportedError):
        parse('describe <urn:1>')

def test_missing_object():
    with pytest.raises(SPARQLSyntaxError):
        parse('select ?p (count(*) as ?c) where { ?s ?p . } group by ?p order by desc(?c)')

def test_incomplete_query():
    with pytest.raises(SPARQLSyntaxError):
        parse('select')

def test_empty_query():
    with pytest.raises(SPARQLSyntaxError):
        parse('')

def test_parse_to_tree():
    assert str(parse_to_tree('PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri ?c WHERE { res:New_York_City dbo:leaderName ?uri ; dbo:country ?c }')) == \
            "[Symbol('prefix'), [[Symbol('dbo:'), Symbol('<http://dbpedia.org/ontology/>')], [Symbol('res:'), Symbol('<http://dbpedia.org/resource/>')]], [Symbol('distinct'), [Symbol('project'), [Symbol('?uri'), Symbol('?c')], [Symbol('bgp'), [Symbol('triple'), Symbol('res:New_York_City'), Symbol('dbo:leaderName'), Symbol('?uri')], [Symbol('triple'), Symbol('res:New_York_City'), Symbol('dbo:country'), Symbol('?c')]]]]]"

def test_search():
    assert str(search(parse_to_tree('PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri ?c WHERE { res:New_York_City dbo:leaderName ?uri ; dbo:country ?c }'), 'bgp')) == \
            "[Symbol('bgp'), [Symbol('triple'), Symbol('res:New_York_City'), Symbol('dbo:leaderName'), Symbol('?uri')], [Symbol('triple'), Symbol('res:New_York_City'), Symbol('dbo:country'), Symbol('?c')]]"
