import Sofa

from SofaRender import Viewer
from scene import Scene

if __name__ == '__main__':

    # SOFA: create and init the scene graph
    root = Sofa.Core.Node('root')
    scene = root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)

    # VIEWER: create and start the rendering
    viewer = Viewer(root_node=root, render_graph=True, animation_player=False)
    viewer.launch()

    # SOFA: run a few time steps
    # VIEWER: update the rendering
    for _ in range(300):
        Sofa.Simulation.animate(root, root.dt.value)
        viewer.render()

    # VIEWER: close the rendering
    viewer.shutdown()
