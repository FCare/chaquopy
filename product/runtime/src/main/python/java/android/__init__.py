"""Copyright (c) 2018 Chaquo Ltd. All rights reserved."""

from __future__ import absolute_import, division, print_function

import os
from os.path import exists, join
import sys
import traceback
from . import stream, importer


def initialize(context, app_path):
    stream.initialize()
    initialize_stdlib(context)
    importer.initialize(context, app_path)


def initialize_stdlib(context):
    # argv defaults to not existing, which may crash some programs.
    sys.argv = [""]

    # executable defaults to "python" on 2.7, or "" on 3.6. But neither of these values (or
    # None, which is mentioned in the documentation) will allow platform.platform() to run
    # without crashing.
    try:
        sys.executable = os.readlink("/proc/{}/exe".format(os.getpid()))
    except Exception:
        # Can't be certain that /proc will work on all devices, so try to carry on.
        traceback.print_exc()
        sys.executable = ""

    # tempfile
    tmpdir = join(str(context.getCacheDir()), "chaquopy/tmp")
    if not exists(tmpdir):
        os.makedirs(tmpdir)
    os.environ["TMPDIR"] = tmpdir
