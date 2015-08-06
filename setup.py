#!/usr/bin/env python
from setuptools import setup

setup(name="criugui",
      version="0.2.0",
      description="Graphical process migration tool",
      author="Tom Clark",
      author_email="tclark@redhat.com",
      install_requires=["paramiko"],
      packages=["criugui", "criugui.view", "criugui.remote"],
      entry_points={
          "gui_scripts": ["criugui = criugui.__main__:main"],
      })
