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

## Limitations

CRIU is always passed the same command line arguments - `criu dump --leave-running --manage-cgroups` and
`criu restore --restore-detached --manage-cgroups`.  It might be a good idea to make this configurable,
since many processes will only dump/restore correctly by adding some arguments.

Shell jobs cannot be migrated.  If the `--shell-job` flag is specified, CRIU checks if stdin is actually
a TTY, and returns an error if it's not.  I'm not sure if shell jobs can be migrated besides manually in
an interactive terminal.

## Screenshots

![00](https://cloud.githubusercontent.com/assets/3964980/9137284/ac57c0e6-3cea-11e5-9ac0-9ed633d51057.png)

![01](https://cloud.githubusercontent.com/assets/3964980/9137285/ac61282a-3cea-11e5-8c49-8564a2cf627f.png)

![02](https://cloud.githubusercontent.com/assets/3964980/9137286/ac63f1f4-3cea-11e5-84c2-4ee0e0003acc.png)

![03](https://cloud.githubusercontent.com/assets/3964980/9137287/ac65259c-3cea-11e5-8150-ba8c55b63a7e.png)

![04](https://cloud.githubusercontent.com/assets/3964980/9137289/ac65ec20-3cea-11e5-937a-fb63d41afcd9.png)

![05](https://cloud.githubusercontent.com/assets/3964980/9137288/ac65a1f2-3cea-11e5-9aba-138eb201ef2f.png)
