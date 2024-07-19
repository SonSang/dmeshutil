from dmeshutil.cgalops import DTStruct
from dmeshutil.utils import extract_faces
import numpy as np
import trimesh
import itertools

class DMesh:

    def __init__(self, ppos: np.ndarray, pw: np.ndarray, pr: np.ndarray, pti: np.ndarray, tok: np.ndarray):
        '''
        N = number of points, M = number of tokens, K = number of values per token.

        @ ppos: [N, 3] numpy array, point positions.
        @ pw: [N] numpy array, point weights.
        @ pr: [N] numpy array, point reals.
        @ pti: [N] numpy array, token index for each point, -1 if not assigned.
        @ tok: [M, K] numpy array, token values.
        '''
        DMesh.validate_input(ppos, pw, pr, pti, tok)

        self.ppos = ppos
        self.pw = pw
        self.pr = pr
        self.pti = pti
        self.tok = tok

        self.faces = None

    @staticmethod
    def validate_input(ppos: np.ndarray, pw: np.ndarray, pr: np.ndarray, pti: np.ndarray, tok: np.ndarray):
        N = ppos.shape[0]
        M = tok.shape[0]
        assert ppos.shape == (N, 3), f"Invalid point position shape: {ppos.shape}"
        assert pw.shape == (N,), f"Invalid point weight shape: {pw.shape}"
        assert pr.shape == (N,), f"Invalid point real shape: {pr.shape}"
        assert pti.shape == (N,), f"Invalid point token shape: {pti.shape}"
        assert np.max(pti) < M, f"Invalid token index: {np.max(pti)}, maximum index: {M - 1}"

    @staticmethod
    def load(path: str):
        if path.endswith(".npz"):
            data = np.load(path)

            # necessary fields
            if 'ppos' not in data:
                raise ValueError("Invalid DMesh file: point position not found")
            if 'pr' not in data:
                raise ValueError("Invalid DMesh file: point real not found")

            ppos = data['ppos']
            pr = data['pr']
            
            # optional fields
            if 'pw' not in data:
                pw = np.zeros_like(data['ppos'][:, 0])  # assume uniform weight
            else:
                pw = data['pw']

            if 'pti' not in data:
                pti = -np.ones_like(data['ppos'][:, 0])
                tok = np.zeros((0, 0))
            else:
                pti = data['pti']
                if 'tok' not in data:
                    print("Warning: token values not found, while token index found")
                    print("Assuming zero token values")
                    maxpti = int(np.max(pti))
                    tok = np.zeros((maxpti + 1, 1))
                else:
                    tok = data['tok']

            return DMesh(ppos, pw, pr, pti, tok)
        else:
            raise ValueError("Invalid DMesh file: unknown file extension")
    
    def save(self, path: str, format: str='npz'):
        if format == 'npz':
            data = {
                "ppos": self.ppos,
                "pw": self.pw,
                "pr": self.pr,
                "pti": self.pti,
                "tok": self.tok
            }
            np.savez(path, data)
        else:
            raise ValueError("Invalid format")

    def extract_faces(self, force: bool):
        if force or self.faces is None:
            # compute wdt
            dt = DTStruct.forward(self.ppos, self.pw, True, False)
            tets = dt.tets_point_id
            faces = extract_faces(tets)
            
            # 1. select faces with only real values
            face_reals = self.pr[faces].min(axis=1)
            faces = faces[face_reals > 0.5]

            # 2. select faces using tokens
            # 2-1. faces comprised of any point with negative [pti] value are included
            faces_pti = self.pti[faces].min(axis=1)
            efaces0 = faces[faces_pti < 0]

            # 2-2. lookup tokens
            faces = faces[faces_pti >= 0]
            face_tokens = self.tok[self.pti[faces]]
            face_existence = DMesh.eval_face_existence_using_tokens(face_tokens)
            efaces1 = faces[face_existence]

            self.faces = np.concatenate([efaces0, efaces1], axis=0)

    @staticmethod
    def eval_face_existence_using_tokens(self, face_tokens: np.ndarray):
        '''
        Evaluate the existence of a face using tokens.
        
        @ face_tokens: [N, D, K] numpy array, token values for each face.
        (N = number of faces, D = number of vertices per face, K = number of values per token)
        
        For each face F, we evaluate following values:
            E(F) = \sum_{point pair P(i, j) in F} dot(Token(P(i)), Token(P(j)))

        If E(F) is larger or equal to zero, the face is considered to exist.
        Else, the face is considered to not exist.
        '''
        N, D, K = face_tokens.shape

        # compute dot products
        E = np.zeros(N)
        combs = itertools.combinations(range(D), 2)
        for comb in combs:
            E += np.sum(face_tokens[:, comb[0]] * face_tokens[:, comb[1]], axis=-1)
        
        return E >= 0

    def to_trimesh(self):
        self.extract_faces(False)
        return trimesh.Trimesh(vertices=self.ppos, faces=self.faces)