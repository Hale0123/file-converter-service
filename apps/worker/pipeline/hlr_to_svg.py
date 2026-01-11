from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone

from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector

from OCP.gp import gp_Dir, gp_Ax2, gp_Pnt
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve


def load_shape(step_path: str):
    reader = STEPControl_Reader()
    if reader.ReadFile(step_path) != IFSelect_RetDone:
        raise RuntimeError("Failed to read STEP file")

    reader.TransferRoots()
    return reader.OneShape()


def run_hlr_isometric(shape):
    view_dir = gp_Dir(1, 1, 1)
    projector = HLRAlgo_Projector(
        gp_Ax2(gp_Pnt(0, 0, 0), view_dir)
    )

    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(projector)
    algo.Update()
    algo.Hide()

    hlr = HLRBRep_HLRToShape(algo)
    return hlr.VCompound(), hlr.HCompound()


def edge_to_polyline(edge, samples=40):
    curve = BRepAdaptor_Curve(edge)
    u0 = curve.FirstParameter()
    u1 = curve.LastParameter()

    pts = []
    for i in range(samples + 1):
        u = u0 + (u1 - u0) * i / samples
        p = curve.Value(u)
        pts.append((p.X(), -p.Y()))  # invert Y for SVG
    return pts


def compound_to_paths(compound):
    paths = []
    exp = TopExp_Explorer(compound, TopAbs_EDGE)
    while exp.More():
        shape = exp.Current()
        edge = TopoDS.Edge(shape)  # ✅ THIS IS THE CORRECT CAST
        paths.append(edge_to_polyline(edge))
        exp.Next()
    return paths


def write_svg(visible, hidden, out_path):
    all_pts = [pt for path in visible + hidden for pt in path]
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    width = maxx - minx
    height = maxy - miny

    def path_d(poly):
        return "M " + " L ".join(
            f"{x - minx},{y - miny}" for x, y in poly
        )

    with open(out_path, "w") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}">\n'
        )

        for p in visible:
            f.write(
                f'<path d="{path_d(p)}" '
                f'stroke="black" fill="none" stroke-width="1"/>\n'
            )

        for p in hidden:
            f.write(
                f'<path d="{path_d(p)}" '
                f'stroke="black" fill="none" '
                f'stroke-dasharray="5,5" stroke-width="0.8"/>\n'
            )

        f.write("</svg>")


if __name__ == "__main__":
    import sys

    step_path = sys.argv[1]
    shape = load_shape(step_path)

    visible, hidden = run_hlr_isometric(shape)

    vis_paths = compound_to_paths(visible)
    hid_paths = compound_to_paths(hidden)

    out_svg = "output/iso.svg"
    write_svg(vis_paths, hid_paths, out_svg)

    print(f"SVG written to {out_svg}")
