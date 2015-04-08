=================
 jinja-mailmerge
=================

``jinja-mailmerge`` is a command line script to create multiple text
files automatically using a template and a spreadsheet.

Todo
====

1. Command line options to choose the output filename from a column in
   the spreadsheet (instead of always taking the first column).  The
   option should allow selection by index (0-based) or by column
   header name.

2. Documentation

3. Unit tests

4. Support more spreadsheet formats:

   - CSV, TSV
   - Excel
     
     - command-line option to choose which sheet to read
       
   - YAML
   - JSON

5. Maybe allow arbitary text processing on the output filename?
   Currently, the output filename is passed through a filter (``subn``
   with ``GERMAN_SUBS``, which could be called ``de2ascii`` or
   something).  It should be possible to specify a transform as a
   command line option, using Jinja template syntax.
