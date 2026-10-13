# Errata: notebook code vs. the printed book

*Robotics, Vision & Control 3e: for Python* (Springer, 2023) was finished
in 2022. Its prime dependencies — RTB, MVTB, bdsim, spatialmath-python —
have all evolved since. Where a notebook's code has to change to keep
working, that's a divergence from what's printed on the page, so it's
recorded here.

**Scope: only entries for changes a reader actually has to make** to get a
notebook cell running as intended. Bugs that were fixed upstream (in RTB,
MVTB, bdsim, or spatialmath-python) with **no notebook-side change**
don't belong here — the printed book code still matches the notebook in
those cases, once the dependency is updated. Keep this list lean; it's not
a running log of every toolbox bug found while testing, only the ones that
actually changed a line the reader would see. (For the fuller
investigation log — including issues that turned out not to need a
notebook change — see `claude-notes/notebook-testing-issues.md`.)

The same applies to a renamed API that keeps a working deprecated alias:
if the printed code still runs against the *released* packages, perhaps
with a `DeprecationWarning`, it isn't an erratum (the notebooks were still
updated). Those are listed under [Not listed](#not-listed-printed-code-still-runs)
at the end. The reader-facing version of this file, with book page numbers
and links to the fixing and causing PRs, is the
[Errata wiki page](https://github.com/petercorke/RVC3-python/wiki/Errata).

## Entry format

One `##` entry per changed cell/line group, in reading order. Section
numbers come from the nearest preceding section-heading markdown cell in
the notebook itself (e.g. `# 2.3.1.1 3D Rotation Matrix`).

```markdown
## §<section number> — <short description of what changed and why>

**Notebook:** `chapN.ipynb`

**Reason:** <one line — which dependency changed and how, or what broke
and why>

**As printed:**
​```python
<code exactly as it appears in the book>
​```

**Current toolbox syntax:**
​```python
<code needed today>
​```
```

---

## §7.1.2.2, §7.1.4, §7.1.5 — `models.list()` removed, use `models.catalog()`

**Notebook:** `chap7.ipynb`

**Reason:** RTB deprecated and removed `models.list()`; the replacement
is `models.catalog()`, and the type-filter kwarg was renamed from `type`
to `mtype` (`type` shadows the Python builtin, which was the reason for
the rename).

**As printed:**
```python
models.list(type="ETS")
models.list(type="URDF")
models.list(type="DH")
```

**Current toolbox syntax:**
```python
models.catalog(mtype="ETS")
models.catalog(mtype="URDF")
models.catalog(mtype="DH")
```

## §13.6.1 — `f=3045` is a book typo for `f=4.25e-3`

**Notebook:** `chap13.ipynb`

**Reason:** Not a toolbox API change -- a transcription error. `rho=1.4e-6`
is in metres, so `f` must be too; `f=3045` (3045 metres) makes `fx = f/rho`
absurdly large (~2.18e9 pixels), which makes every `cv2.solvePnP` call
inside `scene.fiducial()` silently fail. The figure-generation script that
produced the book's own printed figure (`figures/code/chapter13/
fig13_31.py`) uses the correct value, `f=4.25e-3`.

**As printed:**
```python
camera = CentralCamera(f=3045, imagesize=scene.shape, 
                       pp=(2016, 1512), rho=1.4e-6);
```

**Current toolbox syntax:**
```python
camera = CentralCamera(f=4.25e-3, imagesize=scene.shape, 
                       pp=(2016, 1512), rho=1.4e-6);
```

## §13.4.1 — `\phi`/`\theta` need raw strings

**Notebook:** `chap13.ipynb`

**Reason:** Not a toolbox API change -- a plain (non-raw) Python string
containing `\p` and `\t` isn't a recognized escape sequence, so this raises
`SyntaxWarning: invalid escape sequence '\p'` (and would for `\t` too, but
`\t` happens to be a legitimate escape -- tab -- so only `\phi` warns; both
should be raw strings for correctness).

**As printed:**
```python
spherical.disp(axes=("$\phi$", "$\theta$"));
```

**Current toolbox syntax:**
```python
spherical.disp(axes=(r"$\phi$", r"$\theta$"));
```

## §14.8.2 — `Image.paste()` no longer mutates in place

**Notebook:** `chap14.ipynb`

**Reason:** MVTB's `Image` class moved to an immutability model (commit
`9afa287a7`, "Image immutability"): `paste()` used to modify the receiver
in place (when called with its old default `copy=False`) and this is what
the book's own figure-generation script relied on
(`figures/code/chapter14/fig14_49.py`, which predates this change). It now
always returns a new `Image` and leaves the original untouched, matching
every other `Image` method's current functional style -- the `copy=`
parameter is retained on the signature but ignored. Calls that don't
capture the return value are now silent no-ops: `composite` never
accumulates the pasted tiles, so every downstream cell in this section
(SIFT on an all-zero canvas, homography estimation, the second `paste()`)
fails or produces nonsense.

**As printed:**
```python
composite.paste(images[0], (0, 0));
composite.disp();
...
composite.paste(tile, topleft, method="blend");
composite.disp();
```

**Current toolbox syntax:**
```python
composite = composite.paste(images[0], (0, 0));
composite.disp();
...
composite = composite.paste(tile, topleft, method="blend");
composite.disp();
```

## §12.1.3.3 — `np.linalg.eig()` on a symmetric matrix now returns complex dtype

**Notebook:** `chap12.ipynb`

**Reason:** NumPy 2.0 made `np.linalg.eig()` always return complex-dtype
arrays, even when every eigenvalue's imaginary part is exactly zero
(NumPy 1.x returned real dtype in that case). `J` here is a real
symmetric matrix (built from image moments), so its eigenvalues are
always real -- `np.linalg.eigh()` is both the numerically correct choice
for a symmetric matrix and sidesteps this NumPy 2.0 change, since it
guarantees real output.

**As printed:**
```python
lmbda, x = np.linalg.eig(J)
```

**Current toolbox syntax:**
```python
lmbda, x = np.linalg.eigh(J)
```

## §C.1.4 — `np.linalg.eig()` on a symmetric matrix now returns complex dtype

**Notebook:** `app.ipynb`

**Reason:** Same NumPy 2.0 change as §12.1.3.3: `np.linalg.eig()` now
always returns complex-dtype arrays, even when every eigenvalue's
imaginary part is exactly zero (NumPy 1.x returned real dtype in that
case). `E` here is a real symmetric matrix (the ellipse's defining
matrix), so its eigenvalues are always real -- `np.linalg.eigh()` is
both the numerically correct choice for a symmetric matrix and
sidesteps this NumPy 2.0 change. The complex dtype leaking downstream
into `v`/`r` is what broke the following cells' `plot_arrow()` (a bare
`TypeError: ufunc 'hypot' not supported for the input types`) and
`np.arctan2()` calls.

**As printed:**
```python
e, v = np.linalg.eig(E)
```

**Current toolbox syntax:**
```python
e, v = np.linalg.eigh(E)
```

## §11.1, §11.2 — `Image.stats()` replaced by `.stats` property + `.printstats()` method

**Notebook:** `chap11.ipynb`

**Reason:** MVTB 2.0.0 split what used to be a single callable `stats()`
into two: `.stats`, a dict-valued property (doesn't print), and
`.printstats()`, a method that prints the same summary the book's
`stats()` call used to. Same change at 4 call sites.

**As printed:**
```python
street.stats()
```

**Current toolbox syntax:**
```python
street.printstats()
```

## §11.1.7, §11.5, §14.8.2 — `ImageConstantsMixin` factory methods are keyword-only for size

**Notebooks:** `chap11.ipynb`, `chap14.ipynb`

**Reason:** MVTB 2.0.0 changed `Image.Zeros()`/`Image.Constant()`/etc. to
take image dimensions as a keyword-only `size=` tuple rather than
positional width/height arguments.

**As printed:**
```python
canvas = Image.Zeros(1000, 1000, dtype="uint8")
K = Image.Constant(21, 21, value=1/21**2)
```

**Current toolbox syntax:**
```python
canvas = Image.Zeros(size=(1000, 1000), dtype="uint8")
K = Image.Constant(value=1/21**2, size=(21, 21))
```

## §7.1.4 — `ERobot.URDF_read()` removed; use the module-level `URDF_read()` with a bare robot name

**Notebook:** `chap7.ipynb`

**Reason:** RTB's June 2026 xacro/URDF rework removed `URDF_read()` as a
static method on `Robot`/`ERobot` entirely (no deprecation shim -- this
was an architectural change, not a rename) and replaced it with a
module-level function in `roboticstoolbox.models.URDF.URDFRobot`. The
loading mechanism changed too: RTB no longer bundles raw xacro package
trees like `ur_description/` directly, so a full relative xacro path no
longer resolves. Bare robot names (`"ur5"`) now resolve via the
`robot_descriptions` package instead, matching how the packaged
`models.URDF.UR5()` class itself loads its data.

**As printed:**
```python
urdf, *_ = ERobot.URDF_read("ur_description/urdf/ur5_joint_limited_robot.urdf.xacro")
urdf
```

**Current toolbox syntax:**
```python
from roboticstoolbox.models.URDF.URDFRobot import URDF_read
urdf, *_ = URDF_read("ur5")
urdf
```

## §14.8.3 — `visodom.py` limited to 50 frames by default

**Notebook:** `chap14.ipynb`

**Reason:** The bridge dataset has 251 stereo frame pairs; processing all
of them (ORB matching + bundle adjustment per frame) takes several
minutes. Added an optional frame-count argument to
`RVC3/examples/visodom.py` (processes every frame if omitted) and the
notebook now passes 50 for a much faster run. Increase or drop the
argument to process more frames.

**As printed:**
```python
%run -m visodom
```

**Current toolbox syntax:**
```python
%run -m visodom 50
```

## §15.2.2 — bdsim clock log field renamed from `.x` to `.X`

**Notebook:** `chap15.ipynb`

**Reason:** bdsim's per-clock logged state array was renamed from a
lowercase `.x` attribute to `.X`, to match the uppercase convention
used for state-array fields elsewhere in a run's output struct (eg.
the top-level `out.x`/`out.xnames` pairing uses lowercase for the
continuous state but clocked/discrete state blocks use the
uppercase form).

**As printed:**
```python
plt.plot(out.clock0.t, out.clock0.x)
```

**Current toolbox syntax:**
```python
plt.plot(out.clock0.t, out.clock0.X)
```

## §2.3.1.2 — `tripleangledemo` is now an installed CLI command

**Notebook:** `chap2.ipynb`

**Reason:** RTB used to ship `tripleangledemo.py` as a standalone
script; it's now `roboticstoolbox.demo.tripleangledemo`, exposed as
an installed console command (`[project.scripts]` entry point in
RTB's `pyproject.toml`) rather than a bare top-level module, so
`%run -m tripleangledemo` can no longer find it
(`'tripleangledemo' is not a valid modulename on sys.path`). Invoke
it as the installed command directly instead.

**As printed:**
```python
%run -m tripleangledemo
```

**Current toolbox syntax:**
```python
!tripleangledemo
```

## §2.4.8 — `twistdemo` is now an installed CLI command

**Notebook:** `chap2.ipynb`

**Reason:** Same change as `tripleangledemo` above --
`twistdemo.py` is now `roboticstoolbox.demo.twistdemo`, an installed
console command rather than a bare top-level module.

**As printed:**
```python
%run -m twistdemo
```

**Current toolbox syntax:**
```python
!twistdemo
```

## §B.2.1 — `eigdemo` is now an installed CLI command

**Notebook:** `app.ipynb`

**Reason:** Same change as `tripleangledemo`/`twistdemo` above --
`eigdemo.py` is now `roboticstoolbox.demo.eigdemo`, an installed
console command rather than a bare top-level module.

**As printed:**
```python
%run -m eigdemo 1 2 3 4
```

**Current toolbox syntax:**
```python
!eigdemo 1 2 3 4
```

---

## Not listed: printed code still runs

Checked 2026-10-13 against the released packages in a clean venv (RTB 1.4.4,
MVTB 2.4.0, bdsim 1.4.0, pgraph-python 1.0.0, NumPy 2.5; torchvision 0.29.1
checked by reading its source, not executed). Each of these used to have an
entry here. The printed form still works, at most with a `DeprecationWarning`,
so a reader doesn't have to change anything. If a future release removes
the alias, the entry should come back.

| Printed | Replacement | Why it still works |
| ------- | ----------- | ------------------ |
| `ET.eta` (§7.1.1.1) | `.param` | RTB keeps `eta` as a deprecated alias ([RTB#553](https://github.com/petercorke/robotics-toolbox-python/pull/553)) |
| `im.image`, `.A` (§10.4.2, §11.1, §11.5.1.2, §12.x, §13.4, §14.x) | `.array` | MVTB 2.0.0 deprecated aliases |
| `Histogram.plot("ncdf")` (§11.2) | `"cdf"` | accepted as a deprecated alias ([MVTB#85](https://github.com/petercorke/machinevision-toolbox-python/pull/85)) |
| `PointCloud.Read('data/bunny.ply')` (§14.7) | `Read('bunny.ply')` | redundant `data/` prefix is now stripped ([MVTB#92](https://github.com/petercorke/machinevision-toolbox-python/pull/92)) |
| `fcn_resnet50(pretrained=True)` etc. (§12.1.1.3, §12.1.4) | `weights=` | torchvision still maps `pretrained` with a warning |
| `g[1].adjacent()` (§I) | `.neighbours()` | pgraph restored `adjacent()` as the canonical name (2026-10-12) |
| `Image.rank()` (§11.5.2.2) | `.rankfilter()` | deprecated alias |
| `ImageCollection`, `ZipArchive` (§11.1.2, §12.4.2, §13.2.2, §14.8.x) | `FileCollection`, `FileArchive` | deprecated subclasses, same arguments |
| `VideoCamera.grab()`, `WebCam.grab()` (§11.1.3, §11.1.5) | `next(camera)` | deprecated methods call `next()` |
