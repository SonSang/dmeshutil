import numpy as np
from . import _C

class DTStruct:
    def __init__(self):
        # WPoints
        self.ppos: np.ndarray = None
        self.pw: np.ndarray = None
        
        # [# tet, 4], indices of points for each tetrahedron
        self.tets_point_id: np.ndarray = None

        # [# tet, # dim], circumcenters of tetrahedra
        self.tets_cc: np.ndarray = None

        # float, computation time
        self.time_sec: float = -1.

    @staticmethod
    def forward(ppos: np.ndarray,
                pw: np.ndarray, 
                weighted: bool, 
                compute_cc: bool):

        result = _C.delaunay_triangulation(ppos, 
                                        pw, 
                                        weighted,
                                        compute_cc)

        rstruct = DTStruct()
        rstruct.ppos = ppos
        rstruct.pw = pw
        rstruct.tets_point_id = result[0]
        rstruct.tets_cc = result[1]
        rstruct.time_sec = result[2]
        
        return rstruct