#!/usr/bin/env python3
# 
import torch
from torchvision.models.segmentation import fcn_resnet50
from torchvision.transforms.functional import convert_image_dtype
from torchvision.io import read_image
from pathlib import Path
import torchvision.transforms as transforms

CLASSES = [  # Pascal VOC 20 classes
   '_background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']


from machinevisiontoolbox import Image, plot_labelbox
from spatialmath.base import plot_box
import matplotlib.pyplot as plt
import rvcprint


scene = Image.Read('image3.jpg')
scene.disp()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
in_tensor = transform(scene.image)

# image_t = transform(img.image)


# batch_int = torch.stack([image_t])
# batch = convert_image_dtype(batch_int, dtype=torch.float)


batch_int = torch.stack([in_tensor])

model = fcn_resnet50(pretrained=True).eval()


outputs = model(torch.stack([in_tensor]))

labels = Image(torch.argmax(outputs['out'].squeeze(), dim=0).detach().cpu().numpy())

scene.disp()

# ((labels == CLASSES.index("person")) * img).disp()
labels.disp(colormap='viridis', ncolors=len(CLASSES), vrange=[0, len(CLASSES)-1], colorbar=dict(shrink=0.75, aspect=20*0.75))
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

(labels == CLASSES.index("person")).disp()
rvcprint.rvcprint(subfig='c')

# ----------------------------------------------------------------------- #

scene.choose("white", labels != CLASSES.index("person")).disp()
rvcprint.rvcprint(subfig='d')