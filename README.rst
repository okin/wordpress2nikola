wordpress2nikola
================

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
