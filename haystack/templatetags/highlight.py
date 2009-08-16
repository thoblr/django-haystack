from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import template


register = template.Library()


class HighlightNode(template.Node):
    def __init__(self, text_block, query, html_tag='span', css_class='highlighted', max_words=200):
        self.text_block = template.Variable(text_block)
        self.query = template.Variable(query)
        self.html_tag = template.Variable(html_tag)
        self.css_class = template.Variable(css_class)
        self.max_words = template.Variable(max_words)
    
    def render(self, context):
        text_block = self.model.resolve(text_block)
        query = self.model.resolve(query)
        html_tag = self.model.resolve(html_tag)
        css_class = self.model.resolve(css_class)
        max_words = int(self.model.resolve(max_words))
        highlighted_text = ''
        
        # Handle a user-defined highlighting function.
        if hasattr(settings, 'HAYSTACK_CUSTOM_HIGHLIGHTER'):
            # Do the import dance.
            try:
                highlighter_class = __import__(settings.HAYSTACK_CUSTOM_HIGHLIGHTER)
            except ImportError:
                raise ImproperlyConfigured("The highlighter '%s' could not be imported." % settings.HAYSTACK_CUSTOM_HIGHLIGHTER
        else:
            from haystack.utils import Highlighter
            highlighter_class = Highlighter
        
        highlighter = highlighter_class(query, css_class=css_class, max_words=max_words)
        highlighted_text = highlighter.highlight(text_block)
        return highlighted_text


@register.tag
def highlight(parser, token):
    """
    Takes a block of text and highlights words from a provided query within that
    block of text. Optionally accepts an argument to provide the CSS class to
    wrap highlighted word in.
    
    Syntax::
    
        {% highlight <text_block> with <query> [class "class_name"] [tag "span"] [max_words 200] %}
    
    Example::
    
        # Highlight summary with default behavior.
        {% highlight result.summary with request.query %}
        
        # Highlight summary but wrap highlighted words with a span and the
        # following CSS class.
        {% highlight result.summary with request.query tag "span" class "highlight_me_please" %}
        
        # Highlight summary but only show 40 words.
        {% highlight result.summary with request.query max_words 40 %}
    """
    bits = token.split_contents()
    
    if not len(bits) % 2 == 0:
        raise template.TemplateSyntaxError(u"'%s' tag requires valid pairings arguments." % tag_name)
    
    tag_name = bits[0]
    text_block = bits[1]
    
    if bits[2] != 'with':
        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'with'." % tag_name)
    
    query = bits[3]
    
    bits_dict = dict(bits[4:])
    html_tag = None
    css_class = None
    max_words = 200
    
    if 'css_class' in bits_dict:
        css_class = bits_dict['css_class']
    
    if 'html_tag' in bits_dict:
        html_tag = bits_dict['html_tag']
    
    if 'max_words' in bits_dict:
        max_words = bits_dict['max_words']
    
    return HighlightNode(text_block, query, html_tag, css_class, max_words)
