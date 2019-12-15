#!/usr/bin/env python
#coding=utf-8

from gi.repository import Gtk as gtk, GObject as gobj, Gdk as gdk

class mybar(gtk.Table):

    def __init__(self, p):
        super(mybar, self).__init__(1, 100, True)
        self.show()
        self.id = 'mybar'+str(id(self)) ## unique id for the css
        self.set_name(self.id)
        self.p = p
        self.update_w(self.p)

    def update_w(self, p):

        if 'bar' in dir(self): ## don't remove it if it's not there
            self.remove(self.bar)

        self.p = p

        self.bar = gtk.Label()
        self.bar.show()

        m = 0.8 ## this makes the colors darker, 1 for full brightness 0 for black
        if self.p < 0.5:
            r = m
            g = self.p*2*m
        elif self.p > 0.5:
            r = (1-self.p)*2*m
            g = m
        else:
            r = m
            g = m
        color = gdk.RGBA(r,g,0,1)

        css = gtk.CssProvider()
        css.load_from_data('''
@define-color barcolor %s;
#%s GtkLabel {
    font:6px;
    background:-gtk-gradient (linear, center top, center bottom, from (shade (@barcolor, 1.05)), color-stop (0.5, @barcolor), to (shade (@barcolor, 0.95)));
    border-radius:3px;
}
''' % (color.to_string(), self.id) )
        self.bar.get_style_context().add_provider(css, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION )

        if p == 0:
            p = 0.01 ## if it's 0 GTK throws an error
        self.attach(self.bar, 0, int(100*p), 0, 1)

class pbarwin(gtk.Window):

    def __init__(self):
        super(pbarwin, self).__init__(title="Red to green progress bar")
        self.set_border_width(10)
        self.set_position(1)

        self.pbar = mybar(0)
        self.pbar.set_size_request(200,10)
        self.add(self.pbar)

        self.timeout_id = gobj.timeout_add(100, self.main)

    def main(self):
        new = self.pbar.p + 0.01
        if new > 1:
            new = 0
        self.pbar.update_w(new)
        return True ## need True to keep loop running

win = pbarwin()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()