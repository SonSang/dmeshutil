from dmeshutil.cgalops import DTStruct
from dmeshutil.render import render_mesh3d
import numpy as np
import trimesh
from plyfile import PlyData, PlyElement
import igl

class DMesh:

    def __init__(self, ppos: np.ndarray, pw: np.ndarray, pr: np.ndarray):
        self.ppos = ppos
        self.pw = pw
        self.pr = pr

        self.r_faces = None
        self.i_faces = None

    @staticmethod
    def load(path: str):
        if path.endswith(".npz"):
            data = np.load(path)
            if 'ppos' not in data:
                raise ValueError("Invalid DMesh file: point position not found")
            if 'pr' not in data:
                raise ValueError("Invalid DMesh file: point real not found")
            if 'pw' not in data:
                pw = np.zeros_like(data['ppos'][:, 0])  # assume uniform weight
            else:
                pw = data['pw']
            return DMesh(data["ppos"], pw, data["pr"])
        elif path.endswith(".ply"):
            data = PlyData.read(path)

            # ppos
            ppos_x = data['vertex']['x']
            ppos_y = data['vertex']['y']
            ppos_z = data['vertex']['z']
            ppos = np.stack([ppos_x, ppos_y, ppos_z], axis=1)

            # pw
            if 'weight' in data['vertex']:
                pw = data['vertex']['weight']
            else:
                pw = np.zeros_like(ppos_x)

            # pr
            pr = data['vertex']['real']
            return DMesh(ppos, pw, pr)
        else:
            raise ValueError("Invalid DMesh file: unknown extension")
    
    def save(self, path: str):
        if path.endswith(".npz"):
            data = {
                "ppos": self.ppos,
                "pw": self.pw,
                "pr": self.pr
            }
            np.savez(path, data)
        elif path.endswith(".ply"):
            data = [
                ('vertex', [
                    ('x', 'f4'),
                    ('y', 'f4'),
                    ('z', 'f4'),
                    ('real', 'f4'),
                    ('weight', 'f4')
                ])
            ]
            vertices = []
            for i in range(len(self.ppos)):
                vertices.append((self.ppos[i][0], self.ppos[i][1], self.ppos[i][2], self.pr[i], self.pw[i]))
            vertices = np.array(vertices, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('real', 'f4'), ('weight', 'f4')])
            el = PlyElement.describe(vertices, 'vertex')
            PlyData([el], text=True).write(path)
        else:
            raise ValueError("Invalid DMesh file: unknown extension")

    def extract_faces(self, force: bool):
        if force or (self.r_faces is None or self.i_faces is None):
            # compute wdt
            dt = DTStruct.forward(self.ppos, self.pw, True, False)
            tets = dt.tets_point_id
            faces = []
            for comb in [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]:
                faces.append(tets[:, comb])
            faces = np.concatenate(faces, axis=0)
            faces = np.sort(faces, axis=1)
            faces = np.unique(faces, axis=0)
            
            face_reals = self.pr[faces].min(axis=1)
            self.r_faces = faces[face_reals > 0.5]
            self.i_faces = faces[face_reals <= 0.5]

            # orient real faces
            self.r_faces, _ = igl.bfs_orient(self.r_faces)

    def to_trimesh(self):
        self.extract_faces(False)
        return trimesh.Trimesh(vertices=self.ppos, faces=self.faces)
    
    def render_plotly(self, imag_opacity: float, path: str):
        self.extract_faces(False)

        vertices = [self.ppos, self.ppos]
        faces = [self.r_faces, self.i_faces]
        color = ['blue', 'grey']
        opacity = [1.0, imag_opacity]
        render_face = [True, True]
        render_vert = [False, False]
        
        render_mesh3d(vertices, faces, color, opacity, render_face, render_vert, path)