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

        self.entry = Gtk.Entry(placeholder_text="Hostname or IP address")

        box = Gtk.HBox()
        box.pack_start(Gtk.Label("Address:"), False, True, 8)
        box.pack_start(self.entry, True, True, 0)
        self.get_content_area().pack_start(box, True, True, 0)
        box.show_all()
