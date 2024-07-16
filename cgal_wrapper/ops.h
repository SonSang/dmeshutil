#ifndef CGAL_WRAPPER_OPS_H_INCLUDED
#define CGAL_WRAPPER_OPS_H_INCLUDED

#include <vector>
#include <array>
#include <string>

namespace CGALOPS {

    struct DTResult {
        int*    tri_verts_idx = nullptr;
        float*  tri_cc = nullptr;          // circumcenters
        int     num_tri;
        float   time_sec;

        ~DTResult() {
            if (tri_verts_idx)
                delete[] tri_verts_idx;
            if (tri_cc)
                delete[] tri_cc;
        }
    };

    DTResult run_DT(
        int num_points, int dimension,
        const float* positions,
        const float* weights,
        const bool weighted,
        const bool compute_cc
    );
}

#endif