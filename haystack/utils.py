class Highlighter(object):
    css_class = 'highlighted'
    html_tag = 'span'
    max_words = 200
    text_block = ''
    
    def __init__(self, query, max_words=None, html_tag=None, css_class=None):
        self.query = query
        
        if max_words is not None:
            self.max_words = int(max_words)
        
        if html_tag is not None:
            self.html_tag = html_tag
        
        if css_class is not None:
            self.css_class = css_class
    
    def highlight(self, text_block):
        self.text_block = text_block
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        return self.render_html(highlight_locations, start_offset, end_offset)
    
    def find_highlightable_words(self):
        query_words = [word in self.query.split() if not word.startswith('-')]
        word_positions = {}
        
        for word in query_words:
            if not word in word_positions:
                word_positions[word] = []
            
            start_offset = 0
            end_offset = len(self.text_block)
            
            while start_offset < end_offset:
                next_offset = self.text_block.find(word, start_offset, end_offset)
                
                if next_offset == -1:
                    break
                
                word_positions[word].append(next_offset)
                start_offset = next_offset + len(word)
        
        return word_positions
    
    def find_window(self, highlight_locations):
        pass
    
    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        highlighted_chunk = self.text_block
