import sys
from scene.scene import Scene


if __name__ == '__main__':

    use_vedo = False
    if len(sys.argv) > 1:
        use_vedo = sys.argv[1] == '-v'

    if use_vedo:
        from players import run_sofa_with_vedo
        run_sofa_with_vedo(root_node=Scene().root)

    else:
        from players import run_sofa_with_gui
        run_sofa_with_gui(root_node=Scene().root)
