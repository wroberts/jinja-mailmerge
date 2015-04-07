#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
mailmerge.py
(c) Will Roberts  14 October, 2014

A Python script to generate multiple files using a template and a
spreadsheet (in Emacs org-mode format) of variable settings.
'''

import click
import jinja2
import re
import sys
try:
    import pandas
except ImportError:
    pass

def load_org_table(org_filename):
    '''
    Loads a table from file in Emacs org-mode format.  This function
    assumes that the table begins with a header row that contains the
    variable names used in the Jinja2 template.  Returns a list of
    dictionary objects, one for each data row in the table; the
    dictionary contains the header row values as keys and the data row
    values as values.

    Arguments:
    - `org_filename`:
    '''
    with open(org_filename) as input_file:
        lines = input_file.read().decode('utf-8').strip().split('\n')
    # filter out org-mode HLINE lines
    lines = [line for line in lines if not re.match(r'^\|[+-]*\|$', line)]
    # filter out lines that don't match the number of columns of the
    # header
    header_count = lines[0].count('|')
    lines = [line for line in lines if line.count('|') == header_count]
    # split fields on pipe character
    lines = [[field.strip() for field in line.strip().strip('|').split('|')]
             for line in lines]
    # construct dictionaries from each table body line
    header = lines[0]
    return [dict(zip(header, line)) for line in lines[1:]]

GERMAN_SUBS = {u'Ä': u'Ae',
               u'Ö': u'Oe',
               u'Ü': u'Ue',
               u'ß': u'ss',
               u'ä': u'ae',
               u'ö': u'oe',
               u'ü': u'ue'}

def subn(sval, subdict):
    '''
    Multiple repeated substitution on a string `sval` using a
    dictionary of (`before` => `after`) substrings.

    Arguments:
    - `sval`:
    - `subdict`:
    '''
    for (before, after) in subdict.iteritems():
        sval = sval.replace(before, after)
    return sval

def main():
    '''
    Main function.
    '''
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('template.org')

    instances = load_org_table('table.org')

    for instance in instances:
        output_filename = '{}.org'.format(subn(instance['name'], GERMAN_SUBS))
        with open(output_filename, 'w') as output_file:
            output_file.write(template.render(instance).encode('utf-8'))

if __name__ == '__main__' and sys.argv != ['']:
    main()
