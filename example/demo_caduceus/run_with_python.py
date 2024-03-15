import Sofa

from SofaRender import NewViewer as Viewer
from scene import Scene

if __name__ == '__main__':

    # SOFA: create and init the scene graph
    root = Sofa.Core.Node('root')
    scene = root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)

    # VIEWER: create and start the rendering
    viewer = Viewer(root_node=root, render_graph=True)
    viewer.launch()

    # SOFA: run a few time steps
    # VIEWER: update the rendering
    import time
    start = time.time()
    print('start')
    for _ in range(1000):
        Sofa.Simulation.animate(root, root.dt.value)
        viewer.render()
    print((time.time() - start) / 1000)

    # VIEWER: close the rendering
    viewer.shutdown()
