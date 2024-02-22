import Sofa
import Sofa.Gui

from scene import Scene


def createScene(node):
    node.addObject(Scene(root=node))


if __name__ == '__main__':
    root = Sofa.Core.Node('root')
    createScene(node=root)
    Sofa.Simulation.init(root)
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()
