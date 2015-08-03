# criugui - addmachinedialog.py
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


class AddMachineDialog(Gtk.Dialog):

    """
    A Gtk.Dialog subclass that prompts for a hostname/IP address of a remote machine to monitor.
    """

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Machine", parent,
                            use_header_bar=True,
                            resizable=False,
                            modal=True,
                            destroy_with_parent=True,
                            buttons=("Add", Gtk.ResponseType.OK,
                                     "Cancel", Gtk.ResponseType.CANCEL))

        self.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid(row_spacing=5, column_spacing=20, border_width=10)
        self.get_content_area().pack_start(grid, True, True, 0)

        self.hostname_entry = Gtk.Entry(hexpand=True)
        self.hostname_entry.connect("changed", self.__input_changed)
        grid.attach(Gtk.Label("Hostname:"), 0, 0, 1, 1)
        grid.attach(self.hostname_entry, 1, 0, 1, 1)

        self.username_entry = Gtk.Entry(hexpand=True)
        self.username_entry.connect("changed", self.__input_changed)
        grid.attach(Gtk.Label("Username:"), 0, 1, 1, 1)
        grid.attach(self.username_entry, 1, 1, 1, 1)

        self.password_entry = Gtk.Entry(hexpand=True, visibility=False)
        self.password_entry.connect("changed", self.__input_changed)
        grid.attach(Gtk.Label("Password:"), 0, 2, 1, 1)
        grid.attach(self.password_entry, 1, 2, 1, 1)

        self.__input_changed()
        self.show_all()

    def __input_changed(self, *_):
        # Only enable the OK button if the required input fields are filled out
        self.set_response_sensitive(Gtk.ResponseType.OK,
                                    self.get_hostname() and self.get_username())

    def get_hostname(self):
        return self.hostname_entry.get_text()

    def get_username(self):
        return self.username_entry.get_text()

    def get_password(self):
        return self.password_entry.get_text()
