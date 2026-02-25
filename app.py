"""
Fire Detection Flask Web App — Enhanced
Phase A+B: Log, Alert History, Stats, Snapshots, Charts, Settings
"""

import os, io, csv, time, threading, datetime
import cv2
from flask import Flask, render_template, Response, request, jsonify, send_file
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

os.makedirs('uploads', exist_ok=True)
os.makedirs('test_output', exist_ok=True)
os.makedirs('snapshots', exist_ok=True)

# ---------- Model ----------
MODEL_PATH = "reference/Smoke Fire.pt"
model = YOLO(MODEL_PATH)

# ---------- Settings (mutable) ----------
settings = {
    "conf":           0.35,
    "alert_seconds":  10,
    "camera_id":      0,
}
settings_lock = threading.Lock()

# ---------- Shared state ----------
start_time = time.time()
stats = {
    "frames_analyzed": 0,
    "fire_count":  0,
    "smoke_count": 0,
    "alerts_triggered": 0,
}
stats_lock = threading.Lock()

# Persistent detection log  [{time, source, cls, conf}]
detection_log  = []
alert_history  = []   # [{time, duration, snapshot}]
chart_data     = []   # [{ts, fire_conf, smoke_conf}]  — last 300 points (~5 min at 1fps)
log_lock       = threading.Lock()

# ---------- Alert state ----------
alert_state = {
    "active": False,
    "seconds": 0,
    "detected_class": None,
    "first_detect_time": None,
}
alert_lock = threading.Lock()

# Shared current_frame for manual snapshots
current_frame_holder = {"frame": None}
frame_lock = threading.Lock()


def update_alert(detected: bool, cls_name: str | None = None, frame=None):
    with settings_lock:
        threshold = settings["alert_seconds"]

    with alert_lock:
        now = time.time()
        was_active = alert_state["active"]
        if detected:
            if alert_state["first_detect_time"] is None:
                alert_state["first_detect_time"] = now
            elapsed = now - alert_state["first_detect_time"]
            alert_state["seconds"]        = round(elapsed, 1)
            alert_state["detected_class"] = cls_name
            alert_state["active"]         = elapsed >= threshold

            # Trigger alert → save snapshot + history entry
            if alert_state["active"] and not was_active:
                snap_name = f"snapshots/alert_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                if frame is not None:
                    cv2.imwrite(snap_name, frame)
                with log_lock:
                    alert_history.append({
                        "time":     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": round(elapsed, 1),
                        "cls":      cls_name,
                        "snapshot": snap_name,
                    })
                    with stats_lock:
                        stats["alerts_triggered"] += 1
        else:
            alert_state["active"]             = False
            alert_state["first_detect_time"]  = None
            alert_state["seconds"]            = 0
            alert_state["detected_class"]     = None


def add_detection(cls_name, conf_val, source="Live Cam"):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    entry = {"time": ts, "source": source, "cls": cls_name, "conf": round(conf_val * 100, 1)}
    with log_lock:
        detection_log.append(entry)
        if len(detection_log) > 500:
            detection_log.pop(0)
    with stats_lock:
        if cls_name == "fire":
            stats["fire_count"] += 1
        else:
            stats["smoke_count"] += 1


def add_chart_point(fire_conf, smoke_conf):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with log_lock:
        chart_data.append({"ts": ts, "fire": round(fire_conf * 100, 1), "smoke": round(smoke_conf * 100, 1)})
        if len(chart_data) > 60:   # keep last 60 points
            chart_data.pop(0)


# ---------- Webcam  ----------
camera = None
camera_lock = threading.Lock()


def get_camera():
    global camera
    with settings_lock:
        cam_id = settings["camera_id"]
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(cam_id)
    return camera


def generate_frames():
    cap = get_camera()
    prev_cam = settings["camera_id"]

    while True:
        # Hot-swap camera if settings changed
        with settings_lock:
            cur_cam = settings["camera_id"]
        if cur_cam != prev_cam:
            cap.release()
            cap = cv2.VideoCapture(cur_cam)
            prev_cam = cur_cam

        with camera_lock:
            success, frame = cap.read()
        if not success:
            continue

        with settings_lock:
            conf_thr = settings["conf"]

        results = model.predict(frame, conf=conf_thr, verbose=False)
        annotated = results[0].plot()

        with frame_lock:
            current_frame_holder["frame"] = frame.copy()

        with stats_lock:
            stats["frames_analyzed"] += 1

        boxes = results[0].boxes
        detected = len(boxes) > 0
        cls_name, conf_val = None, 0.0
        best_fire_conf, best_smoke_conf = 0.0, 0.0

        for box in boxes:
            cn     = model.names[int(box.cls)]
            conf_v = float(box.conf)
            add_detection(cn, conf_v, source="Live Cam")
            if cn == "fire"  and conf_v > best_fire_conf:  best_fire_conf  = conf_v
            if cn == "smoke" and conf_v > best_smoke_conf: best_smoke_conf = conf_v
            cls_name, conf_val = cn, conf_v

        add_chart_point(best_fire_conf, best_smoke_conf)
        update_alert(detected, cls_name, frame=frame)

        # HUD overlay
        with alert_lock:
            is_alert = alert_state["active"]
            secs     = alert_state["seconds"]
        with settings_lock:
            thr = settings["alert_seconds"]

        if is_alert:
            cv2_mod = annotated.copy()
            cv2.putText(cv2_mod, "!!! TRUE FIRE ALERT !!!", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
            annotated = cv2_mod
        elif detected:
            cv2.putText(annotated, f"Detecting... {secs:.1f}s / {thr}s",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

        _, buf = cv2.imencode('.jpg', annotated)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')


# ===================== ROUTES =====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/alert_status')
def alert_status():
    with alert_lock:
        data = dict(alert_state)
    with settings_lock:
        data["threshold"] = settings["alert_seconds"]
    return jsonify(data)


# --- Stats ---
@app.route('/get_stats')
def get_stats():
    uptime = int(time.time() - start_time)
    h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
    with stats_lock:
        d = dict(stats)
    d["uptime"] = f"{h:02d}:{m:02d}:{s:02d}"
    return jsonify(d)


# --- Detection Log ---
@app.route('/get_log')
def get_log():
    with log_lock:
        return jsonify(list(reversed(detection_log[-200:])))


@app.route('/export_log')
def export_log():
    with log_lock:
        rows = list(detection_log)
    si = io.StringIO()
    w  = csv.DictWriter(si, fieldnames=["time", "source", "cls", "conf"])
    w.writeheader()
    w.writerows(rows)
    output = io.BytesIO(si.getvalue().encode())
    output.seek(0)
    return send_file(output, mimetype='text/csv',
                     as_attachment=True, download_name='detection_log.csv')


# --- Alert History ---
@app.route('/get_alert_history')
def get_alert_history():
    with log_lock:
        return jsonify(list(reversed(alert_history)))


# --- Chart Data ---
@app.route('/get_chart_data')
def get_chart_data():
    with log_lock:
        return jsonify(list(chart_data))


# --- Snapshot ---
@app.route('/snapshot')
def snapshot():
    with frame_lock:
        frame = current_frame_holder["frame"]
    if frame is None:
        return jsonify({"error": "No frame available"}), 400
    results = model.predict(frame, conf=settings["conf"], verbose=False)
    annotated = results[0].plot()
    name = f"snapshots/snap_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(name, annotated)
    return jsonify({"path": name, "detections": [
        {"cls": model.names[int(b.cls)], "conf": round(float(b.conf)*100,1)}
        for b in results[0].boxes
    ]})


@app.route('/get_snapshot')
def get_snapshot():
    path = request.args.get('path')
    if path and os.path.exists(path):
        return send_file(path, mimetype='image/jpeg')
    return "Not found", 404


# --- Settings ---
@app.route('/get_settings')
def get_settings():
    with settings_lock:
        return jsonify(dict(settings))


@app.route('/update_settings', methods=['POST'])
def update_settings():
    data = request.json
    with settings_lock:
        if 'conf' in data:
            settings['conf'] = float(data['conf'])
        if 'alert_seconds' in data:
            settings['alert_seconds'] = int(data['alert_seconds'])
        if 'camera_id' in data:
            settings['camera_id'] = int(data['camera_id'])
    return jsonify({"ok": True, "settings": dict(settings)})


# --- Image Upload ---
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    with settings_lock:
        conf_thr = settings["conf"]
    results = model.predict(filepath, conf=conf_thr, save=True,
                            project='test_output', name='image_result', exist_ok=True)
    detections = [{"class": model.names[int(b.cls)], "confidence": round(float(b.conf)*100,1)}
                  for b in results[0].boxes]
    for d in detections:
        add_detection(d["class"], d["confidence"]/100, source="Image Upload")
    out_dir = 'test_output/image_result'
    imgs    = [f for f in os.listdir(out_dir) if f.endswith(('.jpg','.png'))] if os.path.exists(out_dir) else []
    return jsonify({"detections": detections, "count": len(detections),
                    "annotated_image": os.path.join(out_dir, imgs[-1]) if imgs else None})


@app.route('/get_image')
def get_image():
    path = request.args.get('path')
    if path and os.path.exists(path):
        return send_file(path, mimetype='image/jpeg')
    return "Not found", 404


# --- Video Upload ---
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    with settings_lock:
        conf_thr = settings["conf"]

    cap    = cv2.VideoCapture(filepath)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 25
    writer = cv2.VideoWriter('test_output/video_result.mp4',
                              cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    log    = []
    fn     = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        fn += 1
        results  = model.predict(frame, conf=conf_thr, verbose=False)
        annotated = results[0].plot()
        for b in results[0].boxes:
            cn = model.names[int(b.cls)]
            cv_val = float(b.conf)
            log.append({"frame": fn, "class": cn, "confidence": round(cv_val*100,1)})
            add_detection(cn, cv_val, source="Video Upload")
        writer.write(annotated)
    cap.release(); writer.release()
    fc = sum(1 for d in log if d["class"]=="fire")
    sc = sum(1 for d in log if d["class"]=="smoke")
    ac = round(sum(d["confidence"] for d in log)/len(log),1) if log else 0
    return jsonify({"total_frames":fn,"total_detections":len(log),
                    "fire_count":fc,"smoke_count":sc,"avg_confidence":ac})


@app.route('/get_video')
def get_video():
    p = 'test_output/video_result.mp4'
    return send_file(p, mimetype='video/mp4') if os.path.exists(p) else ("Not found", 404)


if __name__ == '__main__':
    app.run(debug=False, threaded=True, host='0.0.0.0', port=5000)
