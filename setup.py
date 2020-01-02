#
import sys, os
import setuptools
from   setuptools import setup, Extension
from   setuptools.command.build_ext import build_ext

import distutils.cygwinccompiler
#distutils.cygwinccompiler.get_msvcr = lambda: []

__version__ = '1.0.2'  # Get version from cppEDM Parameter.cc ?

# e.g. /tmp/pip-req-build-9ljrp27z/
tmpInstallPath = os.path.dirname( os.path.abspath( __file__ ) )
EDM_Lib_Path   = os.path.join( tmpInstallPath, "cppEDM/lib" )
EDM_H_Path     = os.path.join( tmpInstallPath, "cppEDM/src" )
Bindings_Path  = os.path.join( tmpInstallPath, "src/bindings/" )

# Set default cppEDM library name
platform = sys.platform
if True:#platform == 'darwin' or platform == 'linux':
    cppLibName = 'libEDM.a'
    import subprocess
    build_libEDM = subprocess.Popen(["make", "-C", "./cppEDM/src"], 
                                           stderr=subprocess.STDOUT)
    build_libEDM.wait()

elif sys.platform == 'win32':
    cppLibName = 'EDM.lib'
else: # assume unix
    cppLibName = 'libEDM.a'

cppLibName = "libEDM.a"

# We are building the package, see if libEDM exists
if not os.path.isfile( os.path.join( EDM_Lib_Path, cppLibName ) ) :
    errStr = "Error: " + os.path.join( "./cppEDM/src/lib", cppLibName ) +\
             " does not exist.\n\nYou can install cppEDM manually per: " +\
             "https://github.com/SugiharaLab/pyEDM#manual-install."
    raise Exception( errStr )
         
# Transfer the README.md to the package decsription
with open(os.path.join(tmpInstallPath, 'README.md')) as f:
    long_description = f.read()
    
#----------------------------------------------------------------------
#
#----------------------------------------------------------------------
class get_pybind_include( object ):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked."""

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

#----------------------------------------------------------------------
# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
#----------------------------------------------------------------------
def has_flag( compiler, flagname ):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler."""
    
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------
def cpp_flag( compiler ):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available)."""
    
    if has_flag( compiler, '-std=c++14' ):
        return '-std=c++14'
    elif has_flag( compiler, '-std=c++11' ):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------


class BuildExt( build_ext ):
    
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [ '-llapack' ],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-llapack',
                           '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' %
                        self.distribution.get_version())
            # opts.append('/link /MACHINE:X86')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


on_windows = sys.platform.startswith('win')

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------
Extension_modules = [
    Extension(
        name = 'pyBindEDM',

        sources = [ Bindings_Path + 'PyBind.cpp' ],
        
        include_dirs = [
            get_pybind_include(), # Path to pybind11 headers
            get_pybind_include( user = True ),
            EDM_H_Path # Path to cppEDM headers
        ],
        
        language     = 'c++',
        library_dirs = [ EDM_Lib_Path, '/usr/lib/'],
        extra_compile_args=['-std=c++11',"-D_hypot=hypot"],
        libraries    = ['EDM','openblas','gfortran','pthread','m','quadmath'] if on_windows else ['EDM','lapack'],
        extra_link_args=["-static", "-static-libgfortran", "-static-libgcc"]
    ),
]

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------
setup(
    # name of the *-version.dist-info directory
    name             = 'pyEDM', 
    version          = __version__,
    author           = 'Joseph Park & Cameron Smith',
    author_email     = 'Sugihara.Lab@gmail.com',
    url              = 'https://github.com/SugiharaLab/pyEDM',
    description      = 'Python wrapper for cppEDM using pybind11',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license          = 'Copyright 2019 The Regents of the University ' +\
                       'of California.',
    packages         = setuptools.find_packages(), # Enable ./EDM Python module
    ext_modules      = Extension_modules,
    package_data     = { 'pyEDM' : ['data/*.csv', 'tests/*.py' ]},
    #test_suite      = "tests", # ??? [1]
    install_requires = ['pybind11>=2.2', 'pandas>=0.20.3', 'matplotlib>=2.2'],
    python_requires  = '>=3',
    #cmdclass         = { 'build_ext' : BuildExt }, # Command/class to build .so
    zip_safe         = False,
)
#----------------------------------------------------------------------
# [1] This test_suite doesn't seem terribly useful here in that its use
#     seems to be to enable "python setup.py test" as a way to test
#     functionality prior to deployment, or perhaps from a source
#     distribution (sdist command) build/test. See:
#     https://setuptools.readthedocs.io/en/latest/setuptools.html
#           #test-build-package-and-run-a-unittest-suite
#
#     One can run the tests in EDM/tests: python -m unittest discover
#----------------------------------------------------------------------
