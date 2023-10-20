from os.path import join, exists
from numpy import array, save

from mesh_selector import MeshSelector


for file in ['constraints', 'forces']:

    if not exists(f := join('data', f'{file}.npy')):
        save(f, array([]))

    plt = MeshSelector(mesh_file=join('data', 'volume.vtk'),
                       selection_file=f)
    plt.launch(title=f'{file}_selection')
    plt.save(overwrite=True)
    del plt
