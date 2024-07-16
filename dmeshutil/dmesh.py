from dmeshutil.cgalops import DTStruct
import numpy as np
import trimesh

class DMesh:

    def __init__(self, ppos: np.ndarray, pw: np.ndarray, pr: np.ndarray):
        self.ppos = ppos
        self.pw = pw
        self.pr = pr

        self.faces = None

    @staticmethod
    def load(path: str):
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
    
    def save(self, path: str):
        data = {
            "ppos": self.ppos,
            "pw": self.pw,
            "pr": self.pr
        }
        np.savez(path, data)

    def extract_faces(self, force: bool):
        if force or self.faces is None:
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
            self.faces = faces[face_reals > 0.5]

    def to_trimesh(self):
        self.extract_faces(False)
        return trimesh.Trimesh(vertices=self.ppos, faces=self.faces)