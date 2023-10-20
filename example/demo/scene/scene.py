import Sofa
from os.path import join, dirname
import numpy as np
from vedo import Mesh


def get_file(filename: str):
    data_dir = 'data'
    return join(dirname(__file__), data_dir, *filename.split('/'))


def get_plugin_list():
    with open(get_file('plugins.txt'), 'r') as file:
        plugins = []
        for plugin in file.readlines():
            if plugin != '\n':
                plugins.append(plugin[:-1])
    return plugins


class Scene(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, name='Controller', *args, **kwargs)

        self.root = Sofa.Core.Node('root')
        self.root.addObject(self)
        self.create_graph()
        self.idx_step = 0

    def create_graph(self):

        self.root.dt.value = 0.1
        self.root.addObject('RequiredPlugin', pluginName=get_plugin_list())
        self.root.addObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showForceFields')
        self.root.addObject('DefaultAnimationLoop')
        self.root.addObject('GenericConstraintSolver', maxIterations=10, tolerance=1e-3)
        self.root.addObject('DefaultPipeline')
        self.root.addObject('BruteForceBroadPhase')
        self.root.addObject('BVHNarrowPhase')
        self.root.addObject('DiscreteIntersection')
        self.root.addObject('DefaultContactManager')

        self.root.addChild('logo')
        self.root.logo.addObject('EulerImplicitSolver', firstOrder=False, rayleighMass=0.1, rayleighStiffness=0.1)
        self.root.logo.addObject('CGLinearSolver', iterations=25, tolerance=1e-9, threshold=1e-9)
        self.root.logo.addObject('MeshVTKLoader', name='mesh', filename=get_file('volume.vtk'), rotation=[90, 0, 0])
        self.root.logo.addObject('TetrahedronSetTopologyContainer', name='topology', src='@mesh')
        self.root.logo.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
        self.root.logo.addObject('MechanicalObject', name='state', src='@topology')
        self.root.logo.addObject('TetrahedronFEMForceField', youngModulus=2000, poissonRatio=0.4, method='svd')
        self.root.logo.addObject('MeshMatrixMass', totalMass=0.01)
        self.root.logo.addObject('FixedConstraint', name='constraints')

        self.root.logo.addChild('forces')
        self.root.logo.forces.addObject('MechanicalObject', name='state', src='@../topology')
        self.root.logo.forces.addObject('IdentityMapping')

        self.root.logo.addChild('collision')
        self.root.logo.collision.addObject('TriangleSetTopologyContainer', name='topology')
        self.root.logo.collision.addObject('TriangleSetTopologyModifier', name='Modifier')
        self.root.logo.collision.addObject('Tetra2TriangleTopologicalMapping', input='@../topology', output='@topology')
        self.root.logo.collision.addObject('MechanicalObject', name="state", rest_position="@../state.rest_position")
        self.root.logo.collision.addObject('TriangleCollisionModel')
        self.root.logo.collision.addObject('IdentityMapping')

        self.root.logo.addChild('visual')
        self.root.logo.visual.addObject('MeshOBJLoader', name='mesh', filename=get_file('surface.obj'), rotation=[90, 0, 0])
        self.root.logo.visual.addObject('OglModel', name='ogl', color='0.85 .3 0.1 0.9', src='@mesh')
        self.root.logo.visual.addObject('BarycentricMapping')

    def onSimulationInitDoneEvent(self, _):

        # Get the position of the constraint in Vedo since the indexing is different (SOFA = vtk file)
        positions = Mesh(get_file('volume.vtk')).rotate_x(90).points()[np.load(get_file('constraints.npy'))]
        sofa_pos = np.tile(self.root.logo.state.position.value, (positions.shape[0], 1)).reshape(positions.shape[0], -1,
                                                                                                 3)
        positions = np.tile(positions.reshape((-1, 1, 3)), (sofa_pos.shape[1], 1))
        indices = np.argmin(np.linalg.norm(sofa_pos - positions, axis=-1), axis=1)
        self.root.logo.constraints.indices.value = indices.tolist()

        # Get the position of the forces in Vedo for the same reason
        positions = Mesh(get_file('volume.vtk')).rotate_x(90).points()[np.load(get_file('forces.npy'))]
        sofa_pos = np.tile(self.root.logo.state.position.value, (positions.shape[0], 1)).reshape(positions.shape[0], -1,
                                                                                                 3)
        positions = np.tile(positions.reshape((-1, 1, 3)), (sofa_pos.shape[1], 1))
        indices = np.argmin(np.linalg.norm(sofa_pos - positions, axis=-1), axis=1)
        # Define regions
        n = {i: np.array([], dtype=int) for i in indices}
        for t in self.root.logo.topology.triangles.value:
            for t_i in t:
                if t_i in n:
                    n[t_i] = np.unique(np.concatenate((n[t_i], t)))
                    break
        clusters = []
        for idx, nei in n.items():
            if len(clusters) == 0:
                clusters.append(nei)
            else:
                added = False
                for i_c in range(len(clusters)):
                    if len(set(clusters[i_c]).intersection(set(nei))) > 0:
                        clusters[i_c] = np.unique(np.concatenate((clusters[i_c], nei)))
                        added = True
                        break
                if not added:
                    clusters.append(nei)
        # Create ForceFields
        for i, cluster in enumerate(clusters):
            self.root.logo.forces.addObject('ConstantForceField', name=f'cff_{i}', indices=cluster.tolist(),
                                            force=np.random.uniform(-1, 1, (3,)), showArrowSize=0.5)
        Sofa.Simulation.init(self.root.logo.forces)

    def onAnimateEndEvent(self, _):

        if self.idx_step == 0:
            for o in self.root.logo.forces.objects:
                if o.name.value[:3] == 'cff':
                    o.force.value = np.zeros((3,))
        self.idx_step += 1
