from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Dir, gp_Ax2, gp_Pnt

def hlr_view(shape, direction):
    proj = HLRAlgo_Projector(
        gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*direction))
    )

    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(proj)
    algo.Update()
    algo.Hide()

    out = HLRBRep_HLRToShape(algo)
    return out.VCompound(), out.HCompound()


VIEWS = {
    "front": (0, 1, 0),
    "top":   (0, 0, 1),
    "right": (1, 0, 0),
    "iso":   (1, 1, 1),
}
