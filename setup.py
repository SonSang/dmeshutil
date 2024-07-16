import sys
DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(DIR, "external", "pybind11"))

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os
os.path.dirname(os.path.abspath(__file__))

setup(
    name="dmeshutil",
    packages=['dmeshutil'],
    ext_modules=[
        Pybind11Extension(
            name="dmeshutil._C",
            sources=["dmeshutil/ext.cpp",
                    "dmeshutil/cgalops.cpp",],
            include_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "cgal_wrapper/")],
            library_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "cgal_wrapper/")],
            libraries=["cgal_wrapper", "gmp", "mpfr"],
        ),
    ],
)