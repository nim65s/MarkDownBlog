"""
Markdown extensions for Python:

- `~~strikethrough~~`
- `text~subscript~^superscript^`
- `$mathjax$`
- `%[Video](file.mp4)`
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern, SimpleTagPattern
from markdown.util import etree as ET
from markdown.util import AtomicString


class MathPattern(Pattern):
    def handleMatch(self, m):
        span = ET.Element('span', attrib={'class': 'math inline'})
        span.text = AtomicString(m.group(3))
        return span


class VideoPattern(Pattern):
    def handleMatch(self, m):
        figure = ET.Element('figure')
        video = ET.SubElement(figure, 'video', {'controls': ''})
        video.text = 'Your player does not support the video tag'
        ET.SubElement(video, 'source', {'type': 'video/mp4', 'src': m.group(3)})
        caption = ET.SubElement(figure, 'figcaption')
        caption.text = m.group(2)
        return figure

strikethrough_pattern = SimpleTagPattern(r'(~{2})(.+?)(~{2})', 's')
subscript_pattern = SimpleTagPattern(r'(~{1})([^~]+?)(~{1})', 'sub')
superscript_pattern = SimpleTagPattern(r'(\^{1})([^^]+?)(\^{1})', 'sup')
math_pattern = MathPattern(r'(\${1})([^$]+?)(\${1})')
video_pattern = VideoPattern(r'%\[([^]]+?)\]\(([^)]+?)\)')


class NimExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('strikethrough', strikethrough_pattern, '_end')
        md.inlinePatterns.add('subscript', subscript_pattern, '_end')
        md.inlinePatterns.add('superscript', superscript_pattern, '_end')
        md.inlinePatterns.add('math', math_pattern, '_begin')
        md.inlinePatterns.add('video', video_pattern, '_begin')


def makeExtension(*args, **kwargs):
    return NimExtension(*args, **kwargs)
