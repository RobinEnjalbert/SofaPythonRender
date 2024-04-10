import Sofa

from SofaRender import Viewer
from scene import Scene

if __name__ == '__main__':

    root = Sofa.Core.Node('root')
    root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)
    plt = Viewer(root_node=root)
    plt.launch()

    for _ in range(1000):
        Sofa.Simulation.animate(root, root.dt.value)
        plt.render()
    plt.shutdown()
