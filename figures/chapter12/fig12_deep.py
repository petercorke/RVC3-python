from imageai.Detection import ObjectDetection
from machinevisiontoolbox import Image, plot_labelbox
from spatialmath.base import plot_box
import matplotlib.pyplot as plt
import rvcprint

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( "./yolo.h5")
detector.loadModel()

img = Image.Read('image3.jpg')
out, detections = detector.detectObjectsFromImage(input_image=img.image, input_type="array", output_type="array")#, minimum_percentage_probability=30)

print(detections[0])

img.disp()

for detection in detections:
    print(f'{detection["name"]}: {detection["percentage_probability"]:.1f}%')
    plot_labelbox(detection["name"], ltrb=detection["box_points"], filled=True, alpha=0.3, color="yellow", linewidth=2)

rvcprint.rvcprint()
