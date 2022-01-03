#!/usr/bin/env python3
# 
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import torchvision.transforms as transforms

# CLASSES = [  # COCO 91 classes
#     '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
#     'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
#     'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
#     'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
#     'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
#     'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
#     'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
#     'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
#     'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
#     'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
#     'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
#     'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
# ]

from machinevisiontoolbox import Image, plot_labelbox
import matplotlib.pyplot as plt
import rvcprint


image = Image.Read('image3.jpg')
image.disp()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

transform = transforms.ToTensor() # Convert the image to PyTorch tensor 
in_tensor = transform(image.image)

model = fasterrcnn_resnet50_fpn(pretrained=True).eval()
outputs = model(torch.stack([in_tensor]))

scores = outputs[0]['scores'].detach().numpy()
labels = outputs[0]['labels'].detach().numpy()
boxes = outputs[0]['boxes'].detach().numpy() # x1 y1 x2 y2

print(len(scores))

CLASSES = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',18: 'dog'}
for score, label, box in zip(scores, labels, boxes):
    print(score, label, box)
    if score > 0.5:
        plot_labelbox(CLASSES[label], lbrt=box, filled=True, alpha=0.3, color="yellow", linewidth=2)
print(outputs)


rvcprint.rvcprint(subfig='b')


