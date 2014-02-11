import sys
from cx_Freeze import setup, Executable

build_exe_options = {
#    "packages": ["os"],
    'packages': ['email.mime.multipart','email.mime.base','email.mime.text'],
    'include_files': ["winxp.cfg","win7.cfg"],
#	'build_exe': {'include_msvcr': "C:\\WINDOWS\system32\\"},
    }

setup ( name = "MChron Reports",
        version = "0.0.5",
        description = "Report generator and emailer for Oruga Amarilla",
        options = {"build_exe": build_exe_options},
        executables = [Executable("mchron.py"),Executable("config.py")] )
