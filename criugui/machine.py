# criugui - machine.py
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

import httplib
import json

CRIUGUI_PORT = 8080


class Machine:

    """
        This class contains the hostname of a machine as well as the control group tree, which is
        stored as a nested dict of control groups and processes.
    """

    def __init__(self, hostname, cgtree=None):
        self.hostname = hostname
        self.cgtree = cgtree

    def refresh(self):
        """
            Make an HTTP request to the machine to retreive the latest control group and process
            data.  This method blocks while it waits for a response, so it should not be called
            from the main GUI thread.
        """

        conn = httplib.HTTPConnection(self.hostname, CRIUGUI_PORT)
        conn.request("GET", "/cgtree")

        resp = conn.getresponse().read()
        self.cgtree = json.loads(resp)
