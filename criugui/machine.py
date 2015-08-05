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
from criugui.remote.migrate import migrate

machines = {}


class MachineException(Exception):
    pass


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
        except EnvironmentError as e:
            self.ssh_client = None
            raise MachineException("%s: %s" % (self.hostname, e.strerror))
        except Exception as e:
            self.ssh_client = None
            raise MachineException("%s: %s" % (self.hostname, str(e)))

    def refresh(self):
        """
            Retreive the latest control group and process data from the machine using an SSH
            connection. This method blocks while it waits for a response, so it should not be
            called from the main GUI thread.
        """
        self.__connect()
        with self.ssh_client.open_sftp() as sftp_client:
            self.cgtree = CGTree(sftp_client).tree

    def migrate(self, target, pid):
        """
            Attempt to migrate a process from this machine to another.  This blocks, so it
            shouldn't be called from the main thread.
        """
        self.__connect()
        target.__connect()

        stderr = migrate(self.ssh_client, target.ssh_client, pid)

        if stderr:
            raise MachineException(stderr)

    def get_cgtree(self):
        """
            Return a dict with a tree of control groups and process on the remote machine
            (see criugui.remote.cgtree).
        """

        return self.cgtree
