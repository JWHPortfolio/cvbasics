import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
# Need to pip install wandb
from wandb import Classes


def plot_cv_img(input_image):     
    """     
    Converts an image from BGR to RGB and plots     
    """   
    # change color channels order for matplotlib     
    plt.imshow(cv.cvtColor(input_image, cv.COLOR_BGR2RGB))          

    # For easier view, turn off axis around image     
    plt.axis('off')  
    # Must save prior to show - for show clears the image!
    plt.savefig("DetectionOutput.jpg")
    plt.show()

    
    
# load yolo
net = cv.dnn.readNet("yolov3.weights",
                     "yolov3.cfg")
classes = []
with open("coco.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)


layer_name = net.getLayerNames()
output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load Image
img = cv.imread("bermuda.jpg")
print("Shape: ", img.shape)

#Various mod options
'''
        new_img = cv.resize(
            image,
            (max_tuple[0], max_tuple[1]),
            interpolation = cv2.INTER_AREA
'''
# Turn to grey scale
#img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


img = cv.resize(img, None, fx=0.4, fy=0.4)
height, width, channel = img.shape
print("Shape 2: ", img.shape)
# for greyscale there is no channel
# height, width = img.shape

# Detect Objects
blob = cv.dnn.blobFromImage(
    img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layer)
print(outs)

# Showing Information on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detection
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # cv.circle(img, (center_x, center_y), 10, (0, 255, 0), 2 )
            # Reactangle Cordinate
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# print(len(boxes))
# number_object_detection = len(boxes)

indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)

font = cv.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        print("LABEL: ", label)
        color = colors[i]
        cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv.putText(img, label, (x, y + 30), font, 3, color, 3)

plot_cv_img(img)
