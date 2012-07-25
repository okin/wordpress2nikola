#-*- coding: utf-8 -*-
import os
import re
import glob
from datetime import datetime
from subprocess import check_output
from tempfile import mktemp
from optparse import OptionParser

from lxml.etree import ElementTree

#TODO: how to use the categories (not tags) defined by wordpress?


class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.meta = {}

    def __repr__(self):
        return '<Post: %s, meta: %s>' % (self.title, self.meta)


class WordpressImporter:
    def __init__(self):
        self._original_address = None
        self.posts = []
        self.pages = []

    @classmethod
    def is_valid_post(cls, y):
        return (y.tag == 'item'
                and y.find('{http://wordpress.org/export/1.2/}status').text == 'publish'
                and y.find('{http://wordpress.org/export/1.2/}post_type').text == 'post')

    @classmethod
    def is_valid_page(cls, y):
        return (y.tag == 'item'
                and y.find('{http://wordpress.org/export/1.2/}status').text == 'publish'
                and y.find('{http://wordpress.org/export/1.2/}post_type').text == 'page')

    @classmethod
    def convert_date(cls, wordpress_date):
        match = re.match('\w+, (\d{1,2}) (\w+) (\d{4}) (\d{2}):(\d{2}):\d{2} .\d{4}', wordpress_date)

        #TODO: redo? not very pythonic, but works in the first place ;)
        m_map = {'Apr': 4,
                 'Aug': 8,
                 'Dec': 12,
                 'Feb': 2,
                 'Jan': 1,
                 'Jul': 7,
                 'Jun': 6,
                 'Mar': 3,
                 'May': 5,
                 'Nov': 11,
                 'Oct': 10,
                 'Sep': 9}

        return datetime(
                        int(match.group(3)),
                        m_map[match.group(2)],
                        int(match.group(1)),
                        int(match.group(4)),
                        int(match.group(5))
                        )

    def get_original_blog_address(self, lxml_element=None):
        if not self._original_address and lxml_element:
            channel = lxml_element.find('channel')
            self._original_address = channel.find('link').text

        return self._original_address

    def prepare_link(self, link):
        link = link.replace(self.get_original_blog_address() + '/', '')
        if link[-1] == '/':
            #Nikola has problems with links ending with / so we replace it with a .html.
            link = link[:-1]
            link = link + '.html'
        elif link[-5:] != '.html' or link[-4:] != '.htm':
            link = link + '.html'

        return link

    def convert_posts(self, lxml_element):
        converted_content = convert_html_to_restructured_text(lxml_element.find('{http://purl.org/rss/1.0/modules/content/}encoded').text)

        p = Post(lxml_element.find('title').text, converted_content)

        p.meta['post_id'] = lxml_element.find('{http://wordpress.org/export/1.2/}post_id').text
        p.meta['date'] = self.convert_date(lxml_element.find('pubDate').text)
        p.meta['link'] = self.prepare_link(lxml_element.find('link').text)

        p.meta['category'] = [element.text for element in lxml_element.findall('category')]

        return p

    @classmethod
    def sort_posts_by_date(cls, posts):
        '''Will sort the posts by their date. The lowest date comes first.
        Sorts in place.'''
        def compare_by_date(first, second):
            return cmp(first.meta['date'], second.meta['date'])
        posts.sort(cmp=compare_by_date)

    @classmethod
    def from_wordpress_xml_file(cls, filename):
        x = ElementTree(file=filename)

        new_importer = WordpressImporter()
        new_importer.get_original_blog_address(x)
        new_importer.posts = [new_importer.convert_posts(post) for post in x.getiterator() if cls.is_valid_post(post)]
        new_importer.pages = [new_importer.convert_posts(page) for page in x.getiterator() if cls.is_valid_page(page)]

        cls.sort_posts_by_date(new_importer.posts)

        return new_importer


class NikolaExporter:
    FILE_ENDINGS = ('.txt', '.meta')
    POST_DIRECTORY = 'posts'
    PAGE_DIRECTORY = 'stories'

    def __init__(self, outputdir):
        #TODO: read the configs from the Nikola dir
        self.post_directory = os.path.join(outputdir, self.POST_DIRECTORY)
        self.page_directory = os.path.join(outputdir, self.PAGE_DIRECTORY)

    def clean_folders(self):
        for directory in (self.post_directory, self.page_directory):
            for file_ending in self.FILE_ENDINGS:
                for filename in glob.glob('%s/*%s' % (directory, file_ending)):
                    os.remove(filename)

    def create_content_file(self, directory, name, content):
        filename = '%s/%s.txt' % (directory, name)
        with open(filename, 'w') as postfile:
            if isinstance(content, (list, tuple)):
                for thingy in content:
                    postfile.write(thingy)
                    postfile.write('\n')
            else:
                postfile.write(content)

    def create_metadata_file(self, directory, title, link, date, categories=None, source=None, filename=None):
        if categories is None:
            categories = []

        if source is None:
            source = ''

        if filename is None:
            filename = title

        filename = '%s/%s.meta' % (directory, filename)
        with open(filename, 'w') as metafile:
            for f in (title, link, date.strftime('%Y/%m/%d %H:%M'), ', '.join(categories), source):
                metafile.write(create_writable_unicode(f))
                metafile.write('\n')

    def export_posts(self, posts):
        post_count = 1
        for post in posts:
            print 'Creating post %i (from %s)' % (post_count, post.meta['post_id'])

            if 'source' in post.meta:
                source = post.meta['source']
            else:
                source = None
            
            self.create_metadata_file(self.post_directory, post.title, post.meta['link'], post.meta['date'], post.meta['category'], source, filename=post_count)
            self.create_content_file(self.post_directory, post_count, post.content)

            post_count = post_count + 1

    def export_pages(self, pages):
        for page in pages:
            print 'Creating page %s' % page.title
            self.create_metadata_file(self.page_directory, page.title, page.meta['link'], page.meta['date'], filename=page.title)
            self.create_content_file(self.page_directory, page.title, page.content)

    def export(self, posts=None, pages=None):
        self.clean_folders()
        self.export_posts(posts)
        self.export_pages(pages)


def convert_html_to_restructured_text(html):
    filename = mktemp()
    with open(filename, 'w') as temp_file:
        temp_file.write(create_writable_unicode(html))

    out = check_output(['pandoc', '-f', 'html', '-t', 'rst', '--normalize', '--no-wrap', filename])
    os.remove(filename)

    return out


def create_writable_unicode(string):
    return unicode(string).encode('utf-8')


def run(inputfile, outputdir):
    wpi = WordpressImporter.from_wordpress_xml_file(inputfile)

    nex = NikolaExporter(outputdir)
    nex.export(wpi.posts, wpi.pages)


def get_options(args=None):
    parser = OptionParser()
    parser.add_option("-i", "--inputfile", dest="inputfile", 
                        help="The wordpress export file used as input.", metavar="FILE")
    parser.add_option("-o", "--outputdir", dest="outputdir",
                        help="The directory of the Nikola site where the output will be generated.")

    (options, args) = parser.parse_args(args)

    if not options.inputfile:
        parser.error('Please provide an input file.')

    if not options.outputdir:
        parser.error('Please provide an output directory.')

    return options


if __name__ == '__main__':
    options = get_options()

    run(options.inputfile, options.outputdir)
