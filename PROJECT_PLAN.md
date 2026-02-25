# 🔥 Fire Hazard Detection System — Final Year Project Plan
**MCA Final Year Project | 2025–2026**

---

## 📌 Project Overview

A real-time **Fire & Smoke Detection System** powered by a YOLOv8 object detection model trained on the **Smoke-Fire-Detection-YOLO** dataset from Kaggle. The system detects fire and smoke from live camera feeds or video files and presents alert dashboards via a modern web/desktop UI.

| Attribute | Details |
|---|---|
| **Model Architecture** | YOLOv8n / YOLOv8s (Ultralytics) |
| **Dataset** | Smoke-Fire-Detection-YOLO (Kaggle) — 21,000+ images |
| **Training Platform** | Kaggle Notebooks (free P100 / T4 GPU) |
| **Deployment Target** | Local PC / Raspberry Pi / Web App |
| **Output Format** | ONNX (for broad compatibility) |
| **UI Type** | Desktop GUI (Tkinter/PyQt) OR Web Dashboard (Flask + HTML) |

---

## 🗂️ Dataset Details

- **Kaggle Link**: [sayedgamal99/smoke-fire-detection-yolo](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo)
- **Classes**: `fire`, `smoke` (object detection with bounding boxes)
- **Format**: YOLO format (`.txt` label files + YAML config)
- **Size**: 21,000+ images with train/val/test splits
- **Source**: Aggregated from the D-Fire dataset (GitHub: saife245/fire-detection) and additional public sources

---

## 📋 Project Phases

---

### Phase 1 — Research & Setup ✅ (Week 1–2)

- [ ] Study YOLOv8 architecture and Ultralytics API
- [ ] Explore the Kaggle dataset structure and label format
- [ ] Set up GitHub repository for version control
- [ ] Set up local Python environment (optional for inference UI)
- [ ] Read relevant papers on fire detection using deep learning
- [ ] Document background for college report

**Deliverable**: Research notes + GitHub repo initialized

---

### Phase 2 — Data Preparation (Week 2–3)

- [ ] Download and explore the dataset on Kaggle
- [ ] Verify dataset integrity: check label files, class distribution
- [ ] Visualize sample images with bounding boxes
- [ ] Analyze class imbalance (fire vs smoke distribution)
- [ ] Apply data augmentation strategy in training config:
  - Horizontal flip, mosaic, color jitter, random scale
- [ ] Create `data.yaml` or verify the provided one

**Deliverable**: EDA notebook committed on Kaggle

---

### Phase 3 — Model Training on Kaggle (Week 3–5)

> ✅ All training happens on Kaggle (free GPU T4/P100 — up to 30 hrs/week)

#### 3.1 Kaggle Notebook Setup
```python
# Install Ultralytics
!pip install ultralytics -q

# Verify GPU
import torch
print(torch.cuda.is_available())  # Should print True
```

#### 3.2 Training Script
```python
from ultralytics import YOLO

# Load pretrained base model
model = YOLO('yolov8n.pt')  # Start with nano; try small for better accuracy

# Train on the dataset
results = model.train(
    data='/kaggle/input/smoke-fire-detection-yolo/data.yaml',
    epochs=50,          # Start with 50, extend to 100 if needed
    imgsz=640,          # Standard YOLO input size
    batch=16,           # Fits in Kaggle GPU memory
    name='fire_smoke_v1',
    patience=10,         # Early stopping
    device=0             # GPU
)
```

#### 3.3 Evaluation
```python
# Validate model
metrics = model.val()
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

#### 3.4 Export to ONNX
```python
# Export the best model to ONNX format
model.export(format='onnx', imgsz=640, opset=12)
# Output: best.onnx
```

#### 3.5 Download from Kaggle
- After training, go to **Output** section of the notebook
- Download `best.pt` (PyTorch) and `best.onnx`
- Save to: `mca_final_fire/models/`

**Deliverable**: `fire_smoke_v1.onnx` + training metrics (mAP, loss curves)

---

### Phase 4 — Local Inference Engine (Week 5–6)

Create a Python inference script that runs on the local machine using the downloaded ONNX model.

#### File: `detect_fire.py`
- Load ONNX model via `onnxruntime` or use `ultralytics` directly with `.pt`
- Accept input: webcam stream / video file / image folder
- Draw bounding boxes with class labels (`fire` / `smoke`)
- Display confidence score
- Trigger alert logic when detection confidence > threshold

#### Dependencies (local)
```
ultralytics>=8.0
onnxruntime
opencv-python
numpy
Pillow
```

---

### Phase 5 — UI Development (Week 6–8)

Two options (choose one based on preference):

#### Option A: Desktop GUI (Recommended for demo)
**Tech**: Python + Tkinter or PyQt5

Features:
- Live camera feed with bounding box overlay
- Sidebar: detection log with timestamps
- Alert panel: audio/visual alarm when fire/smoke detected
- Snapshot button (save frames on detection)
- Configurable confidence threshold slider

#### Option B: Web Dashboard (More impressive for presentation)
**Tech**: Flask (Python backend) + HTML/CSS/JS frontend

Features:
- Video stream via MJPEG or WebSocket
- Real-time detection overlay on browser
- Alert notification panel
- Detection history with timestamps
- Analytics page: detection counts, confidence trends
- Mobile-responsive design

**Recommended**: **Option B (Web Dashboard)** — more visual impact for final year presentation

**Deliverable**: Working UI connected to the inference engine

---

### Phase 6 — Integration & Testing (Week 8–9)

- [ ] Connect UI to live webcam feed
- [ ] Test on video files with known fire/smoke scenarios
- [ ] Test edge cases: low light, partial smoke, indoor fire
- [ ] Measure FPS performance on local hardware
- [ ] Test ONNX model vs PyTorch model speed
- [ ] Fine-tune confidence threshold for best precision/recall balance
- [ ] Stress test: 30-min continuous run

---

### Phase 7 — Documentation & Report (Week 9–11)

- [ ] Write methodology section (YOLO architecture, transfer learning)
- [ ] Add results: mAP, precision, recall, F1 score tables
- [ ] Add screenshots/demo video of the UI
- [ ] Compare with baseline (classical CV methods)
- [ ] Create presentation slides (15–20 slides)
- [ ] Record demo video (2–3 minutes)
- [ ] Write abstract, introduction, literature review, conclusion

**Deliverables**: Project report (Word/PDF) + PPT presentation

---

### Phase 8 — Final Submission & Demo (Week 11–12)

- [ ] Code cleanup and commenting
- [ ] Push final code to GitHub (public or private)
- [ ] Create `README.md` with setup instructions
- [ ] Package everything (models, code, report, demo video)
- [ ] Practice viva questions

---

## 📁 Project Folder Structure

```
mca_final_fire/
│
├── models/
│   ├── best.pt                  # PyTorch model (downloaded from Kaggle)
│   └── best.onnx                # ONNX model (for deployment)
│
├── notebooks/
│   └── fire_detection_training.ipynb   # Kaggle training notebook
│
├── src/
│   ├── detect_fire.py           # Core inference engine
│   ├── app.py                   # Flask web app (if Option B)
│   └── utils.py                 # Helper functions
│
├── ui/
│   ├── templates/               # HTML templates
│   │   └── index.html
│   └── static/                  # CSS, JS, images
│
├── data/
│   └── samples/                 # Test images/videos
│
├── docs/
│   ├── report.docx
│   └── presentation.pptx
│
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md              # This file
```

---

## 🛠️ Tech Stack Summary

| Layer | Technology |
|---|---|
| Model Training | YOLOv8 (Ultralytics) on Kaggle |
| Model Format | `.pt` (training) → `.onnx` (deployment) |
| Inference Engine | Python + ONNX Runtime / Ultralytics |
| UI Backend | Flask (Python) |
| UI Frontend | HTML5 + CSS3 + JavaScript |
| Video Processing | OpenCV |
| Version Control | GitHub |
| Training Platform | Kaggle Notebooks (free GPU) |

---

## 🎯 Expected Model Performance Targets

| Metric | Target |
|---|---|
| mAP@0.5 | ≥ 0.85 |
| Precision | ≥ 0.80 |
| Recall | ≥ 0.80 |
| FPS (local PC) | ≥ 15 FPS |
| Inference Latency | < 100ms per frame |

---

## ⚠️ Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Kaggle session timeout during training | Use `model.train(resume=True)`, save checkpoints |
| Low mAP | Try YOLOv8s (small) instead of YOLOv8n, increase epochs |
| ONNX export issues | Test with opset 11 or 12; use `.pt` as fallback |
| Dataset imbalance | Use `augment=True`, weighted loss in YOLO config |
| Low FPS on weak hardware | Use YOLOv8n (fastest), reduce input size to 416 |

---

## 📅 Timeline (12 Weeks)

```
Week 1–2   : Phase 1 — Research & Environment Setup
Week 2–3   : Phase 2 — Dataset Exploration & EDA
Week 3–5   : Phase 3 — Model Training on Kaggle
Week 5–6   : Phase 4 — Local Inference Engine
Week 6–8   : Phase 5 — UI Development
Week 8–9   : Phase 6 — Integration & Testing
Week 9–11  : Phase 7 — Documentation & Report
Week 11–12 : Phase 8 — Final Submission & Demo
```

---

## 🔗 Key References

1. **Dataset**: [Smoke-Fire-Detection-YOLO on Kaggle](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo)
2. **D-Fire Dataset Source**: [GitHub — saife245/fire-detection](https://github.com/saife245/fire-detection)
3. **YOLOv8 Docs**: [Ultralytics YOLOv8](https://docs.ultralytics.com/)
4. **ONNX Runtime**: [onnxruntime.ai](https://onnxruntime.ai/)
5. **Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)

---

## 🚀 Immediate Next Steps

1. **Create a Kaggle account** (if not done) and enable GPU in notebook settings
2. **Fork/copy the dataset** to your Kaggle workspace
3. **Create the training notebook** using the script in Phase 3
4. **Set up the local project folder structure** as shown above
5. **Initialize GitHub repo** and push the project plan

---

*Last Updated: February 2026 | MCA Final Year Project*
