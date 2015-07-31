# criugui - machineview.py
# Copyright (C) 2015 Red Iat Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from gi.repository import Gtk
from criugui.view.cgtreeview import CGTreeView


class MachineView(Gtk.Notebook):

    """
        A Gtk widget that contains a CGTreeView, as well as a title that shows the machine's
        hostname, and a few other widgets for scrollbars and such.
    """

    def __init__(self, machine):
        Gtk.Notebook.__init__(self)

        self.machine = machine

        self.header = Gtk.Label()
        self.treeview = CGTreeView()

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.add(self.treeview)
        scrolledwin.set_property("expand", True)

        sep = Gtk.Separator()
        sep.set_orientation(Gtk.Orientation.VERTICAL)

        box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        box.add(scrolledwin)
        box.add(sep)

        self.append_page(box, self.header)

        self.update()

    def update(self):
        """Update the view with the latest data in self.machine."""
        self.header.set_markup("<b>%s</b>" % self.machine.hostname)

        self.treeview.cgtree = self.machine.cgtree
        self.treeview.update()
