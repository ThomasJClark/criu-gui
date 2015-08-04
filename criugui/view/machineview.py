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

from gi.repository import Gtk, GLib
from criugui.view.cgtreeview import CGTreeView


class MachineView(Gtk.Notebook):

    """
        A Gtk widget that contains a CGTreeView, as well as a title that shows the machine's
        hostname, and a few other widgets for scrollbars and such.
    """

    def __init__(self, machine):
        Gtk.Notebook.__init__(self)

        self.machine = machine

        self.label = Gtk.Label()
        self.treeview = CGTreeView()

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.add(self.treeview)
        scrolledwin.set_property("expand", True)

        sep = Gtk.Separator()
        sep.set_orientation(Gtk.Orientation.VERTICAL)

        closebutton = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        closebutton.connect("clicked", self.remove_machine)

        header = Gtk.HBox()
        header.pack_start(self.label, True, True, 0)
        header.pack_start(closebutton, True, False, 5)
        header.show_all()

        self.grid = Gtk.Grid()
        self.grid.attach(scrolledwin, 0, 0, 1, 1)
        self.grid.attach(sep, 1, 0, 1, 2)
        self.append_page(self.grid, header)

        self.update()

    def remove_machine(self, *_):
        """Remove this machine from the list of connected machines and close the SSH connection."""

        if self.machine.ssh_client:
            self.machine.ssh_client.close()

        self.destroy()

    def update(self):
        """Update the view with the latest data in self.machine."""

        self.label.set_markup("<b>%s</b>" % GLib.markup_escape_text(self.machine.hostname))

        # If an error occured while loading the process data, add an infobar containing the error
        # message.
        if self.machine.error_text:
            def on_infobar_response(infobar, response):
                if response == Gtk.ResponseType.CLOSE:
                    infobar.destroy()
                elif response == Gtk.ResponseType.REJECT:
                    self.remove_machine()

            infobar = self.grid.get_child_at(0, 1)

            if infobar is None:
                infobar = Gtk.InfoBar(message_type=Gtk.MessageType.ERROR, show_close_button=True)
                infobar.add_button("Remove", Gtk.ResponseType.REJECT)
                infobar.get_content_area().add(Gtk.Label())
                infobar.connect("response", on_infobar_response)
                self.grid.attach(infobar, 0, 1, 1, 1)

            infobar.get_content_area().get_children()[0].set_text(self.machine.error_text)

        self.treeview.cgtree = self.machine.get_cgtree()
        self.treeview.update()
        self.show_all()
