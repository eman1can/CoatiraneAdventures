from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout

# KV Import
from loading.kv_loader import load_kv
load_kv(__name__)


class DomainDisplay(RelativeLayout):
    domain = ObjectProperty(None)

    title = StringProperty('')
    description = StringProperty('')

    def on_domain(self, *args):
        print(self.domain, self.domain.get_title())


class SmallDomainDisplay(DomainDisplay):
    def on_domain(self, *args):
        self.title = self.domain.get_title()
        self.description = self.domain.get_small_description()

    def select(self):
        self.parent.goto_widget(self)


class LargeDomainDisplay(DomainDisplay):
    def on_domain(self, *args):
        self.title = self.domain.get_title()
        self.description = self.domain.get_large_description()
