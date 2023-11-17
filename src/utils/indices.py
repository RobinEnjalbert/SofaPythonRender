import Sofa
from vedo import Mesh
import numpy as np


def __convert_indices(src_pos: np.ndarray, dst_pos: np.ndarray, indices: np.ndarray):
    src_pos = src_pos[indices]
    dst_pos = np.tile(dst_pos, reps=(src_pos.shape[0], 1)).reshape((src_pos.shape[0], -1, 3))
    src_pos = np.tile(src_pos.reshape((-1, 1, 3)), reps=(dst_pos.shape[1], 1))
    return np.argmin(np.linalg.norm(dst_pos - src_pos, axis=-1), axis=1)


def vedo_to_sofa_indices(vedo_mesh: Mesh, sofa_mesh: Sofa.Core.Object, indices: np.ndarray):
    return __convert_indices(src_pos=vedo_mesh.vertices,
                             dst_pos=sofa_mesh.position.value,
                             indices=indices)


def sofa_to_vedo_indices(sofa_mesh: Sofa.Core.Object, vedo_mesh: Mesh, indices: np.ndarray):
    return __convert_indices(src_pos=sofa_mesh.position.value,
                             dst_pos=vedo_mesh.vertices,
                             indices=indices)
