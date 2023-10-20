import Sofa
from SofaRender.render.vedo_player import VedoPlayer


def run_sofa_with_vedo(root_node: Sofa.Core.Node):

    Sofa.Simulation.init(root_node)
    VedoPlayer(root_node).show(axes=4, title="SOFA with Vedo").close()


def run_sofa_with_gui(root_node: Sofa.Core.Node):

    import Sofa.Gui

    Sofa.Simulation.init(root_node)
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(root_node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 1080)
    Sofa.Gui.GUIManager.MainLoop(root_node)
    Sofa.Gui.GUIManager.closeGUI()
