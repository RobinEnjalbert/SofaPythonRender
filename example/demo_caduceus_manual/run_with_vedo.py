import Sofa

from SofaRender import VedoViewer
from scene import Scene

if __name__ == '__main__':

    # Create the root node and the scene graph
    root = Sofa.Core.Node('root')
    scene = root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)

    def step_function():
        """
        Simulation loop that will be called by the viewer in the timer callback.
        """
        if scene.idx_step == 100:
            Sofa.Simulation.reset(root)
            scene.idx_step = 0
        else:
            Sofa.Simulation.animate(root, root.dt.value)

    # Create the viewer and create objects
    plt = VedoViewer(root_node=root, step_function=step_function)
    scene.init_viewer(viewer=plt)

    # Launch the viewer and the simulation loop
    plt.show(axes=4, title="SOFA with Vedo").close()
