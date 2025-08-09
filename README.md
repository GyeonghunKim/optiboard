# optiboard

Lay out and visualize optics breadboards (metric or imperial) with simple components and beam paths.

## Features (v0)

- Board generator (25 mm or 1″ pitch), hole snapping.
- Components: `PostHolder`, `Post`, `KinematicMount` (footprint placeholders).
- Beam polylines and Gaussian beam paths with \( w(z) \).
- CLI: load a scene JSON and render to PNG/SVG.

## Quickstart

```bash
# dev install
pip install -e .

# render an example
optiboard examples/scene_min.json --out layout.svg
