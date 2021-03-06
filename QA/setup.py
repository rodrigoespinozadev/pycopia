#!/usr/bin/python2.7
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab


import sys
import os

import platutils

from glob import glob
from setuptools import setup, find_packages

NAME = "pycopia-QA"
VERSION = "1.0"


platinfo = platutils.get_platform()
CACHEDIR="/var/cache/pycopia"

# Some services, such as the Pyro nameserver, are set up to run as the
# "tester" psuedo-user.  This also creates the "testers" group that testing
# personnel should also be a member of.
def system_setup():
    if platinfo.is_linux():
        import os, pwd, grp
        if os.getuid() == 0:
            if platinfo.is_gentoo():
                try:
                    pwent = pwd.getpwnam("tester")
                except KeyError:
                    os.system("groupadd testers")
                    os.system("useradd -c Tester -g testers "
                    "-G users.uucp,audio,cdrom,dialout,video,games,usb,crontab,messagebus,plugdev "
                    "-m tester")
                    print ("Remember to change password for new user tester.")
                    #os.system("passwd tester")
                    pwent = pwd.getpwnam("tester")
                if not os.path.isdir(CACHEDIR):
                    tgrp = grp.getgrnam("testers")
                    os.mkdir(CACHEDIR)
                    os.chown(CACHEDIR, pwent.pw_uid, tgrp.gr_gid)
                    os.chmod(CACHEDIR, 0o770)


if platinfo.is_linux():
    DATA_FILES = [
            ('/etc/pycopia', glob("etc/*.dist")),
    ]
    if platinfo.is_gentoo():
        DATA_FILES.append(('/etc/init.d', glob("etc/init.d/gentoo/*")))
    elif platinfo.is_redhat():
        DATA_FILES.append(('/etc/init.d', glob("etc/init.d/redhat/*")))
    if os.path.isdir("/etc/systemd/system"):
        DATA_FILES.append(('/etc/systemd/system', glob("etc/systemd/system/*")))
    SCRIPTS = glob("bin/*")

    WEBSITE = os.environ.get("WEBSITE", "localhost")
    DATA_FILES.extend([
        #(os.path.join("/var", "www", WEBSITE, 'htdocs'), glob("doc/html/*.html")),
        #(os.path.join("/var", "www", WEBSITE, 'cgi-bin'), glob("doc/html/cgi-bin/*.py")),
        (os.path.join("/var", "www", WEBSITE, 'media', 'js'), glob("media/js/*.js")),
        (os.path.join("/var", "www", WEBSITE, 'media', 'css'), glob("media/css/*.css")),
        #(os.path.join("/var", "www", WEBSITE, 'media', 'images'), glob("media/images/*.png")),
    ])

else:
    DATA_FILES = []
    SCRIPTS = []


setup (name=NAME, version=VERSION,
    namespace_packages = ["pycopia"],
    packages = find_packages(),
#    install_requires = [
#        'pycopia-CLI>=1.0.dev-r138,<=dev',
#        'pycopia-storage>=1.0.dev-r138,<=dev',
#        'pycopia-WWW>=1.0.dev-r279,<=dev',
#        'Pyro4>=4.13',
#        'chardet>=2.2',
#        ],
    dependency_links = [
            "http://www.pycopia.net/download/"
                ],
    scripts = SCRIPTS,
    data_files = DATA_FILES,
    package_data = {"": ['*.glade']},
    test_suite = "test.QATests",

    description = "Pycopia packages to support professional QA roles.",
    long_description = """Pycopia packages to support professional QA roles.
    A basic QA automation framework. Provides base classes for test cases,
    test suites, test runners, reporting, lab models, terminal emulators,
    remote control, and other miscellaneous functions.
    """,
    license = "LGPL",
    author = "Keith Dart",
    author_email = "keith@dartworks.biz",
    keywords = "pycopia QA framework",
    url = "http://www.pycopia.net/",
    #download_url = "ftp://ftp.pycopia.net/pub/python/%s.%s.tar.gz" % (NAME, VERSION),
    classifiers = ["Operating System :: POSIX",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Software Development :: Quality Assurance",
                   "Intended Audience :: Developers"],
)


if "install" in sys.argv:
    system_setup()

