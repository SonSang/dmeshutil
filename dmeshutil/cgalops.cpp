#include <math.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cstdio>
#include <sstream>
#include <iostream>
#include <tuple>
#include <stdio.h>
#include <memory>
#include <fstream>
#include <string>
#include <functional>
#include <chrono>

#include "ops.h"

namespace py = pybind11;

std::tuple<py::array_t<int>, py::array_t<float>, float>
ComputeDT(
    const py::array_t<float>& positions,
    const py::array_t<float>& weights,
    const bool weighted,
    const bool compute_cc) {
    
    auto positions_buf = positions.request();
    int num_points = positions_buf.shape[0];
    int dimension = positions_buf.shape[1];

    const float* positions_ptr = static_cast<float*>(positions.request().ptr);
    const float* weights_ptr = static_cast<float*>(weights.request().ptr);

    auto dt_result = CGALOPS::run_DT(
        num_points, dimension,
        positions_ptr,
        weights_ptr,
        true,
        compute_cc
    );

    py::array_t<int> tet_array({dt_result.num_tri, 4});
    auto tet_ptr = tet_array.mutable_unchecked<2>();
    std::memcpy(tet_ptr.mutable_data(0, 0), dt_result.tri_verts_idx, dt_result.num_tri * 4 * sizeof(int));

    py::array_t<float> cc_array({0,});
    if (compute_cc) {
        cc_array.resize({dt_result.num_tri, dimension});
        auto cc_ptr = cc_array.mutable_unchecked<2>();
        std::memcpy(cc_ptr.mutable_data(0, 0), dt_result.tri_cc, dt_result.num_tri * dimension * sizeof(float));
    }

    return std::make_tuple(tet_array, cc_array, dt_result.time_sec);
}