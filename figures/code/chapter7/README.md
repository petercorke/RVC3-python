# Chapter 7 PyVista figures

`fig7_4a.py`, `fig7_4b.py`, `fig7_4c.py`, `fig7_6.py` and `fig7_7.py` render a
3D scene with PyVista and save a PNG with `RVC3.tools.pvplus.save()`, not with
`rvcprint`. `pvplus.outfile()` writes the PNG **next to the script**, with the
script's name, for example `fig7_4a.png`. (`rvcprint` writes to the current
directory instead. The two helpers disagree.)

## The tracked PNGs

`fig7_4a.png`, `fig7_4b.png`, `fig7_4c.png` and `fig7_6.png` are tracked. They
are the versions used in the book, added in 96dfb7e (2023-01-06). `fig7_7.png`
is not tracked. These PNGs are the reference, so do not overwrite them casually.

## What happened on 2026-11-28

- The figure smoke test (`tests/test_figures.py`) ran these scripts. Because
  `pvplus.save()` writes next to the script, it overwrote the four tracked PNGs
  and created `fig7_7.png` inside the repository.
- The four overwritten PNGs were committed by mistake in c3e1d5b (branch
  `fix/pyvista-transform-inplace`). They were restored to the book versions in
  98468bc (branch `fix/figures-test-no-repo-writes`).
- The test runner now sends `pvplus` output to a temporary directory, so running
  the test no longer touches this folder.

## Regenerating gives a different picture

With PyVista 0.49.3 (Matplotlib 3.11, RTB 1.5.0, MVTB 2.5.0), the scripts
produce images that differ from the book's:

- **Clipping.** The scripts call `pvplus.save(..., zoom=1.2)`. At that zoom the
  scene runs off the window. For `fig7_4a` the content spans columns 0 to 1656 of
  the 2000 pixel wide window, so the left edge (the `q` label, the arrow tip and
  the joint) is cut off. `fig7_4b`, `fig7_4c`, `fig7_6` and `fig7_7` touch both
  the left and right edges. The book versions are not clipped, so the same zoom
  framed the scene differently with the PyVista used then.
- **Size.** The regenerated `fig7_4a` is 1656 x 1345 pixels. The book version is
  1570 x 1145, so the scene is taller as well as wider.
- **Color.** The joint shaft was silver in the book. It is blue-grey now.

The scripts now use `zoom=1.0`, at which all five fit inside the window with at
least 25 pixels to spare. This stops the clipping. It does not reproduce the
book's framing or colors exactly, and the tracked PNGs were not regenerated.

## Possible causes (not tested)

The PyVista version used for the book is not recorded. These are guesses about
what changed since:

- default lighting, which would explain the shaft color;
- how the camera is reset and how `camera.Zoom()` is applied about the focal
  point after `camera_position` is set;
- the default geometry of `pv.Arrow` and `pv.Text3D`, which would change the
  scene's size;
- off-screen window size and pixel scaling.

One related PyVista change is already handled: `translate()`, `rotate_*()` and
`transform()` no longer modify a mesh in place by default, and `pvplus` and the
scripts now pass `inplace=True`.

## Regenerating a figure by hand

Run the script from a scratch directory and copy the result across only if it
looks right:

    mkdir /tmp/fig && cd /tmp/fig && python /path/to/fig7_4a.py

Since `pvplus.outfile()` writes next to the script, copy the script to the
scratch directory first, or the PNG will land in this folder.
