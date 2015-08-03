# criugui - criuguiwindow.py
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
from gi.repository import Gtk, GLib
from criugui.machine import Machine
from criugui.view.machineview import MachineView
from criugui.view.addmachinedialog import AddMachineDialog


class CRIUGUIWindow(Gtk.ApplicationWindow):

    """
        The main application window.  This class sets up a headerbar with signal handlers for each
        of the buttons, and adds a MachineView for each connected machine being monitored.
    """

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self,
                                       icon_name="utilities-system-monitor",
                                       default_width=1000,
                                       default_height=800)

        self.box = Gtk.HBox()
        self.add(self.box)

        headerbar = Gtk.HeaderBar()
        headerbar.set_title("CRIUGUI")
        headerbar.set_show_close_button(True)
        self.set_titlebar(headerbar)

        addbutton = Gtk.Button.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
        addbutton.connect("clicked", self.add_machine)
        headerbar.pack_start(addbutton)

        refreshbutton = Gtk.Button.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
        refreshbutton.connect("clicked", self.refresh_machines)
        headerbar.pack_start(refreshbutton)

        searchbutton = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
        # search.button.connect("clicked", self.search TODO: search action
        headerbar.pack_start(searchbutton)

        self.connect("delete-event", Gtk.main_quit)

    def add_machine(self, *_):
        """
            Show a dialog prompting for a new address, then connect to that machine and create a
            view for it.
        """

        def add_machine_done(dialog, response):
            if response == Gtk.ResponseType.OK:
                machine = Machine(dialog.entry.get_text())
                view = MachineView(machine)

                self.box.pack_start(view, True, True, 0)
                self.box.show_all()

                self.refresh_machines()

            dialog.destroy()

        amv = AddMachineDialog(self)
        amv.connect("response", add_machine_done)
        amv.run()

    def refresh_machines(self, *_):
        """Reload each Machine in a new thread, then update the views."""

        def refresh_machine_view(view):
            view.machine.refresh()
            GLib.idle_add(view.update)

        for view in self.box.get_children():
            if isinstance(view, MachineView):
                thread = threading.Thread(target=refresh_machine_view, kwargs={"view": view})
                thread.daemon = True
                thread.start()
