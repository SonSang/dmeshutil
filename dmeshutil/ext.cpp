#include <pybind11/pybind11.h>
#include "cgalops.h"

PYBIND11_MODULE(_C, m) {
    m.def("delaunay_triangulation", &ComputeDT);
}