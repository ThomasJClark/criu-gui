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

import web
import os
import json

CONTROL_GROUPS_PATH = "/sys/fs/cgroup/systemd"


class CGTree:

    def GET(self):
        tree = self.__parse_cgroups(CONTROL_GROUPS_PATH)

        web.header("Content-Type", "application/json")
        return json.dumps(tree)

    def __parse_proc(self, pid):
        """
        Read a "/proc/.../stat" file and return a dictionary of the important properties
        """
        with open(os.path.join("/proc", pid, "stat")) as stat:
            line = stat.readline()
            a, b = line.find("("), line.rfind(")")
            name = line[a + 1:b]
            ppid = line[b + 2:].split(" ")[1]

        return {"name": name, "pid": pid, "ppid": ppid, "children": []}

    def __unflatten_procs(self, procs):
        """
        Given an flat array of dicts (as returned by __parse_proc), return an array of the dicts
        whose parents were not in the original array, with the rest added to the children arrays in
        the parents' dicts.
        """
        for proc in procs:
            for proc2 in procs:
                if "ppid" in proc and proc2["pid"] == proc["ppid"]:
                    proc2["children"].append(proc)
                    del proc["ppid"]
                    break

        for proc in procs:
            if "ppid" in proc:
                del proc["ppid"]
                yield proc

    def __parse_cgroups(self, path):
        """
        Return a dict representing the control group at the given path in "/sys/fs/cgroup/...".
        The dict contains a name and a list of children, which include both child control groups
        and the processes in this group.
        """
        dirpath, subgroups, filenames = next(os.walk(path))

        with open(os.path.join(dirpath, "cgroup.procs")) as f:
            procs = list(self.__unflatten_procs([self.__parse_proc(pid[:-1]) for pid in f]))
        cgroups = [self.__parse_cgroups(os.path.join(dirpath, cgroup)) for cgroup in subgroups]

        return {"name": os.path.basename(path), "children": procs + cgroups}
