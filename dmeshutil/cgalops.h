#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cstdio>
#include <tuple>
#include <string>

/*
CGAL operations
*/

namespace py = pybind11;

// Delaunay triangulation
std::tuple<py::array_t<int>, py::array_t<float>, float>
ComputeDT(
    const py::array_t<float>& positions,
    const py::array_t<float>& weights,
    const bool weighted,
    const bool compute_cc
);