import Sofa

from SofaRender import VedoPlayer
from scene import Scene

if __name__ == '__main__':

    root = Sofa.Core.Node('root')
    scene = root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)

    def step_function():
        if scene.idx_step == 100:
            Sofa.Simulation.reset(root)
            scene.idx_step = 0
        else:
            Sofa.Simulation.animate(root, root.dt.value)

    plt = VedoPlayer(root_node=root, step_function=step_function)
    plt.show(axes=4, title="SOFA with Vedo").close()
