# criugui - cgtree.py
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


import os
import stat


class CGTree:

    """
        Given a paramiko.SFTPClient, this class builds up a tree of control groups and child
        processes on the remote machine and parses it into a dictionary with the following form:

        cgt.tree = {"name": "my_control_group", "children": [
                     {"name": "my_parent_process", "pid": 10000, "children": [
                       {"name": "my_child_process1", "pid": 10001, "children": [] },
                       {"name": "my_child_process2", "pid": 10002, "children": [] }]}]}

        This is used to monitor running processes on another machine using only an SSH server, so
        it can work with machines not running a special server specific to this application.
    """

    def __init__(self, sftp_client):
        self.sftp_client = sftp_client
        self.tree = self.__parse_cgroups()

    def __parse_cgroups(self, path="/sys/fs/cgroup/systemd"):
        """
            Return a tree of all of the processes and subgroups in the control group that is at the
            given path.
        """

        # Get a process tree that includes all processes in this control group from the remote
        # machine.  The file "cgroup.procs" has a list of PIDS, so we can just look up all of those
        # processes and unflatten them into a tree.
        with self.sftp_client.file(os.path.join(path, "cgroup.procs")) as pids:
            flatprocs = [self.__parse_proc(pid[:-1]) for pid in pids]
            procs = self.__unflatten_procs(flatprocs)

        # Recursively call this function on each subdirectory, building up a tree of control groups
        # and processes.
        subgroups = []
        for subgroup in self.sftp_client.listdir(path.encode("utf-8")):
            if stat.S_ISDIR(self.sftp_client.stat(os.path.join(path, subgroup)).st_mode):
                subgroups.append(self.__parse_cgroups(os.path.join(path, subgroup)))

        return {"name": os.path.basename(path), "children": procs + subgroups}

    def __parse_proc(self, pid):
        """Read a "/proc/.../stat" file and return a dictionary of the important properties."""

        try:
            with self.sftp_client.file(os.path.join("/proc", pid, "stat")) as stat:
                    line = stat.readline()
                    a, b = line.find("("), line.rfind(")")
                    name = line[a + 1:b]
                    ppid = line[b + 2:].split(" ")[1]

            return {"name": name, "pid": pid, "ppid": ppid, "children": []}
        except IOError:
            # It's possible for the process to terminate in the middle of us building up the tree.
            # In that case, ignore it - it isn't running anyway.
            pass

    def __unflatten_procs(self, procs):
        """
        Given an flat array of dicts (as returned by __parse_proc), return an array of the dicts
        whose parents were not in the original array, with the rest added to the children arrays in
        the parents' dicts, essentially rearranging the same flat list of processes into a tree.
        """

        for proc in procs:
            for proc2 in procs:
                if proc and proc2 and ("ppid" in proc) and (proc2["pid"] == proc["ppid"]):
                    proc2["children"].append(proc)
                    del proc["ppid"]
                    break

        newprocs = []
        for proc in procs:
            if proc and ("ppid" in proc):
                del proc["ppid"]
                newprocs.append(proc)

        return newprocs
