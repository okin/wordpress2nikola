wordpress2nikola
================

Converting your content from Wordpress to Nikola.

The aim of this is to make the move from Wordpress to Nikola as painless as possible.
It uses the information contained in Wordpress export files. It will only transfer published posts or pages.

Usage
-----
The script wants two arguments:
The first one is the path to a wordpress export file. The second is the path to your Nikola instance where the export will be created.

**The script will delete any existing posts and stories!**

``python wp2nikola.py path/to/wordpress_export_file.xml path/to/nikola/instance``

Creating a Wordpress Export File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The extraction of your wordpress content is described in the Wordpress documentation.
http://codex.wordpress.org/Tools_Export_Screen
