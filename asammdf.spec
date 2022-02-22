# -*- mode: python -*-
import argparse
from pathlib import Path
import site
import sys

asammdf_path = Path.cwd() / "asammdf" / "gui" / "asammdfgui.py"


def _cmd_line_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "spec",
        help="specfile",
    )

    parser.add_argument(
        "--console",
        action="store_true",
        help="show console, default False",
    )

    parser.add_argument(
        "--onefile",
        action="store_true",
        help="create single file, default False",
    )

    return parser


parser = _cmd_line_parser()
args, unknown = parser.parse_known_args(sys.argv[1:])


block_cipher = None
added_files = []

for root, dirs, files in os.walk(asammdf_path.parent / "ui"):
    for file in files:
        if file.lower().endswith(("ui", "png", "qrc")):
            added_files.append(
                (os.path.join(root, file), os.path.join("asammdf", "gui", "ui"))
            )

import pyqtlet2

pyqtlet_path = Path(pyqtlet2.__path__[0]).resolve()
site_packages = pyqtlet_path.parent
site_packages_str = os.path.join(str(site_packages), "")
for root, dirs, files in os.walk(pyqtlet_path):
    for file in files:
        if not file.lower().endswith(("py", "pyw")):
            file_name = os.path.join(root, file)
            dest = root.replace(site_packages_str, "")
            added_files.append((file_name, dest))

a = Analysis(
    [asammdf_path],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        "numpy.core._dtype_ctypes",
        "canmatrix.formats",
        "canmatrix.formats.dbc",
        "canmatrix.formats.arxml",
        "asammdf.blocks.cutils",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=not args.onefile,
)

if args.onefile:
    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        Tree(asammdf_path.parent),
        name="asammdfgui",
        debug=False,
        strip=False,
        upx=True,
        console=args.console,
        icon="asammdf.ico",
    )
else:
    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    exe = EXE(
        pyz,
        a.scripts,
        [],
        name="asammdfgui",
        exclude_binaries=True,
        bootloader_ignore_signals=False,
        debug=False,
        strip=False,
        console=args.console,
        icon="asammdf.ico",
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        Tree(asammdf_path.parent),
        upx=False,
        upx_exclude=[],
        name="asammdfgui",
    )
