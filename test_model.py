"""
Fire & Smoke Detection Test Script
Usage:
    python test_model.py                        → webcam live test
    python test_model.py --image  <path>        → test on a single image
    python test_model.py --video  <path>        → test on a video file
"""

import sys
import os
import cv2
from ultralytics import YOLO

MODEL_PATH = "reference/Smoke Fire.pt"
CONF_THRESHOLD = 0.3


def test_on_webcam():
    print("🔥 Loading model...")
    model = YOLO(MODEL_PATH)
    print("✅ Model loaded | 📷 Opening webcam... Press Q to quit.\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam not found. Use: python test_model.py --video <path>")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)
        annotated = results[0].plot()
        for box in results[0].boxes:
            print(f"  🔥 {model.names[int(box.cls)]} — {float(box.conf):.2%}", end="\r")
        cv2.imshow("Fire & Smoke Detection | Q to quit", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def test_on_image(image_path):
    print("🔥 Loading model...")
    model = YOLO(MODEL_PATH)
    print(f"✅ Model loaded | 🖼️  Testing on: {image_path}\n")

    results = model.predict(image_path, conf=CONF_THRESHOLD, save=True)
    print("📊 Detections:")
    for box in results[0].boxes:
        print(f"   ✅ {model.names[int(box.cls)]} — {float(box.conf):.2%}")
    if not results[0].boxes:
        print("   ℹ️  Nothing detected.")
    print(f"\n💾 Output saved to: runs/detect/predict/")


def test_on_video(video_path):
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        return

    print("🔥 Loading model...")
    model = YOLO(MODEL_PATH)
    print(f"✅ Model loaded | 🎬 Testing on: {video_path}\n")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Could not open video file.")
        return

    # Setup output video writer
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 25
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    os.makedirs("test_output", exist_ok=True)
    out_path = "test_output/output_detected.mp4"
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    frame_num = 0
    detection_log = []  # (frame, class, confidence)

    print(f"📐 Resolution: {width}x{height} | FPS: {fps:.1f} | Frames: {total}")
    print("⏳ Processing... Press Q to stop early.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1
        results = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)
        annotated = results[0].plot()

        # Log detections
        for box in results[0].boxes:
            cls_name = model.names[int(box.cls)]
            conf = float(box.conf)
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


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        mode = sys.argv[1]
        path = sys.argv[2]
        if mode == "--image":
            test_on_image(path)
        elif mode == "--video":
            test_on_video(path)
        else:
            print("Usage: python test_model.py --video <path>  OR  --image <path>")
    else:
        test_on_webcam()
