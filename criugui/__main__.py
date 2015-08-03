# criugui - __main__.py
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

import threading
from gi.repository import Gtk, GObject, GLib
from criugui.view.machineview import MachineView
from criugui.view.addmachinedialog import AddMachineDialog
from criugui.machine import Machine

win = Gtk.Window()
machinebox = Gtk.HBox()


def add_machine(*_):
    def add_machine_done(dialog, response):
        if response == Gtk.ResponseType.OK:
            machine = Machine(dialog.entry.get_text())
            view = MachineView(machine)

            machinebox.pack_start(view, True, True, 0)
            machinebox.show_all()

            refresh_machines()

        dialog.destroy()

    amv = AddMachineDialog(win)
    amv.connect("response", add_machine_done)
    amv.run()


def refresh_machines(*_):
    """Reload each Machine in a new thread, then update the views."""

    def refresh_machine_view(view):
        view.machine.refresh()
        GLib.idle_add(view.update)

    for view in machinebox.get_children():
        if isinstance(view, MachineView):
            thread = threading.Thread(target=refresh_machine_view, kwargs={"view": view})
            thread.daemon = True
            thread.start()


def main():
    GObject.threads_init()

    icontheme = Gtk.IconTheme.get_default()

    headerbar = Gtk.HeaderBar()
    headerbar.set_title("CRIUGUI")
    headerbar.set_show_close_button(True)

    addbutton = Gtk.Button.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
    addbutton.connect("clicked", add_machine)
    headerbar.pack_start(addbutton)

    refreshbutton = Gtk.Button.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
    refreshbutton.connect("clicked", refresh_machines)
    headerbar.pack_start(refreshbutton)

    searchbutton = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
    headerbar.pack_start(searchbutton)

    win.connect("delete-event", Gtk.main_quit)
    win.set_icon_name("utilities-system-monitor")
    win.set_titlebar(headerbar)
    win.set_default_size(1000, 800)
    win.add(machinebox)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
