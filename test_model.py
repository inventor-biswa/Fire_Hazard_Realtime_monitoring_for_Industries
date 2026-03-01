"""
Fire & Smoke Detection Test Script
Usage:
    python test_model.py                                    → webcam, default model
    python test_model.py --model best                      → webcam, best.pt model
    python test_model.py --model fire_only --image <path>  → image test
    python test_model.py --model smoke_fire --video <path> → video test

Available model keys:  smoke_fire | best | fire_only
"""

import sys
import os
import cv2
from ultralytics import YOLO

# ------------------------------------------------------------------
# Model Registry — mirrors app.py
# ------------------------------------------------------------------
MODEL_REGISTRY = {
    "smoke_fire": {
        "label": "Smoke & Fire (YOLOv12)",
        "path":  "reference/Smoke Fire.pt",
        "description": "General smoke and fire detection — default model",
    },
    "best": {
        "label": "Best Weights (Fire-only)",
        "path":  "reference/best_fixed.pt",
        "description": "Custom-trained best checkpoint — fire class only",
    },
    "fire_only": {
        "label": "Fire-Only Model",
        "path":  "reference/fire_fixed.pt",
        "description": "Specialised fire-only detection model",
    },
    "fire_smoke_best": {
        "label": "Fire & Smoke Best (v2)",
        "path":  "reference/fire_smoke_best.pt",
        "description": "Smoke + fire detection — 2 classes (best weights)",
    },
}

CONF_THRESHOLD = 0.3


def resolve_model(key: str) -> tuple[str, str]:
    """Return (path, label) for a model key, or exit with error."""
    if key not in MODEL_REGISTRY:
        print(f"❌  Unknown model key: '{key}'")
        print(f"    Available keys: {', '.join(MODEL_REGISTRY.keys())}")
        sys.exit(1)
    entry = MODEL_REGISTRY[key]
    return entry["path"], entry["label"]


def load_model(key: str) -> YOLO:
    path, label = resolve_model(key)
    print(f"🔥 Loading model [{label}]  ←  {path}")
    model = YOLO(path)
    print(f"✅ Model loaded — classes: {list(model.names.values())}\n")
    return model


# ------------------------------------------------------------------
# Test modes
# ------------------------------------------------------------------

def test_on_webcam(model: YOLO):
    print("📷 Opening webcam... Press Q to quit.\n")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam not found. Use: python test_model.py --video <path>")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results  = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)
        annotated = results[0].plot()
        for box in results[0].boxes:
            print(f"  🔥 {model.names[int(box.cls)]} — {float(box.conf):.2%}", end="\r")
        cv2.imshow("Fire & Smoke Detection | Q to quit", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def test_on_image(model: YOLO, image_path: str):
    print(f"🖼️  Testing on: {image_path}\n")
    results = model.predict(image_path, conf=CONF_THRESHOLD, save=True)
    print("📊 Detections:")
    for box in results[0].boxes:
        print(f"   ✅ {model.names[int(box.cls)]} — {float(box.conf):.2%}")
    if not results[0].boxes:
        print("   ℹ️  Nothing detected.")
    print(f"\n💾 Output saved to: runs/detect/predict/")


def test_on_video(model: YOLO, video_path: str):
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        return

    print(f"🎬 Testing on: {video_path}\n")
    cap    = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Could not open video file.")
        return

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 25
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    os.makedirs("test_output", exist_ok=True)
    out_path = "test_output/output_detected.mp4"
    writer   = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    frame_num     = 0
    detection_log = []

    print(f"📐 Resolution: {width}x{height} | FPS: {fps:.1f} | Frames: {total}")
    print("⏳ Processing... Press Q to stop early.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1
        results   = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)
        annotated = results[0].plot()

        for box in results[0].boxes:
            cls_name = model.names[int(box.cls)]
            conf     = float(box.conf)
            detection_log.append((frame_num, cls_name, conf))
            print(f"  Frame {frame_num}/{total} | 🔥 {cls_name} {conf:.2%}", end="\r")

        writer.write(annotated)
        cv2.imshow("Fire & Smoke Detection | Q to quit", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n⛔ Stopped early by user.")
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    # Summary
    print(f"\n\n{'='*50}")
    print(f"📊 Detection Summary — {frame_num} frames processed")
    print(f"{'='*50}")
    fire_count  = sum(1 for _, c, _ in detection_log if c == "fire")
    smoke_count = sum(1 for _, c, _ in detection_log if c == "smoke")
    print(f"   🔥 Fire  detections : {fire_count}")
    print(f"   💨 Smoke detections : {smoke_count}")
    print(f"   📦 Total detections : {len(detection_log)}")
    if detection_log:
        avg_conf = sum(c for _, _, c in detection_log) / len(detection_log)
        print(f"   📈 Avg confidence  : {avg_conf:.2%}")
    print(f"\n💾 Output video saved to: {out_path}")


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------

def _parse_args():
    """Minimal arg parser without importing argparse for simplicity."""
    args = sys.argv[1:]
    model_key  = "smoke_fire"
    mode       = "webcam"
    media_path = None

    i = 0
    while i < len(args):
        token = args[i]
        if token == "--model" and i + 1 < len(args):
            model_key = args[i + 1]; i += 2
        elif token == "--image" and i + 1 < len(args):
            mode = "image"; media_path = args[i + 1]; i += 2
        elif token == "--video" and i + 1 < len(args):
            mode = "video"; media_path = args[i + 1]; i += 2
        elif token in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"⚠️  Unknown argument: {token}")
            print("Run with --help for usage.")
            sys.exit(1)

    return model_key, mode, media_path


if __name__ == "__main__":
    model_key, mode, media_path = _parse_args()

    print(f"\n{'='*55}")
    print(f"  🔥 Fire Detection Test  |  Model: {model_key}")
    print(f"{'='*55}\n")

    # Print all available models
    print("📋 Available models:")
    for k, v in MODEL_REGISTRY.items():
        marker = " ◀ selected" if k == model_key else ""
        print(f"   [{k}]  {v['label']}{marker}")
    print()

    model = load_model(model_key)

    if mode == "image":
        test_on_image(model, media_path)
    elif mode == "video":
        test_on_video(model, media_path)
    else:
        test_on_webcam(model)
