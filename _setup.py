from distutils.core import setup
import py2exe, sys, os

sys.argv.append("py2exe")
sys.path.append("./src")

setup(
    options = {"py2exe": {
        "optimize": 2,
        "dll_excludes": ["MSVCP90.dll"],
        'dist_dir': "bin"
    }},
    windows = [{
		"script": "src/main.py",
		"dest_base": "bg",
	}],
)