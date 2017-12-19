# based on Gedit devhelp plugin:
#    Copyright (C) 2006 Imendio AB
#    Copyright (C) 2011 Red Hat, Inc.
#
#    Author: Richard Hult <richard@imendio.com>
#    Author: Dan Williams <dcbw@redhat.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gedit, GLib, Gio, GObject, GtkSource

# See https://developer.gnome.org/gtk3/stable/gtk3-Keyboard-Accelerators.html#gtk-accelerator-parse

ACCELS = [('F3', 'cpp'),
          ('F4', 'python')]

class QuickLanguageSelector(GObject.Object, Gedit.AppActivatable):
    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        for key, langid in ACCELS:
            self.app.add_accelerator(key, 'win.quicklangsel',
                                     GLib.Variant.new_string(langid))

    def do_deactivate(self):
        for key, langid in ACCELS:
            self.app.remove_accelerator(key, 'win.quicklangsel',
                                        GLib.Variant.new_string(langid))


class QuickLanguageSelectorWindow(GObject.Object, Gedit.WindowActivatable):
    window = GObject.Property(type=Gedit.Window)
    manager = GtkSource.LanguageManager()

    def __init__(self):
        GObject.Object.__init__(self)

    def select_language(self, langid):
        lang = self.manager.get_language(langid)
        self.window.get_active_document().set_language(lang)

    def do_activate(self):
        action = Gio.SimpleAction(name='quicklangsel',
                                  parameter_type=GLib.VariantType('s'))
        action.connect('activate',
                       lambda a, p: self.select_language(p.get_string()))
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action("quicklangsel")

    def do_update_state(self):
        self.window.lookup_action("quicklangsel").set_enabled(self.window.get_active_document() is not None)
