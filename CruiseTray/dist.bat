rm -rf dist CruiseTray CruiseTray.zip
setup.py py2exe --bundle 1 --dll-excludes msvcp90.dll
move dist CruiseTray
del CruiseTray\w9xpopen.exe
copy cruiseTrayIcon.py CruiseTray
zip -r CruiseTray.zip CruiseTray
copy CruiseTray.zip d:\bconrad\public
