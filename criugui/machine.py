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

import json
import paramiko
from criugui.remote.cgtree import CGTree

machines = {}


class Machine:

    """
        This class contains the hostname of a machine as well as the control group tree, which is
        stored as a nested dict of control groups and processes.
    """

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = None
        self.cgtree = None
        self.error_text = None

        machines[self.hostname] = self

    def __connect(self):

        try:
            if self.ssh_client is None:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=self.hostname,
                                        username=self.username,
                                        password=self.password)
            self.error_text = None
            return True
        except EnvironmentError as e:
            self.ssh_client = None
            self.error_text = "%s: %s" % (self.hostname, e.strerror)
        except Exception as e:
            self.ssh_client = None
            self.error_text = "%s: %s" % (self.hostname, str(e))

        return False

    def refresh(self):
        """
            Retreive the latest control group and process data from the machine using an SSH
            connection. This method blocks while it waits for a response, so it should not be
            called from the main GUI thread.
        """
        if self.__connect():
            with self.ssh_client.open_sftp() as sftp_client:
                self.cgtree = CGTree(sftp_client).tree

    def get_cgtree(self):
        """
            Return a dict with a tree of control groups and process on the remote machine
            (see criugui.remote.cgtree).
        """

        return self.cgtree
