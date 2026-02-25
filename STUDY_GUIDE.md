# 📚 Fire Detection Project — Step-by-Step Study Guide

> A curated learning path for every concept used in this project.
> Designed for MCA students. Study in order — each topic builds on the previous one.

---

## 🗺️ Learning Roadmap

```
Python Basics → OpenCV → Machine Learning Basics
    → Deep Learning → CNNs → YOLO → Ultralytics
        → ONNX → Flask → UI / Dashboard
```

---

## 📌 Module 1 — Python Foundations

**Why?** All code in this project is Python. You need to be comfortable with it before anything else.

| Topic | What to Study | Resource |
|---|---|---|
| Python basics | Variables, loops, functions, file I/O | [Python Official Tutorial](https://docs.python.org/3/tutorial/) |
| Libraries & pip | Installing packages, virtual environments | [Real Python — pip guide](https://realpython.com/what-is-pip/) |
| NumPy | Arrays, matrix operations (essential for images) | [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) |
| Matplotlib | Plotting images, graphs, loss curves | [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html) |
| Pathlib / os | File system operations | [Real Python — pathlib](https://realpython.com/python-pathlib/) |

**When to use**: Before writing any ML code. If you can write a Python script that reads a folder and processes files, you're ready.

---

## 📌 Module 2 — OpenCV (Computer Vision Basics)

**Why?** OpenCV is used to read images, draw bounding boxes, and process webcam/video streams.

| Topic | What to Study | Resource |
|---|---|---|
| Reading images/videos | `cv2.imread`, `cv2.VideoCapture` | [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) |
| Drawing on images | `cv2.rectangle`, `cv2.putText` | [OpenCV Drawing](https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html) |
| Color spaces | BGR vs RGB, `cv2.cvtColor` | [Color Space tutorial](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html) |
| Webcam stream | `cap.read()`, frame loop | [Real Python — OpenCV](https://realpython.com/opencv-face-recognition/) |
| Image resizing | `cv2.resize`, for model input | [OpenCV Geometric](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) |

**When to use**: When building the inference script (`fire.py`) to display detections on live video.

---

## 📌 Module 3 — Machine Learning Basics

**Why?** You need to understand the theory behind what the model is doing.

| Topic | What to Study | Resource |
|---|---|---|
| What is ML? | Supervised vs Unsupervised learning | [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/ml-intro) |
| Training vs Testing | Overfitting, underfitting, validation | [ML Glossary](https://ml-cheatsheet.readthedocs.io/en/latest/) |
| Loss functions | What the model optimizes | [Towards DS — Loss Functions](https://towardsdatascience.com/loss-functions-and-their-use-in-neural-networks-a470e703f1e9) |
| Metrics | mAP, Precision, Recall, F1-score | [Towards DS — mAP explained](https://towardsdatascience.com/breaking-down-mean-average-precision-map-ae462f623a52) |
| Confusion Matrix | TP, FP, TN, FN | [Scikit-learn — Confusion Matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) |

**When to use**: Before training. Helps you understand what metrics like `mAP50: 0.87` actually mean in your results.

---

## 📌 Module 4 — Deep Learning & Neural Networks

**Why?** YOLO is a deep learning model — you need to understand how neural networks learn.

| Topic | What to Study | Resource |
|---|---|---|
| What is a Neural Network? | Neurons, layers, activations | [3Blue1Brown — Neural Networks (YouTube)](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) |
| Backpropagation | How weights are updated | [ML Cheatsheet — Backprop](https://ml-cheatsheet.readthedocs.io/en/latest/backpropagation.html) |
| Gradient Descent | Optimizers: SGD, Adam | [DeepLearning.AI lecture](https://www.deeplearning.ai/courses/deep-learning-specialization/) |
| Batch & Epochs | What happens per training cycle | [Jason Brownlee — Epochs](https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/) |
| Transfer Learning | Using pretrained weights (e.g., COCO) | [TF Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning) |

**When to use**: To explain your project methodology in the college report.

---

## 📌 Module 5 — Convolutional Neural Networks (CNNs)

**Why?** YOLO is built on CNNs. Understanding CNNs helps you explain how your model sees fire.

| Topic | What to Study | Resource |
|---|---|---|
| What is a CNN? | Filters, feature maps, pooling | [CS231n Stanford Notes](https://cs231n.github.io/convolutional-networks/) |
| Conv layers | How edges/shapes/textures are learned | [CNN Explainer (Interactive)](https://poloclub.github.io/cnn-explainer/) |
| Pooling | MaxPool, AvgPool, downsampling | [Towards DS — Pooling](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53) |
| Backbone networks | ResNet, MobileNet (feature extractors used in YOLO) | [Papers With Code — ResNet](https://paperswithcode.com/model/resnet) |

**When to use**: Directly relevant to explaining your model architecture in the report.

---

## 📌 Module 6 — Object Detection Concepts

**Why?** This project is object detection, not just classification. You need to understand bounding boxes.

| Topic | What to Study | Resource |
|---|---|---|
| Classification vs Detection | What's different | [Towards DS — Detection overview](https://towardsdatascience.com/object-detection-in-20-years-a-survey-1e1f9fa1a2d5) |
| Bounding Boxes | x_center, y_center, width, height (YOLO format) | [Roboflow — YOLO format](https://blog.roboflow.com/yolo-bounding-box-format/) |
| IoU (Intersection over Union) | How detection accuracy is measured | [Towards DS — IoU](https://towardsdatascience.com/intersection-over-union-iou-calculation-for-evaluating-an-image-segmentation-model-8b22e2e84686) |
| Non-Max Suppression (NMS) | Removing duplicate bounding boxes | [Towards DS — NMS](https://towardsdatascience.com/non-max-suppression-nms-93ce178e177c) |
| Anchor Boxes | What older YOLO versions use | [ML Mastery — Anchors](https://machinelearningmastery.com/anchor-boxes-for-object-detection/) |
| mAP | Mean Average Precision explained | [Towards DS — mAP deep dive](https://towardsdatascience.com/breaking-down-mean-average-precision-map-ae462f623a52) |

**When to use**: Core knowledge for your viva. Expect to be asked about IoU and mAP.

---

## 📌 Module 7 — YOLO Architecture

**Why?** Your model IS a YOLO model. Know it inside out.

| Topic | What to Study | Resource |
|---|---|---|
| YOLO history (v1→v12) | How it evolved | [YOLO Timeline — Towards DS](https://towardsdatascience.com/a-look-at-the-yolo-object-detectors-series-from-yolov1-to-yolov8-c44e7be3e6fd) |
| YOLOv8 architecture | Backbone, neck, head | [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/models/yolov8/) |
| YOLO12 (your model) | Attention-based improvements | [Ultralytics YOLO12 Docs](https://docs.ultralytics.com/models/yolo12/) |
| YOLO config params | `epochs`, `imgsz`, `batch`, `patience` | [Ultralytics Train Docs](https://docs.ultralytics.com/modes/train/) |
| YOLO label format | Class x_c y_c w h (normalized) | [Ultralytics Dataset Docs](https://docs.ultralytics.com/datasets/detect/) |

**When to use**: This is the heart of your project — study this thoroughly.

---

## 📌 Module 8 — Kaggle & Training Workflow

**Why?** You're training on Kaggle's free GPU. Know how to use it properly.

| Topic | What to Study | Resource |
|---|---|---|
| What is Kaggle? | Notebooks, datasets, GPUs | [Kaggle Learn — Intro](https://www.kaggle.com/learn) |
| Using Kaggle GPU | T4 GPU, enabling accelerator | [Kaggle Docs — Notebooks](https://www.kaggle.com/docs/notebooks) |
| Saving outputs | `/kaggle/working/` folder | [Kaggle Output Guide](https://www.kaggle.com/docs/notebooks#notebook-output) |
| Session limits | 30 hrs/week, 9hr per session limit | Kaggle FAQ |
| Resuming training | `model.train(resume=True)` | [Ultralytics — Resume](https://docs.ultralytics.com/modes/train/#resuming-interrupted-trainings) |

**When to use**: Right now — your model is currently training on Kaggle.

---

## 📌 Module 9 — ONNX (Model Export & Deployment)

**Why?** After training, you export to ONNX so it works on any machine without needing PyTorch installed.

| Topic | What to Study | Resource |
|---|---|---|
| What is ONNX? | Open Neural Network Exchange format | [ONNX Official Site](https://onnx.ai/) |
| Why use ONNX? | Portability across frameworks | [ONNX Runtime Docs](https://onnxruntime.ai/docs/) |
| Export from YOLO | `model.export(format='onnx')` | [Ultralytics Export Docs](https://docs.ultralytics.com/modes/export/) |
| ONNX Runtime inference | Running a `.onnx` file in Python | [ONNX Runtime Python](https://onnxruntime.ai/docs/get-started/with-python.html) |
| opset versions | `opset=12` (safest choice) | [ONNX opset reference](https://onnx.ai/onnx/intro/opset.html) |

**When to use**: After training is complete and you need to run the model in your UI.

---

## 📌 Module 10 — Flask (Web UI Backend)

**Why?** Flask lets you create a web dashboard that shows live camera feed with detection overlays.

| Topic | What to Study | Resource |
|---|---|---|
| Flask basics | Routes, templates, running a server | [Flask Official Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/) |
| Rendering HTML | `render_template`, Jinja2 | [Jinja2 Docs](https://jinja.palletsprojects.com/en/3.1.x/) |
| Video streaming (MJPEG) | Streaming camera frames to browser | [Miguel Grinberg — Video Streaming](https://blog.miguelgrinberg.com/post/video-streaming-with-flask) |
| POST/GET requests | Handling button clicks from UI | [Flask Request Handling](https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data) |
| Static files | Serving CSS, JS, images | [Flask Static Files](https://flask.palletsprojects.com/en/stable/quickstart/#static-files) |

**When to use**: Phase 5 of the project — after the inference engine (`fire.py`) is working.

---

## 📌 Module 11 — Frontend (HTML + CSS + JavaScript)

**Why?** Your web dashboard needs a nice, modern UI for the viva/demo.

| Topic | What to Study | Resource |
|---|---|---|
| HTML5 basics | Structure, semantic tags | [MDN HTML Guide](https://developer.mozilla.org/en-US/docs/Learn/HTML) |
| CSS3 | Flexbox, Grid, animations | [CSS Tricks — Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) |
| JavaScript DOM | Updating UI dynamically | [MDN JS Guide](https://developer.mozilla.org/en-US/docs/Learn/JavaScript) |
| Fetch API | Polling server for detection data | [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) |
| Chart.js | Drawing confidence/detection graphs | [Chart.js Docs](https://www.chartjs.org/docs/latest/) |

**When to use**: While building the dashboard in Phase 5.

---

## 📌 Module 12 — Dataset Understanding (YOLO Format)

**Why?** Your notebook already cleans the dataset — understand why those steps exist.

| Topic | What to Study | Resource |
|---|---|---|
| YOLO dataset structure | `images/`, `labels/`, `data.yaml` | [Roboflow — YOLO dataset](https://blog.roboflow.com/yolo-bounding-box-format/) |
| `data.yaml` explained | `nc`, `names`, `train`, `val`, `test` keys | [Ultralytics — data.yaml](https://docs.ultralytics.com/datasets/detect/) |
| Label file format | `class x_c y_c w h` per row, normalized | [Roboflow Label Format](https://blog.roboflow.com/label-a-dataset-for-object-detection/) |
| Data augmentation | Mosaic, flips, color jitter in YOLO | [Ultralytics Augmentation](https://docs.ultralytics.com/reference/data/augment/) |
| Train/Val/Test split | Why 70/20/10 or 80/10/10 is used | [Towards DS — Data Splits](https://towardsdatascience.com/train-validation-and-test-sets-72cb40cba9e7) |

**When to use**: During EDA (Phase 2) and to explain dataset preparation in your report.

---

## 🎓 Recommended Video Course Path

For a structured video learning experience, follow this sequence:

1. **[Python for Everybody](https://www.coursera.org/specializations/python)** — Coursera (free audit)
2. **[OpenCV Python Tutorials](https://www.youtube.com/playlist?list=PLS1QulWo1RIa7D1O6skqDQ-JZ1GGHKK-K)** — YouTube (PySource)
3. **[Neural Networks by 3Blue1Brown](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)** — YouTube (free)
4. **[YOLOv8 Complete Tutorial](https://www.youtube.com/watch?v=m9fH9OWn8YM)** — YouTube (Nicolai Nielsen)
5. **[Flask Web App Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)** — YouTube (Corey Schafer)

---

## 📝 Quick Reference — Key Terms for Viva

| Term | One-line Definition |
|---|---|
| **YOLO** | You Only Look Once — single-pass real-time object detector |
| **mAP** | Mean Average Precision — primary metric for object detection |
| **IoU** | Overlap between predicted and ground-truth bounding box |
| **NMS** | Removes duplicate detections for the same object |
| **Transfer Learning** | Starting from pretrained weights instead of random initialization |
| **ONNX** | Portable model format that runs without the original framework |
| **Epoch** | One complete pass through the entire training dataset |
| **Batch Size** | Number of images processed per weight update |
| **Overfitting** | Model memorizes training data but fails on new data |
| **Confidence Threshold** | Minimum score to accept a detection (e.g., 0.5) |
| **data.yaml** | Config file that tells YOLO where the dataset and classes are |
| **Backbone** | Feature extraction part of the neural network |

---

*Study Guide created for: MCA Final Year Project — Fire Hazard Detection | Feb 2026*
