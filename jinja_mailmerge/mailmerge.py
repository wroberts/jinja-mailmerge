#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
mailmerge.py
(c) Will Roberts  14 October, 2014

A Python script to generate multiple files using a template and a
spreadsheet (in Emacs org-mode format) of variable settings.
'''

import click
import itertools
import jinja2
import re
import sys
# ordered dict
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
# pandas
try:
    import pandas
except ImportError:
    pass
# unidecode
try:
    from unidecode import unidecode
except ImportError:
    try:
        from text_unidecode import unidecode
    except ImportError:
        pass

def firstrun(pred, seq):
    '''
    Make an iterator that returns elements from the iterable as long
    as the predicate is true, and then stops; it ignores elements at
    the beginning of the sequence for which predicate is False.

    Arguments:
    - `pred`:
    - `seq`:
    '''
    for x in itertools.takewhile(lambda x: not pred(x), seq):
        pass
    for x in itertools.takewhile(pred, seq):
        yield x

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
    # filter to org-mode table lines
    lines = list(firstrun(lambda x: re.match(r'^\s*\|', x), lines))
    # strip whitespace
    lines = [line.strip() for line in lines]
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
    return [OrderedDict(zip(header, line)) for line in lines[1:]]

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

def filter_de2ascii(sval):
    '''
    Filter German accent characters out of unicode using Latin
    character equivalents.
    '''
    return subn(sval, GERMAN_SUBS)

@click.command()
@click.argument('table', type=click.Path(exists=True, dir_okay=False))
@click.argument('template', type=click.Path(exists=True, dir_okay=False))
@click.option('--filename-field', '-f', type=click.STRING, default='0',
              help='the name or 0-based index of the field in the table '
              'which is used as the file name of the output')
@click.option('--extension', '-e', type=click.STRING, default=None,
              help='the file name extension used for files created '
              '(defaults to the same extension as the template file)')
@click.option('--unidecode/--no-unidecode', default=False,
              help='pass the filenames through unidecode to get straight ASCII')
def main(table, template, filename_field, extension, use_unidecode):
    '''
    Generate a number of text files using a database table with fields
    and values, and a template file.  Arguments:

        TABLE     the spreadsheet table with data to fill in the template
        TEMPLATE  a file containing the template, in jinja2 format
    '''
    table_filename = click.format_filename(table)
    template_filename = click.format_filename(template)
    if filename_field.isdigit():
        filename_field = int(filename_field)
    if extension is None:
        extension = template_filename.split('.')[-1]

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template(template_filename)

    #if table_filename.lower().endswith('.org'):
    instances = load_org_table(table_filename)

    if isinstance(filename_field, int):
        filename_field_fn = lambda x: x.values()[filename_field]
    else:
        filename_field_fn = lambda x: x[filename_field]

    for instance in instances:
        output_basename = filename_field_fn(instance)
        #output_basename = filter_de2ascii(output_basename)
        if use_unidecode:
            output_basename = unidecode(output_basename)
        output_filename = '{0}.{1}'.format(output_basename, extension)
        with open(output_filename, 'w') as output_file:
            output_file.write(template.render(instance).encode('utf-8'))

if __name__ == '__main__' and sys.argv != ['']:
    main()
