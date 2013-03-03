wordpress2nikola
================

**Nikola has it's own import mechanism and I'd recommend you to use 
it because it's for mor evolved.
Please have a look at the 
`Nikola handbook <http://nikola.ralsina.com.ar/handbook.html>`_ 
for information about how to use it.**

Converting your content from Wordpress to Nikola.

The aim of this is to make the move from Wordpress to Nikola as painless as possible.
It uses the information contained in Wordpress export files. It will only transfer published posts or pages.

Requirements
------------

* lxml
* `pandoc <http://johnmacfarlane.net/pandoc/>`_

Usage
-----
You can use ``python wp2nikola.py --help`` to show the existing options.

**WARNING: The script will delete any existing posts and stories!**

``-i`` is used to set the input file and ``-o`` gives the path to the nikola instance where the output will be generated.

``python wp2nikola.py -i path/to/wordpress_export_file.xml -o path/to/nikola/instance``

Creating a Wordpress Export File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The extraction of your wordpress content is described in the Wordpress documentation.
http://codex.wordpress.org/Tools_Export_Screen


Troubleshooting
---------------

Running ``doit`` fails with message *Undefined substitution referenced*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The error message contains a file and a line. Please check for possibly incorrent references, i.e. something like the following:

    ``|Linked Image|Text starting here``

The solution to this to put a space between the image declaration and the text:

    ``|Linked Image| Text starting here``
