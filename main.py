#!/usr/bin/python3

import sys
import editor
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


if len(sys.argv) == 3:
    print ("new empty map")
    win = editor.GtkEditor(int(sys.argv[1]), int(sys.argv[2]))
else:
    print ("new empty map with default width and height")
    win = editor.GtkEditor(800, 600)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
Gtk.main()

    
