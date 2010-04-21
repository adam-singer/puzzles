#!/usr/bin/python

from scc import strongly_connected_components

G = {}
G['a'] = []
G['a'].append('b')
G['b'] = []
G['c'] = []
G['c'].append('d')
G['c'].append('g')
G['d'] = []
G['d'].append('h')
G['d'].append('c')
G['h'] = []
G['h'].append('g')
G['h'].append('d')
G['b'].append('c')
G['b'].append('e')
G['b'].append('f')
G['e'] = []
G['e'].append('a')
G['e'].append('f')
G['f'] = []
G['f'].append('g')
G['g'] = []
G['g'].append('f')

components = strongly_connected_components(G)
print components
