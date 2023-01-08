# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from math import pi
np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)

from machinevisiontoolbox.base import *
from machinevisiontoolbox import *
from spatialmath.base import *
from spatialmath import *

# ------------------------------ #
 
# # 12.1 Region Features
# ## 12.1.1 Pixel Classification
# ### 12.1.1.1 Monochrome Image Classification
#

castle = Image.Read("castle.png", dtype="float");

(castle >= 0.7).disp();

# # castle.ithresh()
#

castle.hist().plot();

t = castle.otsu()

castle2 = Image.Read("castle2.png", dtype="float");

t = castle2.otsu()

castle2.threshold_adaptive().disp();

# ### 12.1.1.2 Color Image Classification
#

targets = Image.Read("yellowtargets.png", dtype="float", gamma="sRGB");

garden = Image.Read("tomato_124.png", dtype="float", gamma="sRGB");

ab = targets.colorspace("L*a*b*").plane("a*:b*")

ab.plane("b*:").disp();

targets_labels, targets_centroids, resid = ab.kmeans_color(k=2, seed=0)

targets_labels.disp(colormap="jet", colorbar=True);

targets_centroids

plot_chromaticity_diagram(colorspace="a*b*");
plot_point(targets_centroids, marker="*", text="{}");

[color2name(c, "a*b*") for c in targets_centroids.T]

resid / ab.npixels

labels = ab.kmeans_color(centroids=targets_centroids)

objects = (labels == 0)

objects.disp();

ab = garden.colorspace("L*a*b*").plane("a*:b*")
garden_labels, garden_centroids, resid = ab.kmeans_color(k=3, seed=0);
garden_centroids

[color2name(c, "a*b*") for c in garden_centroids.T]

tomatoes = (garden_labels == 2);

data = np.random.rand(500, 2);  # 500 x 2D data points

from scipy.cluster.vq import kmeans2
centroids, labels = kmeans2(data, k=3)

for i in range(3):
  plot_point(data[labels==i, :].T, color="rgb"[i], marker=".", markersize=10)

tomatoes_binary = tomatoes.close(Kernel.Circle(radius=15));
tomatoes_binary.disp();

# ### 12.1.1.3 Semantic Classification
#

scene = Image.Read("image3.jpg")
scene.disp();

import torch
import torchvision as tv

transform = tv.transforms.Compose([
   tv.transforms.ToTensor(),
   tv.transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])]);
in_tensor = transform(scene.image);

model = tv.models.segmentation.fcn_resnet50(pretrained=True).eval();
outputs = model(torch.stack([in_tensor]));

labels = Image(torch.argmax(outputs["out"].squeeze(), dim=0).detach().cpu().numpy());
labels.disp(colormap="viridis", ncolors=20, colorbar=True);

(labels == 15).disp();
scene.choose([255, 255, 255], labels != 15).disp();

# ## 12.1.2 Object Instance Representation
# ### 12.1.2.1 Creating Binary Blobs
#

sharks = Image.Read("sharks.png");
sharks.disp();

labels, m = sharks.labels_binary()
m

labels.disp(colorbar=True);

right_shark = (labels == 3);
right_shark.disp();

# ### 12.1.2.2 Maximally Stable Extremal Regions (MSER)
#

labels, m = castle2.labels_MSER()

m

labels.disp(colormap="viridis_r", ncolors=m);

# ### 12.1.2.3 Graph-Based Segmentation
#

grain = Image.Read("58060.png")
grain.disp();

labels, m = grain.labels_graphseg()
m

labels.disp(colormap="viridis_r", ncolors=m);

# ## 12.1.3 Object Instance Description
# ### 12.1.3.1 Area
#

right_shark.sum()

# ### 12.1.3.2 Bounding Boxes
#

u, v = right_shark.nonzero()

u.shape

umin = u.min()
umax = u.max()
vmin = v.min()
vmax = v.max()

plot_box(lrbt=[umin, umax, vmin, vmax], color="g");

# ### 12.1.3.3 Moments
#

m00 = right_shark.mpq(0, 0)

uc = right_shark.mpq(1, 0) / m00
vc = right_shark.mpq(0, 1) / m00

plot_point((uc, vc), ["bo", "bx"]);

u20 = right_shark.upq(2, 0); u02 = right_shark.upq(0, 2); u11 = right_shark.upq(1, 1);
J = np.array([[u20, u11], [u11, u02]])

plot_ellipse(4 * J  / m00, centre=(uc, vc), inverted=True, color="blue");

lmbda, x = np.linalg.eig(J)
lmbda

a = 2 * np.sqrt(lmbda.max() / m00)
b = 2 * np.sqrt(lmbda.min() / m00)

b / a

x

i = np.argmax(lmbda)  # get index of largest eigenvalue
v = x[:, i]

np.rad2deg(np.arctan2(v[1], v[0]))

# ### 12.1.3.4 Blob Descriptors
#

blobs = sharks.blobs();

blobs

len(blobs)

blobs[3]

blobs[3].area
blobs[3].umin
blobs[3].aspect
blobs[3].centroid

blobs[3].moments.m00   # moment p=q=0
blobs[3].moments.mu11  # central moment p=q=1
blobs[3].moments.nu03  # normalized central moment p=0, q=3

blobs.area

blobs[3].plot_box(color="red")

blobs[:2].plot_box(color="red")

blobs.plot_centroid(marker="+", color="blue")
blobs.plot_box(color="red")

sharks.roi(blobs[1].bbox).rotate(blobs[1].orientation).disp();

blobs[blobs.area > 10_000]

tomato_blobs = tomatoes_binary.blobs()

tomato_blobs.filter(area=(1_000, 5_000))

tomato_blobs.filter(touch=False)

tomato_blobs.filter(area=[1000, 5000], touch=False, color=1)

# ### 12.1.3.5 Blob Hieararchy
#

multiblobs = Image.Read("multiblobs.png");
multiblobs.disp();

labels, m = multiblobs.labels_binary()
m
multiblobs.disp();

blobs = multiblobs.blobs()

blobs[1].children
blobs[1].parent

blobs.label_image().disp();

blobs.dotfile(show=True);

# ### 12.1.3.6 Shape from Moments
#

blobs = sharks.blobs()

blobs.aspect

blobs.humoments

# ### 12.1.3.7 Shape from Perimeter
#

blobs[1].perimeter[:, :5]

blobs[1].perimeter.shape

blobs[1].plot_perimeter(color="orange")

sharks.disp();
blobs.plot_perimeter(color="orange")
blobs.plot_centroid()

p = blobs[1].perimeter_length

blobs.circularity

p = Polygon2(blobs[1].perimeter).moment(0, 0)

r, th = blobs[1].polar();
plt.plot(r, "r", th, "b");

for blob in blobs:
  r, theta = blob.polar()
  plt.plot(r / r.sum());

similarity, _ = blobs.polarmatch(1)
similarity

# ## 12.1.4 Object Detection using Deep Learning
#

scene = Image.Read("image3.jpg")
scene.disp();

import torch
import torchvision as tv
transform = tv.transforms.ToTensor();
in_tensor = transform(scene.image);

model = tv.models.detection.fasterrcnn_resnet50_fpn(pretrained=True).eval();
outputs = model(torch.stack([in_tensor]));

scores = outputs[0]["scores"].detach().numpy(); # list of confidence scores
labels = outputs[0]["labels"].detach().numpy(); # list of class names as strings
boxes = outputs[0]["boxes"].detach().numpy();   # list of boxes as array([x1, y1, x2, y2])

len(scores)

classname_dict = {1: "person", 2: "bicycle", 3: "car", 4: "motorcycle", 18: "dog"};
for score, label, box in zip(scores, labels, boxes):
  if score > 0.5:  # only confident detections
    plot_labelbox(classname_dict[label], lbrt=box, filled=True, alpha=0.3, 
                  color="yellow", linewidth=2);

# ## 12.1.5 Summary
# # 12.2 Line Features
#

points5 = Image.Read("5points.png", dtype="float");

square = Image.Squares(number=1, size=256, fg=128).rotate(0.3)

edges = square.canny();

h = edges.Hough();

h.plot_accumulator()

plt.plot(h.votes);
plt.yscale("log");

lines = h.lines(60)


church = Image.Read("church.png", mono=True)
edges = church.canny()
h = edges.Hough();
lines = h.lines_p(100, minlinelength=200, maxlinegap=5, seed=0);

church.disp();
h.plot_lines(lines, "r--")

# ## 12.2.1 Summary
# # 12.3 Point Features
# ## 12.3.1 Classical Corner Detectors
#

view1 = Image.Read("building2-1.png", mono=True);
view1.disp();

harris1 = view1.Harris(nfeat=500)

len(harris1)

harris1[0]

harris1[0].p
harris1[0].strength

harris1[:5].p
harris1[:5].strength

view1.disp(darken=True);
harris1.plot();

harris1[::5].plot()

harris1.subset(20).plot()

harris1 = view1.Harris(nfeat=500, scale=15)

view1.Harris_corner_strength().disp();

view2 = Image.Read("building2-2.png", mono=True);

harris2 = view2.Harris(nfeat=250);
view2.disp(darken=True);
harris2.plot();

# ## 12.3.2 Scale-Space Corner Detectors
#

foursquares = Image.Read("scale-space.png", dtype="float");

G, L, s = foursquares.scalespace(60, sigma=2); 

L[5].disp(colormap="signed");

s[5]

plt.plot(s[:-1], [-Ls.image[63, 63] for Ls in L]);

features = findpeaks3d(np.stack([np.abs(Lk.image) for Lk in L], axis=2), npeaks=4)

foursquares.disp();
for feature in features:
  plt.plot(feature[0], feature[1], 'k+')
  scale = s[int(feature[2])]
  plot_circle(radius=scale * np.sqrt(2), centre=feature[:2], color="y")

mona = Image.Read("monalisa.png", dtype="float");

G, L, _ = mona.scalespace(8, sigma=8);

Image.Hstack(G).disp();
Image.Hstack(L).disp();

# ### 12.3.2.1 Scale-Space Point Feature
#

sift1 = view1.SIFT(nfeat=200)

sift1[0]

view1.disp(darken=True);
sift1.plot(filled=True, color="y", hand=True, alpha=0.3)

plt.hist(sift1.scale, bins=100);

# # 12.4 Applications
# ## 12.4.1 Character Recognition
#

import pytesseract as tess
penguins = Image.Read("penguins.png");
ocr = tess.image_to_data(penguins.image < 100, output_type=tess.Output.DICT);

for confidence, text in zip(ocr["conf"], ocr["text"]):
  if text.strip() != "" and confidence > 0:
    print(confidence, text)

for i, (text, confidence) in enumerate(zip(ocr["text"], ocr["conf"])):
  if text.replace(" ", "") != "" and confidence > 50:
    plot_labelbox(text,
       lb=(ocr["left"][i], ocr["top"][i]), wh=(ocr["width"][i], ocr["height"][i]),
       color="y", filled=True, alpha=0.2)

# ## 12.4.2 Image Retrieval
#

images = ImageCollection("campus/*.png", mono=True);

features = [];
for image in images:
  features += image.SIFT()
features.sort(by="scale", inplace=True);

len(features)

features[:10].table()

supports = [];
for feature in features[:400]:
   supports.append(feature.support(images))
Image.Tile(supports, columns=20).disp(plain=True);

feature = features[108]

images[feature.id].disp();
feature.plot(filled=True, color="y", hand=True, alpha=0.5)

bag = BagOfWords(features, 2_000, seed=0)

w = bag.word(108)

bag.occurrence(w)

bag.contains(w)

bag.exemplars(w, images).disp();

word, freq = bag.wordfreq();

np.max(freq)
np.median(freq)

plt.bar(word, -np.sort(-freq), width=1);  # sort in descending order

bag = BagOfWords(features, 2_000, nstopwords=50, seed=0)

v10 = bag.wwfv(10);
v10.shape

sim_10 = bag.similarity(v10);

k = np.argsort(-sim_10)

query = ImageCollection("campus/holdout/*.png", mono=True);

S = bag.similarity(query);

Image(S).disp(colorbar=True);

np.argmax(S, axis=1)

bag.retrieve(query[0])
bag.retrieve(query[1])

