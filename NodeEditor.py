#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: LGPL

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NodeEditor(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="EMPER - Node Editor")


    def on_button_clicked(self, widget):
        print("Hello World")

win = NodeEditor()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
