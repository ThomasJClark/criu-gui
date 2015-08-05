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

from gi.repository import Gtk, Gdk
from gi.repository import Pango
import json


class CGTreeView(Gtk.TreeView):

    """
        A subclass of Gtk.TreeView that renders processes in control groups, similarly to the
        systemd-cgls command.
    """

    PROC_TYPE = Gdk.Atom.intern("process", False)

    NAME_COL, PID_COL, WEIGHT_COL = range(3)

    def __init__(self):
        Gtk.TreeView.__init__(self, Gtk.TreeStore(str, str, Pango.Weight))

        self.cgtree = None

        text = Gtk.CellRendererText()

        namecol = Gtk.TreeViewColumn("Name", text, text=self.NAME_COL)
        namecol.set_fixed_width(200)
        namecol.set_resizable(True)
        self.append_column(namecol)

        pidcol = Gtk.TreeViewColumn("PID", text, text=self.PID_COL, weight=self.WEIGHT_COL)
        self.append_column(pidcol)

        self.set_search_column(self.NAME_COL)

    def update(self):
        """
            Recursively add the process tree to the treestore.  cgtree is a dictionary with the
            keys "name", "children", and possibly "pid".  "children" maps to an array of dicts
            similar to data, and "pid" is specified only if the data refers to a process and not a
            cgroup.
        """

        self.get_model().clear()
        self.__append_cg_data(self.cgtree)
        self.expand_all()

    def __append_cg_data(self, data, parent=None):
        if data is None:
            return

        # The entry may be a cgroup or a process - we can tell by checking for a "pid" key.
        if "pid" in data:
            row = (data["name"], data["pid"], Pango.Weight.NORMAL)
        else:
            row = (data["name"], "", Pango.Weight.BOLD)

        # The array in data["children"] refers to the child processes or control group contents of
        # data.  Either way, recursively add all of the children under this row.
        newparent = self.get_model().append(parent, row)
        for child in data["children"]:
            self.__append_cg_data(child, newparent)
