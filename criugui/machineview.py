# criugui - cgtreeview.py
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
from criugui.cgtreeview import CGTreeView


class MachineView(Gtk.Grid):

    """
        A Gtk widget that contains a CGTreeView, as well as a title that shows the machine's
        hostname, and a few other widgets for scrollbars and such.
    """

    def __init__(self):
        Gtk.Grid.__init__(self)

        self.header = Gtk.HeaderBar()
        self.treeview = CGTreeView()

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.add(self.treeview)
        scrolledwin.set_property("expand", True)

        sep = Gtk.Separator()
        sep.set_orientation(Gtk.Orientation.VERTICAL)

        self.attach(self.header, 0, 0, 2, 1)
        self.attach(scrolledwin, 0, 1, 1, 1)
        self.attach(sep, 1, 1, 1, 1)
