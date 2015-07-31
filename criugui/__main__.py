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

from gi.repository import Gtk
from criugui.view.machineview import MachineView

# Sample control group data, until the server is finished
cgdata1 = {"name": "systemd", "pid": "1", "children": [
           {"name": "atom", "pid": "1234", "children": []},
           {"name": "gedit", "pid": "5678", "children": []},
           {"name": "firefox", "pid": "9012", "children": []},
           {"name": "system.slice", "children": [
            {"name": "avahi-daemon.service", "children": [
             {"name": "avahi-daemon", "pid": "912", "children": []},
             {"name": "avahi-daemon", "pid": "931", "children": []}]},
            {"name": "dbus.service", "children": [
             {"name": "dbus-daemon", "pid": "914", "children": []}]}]}]}

cgdata2 = {"name": "sssd.service", "children": [
           {"name": "sssd", "pid": "17523",  "children": [
            {"name": "sssd_be", "pid": "17524", "children": []},
            {"name": "sssd_nss", "pid": "17541", "children": []},
            {"name": "sssd_pam",     "pid": "17542", "children": []}]}]}

cgdata3 = {"name": "gdm-wayland-ses", "pid": "1454",
           "children": [
               {"name": "dbus-daemon", "pid": "1458", "children": []},
               {"name": "gnome-session", "pid": "1471", "children": [
                {"name": "gnome-shell", "pid": "1481", "children": [
                 {"name": "Xwayland", "pid": "1531", "children": []},
                 {"name": "ibus-daemon", "pid": "1693", "children": [
                  {"name": "ibus-dconf", "pid": "1697", "children": []},
                  {"name": "ibus-engine-sim", "pid": "1875", "children": []}]}]},
                {"name": "gnome-settings-", "pid": "1713", "children": []}]}]}


def main():
    headerbar = Gtk.HeaderBar()
    headerbar.set_title("CRIUGUI")
    headerbar.set_show_close_button(True)

    box = Gtk.HBox()

    for hostname, data in (("localhost", cgdata1), ("nuc", cgdata2), ("utx", cgdata3)):
        machineview = MachineView()
        machineview.header.set_title(hostname)
        machineview.header.set_subtitle("127.0.0.1")
        machineview.treeview.set_cg_data(data)
        box.pack_start(machineview, True, True, 0)

    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)
    win.set_titlebar(headerbar)
    win.set_default_size(1000, 800)
    win.add(box)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
