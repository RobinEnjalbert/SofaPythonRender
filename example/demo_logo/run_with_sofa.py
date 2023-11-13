import Sofa
import Sofa.Gui

from scene import Scene


if __name__ == '__main__':
    root = Sofa.Core.Node('root')
    root.addObject(Scene(root=root))
    Sofa.Simulation.init(root)
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()
