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

from gi.repository import Gtk, GLib, Gdk
from criugui.view.cgtreeview import CGTreeView
from criugui.machine import machines
import json


class MachineView(Gtk.Notebook):

    """
        A Gtk widget that contains a CGTreeView, as well as a title that shows the machine's
        hostname, and a few other widgets for scrollbars and such.
    """

    def __init__(self, machine):
        Gtk.Notebook.__init__(self)

        self.machine = machine
        self.error_message = None

        self.label = Gtk.Label()
        self.treeview = CGTreeView()

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.add(self.treeview)
        scrolledwin.set_property("expand", True)

        sep = Gtk.Separator()
        sep.set_orientation(Gtk.Orientation.VERTICAL)

        self.spinner = Gtk.Spinner()

        closebutton = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        closebutton.connect("clicked", self.remove_machine)

        header = Gtk.HBox()
        header.pack_start(self.spinner, True, False, 5)
        header.pack_start(self.label, True, True, 0)
        header.pack_start(closebutton, True, False, 5)
        header.show_all()

        self.grid = Gtk.Grid()
        self.grid.attach(scrolledwin, 0, 0, 1, 1)
        self.grid.attach(sep, 1, 0, 1, 2)
        self.append_page(self.grid, header)

        # Set up drag & drop methods and signals.  Drag & drop is used with MachineView to allow
        # to drag and drop processes from one machine to another, initiating a process migration.
        target_entry = Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, 1)
        drag_actions = Gdk.DragAction.MOVE | Gdk.DragAction.COPY

        # Processes and control groups can be dragged from the TreeView.
        self.treeview.connect("drag-data-get", self.__get_dragged_process)
        self.treeview.connect("drag-data-delete", self.__delete_dragged_process)
        self.treeview.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK, [target_entry], drag_actions)

        # Processes and control groups to be dropped anywhere on a MachineView.  This begins the
        # series of steps to migrate the process to this machine.
        self.connect("drag-data-received", self.__receive_dragged_process)
        self.drag_dest_set(Gtk.DestDefaults.ALL, [target_entry], drag_actions)

        self.update()

    def __get_dragged_process(self, widget, context, selection_data, info, time):
        """
            Store the information about the dragged process into selection_data so it can be
            migrated.
        """

        model, iter = widget.get_selection().get_selected()
        name, pid = model.get(iter, CGTreeView.NAME_COL, CGTreeView.PID_COL)
        data = {"hostname": self.machine.hostname, "name": name, "pid": pid}

        selection_data.set_text(json.dumps(data), -1)

    def __receive_dragged_process(self, widget, context, x, y, selection_data, info, time):
        """Dump the selection data and perform the migration."""

        data = json.loads(selection_data.get_text())
        machine = machines[data["hostname"]]
        name = data["name"]
        pid = data["pid"]

        print("TODO: migrate [%s@%s %s (%s)] to [%s@%s]" % (machine.username, machine.hostname,
                                                            name, pid, self.machine.username,
                                                            self.machine.hostname))
        # machine.migrate(self.machine, pid)

    def __delete_dragged_process(self, widget, context):
        """
            Kill the process on this machine.  This is called after a successful MOVE DragAction,
            while a COPY DragAction results in a migration occuring without killing the original
            process.
        """

        model, iter = widget.get_selection().get_selected()
        name, pid = model.get(iter, CGTreeView.NAME_COL, CGTreeView.PID_COL)

        print("TODO: kill [%s@%s %s (%s)]" % (self.machine.username, self.machine.hostname, name,
                                              pid))

    def __show_error_message(self):
        """
            Show an error message in an infobar at the bottom of the MachineView, including the
            text self.error_message.
        """

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

        infobar.get_content_area().get_children()[0].set_text(self.error_message)

    def remove_machine(self, *_):
        """Remove this machine from the list of connected machines and close the SSH connection."""

        if self.machine.ssh_client:
            self.machine.ssh_client.close()

        self.destroy()

    def refresh(self):
        """
            Reload the data in self.machine and update the view when it arrives.  This blocks, so
            it isn't called from the main GUI thread.
        """

        def before_refresh():
            self.spinner.start()
            self.treeview.set_property("sensitive", False)

        def after_refresh():
            self.spinner.stop()
            self.treeview.set_property("sensitive", True)
            self.update()

        try:
            GLib.idle_add(before_refresh)
            self.machine.refresh()
        except Exception as e:
            self.error_message = str(e)
            GLib.idle_add(self.__show_error_message)
        finally:
            GLib.idle_add(after_refresh)

    def update(self):
        """Update the view with the latest data in self.machine."""

        self.label.set_markup("<b>%s</b>" % GLib.markup_escape_text(self.machine.hostname))
        self.treeview.cgtree = self.machine.get_cgtree()
        self.treeview.update()
        self.show_all()
