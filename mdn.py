import sublime, sublime_plugin, webbrowser, re

MDN_URL = 'https://developer.mozilla.org/'
MDN_SEARCH = '/search?q='

class MdnSelectionSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                s = self.view.word(region)
                s = self.view.substr(s)
            else:
                s = self.view.substr(region)
            topic = self.view.settings().get('syntax')
            topic_url = getTopicFromSyntax(topic)
            searchOnMDN(s, topic_url)

class MdnInputSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            'Search on MDN:',
            '',
            self.on_done,
            self.on_change,
            self.on_cancel
        )

    def on_done(self, input):
        s, topic_url = getTopicFromHashTag(input)
        searchOnMDN(s, topic_url)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass

def searchOnMDN(s, topic_url = ''):
    settings = sublime.load_settings('mdn.sublime-settings')
    locale = settings.get('mdn_locale') or 'en-US'
    webbrowser.open_new_tab(MDN_URL + locale + MDN_SEARCH + s + topic_url)

def getTopicFromSyntax(topic):
    if 'JavaScript' in topic:
        return '&topic=js&topic=api'
    if 'CSS' in topic or 'Stylus' in topic or 'Sass' in topic or 'LESS' in topic:
        return '&topic=css'
    if 'HTML' in topic:
        return '&topic=html&topic=svg&topic=mathml'
    if 'XML' in topic:
        return '&topic=svg'
    else:
        return ''

def getTopicFromHashTag(input):
    hash_tag = r'#\w(?:[-\w]*\w)?'
    topics = re.findall(hash_tag, input)
    s = re.sub(hash_tag, '', input)
    s = s.strip()
    topic_url = ''
    for topic in topics:
        topic_url = topic_url + '&topic=' + topic[1:].lower()
    return s,topic_url