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
        self.treemodel = Gtk.TreeStore(str, str, Pango.Weight)
        self.filtermodel = Gtk.TreeModelFilter(child_model=self.treemodel)
        self.filtermodel.set_visible_func(self.__visible_func)

        self.filtertext = ""

        Gtk.TreeView.__init__(
            self, model=self.filtermodel, enable_search=False, enable_tree_lines=True)

        self.cgtree = None

        text = Gtk.CellRendererText()

        namecol = Gtk.TreeViewColumn("Name", text, text=self.NAME_COL)
        namecol.set_fixed_width(200)
        namecol.set_resizable(True)
        self.append_column(namecol)

        pidcol = Gtk.TreeViewColumn("PID", text, text=self.PID_COL, weight=self.WEIGHT_COL)
        self.append_column(pidcol)

    def set_filter_text(self, widget, filtertext):
        self.filtertext = filtertext
        self.filtermodel.refilter()
        self.expand_all()

    def update(self):
        """
            Recursively add the process tree to the treestore.  cgtree is a dictionary with the
            keys "name", "children", and possibly "pid".  "children" maps to an array of dicts
            similar to data, and "pid" is specified only if the data refers to a process and not a
            cgroup.
        """

        self.treemodel.clear()
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
        newparent = self.treemodel.append(parent, row)
        for child in data["children"]:
            self.__append_cg_data(child, newparent)

    def __visible_func(self, model, iter, data):
        """Return True if the given row or any of its children matches the current filter."""
        child = model.iter_children(iter)
        while child:
            if self.__visible_func(model, child, data):
                return True
            child = model.iter_next(child)

        name, = model.get(iter, CGTreeView.NAME_COL)

        # This row "matches" if the filter text appears at all with some capitalization/whitespace
        # in the process name.
        return self.filtertext.lower().strip() in name.lower().strip()
