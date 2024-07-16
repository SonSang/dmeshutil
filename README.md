# Dmeshutil

Dmeshutil provides functions to handle `dmesh` data formats. A `dmesh` file is currently represented as a `.npz` file that contains point positions, weights, and reality values. Point positions and weights are used for Weighted Delaunay Triangulation (WDT), and reality values are used to extract faces on the tetrahedralization to define the mesh.

## Install

Please clone this repository recursively to include all submodules.

```bash
git clone https://github.com/SonSang/dmeshutil.git --recursive
```

### Dependencies

Please install necessary python libraries as follows.

```bash
pip install -r requirements.txt
```

### CGAL

We use [CGAL](https://github.com/CGAL/cgal) to run the Weighted Delaunay Triangulation (WDT) algorithm. If you cloned this repository recursively, you should already have the latest CGAL source code in the `external/cgal` directory. Please follow the instructions below to build and install CGAL.

```bash
cd external/cgal
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
```

You might need to install some additional dependencies to build CGAL. Please refer to the [official documentation](https://doc.cgal.org/latest/Manual/thirdparty.html) and install essential third party libraries, such as Boost, GMP, and MPFR, to build CGAL and CGAL-dependent code successfully. If you are using Ubuntu, you can install GMP and MPFR with following commands.

```bash
sudo apt-get install libgmp3-dev
sudo apt-get install libmpfr-dev
```

Then, run the following commands to build CGAL-dependent codes. You would be able to find `libcgal_diffdt.a` file in cgal_wrapper/ directory.

```bash
cd cgal_wrapper
cmake -DCMAKE_BUILD_TYPE=Release .
make
```

Finally, run following command.

```bash
pip install -e .
```

## Usage

### dmesh to .obj

Following command converts dmesh files in `data` folder to `.obj` files, which would be stored in `output` folder. We converted two mesh data from [Thingi10K](https://ten-thousand-models.appspot.com/) dataset into `dmesh` format, and use it for this example.

```bash
python dmesh_obj_converter.py
```