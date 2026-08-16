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

## §7.1.1.1 — `ET.eta` deprecated, use `.param`

**Notebook:** `chap7.ipynb`

**Reason:** RTB deprecated `ET.eta` since 1.4.0 in favour of `.param`.

**As printed:**
```python
e[1].eta
e[1].A()
```

**Current toolbox syntax:**
```python
e[1].param
e[1].A()
```

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

## §10.4.2, §11.1, §11.5.1.2, §12.1.1.3, §12.1.4, §12.3.2, §12.4, §14.3.1, §14.4.2.4, §14.4.2.8 — `Image.image` renamed to `Image.array`

**Notebooks:** `chap10.ipynb`, `chap11.ipynb`, `chap12.ipynb`, `chap14.ipynb`

**Reason:** MVTB 2.0.0 renamed the `Image` class's raw-pixel-data property
from `.image` to `.array`. Same one-line change everywhere it appears —
listed once here rather than per occurrence (roughly 15 individual cells
across these four notebooks).

**As printed:**
```python
s = shadow_invariant(im.image, 0.7)
```

**Current toolbox syntax:**
```python
s = shadow_invariant(im.array, 0.7)
```

## §13.4 — `Image.A` renamed to `Image.array`

**Notebook:** `chap13.ipynb`

**Reason:** Same MVTB 2.0.0 rename as `.image`→`.array` above, but from
the older `.A` alias rather than `.image`.

**As printed:**
```python
facecolors=spherical.colorize().A, cstride=1, rstride=1
```

**Current toolbox syntax:**
```python
facecolors=spherical.colorize().array, cstride=1, rstride=1
```

## §11.2 — `Histogram.plot()`'s `'ncdf'` type renamed to `'cdf'`

**Notebook:** `chap11.ipynb`

**Reason:** A real CDF is normalized by definition, so MVTB simplified the
name -- `'cdf'` is what `'ncdf'` (normalized CDF) always meant. `'ncdf'`
remains accepted as a deprecated alias.

**As printed:**
```python
h.plot("ncdf", color="blue")
```

**Current toolbox syntax:**
```python
h.plot("cdf", color="blue")
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

## §11.5.2.2 — `Image.rank()` renamed to `Image.rankfilter()`

**Notebook:** `chap11.ipynb`

**Reason:** MVTB 2.0.0 renamed this method. Same change at 4 call sites
in this section.

**As printed:**
```python
mx = mona.rank(rank=0, h=2)
```

**Current toolbox syntax:**
```python
mx = mona.rankfilter(rank=0, h=2)
```

## §11.1.2, §12.4.2, §13.2.2, §14.8.2 — `ImageCollection` renamed to `FileCollection`

**Notebooks:** `chap11.ipynb`, `chap12.ipynb`, `chap13.ipynb`, `chap14.ipynb`

**Reason:** MVTB 2.0.0 renamed this class.

**As printed:**
```python
images = ImageCollection("seq/*.png")
```

**Current toolbox syntax:**
```python
images = FileCollection("seq/*.png")
```

## §11.1.2, §14.8.3 — `ZipArchive` renamed to `FileArchive`

**Notebooks:** `chap11.ipynb`, `chap14.ipynb`

**Reason:** MVTB 2.0.0 renamed this class.

**As printed:**
```python
images = ZipArchive("bridge-l.zip", "*.pgm")
```

**Current toolbox syntax:**
```python
images = FileArchive("bridge-l.zip", "*.pgm")
```

## §11.1.3 — `VideoCamera.grab()` replaced by the iterator protocol

**Notebook:** `chap11.ipynb`

**Reason:** MVTB 2.0.0 moved camera frame-grabbing onto Python's iterator
protocol.

**As printed:**
```python
camera = VideoCamera(0)
image = camera.grab()
camera.release()
image.disp()
```

**Current toolbox syntax:**
```python
camera = VideoCamera(0)
image = next(camera)
camera.release()
image.disp()
```

## §11.1.5 — `WebCam.grab()` replaced by the iterator protocol

**Notebook:** `chap11.ipynb`

**Reason:** Same change as `VideoCamera.grab()` above, applied to `WebCam`.

**As printed:**
```python
porjus= WebCam("http://uk.jokkmokk.jp/photo/nr4/latest.jpg");
porjus.grab().disp();
```

**Current toolbox syntax:**
```python
porjus= WebCam("http://uk.jokkmokk.jp/photo/nr4/latest.jpg");
next(porjus).disp();
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
