import Sofa

from SofaRender import Viewer
from scene import Scene

if __name__ == '__main__':

    root = Sofa.Core.Node('root')
    scene = root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)

    def fnc():
        while True:
            if scene.idx_step == 100:
                Sofa.Simulation.reset(root)
                scene.idx_step = 0
            else:
                Sofa.Simulation.animate(root, root.dt.value)


    def step():
        if scene.idx_step == 100:
            Sofa.Simulation.reset(root)
            scene.idx_step = 0
        else:
            Sofa.Simulation.animate(root, root.dt.value)

    # import threading
    # t = threading.Thread(target=fnc)
    # t.start()
    # print('DONE')
    # t.join()

    plt = Viewer(root_node=root)
    # scene.init_viewer(plt)
    plt.show(axes=4, title="SOFA with Vedo")
