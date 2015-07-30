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
from criugui.cgtreeview import CGTreeView

testdata = {"name": "systemd", "pid": "1", "children": [
            {"name": "atom", "pid": "1234", "children": []},
            {"name": "gedit", "pid": "5678", "children": []},
            {"name": "firefox", "pid": "9012", "children": []},
            {"name": "system.slice", "children": [
             {"name": "avahi-daemon.service", "children": [
              {"name": "avahi-daemon", "pid": "912", "children": []},
              {"name": "avahi-daemon", "pid": "931", "children": []}]},
             {"name": "dbus.service", "children": [
              {"name": "dbus-daemon", "pid": "914", "children": []}]}]}]}


def main():
    headerbar = Gtk.HeaderBar()
    headerbar.set_title("CRIUGUI")
    headerbar.set_show_close_button(True)

    cgtreeview = CGTreeView()
    cgtreeview.set_cg_data(testdata)

    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)
    win.set_titlebar(headerbar)
    win.set_size_request(800, 600)
    win.add(cgtreeview)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
