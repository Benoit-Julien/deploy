#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup.py file generated by PkgLTS."""

# {{pkglts pysetup.kwds,
# format setup arguments
from os import walk
from os.path import abspath, normpath
from os.path import join as pj
from setuptools import setup, find_packages


short_descr = "OpenAlea.Deploy support the installation of OpenAlea packages via the network and manage their dependencies. It is an extension of Setuptools. "
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

# find version number in /src/$pkg_pth/version.py
version = {}
with open("src/openalea/deploy/version.py") as fp:
    exec(fp.read(), version)



setup_kwds = dict(
    name='openalea.deploy',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="openalea",
    author_email='christophe dot pradal at cirad dot fr',
    url='https://openalea.gforge.inria.fr',
    license="cecill-c",
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={},
    keywords='setuptools, openalea',
    test_suite='nose.collector',
)
# }}
# change setup_kwds below before the next pkglts tag

entry_points = {
    "distutils.setup_keywords": [
        "lib_dirs = openalea.deploy.command:validate_bin_dirs",
        "inc_dirs = openalea.deploy.command:validate_bin_dirs",
        "bin_dirs = openalea.deploy.command:validate_bin_dirs",
        "share_dirs = openalea.deploy.command:validate_share_dirs",
        "cmake_scripts = openalea.deploy.command:validate_cmake_scripts",
        "scons_scripts = openalea.deploy.command:validate_scons_scripts",
        "pylint_packages = openalea.deploy.command:validate_pylint_packages",
        "pylint_options = openalea.deploy.command:validate_pylint_options",
        "scons_parameters = setuptools.dist:assert_string_list",
        "create_namespaces = openalea.deploy.command:validate_create_namespaces",
        "postinstall_scripts = openalea.deploy.command:validate_postinstall_scripts",
        "add_plat_name = openalea.deploy.command:validate_add_plat_name",
    ],

    "egg_info.writers": [
        "lib_dirs.txt = openalea.deploy.command:write_keys_arg",
        "inc_dirs.txt = openalea.deploy.command:write_keys_arg",
        "bin_dirs.txt = openalea.deploy.command:write_keys_arg",
        "postinstall_scripts.txt = setuptools.command.egg_info:write_arg",
    ],

    "distutils.commands": [
        "cmake = openalea.deploy.command:cmake",
        "scons = openalea.deploy.command:scons",
        "create_namespaces = openalea.deploy.command:create_namespaces",
        "alea_install = openalea.deploy.command:alea_install",
        "alea_upload = openalea.deploy.command:alea_upload",
        "upload_sphinx = openalea.deploy.command:upload_sphinx",
        "pylint = openalea.deploy.command:pylint",
        "clean = openalea.deploy.command:clean",
        "egg_upload = openalea.deploy.command:egg_upload",
    ],

    "console_scripts": [
        "alea_install = openalea.deploy.alea_install:main",
        # "alea_uninstall = openalea.deploy.alea_update:uninstall_egg",
        "alea_config = openalea.deploy.alea_config:main",
        "alea_clean = openalea.deploy.alea_update:clean_version",
        "alea_update_all = openalea.deploy.alea_update:update_all",
        "alea_dependency_builder = openalea.deploy.system_dependencies.dependency_builder:main",
        "alea_system_deploy = openalea.deploy.system_dependencies.deploy_system2:main",
    ],

}
setup_kwds["entry_points"] = entry_points
setup_kwds["namespace_packages"] = ["openalea"]
setup_kwds["include_package_data"] = True

# do not change things below
# {{pkglts pysetup.call,
setup(**setup_kwds)
# }}
