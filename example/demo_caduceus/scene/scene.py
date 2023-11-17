import Sofa
from os.path import join, dirname


def get_file(filename: str):
    data_dir = 'data'
    return join(dirname(__file__), data_dir, *filename.split('/'))


def get_plugin_list():
    with open(get_file('plugins.txt'), 'r') as file:
        plugins = []
        for plugin in file.readlines():
            if plugin != '\n':
                plugin = plugin[:-1] if plugin[-1] == '\n' else plugin
                plugins.append(plugin)
    return plugins


class Scene(Sofa.Core.Controller):

    def __init__(self, root: Sofa.Core.Node, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, name='Controller', *args, **kwargs)

        self.root = root
        self.create_graph()
        self.idx_step = 0

    def create_graph(self):

        self.root.dt.value = 0.04
        self.root.gravity.value = [0, -1000, 0]
        self.root.addObject('RequiredPlugin', pluginName=get_plugin_list())
        self.root.addObject('VisualStyle', displayFlags='showVisualModels')

        self.root.addObject('FreeMotionAnimationLoop', parallelCollisionDetectionAndFreeMotion=True)
        self.root.addObject('DefaultPipeline', depth=15, verbose=0, draw=0)
        self.root.addObject('BruteForceBroadPhase')
        self.root.addObject('BVHNarrowPhase')
        self.root.addObject('MinProximityIntersection', alarmDistance=1.5, contactDistance=1)
        self.root.addObject('DefaultContactManager', response='FrictionContactConstraint')
        self.root.addObject('LCPConstraintSolver', tolerance=1e-3, maxIt=1000, initial_guess=False, build_lcp=False,
                            printLog=0, mu=0.2)

        self.root.addObject('InteractiveCamera', position=[0, 30, 90], lookAt=[0, 30, 0])
        self.root.addObject('LightManager')
        self.root.addObject('SpotLight', position=[0, 80, 25], direction=[0, -1, -0.8], cutoff=30, exponent=1)
        self.root.addObject('SpotLight', position=[0, 40, 100], direction=[0, 0, -1], cutoff=30, exponent=1)

        # Snake.Physics
        self.root.addChild('snake')
        self.root.snake.addObject('MeshOBJLoader', name='Snake', filename=get_file('snake_body.obj'))
        self.root.snake.addObject('EulerImplicitSolver', rayleighMass=1, rayleighStiffness=0.03)
        self.root.snake.addObject('CGLinearSolver', iterations=20, tolerance=1e-12, threshold=1e-18,
                                  template='CompressedRowSparseMatrixMat3x3d')
        self.root.snake.addObject('SparseGridRamificationTopology', name='Grid', src='@Snake', n=[4, 12, 3],
                                  nbVirtualFinerLevels=3, finestConnectivity=0)
        self.root.snake.addObject('MechanicalObject', src='@Grid', scale=1, dy=2)
        self.root.snake.addObject('UniformMass', totalMass=1.)
        self.root.snake.addObject('HexahedronFEMForceField', youngModulus=10000, poissonRatio=0.3, method='large',
                                  updateStiffnessMatrix=False)
        self.root.snake.addObject('UncoupledConstraintCorrection', useOdeSolverIntegrationFactors=False)

        # Snake.Collision
        self.root.snake.addChild('collision')
        self.root.snake.collision.addObject('MeshOBJLoader', name='SnakeColl', filename=get_file('meca_snake_900tri.obj'))
        self.root.snake.collision.addObject('MeshTopology', name='SnakeCollTopo', src='@SnakeColl')
        self.root.snake.collision.addObject('MechanicalObject', name='SnakeCollMo', src='@SnakeColl')
        self.root.snake.collision.addObject('TriangleCollisionModel', selfCollision=False)
        self.root.snake.collision.addObject('LineCollisionModel', selfCollision=False)
        self.root.snake.collision.addObject('PointCollisionModel', selfCollision=False)
        self.root.snake.collision.addObject('BarycentricMapping', input='@..', output='@.')

        # Snake.Visual
        self.root.snake.addChild('visual')
        self.root.snake.visual.addChild('body')
        self.root.snake.visual.body.addObject('MeshOBJLoader', name='SnakeBody', filename=get_file('snake_body.obj'))
        self.root.snake.visual.body.addObject('OglModel', name='OglBody', src='@SnakeBody',
                                              texturename=get_file('snakeColorMap.png'))
        self.root.snake.visual.body.addObject('BarycentricMapping', input='@../..', output='@.')
        self.root.snake.visual.addChild('eye')
        self.root.snake.visual.eye.addObject('MeshOBJLoader', name='SnakeEye', filename=get_file('snake_yellowEye.obj'))
        self.root.snake.visual.eye.addObject('OglModel', name='OglEye', src='@SnakeEye')
        self.root.snake.visual.eye.addObject('BarycentricMapping', input='@../..', output='@.')

        # Base.Collision
        self.root.addChild('base')
        self.root.base.addChild('stick')
        self.root.base.stick.addObject('MeshOBJLoader', name='Stick', filename=get_file('collision_batons.obj'))
        self.root.base.stick.addObject('MeshTopology', name='StickCollTopo', src='@Stick')
        self.root.base.stick.addObject('MechanicalObject', src='@Stick')
        self.root.base.stick.addObject('LineCollisionModel', simulated=False, moving=False)
        self.root.base.stick.addObject('PointCollisionModel', simulated=False, moving=False)
        self.root.base.addChild('blobs')
        self.root.base.blobs.addObject('MeshOBJLoader', name='Blobs', filename=get_file('collision_boules_V3.obj'))
        self.root.base.blobs.addObject('MeshTopology', name='BlobsCollTopo', src='@Blobs')
        self.root.base.blobs.addObject('MechanicalObject', src='@Blobs')
        self.root.base.blobs.addObject('TriangleCollisionModel', simulated=False, moving=False)
        self.root.base.blobs.addObject('LineCollisionModel', simulated=False, moving=False)
        self.root.base.blobs.addObject('PointCollisionModel', simulated=False, moving=False)
        self.root.base.addChild('foot')
        self.root.base.foot.addObject('MeshOBJLoader', name='Foot', filename=get_file('collision_pied.obj'))
        self.root.base.foot.addObject('MeshTopology', name='FootCollTopo', src='@Foot')
        self.root.base.foot.addObject('MechanicalObject', src='@Foot')
        self.root.base.foot.addObject('TriangleCollisionModel', simulated=False, moving=False)
        self.root.base.foot.addObject('LineCollisionModel', simulated=False, moving=False)
        self.root.base.foot.addObject('PointCollisionModel', simulated=False, moving=False)

        # Base.Visual
        self.root.base.addChild('visual')
        self.root.base.visual.addObject('MeshOBJLoader', name='Base', filename=get_file('SOFA_pod.obj'))
        self.root.base.visual.addObject('OglModel', name='OglBase', src='@Base')
