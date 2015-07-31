#!/usr/bin/env python
from setuptools import setup

setup(name="criugui",
      version="0.2.0",
      description="Graphical process migration tool",
      author="Tom Clark",
      author_email="tclark@redhat.com",
      install_requires=["web.py"],
      packages=["criugui", "criugui.view", "criuserver"],
      entry_points={
          "gui_scripts": ["criugui = criugui.__main__:main"],
          "console_scripts": ["criuserver = criuserver.__main__:main"]
      })
