# criugui - setcommandsdialog.py
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

from gi.repository import Gtk, Pango
import criugui.remote.migrate


class SetCommandsDialog(Gtk.Dialog):

    """
    A Gtk.Dialog subclass that lets the user configure what commands are executed for checkpointing
    and restoring processes.  This can be used to pass command line options to CRIU for processes
    that don't work with the default settings.
    """

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Commands", parent,
                            use_header_bar=True,
                            resizable=False,
                            modal=True,
                            destroy_with_parent=True,
                            buttons=("OK", Gtk.ResponseType.OK,
                                     "Cancel", Gtk.ResponseType.CANCEL))

        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", SetCommandsDialog.__done)

        grid = Gtk.Grid(row_spacing=5, column_spacing=20, border_width=10)
        self.get_content_area().pack_start(grid, True, True, 0)

        self.checkpoint_entry = Gtk.Entry(
            hexpand=True, text=criugui.remote.migrate.DUMP_CMD, width_chars=80)
        self.checkpoint_entry.override_font(Pango.FontDescription("monospace"))
        self.checkpoint_entry.connect("changed", self.__input_changed)
        grid.attach(Gtk.Label("Checkpoint Command:"), 0, 0, 1, 1)
        grid.attach(self.checkpoint_entry, 1, 0, 1, 1)

        self.restore_entry = Gtk.Entry(
            hexpand=True, text=criugui.remote.migrate.RESTORE_CMD, width_chars=80)
        self.restore_entry.override_font(Pango.FontDescription("monospace"))
        self.restore_entry.connect("changed", self.__input_changed)
        grid.attach(Gtk.Label("Restore Command:"), 0, 1, 1, 1)
        grid.attach(self.restore_entry, 1, 1, 1, 1)

        self.__input_changed()
        self.show_all()

    def __input_changed(self, *_):
        # Only enable the OK button if the hostname is filled out

        if self.get_checkpoint_command().count("%s") != 2:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)
        elif self.get_restore_command().count("%s") != 1:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)
        else:
            self.set_response_sensitive(Gtk.ResponseType.OK, True)

    def __done(self, response):
        if response == Gtk.ResponseType.OK:
            criugui.remote.migrate.DUMP_CMD = self.get_checkpoint_command()
            criugui.remote.migrate.RESTORE_CMD = self.get_restore_command()
            print("k")

        self.destroy()

    def get_checkpoint_command(self):
        return self.checkpoint_entry.get_text()

    def get_restore_command(self):
        return self.restore_entry.get_text()
