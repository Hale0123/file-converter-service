from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone

from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector

from OCP.gp import gp_Dir, gp_Ax2, gp_Pnt
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE


def load_shape(step_path: str):
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_path)
    if status != IFSelect_RetDone:
        raise RuntimeError("Failed to read STEP file")

    reader.TransferRoots()
    return reader.OneShape()


def run_hlr_isometric(shape):
    # Isometric direction (classic)
    view_dir = gp_Dir(1, 1, 1)
    proj = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), view_dir))

    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(proj)
    algo.Update()
    algo.Hide()

    hlr_shapes = HLRBRep_HLRToShape(algo)

    visible = hlr_shapes.VCompound()
    hidden = hlr_shapes.HCompound()

    return visible, hidden


def count_edges(compound):
    exp = TopExp_Explorer(compound, TopAbs_EDGE)
    count = 0
    while exp.More():
        count += 1
        exp.Next()
    return count


if __name__ == "__main__":
    import sys

    shape = load_shape(sys.argv[1])
    visible, hidden = run_hlr_isometric(shape)

    print("Visible edges:", count_edges(visible))
    print("Hidden edges:", count_edges(hidden))
