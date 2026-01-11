from apps.worker.pipeline.hlr_views import VIEWS, hlr_view
from apps.worker.pipeline.hlr_to_svg import load_shape, compound_to_paths, write_svg


def offset_paths(paths, dx, dy):
    """Translate a list of polylines by (dx, dy)."""
    out = []
    for poly in paths:
        out.append([(x + dx, y + dy) for x, y in poly])
    return out


def main(step_path: str, out_svg: str = "output/sheet.svg"):
    shape = load_shape(step_path)

    sheet_visible = []
    sheet_hidden = []

    # Spacing between view blocks (tune later)
    spacing = 1200

    # Simple layout: iso + 3 orthos
    positions = {
        "iso": (0, 0),
        "front": (spacing, 0),
        "top": (spacing, -spacing),
        "right": (2 * spacing, 0),
    }

    # Generate each view and place onto the sheet
    for name, direction in VIEWS.items():
        vis_comp, hid_comp = hlr_view(shape, direction)

        vis_paths = compound_to_paths(vis_comp)
        hid_paths = compound_to_paths(hid_comp)

        dx, dy = positions[name]
        sheet_visible += offset_paths(vis_paths, dx, dy)
        sheet_hidden += offset_paths(hid_paths, dx, dy)

    write_svg(sheet_visible, sheet_hidden, out_svg)
    print(f"Drawing sheet written to {out_svg}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python apps/worker/pipeline/sheet_svg.py <step_file>")
        raise SystemExit(1)

    main(sys.argv[1])
