#!/usr/bin/env python
from __future__ import division
import re
import string


def bail(htm):
    open('gospels.htm', 'w+').write(htm)
    raise SystemExit(1)

def fail(msg):
    print msg
    raise SystemExit(1)

htm = open("gospels.raw.htm").read()


# EOL
pat = re.compile("\r\n")
htm = pat.sub("\n", htm)

# HTML front matter
pat = re.compile(r"<!DOCTYPE.*?jsmissingend\(\);</script>", re.DOTALL)
htm = pat.sub("", htm)

# HTML back matter
pat = re.compile(r"<p>\n<p>\n<p><hr><p>Notes:.*?</html>", re.DOTALL)
htm = pat.sub("", htm)

# Notes (*)
pat = re.compile(r'<font.*?font>', re.DOTALL)
htm = pat.sub(r"", htm)

# Notes (Actual Words)
pat = re.compile(r'<a\s+href="#N\d+">(.*?)</a>', re.DOTALL)
htm = pat.sub(r"\1", htm)

# Words of Jesus Christ
pat = re.compile(r'<span\s+class="j">', re.DOTALL)
htm = pat.sub("", htm)
pat = re.compile(r'</span>')
htm = pat.sub("", htm)

# Baptizer => Baptist
htm = htm.replace("Baptizer", "Baptist")

# Semicolons (for Cormac)
htm = htm.replace(';', ',')

# Missing breaks
for line in open('paragraphs.txt'):
    pattern = line.split('#', 1)[0].strip()
    if not pattern:
        continue
    htm, n = re.subn('(%s)' % pattern, '\\1 <p>', htm) 
    if n != 1:
        print "%d matches for paragraph pattern: %s" % (n, pattern)
        raise SystemExit


# Chapters
# ========
# All chapters should be z-indexed above verses. There are 31,102 verses in the
# Bible and 1,189 chapters.

pat = re.compile(r'<script\s+type="text/javascript">c[bj]\((\d+),1\),</script>')
lnum = ['F639', 'F6DC', 'F63A', 'F63B', 'F63C', 'F63D', 'F63E', 'F63F', 'F640'
       , 'F641']
class ChapterReplacer:
    def __call__(self, match):
        chapter = match.group(1)
        chapter = ''.join(['&#x%s;' % lnum[int(d)] for d in chapter])
        return '<SPAN class="chapter">%s</SPAN>' % chapter
htm = pat.sub(ChapterReplacer(), htm)


# Verses
# ======
# When there are two verses on a line we want to show the range. When a verse
# starts a line we need to move the verse number down a line.

doubles = [] # stack
for line in open('doubles.txt'):
    line = line.split('#', 1)[0].strip()
    if not line or ':' not in line:
        continue
    chapter, verse = line.split(':')
    doubles.append((chapter, verse))
doubles.reverse()

next_line = [] # stack
for line in open('next-line.txt'):
    line = line.split('#', 1)[0].strip()
    if not line or ':' not in line:
        continue
    chapter, verse = line.split(':')
    next_line.append((chapter, verse))
next_line.reverse()

pat = re.compile(r'<script\s+type="text/javascript">c[bj]\((\d+),(\d+)\),</script>')
tnum = ['F643', 'F644', 'F645', 'F646', 'F647', 'F648', 'F649', 'F64A', 'F64B'
       , 'F64C']
class VerseReplacer:
    next_double = doubles.pop()
    next_next_line = next_line.pop()
    def __call__(self, match):
        chapter = match.group(1)
        verse = match.group(2)
        verse_tnum = ''.join(['&#x%s;' % tnum[int(d)] for d in verse])
        css_class = ''
        if (chapter, verse) == self.next_next_line:
            try:
                self.next_next_line = next_line.pop()
            except IndexError:
                self.next_next_line = (-1, -1)
            css_class += ' newline' # class to push a verse number down a line
        if (chapter, str(int(verse) + 1)) == self.next_double:
            return '' # for ranges, take out the first verse; fixes Luke 24:9
        if (chapter, verse) == self.next_double:
            try:
                self.next_double = doubles.pop()
            except IndexError:
                self.next_double = (-1, -1) 
            if verse == '2':
                return ''
            previous = str(int(verse) - 1)
            previous = ''.join(['&#x%s;' % tnum[int(d)] for d in previous])
            verse_tnum = previous + '&nbsp;&nbsp;' + verse_tnum
                                    # double nbsp turns into a long space
            css_class += ' range'
        r = (chapter, chapter, chapter, verse, css_class, verse, verse_tnum)
        return ('<SPAN class="tab-chapter c%s">%s</SPAN><SPAN '
                'class="v%s-%s verse%s" '
                'verse="%s">%s</SPAN>' % r)
htm = pat.sub(VerseReplacer(), htm)

# Dashes and Smart Quotes
htm = htm.replace('Yes\xe2\x80\x99', 'Yes') # special case
assert 'CHEESE' not in htm
pat = re.compile('\xe2\x80\x99([a-z])')
htm, n = pat.subn(r'CHEESE\1', htm)
print n, "apostrophes saved from certain death"
pat = re.compile('s\xe2\x80\x99(\\s)', re.DOTALL)
htm, n = pat.subn(r'sCHEESE\1', htm)
print n, "more apostrophes saved from certain death"
htm = htm.replace('s\xe2\x80\x99', 'sCHEESE') #'&rsquo;')
htm = htm.replace('\xe2\x80\x94', '&mdash;')
htm = htm.replace('\xe2\x80\x98', '') #'&lsquo;')
htm = htm.replace('\xe2\x80\x99', '') #'&rsquo;')
htm = htm.replace('\xe2\x80\x9c', '') #'&ldquo;')
htm = htm.replace('\xe2\x80\x9d', '') #'&rdquo;')
htm = htm.replace('CHEESE', '&rsquo;')

# Headings
pat = re.compile(r'<h1>\nThe Good News According to (.*)\n</h1>')
htm = pat.sub(r'</div></div><div class="blank-left"></div><div id="\1" '
              r'class="book">'
              r'<div id="\1TabHack" class="TabHack"><span></span></div>'
              r'<div id="\1Tab" class="Tab"><span></span></div>'
              r'<h1>\1</h1><div class="section A"><h2>Section A</h2>', htm)
htm = htm[13:] + '</div></div>'

# Ligatures
# ... are taken care of for us automatically by OTF/Prince! Yay!
pass

# Prune the end of Mark.
pat = re.compile(r'<SPAN[^/]*/SPAN>Now when he had risen.*?Amen\.', re.DOTALL)
htm = pat.sub('', htm)

# Mix in section breaks.
section = '\\1</div><div class="section %s"><h2>Section %s</h2>'
i = 0
for line in open('sections.txt'):
    pattern = line.split('#', 1)[0].strip()
    if not pattern:
        j = 0
    else:
        j += 1
        letter = string.uppercase[j]
        rep = section % (letter, letter)
        htm, n = re.subn("(%s)" % pattern, rep, htm)
        if n != 1:
            print "%d matches for section pattern: %s" % (n, pattern)
            raise SystemExit 
        i += 1
print "%d sections added" % i

# Small caps for first phrase of section. Drop cap for first letter.
phrases = []
for line in open('phrases.txt'): # for when we can't use ,.
    phrase = line.split('#')[0].strip()
    if not phrase:
        continue
    pat = re.compile('('+phrase+')')
    htm, n = pat.subn(r'\1|', htm)
    if n == 0:
        fail("phrase matcheth not: " + phrase)
    if n != 1:
        fail("phrase matcheth too much: " + phrase)
pat = re.compile( r'(<h2>Section )([A-Z])(.*?>)([A-Z])(.*?[.,|])'
                , re.DOTALL)
htm = pat.sub( r'\1\2\3<span class="first-letter \2">\4</span>'
             + r'<span class="section-start">\5</span>', htm)
htm = htm.replace('|', '')

# Take <h2>Section A</h2> back out
htm = htm.replace('<h2>Section A</h2>', '')

# Generate CSS for page numbers.
TMPL = """
@page %(book)s:left {
    @bottom-right { 
        content: string(book);
        font: italic 8pt/8pt "Adobe Caslon Pro";
    }
    @bottom-left {
        font: normal 8pt/8pt "Adobe Caslon Pro";
        content: counter(page);
        font-variant: prince-opentype(onum);
    }
}
@page %(book)s:right {
    @bottom-left { 
        content: "Section " counter(section, upper-alpha);
        font: italic 8pt/8pt "Adobe Caslon Pro";
    }
    @bottom-right {
        font: normal 8pt/8pt "Adobe Caslon Pro";
        content: counter(page);
        font-variant: prince-opentype(onum);
    }
}
"""

fp = open('page-numbers.css', 'w+')
for book in ('Mark', 'Matthew', 'Luke', 'John'):
    fp.write(TMPL % {'book': book})



# Generate CSS for Tabs
class Tab:

    tabs = []

    def __init__(self, name, nchapters, offset=0, bonus=0):
        self.name = name
        self.nchapters = nchapters
        self.offset = offset
        self.bonus = bonus
        self.size = self.sizeof(name)
        self._top = self._height = self._total = None
        self.tabs.append(self) # registry

    def sizeof(self, name):
        bytes = re.findall('<div id="%s".*?\n</div>' % name, htm, re.DOTALL)[0]
        bytes = re.sub(r'<SPAN[^/]*/SPAN>', '', bytes)
        bytes = re.sub(r'<d.>', '', bytes)
        bytes = bytes.replace('</dl>', '')
        bytes = bytes.replace('<p>', '')
        return len(bytes)

    @property
    def total(self):
        if self._total is None:
            self._total = sum([tab.size for tab in self.tabs])
        return self._total

    @property
    def top(self):
        if self._top is None:
            i = self.tabs.index(self)
            self._top = -1.125 + sum([t.height for t in self.tabs[:i]])
        return self._top

    @property
    def height(self):
        if self._height is None:
            self._height = ((self.size / self.total) * 9) + self.bonus;
        return self._height

    def tab(self):
        out = ["""\
#%sTab SPAN {
    /* %6d / %6d = %5.1f%% */
    /* * 9in: %fin */
    top: %fin;
    height: %fin;
}""" % (        self.name
              , self.size
              , self.total
              , (self.size / self.total) * 100
              , (self.size / self.total) * 9
              , self.top
              , self.height
               )]
        top = -1 
        space_for = lambda t: (t.size / t.total) * 9
        for t in self.tabs[:self.tabs.index(self)]:
            top += space_for(t)
        field = space_for(self) - (1/9) # 1/9 == 8pt in inches
        for chapter in range(1, self.nchapters+1):
            way_through = (chapter-1) / (self.nchapters-1)
            _top = top + (way_through * field)
            out.append("#%s .c%d { top: %fin }" % (self.name, chapter, _top))
        out.append('')
        return "\n".join(out)

mark = Tab("Mark", 16, bonus=0.125)
matthew = Tab("Matthew", 28, offset=0.125)
luke = Tab("Luke", 24, offset=0.125)
john = Tab("John", 21, offset=0.125, bonus=0.125)

fp = open("tabs.css", "w+")
for book in (mark, matthew, luke, john):
    print >> fp, book.tab()

# Poetry linewraps (further indent by 2em)
for line in open('linewraps.txt'):
    line = line.split('#', 1)[0].strip()
    if not line:
        continue
    line = eval('"%s"' % line) # to pick up \n
    if htm.count(line) > 1:
       raise Exception("more than one of '%s'" % line)
    foo, bar = line.rsplit(None, 1)
    wrapped = '%s <span class="poetry-linewrap">%s</span>' % (foo, bar)
    htm = htm.replace(line, wrapped)

# Final hacks.
htm = htm.replace('much.<', 'much. <')      # Mark 4:9
htm = htm.replace( 'prophesied, saying,\n<dl>'  # Luke 1:68
                 , 'prophesied, saying,\n<dl class="unorphan">'
                  )
htm = htm + open('colophon.htm').read()

endings = [ "for they were afraid."
          , "of the age. Amen."
          , "blessing God. Amen."
          , "would be written."
           ]
for ending in endings:
    if htm.count(ending) != 1:
        raise SystemExit("bad ending")
    htm = htm.replace(ending, ending + ' <span class="ending">&#xE018;</span>')

# Done. Write back.
open("gospels.htm", "w+").write(htm)
