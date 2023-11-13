import Sofa

from SofaRender import VedoPlayer
from scene import Scene

if __name__ == '__main__':

    root = Sofa.Core.Node('root')
    root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)
    plt = VedoPlayer(root_node=root)
    plt.show(axes=4, title="SOFA with Vedo").close()
