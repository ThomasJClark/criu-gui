# CRIU Process Migration GUI

A GTK interface for live process migration with CRIU.

This program displays control groups on any number of remote machines in a tree format.  The user
can migrate a process from one machine to another by simply dragging and dropping it into a
another tree.

## Dependencies

* Python 2 or 3
* GTK+ 3.10 or newer
* Paramiko (`pip install paramiko`)
* [CRIU](http://criu.org/) and a kernel new enough for CRIU to run on (on the remote machines)

## Instructions
Run `python -m criugui` to start the program.

To add a new machine, use the "+" button and fill out the dialog.  SSH will be used to connect to the
machine, so a special server is not needed, but you must be able to log in as root.

The tree under each machine displays the hierarchy of control groups on the system, and a process tree is
shown within each control group.  If a new process is started or an existing one terminates, you can
reload the processes with the refresh button.  To search for a process by name, just begin typing.

To migrate a process, click and drag it from one machine to another.  You will be informed of the success
or failure of the migration when it completes.

The command line options passed to CRIU default to basically `--leave-running --manage-cgroups` for dumping
and `-restore-detached --manage-cgroups` for restoring.  To edit these, click the terminal button in the
headerbar.

## Limitations

Shell jobs cannot be migrated.  If the `--shell-job` flag is specified, CRIU checks if stdin is actually
a TTY, and returns an error if it's not.  I'm not sure if shell jobs can be migrated besides manually in
an interactive terminal.

## Screenshots

![00](https://cloud.githubusercontent.com/assets/3964980/9142609/dd2aac0a-3d0e-11e5-97b1-6fd257175cec.png)

![01](https://cloud.githubusercontent.com/assets/3964980/9142611/dd567c9a-3d0e-11e5-9c1d-81073815bf0e.png)

![02](https://cloud.githubusercontent.com/assets/3964980/9142612/dd5678c6-3d0e-11e5-9e3e-9f34c57386e6.png)

![03](https://cloud.githubusercontent.com/assets/3964980/9142610/dd551de6-3d0e-11e5-8faa-8a3b5bd7cc30.png)

![04](https://cloud.githubusercontent.com/assets/3964980/9142614/dd57c992-3d0e-11e5-8931-a65ae77405e8.png)

![05](https://cloud.githubusercontent.com/assets/3964980/9142613/dd579846-3d0e-11e5-85c8-6f951421a662.png)

