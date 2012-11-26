#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    project_path = os.path.join(os.path.dirname(__file__), '..')
    sys.path.insert(1, os.path.realpath(os.path.realpath(project_path)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
