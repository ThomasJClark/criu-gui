# criugui - migrate.py
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

DUMP_CMD = "/usr/sbin/criu dump --leave-running --manage-cgroups -t %s -D %s"
RESTORE_CMD = "/usr/sbin/criu restore --restore-detached --manage-cgroups -D %s"
ARCHIVE_CMD = "tar czf %s %s"
EXTRACT_CMD = "tar xzf %s -C /"


def migrate(source_ssh, target_ssh, pid):
    """
        Given a source and target paramiko.SSHClient, migrate the specified process from one
        machine to the other.  If CRIU prints out any error messages, they will be returned by
        this function.
    """

    temptar = get_stdout(source_ssh, "mktemp")
    tempdir = get_stdout(source_ssh, "mktemp -d")

    # Dump the process on the source machine
    stderr = get_stderr(source_ssh, DUMP_CMD % (pid, tempdir))
    if "Error" in stderr:
        return stderr

    # Archive the images and copy them over to the target machine
    get_stdout(source_ssh, ARCHIVE_CMD % (temptar, tempdir))

    with source_ssh.open_sftp() as source_sftp, target_ssh.open_sftp() as target_sftp:
        target_sftp.putfo(source_sftp.file(temptar), temptar, 0)

    # Extract the archive and restore the process on the target machine
    get_stdout(target_ssh, EXTRACT_CMD % temptar)
    stderr = get_stderr(target_ssh, RESTORE_CMD % tempdir)
    if "Error" in stderr:
        return stderr


def get_stdout(ssh_client, cmd):
    """
        Execute the given command with the given ssh client and return the entire stripped standard
        output.
    """
    _, stdout, _ = ssh_client.exec_command(cmd)
    return stdout.read().strip()


def get_stderr(ssh_client, cmd):
    """
        Execute the given command with the given ssh client and return the entire stripped standard
        error.
    """
    _, _, stderr = ssh_client.exec_command(cmd)
    return stderr.read().strip()
