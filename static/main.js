// ===== FIRE DETECTION DASHBOARD — ENHANCED JS =====

// ---- Camera Toggle ----
let cameraRunning = false;

async function toggleCamera() {
  const btn = document.getElementById('cam-toggle-btn');
  const feed = document.getElementById('live-feed');
  const placeholder = document.getElementById('cam-placeholder');
  const dot = document.getElementById('live-dot');
  const statusTxt = document.getElementById('live-status-text');
  const snapBtn = document.getElementById('snap-btn');

  btn.disabled = true;

  if (!cameraRunning) {
    // --- START ---
    const res = await fetch('/start_camera', { method: 'POST' }).then(r => r.json()).catch(() => null);
    if (res && res.ok) {
      cameraRunning = true;
      feed.src = '/video_feed';
      feed.style.display = 'block';
      placeholder.style.display = 'none';
      btn.textContent = '⏹ Stop Camera';
      btn.classList.add('btn-cam-stop');
      dot.style.background = '#ef4444';   // red = live
      statusTxt.textContent = 'LIVE';
      statusTxt.style.color = '#ef4444';
      snapBtn.disabled = false;
    }
  } else {
    // --- STOP ---
    feed.src = '';   // disconnect the MJPEG stream
    feed.style.display = 'none';
    placeholder.style.display = 'flex';
    const res = await fetch('/stop_camera', { method: 'POST' }).then(r => r.json()).catch(() => null);
    cameraRunning = false;
    btn.textContent = '▶ Start Camera';
    btn.classList.remove('btn-cam-stop');
    dot.style.background = '#555';        // grey = off
    statusTxt.textContent = 'CAMERA OFF';
    statusTxt.style.color = '#888';
    snapBtn.disabled = true;
    document.getElementById('snap-result').textContent = '';
  }

  btn.disabled = false;
}

// ---- Sound Alert (Web Audio API) ----
let soundEnabled = true;
let alarmPlaying = false;

function playAlarm() {
  if (!soundEnabled || alarmPlaying) return;
  alarmPlaying = true;
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const beep = (freq, start, dur) => {
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.connect(g); g.connect(ctx.destination);
    o.frequency.value = freq;
    o.type = 'square';
    g.gain.setValueAtTime(0.3, ctx.currentTime + start);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + dur);
    o.start(ctx.currentTime + start);
    o.stop(ctx.currentTime + start + dur + 0.05);
  };
  // Three-beep siren pattern
  [0, 0.4, 0.8].forEach(t => { beep(880, t, 0.3); beep(660, t + 0.15, 0.15); });
  setTimeout(() => { alarmPlaying = false; }, 1500);
}

// ---- Tab Switching ----
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(target).classList.add('active');
  });
});

// ---- Alert Banner ----
let manualClose = false;
const alertBanner = document.getElementById('alert-banner');
const alertText = document.getElementById('alert-text');
document.getElementById('alert-close').addEventListener('click', () => {
  alertBanner.classList.remove('visible');
  manualClose = true;
});

// ---- Circular Ring ----
const CIRCUMFERENCE = 2 * Math.PI * 45; // r=45
const ringFill = document.getElementById('ring-fill');
const ringLabel = document.getElementById('ring-label');
ringFill.style.strokeDasharray = CIRCUMFERENCE;
ringFill.style.strokeDashoffset = CIRCUMFERENCE;

// ---- Alert Polling ----
async function pollAlert() {
  try {
    const data = await fetch('/alert_status').then(r => r.json());
    const pct = Math.min(data.seconds / data.threshold, 1);
    ringFill.style.strokeDashoffset = CIRCUMFERENCE - pct * CIRCUMFERENCE;
    ringLabel.textContent = `${data.seconds.toFixed(1)}s`;
    document.getElementById('ring-threshold').textContent = `Alert at ${data.threshold}s`;
    document.getElementById('logic-seconds').textContent = data.threshold;

    if (data.active && !manualClose) {
      alertBanner.classList.add('visible');
      alertText.textContent = `⚠️ TRUE FIRE ALERT — ${(data.detected_class || '').toUpperCase()} confirmed for ${data.seconds.toFixed(0)}s!`;
      playAlarm();
    } else if (!data.active) {
      alertBanner.classList.remove('visible');
      manualClose = false;
    }
  } catch (e) { }
}
setInterval(pollAlert, 500);

// ---- Stats Polling ----
async function pollStats() {
  try {
    const d = await fetch('/get_stats').then(r => r.json());
    document.getElementById('h-uptime').textContent = d.uptime;
    document.getElementById('h-frames').textContent = d.frames_analyzed.toLocaleString();
    document.getElementById('h-fire').textContent = d.fire_count;
    document.getElementById('h-smoke').textContent = d.smoke_count;
    document.getElementById('h-alerts').textContent = d.alerts_triggered;
  } catch (e) { }
}
setInterval(pollStats, 2000);

// ---- Mini Log (Live tab) ----
async function pollMiniLog() {
  try {
    const entries = await fetch('/get_log').then(r => r.json());
    const el = document.getElementById('mini-log');
    if (!entries.length) return;
    el.innerHTML = entries.slice(0, 8).map(e => `
      <div class="log-entry">
        <span class="log-badge badge-${e.cls}">${e.cls.toUpperCase()}</span>
        <span class="log-source">${e.source}</span>
        <span class="log-conf">${e.conf}%</span>
        <span class="log-time">${e.time}</span>
      </div>`).join('');
  } catch (e) { }
}
setInterval(pollMiniLog, 1000);

// ---- Full Log Table (Dashboard tab) ----
async function pollFullLog() {
  try {
    const entries = await fetch('/get_log').then(r => r.json());
    const tbody = document.getElementById('log-tbody');
    if (!entries.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="log-empty">No detections yet</td></tr>';
      return;
    }
    tbody.innerHTML = entries.map(e => `
      <tr>
        <td>${e.time}</td>
        <td><span class="src-badge">${e.source}</span></td>
        <td><span class="log-badge badge-${e.cls}">${e.cls}</span></td>
        <td><div class="conf-bar-wrap"><div class="conf-bar" style="width:${e.conf}%"></div><span>${e.conf}%</span></div></td>
      </tr>`).join('');
  } catch (e) { }
}
setInterval(pollFullLog, 2000);

// ---- Alert History ----
async function pollAlertHistory() {
  try {
    const entries = await fetch('/get_alert_history').then(r => r.json());
    const el = document.getElementById('alert-history');
    document.getElementById('alert-count-badge').textContent = `${entries.length} alert${entries.length !== 1 ? 's' : ''}`;
    if (!entries.length) {
      el.innerHTML = '<div class="log-empty">No alerts triggered yet.</div>';
      return;
    }
    el.innerHTML = entries.map(e => `
      <div class="alert-history-item">
        <div class="ah-icon">🚨</div>
        <div class="ah-info">
          <div class="ah-time">${e.time}</div>
          <div class="ah-detail">${(e.cls || '').toUpperCase()} detected for <strong>${e.duration}s</strong></div>
        </div>
        ${e.snapshot ? `<a href="/get_snapshot?path=${encodeURIComponent(e.snapshot)}" target="_blank" class="ah-snap-link">📸 View</a>` : ''}
      </div>`).join('');
  } catch (e) { }
}
setInterval(pollAlertHistory, 3000);

// ---- Charts ----
const confCtx = document.getElementById('conf-chart').getContext('2d');
const confChart = new Chart(confCtx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label: '🔥 Fire', data: [], borderColor: '#ff4500', backgroundColor: 'rgba(255,69,0,0.1)', tension: 0.4, fill: true, pointRadius: 2 },
      { label: '💨 Smoke', data: [], borderColor: '#9ca3af', backgroundColor: 'rgba(156,163,175,0.1)', tension: 0.4, fill: true, pointRadius: 2 }
    ]
  },
  options: {
    animation: false,
    responsive: true,
    plugins: { legend: { labels: { color: '#94a3b8' } } },
    scales: {
      x: { ticks: { color: '#94a3b8', maxTicksLimit: 8 }, grid: { color: 'rgba(255,255,255,0.05)' } },
      y: { min: 0, max: 100, ticks: { color: '#94a3b8', callback: v => v + '%' }, grid: { color: 'rgba(255,255,255,0.05)' } }
    }
  }
});

const bdCtx = document.getElementById('breakdown-chart').getContext('2d');
const bdChart = new Chart(bdCtx, {
  type: 'doughnut',
  data: {
    labels: ['🔥 Fire', '💨 Smoke'],
    datasets: [{
      data: [0, 0], backgroundColor: ['rgba(255,69,0,0.8)', 'rgba(156,163,175,0.8)'],
      borderColor: ['#ff4500', '#9ca3af'], borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { labels: { color: '#94a3b8' } } }
  }
});

async function pollCharts() {
  try {
    const pts = await fetch('/get_chart_data').then(r => r.json());
    const stats = await fetch('/get_stats').then(r => r.json());
    // Confidence line chart
    confChart.data.labels = pts.map(p => p.ts);
    confChart.data.datasets[0].data = pts.map(p => p.fire);
    confChart.data.datasets[1].data = pts.map(p => p.smoke);
    confChart.update('none');
    // Doughnut
    bdChart.data.datasets[0].data = [stats.fire_count, stats.smoke_count];
    bdChart.update('none');
  } catch (e) { }
}
setInterval(pollCharts, 2000);

// ---- Manual Snapshot ----
document.getElementById('snap-btn').addEventListener('click', async () => {
  const btn = document.getElementById('snap-btn');
  btn.disabled = true; btn.textContent = '⏳ Capturing...';
  try {
    const data = await fetch('/snapshot').then(r => r.json());
    const el = document.getElementById('snap-result');
    if (data.error) { el.textContent = '❌ ' + data.error; return; }
    const pills = data.detections.map(d =>
      `<span class="detection-pill pill-${d.cls}">${d.cls} ${d.conf}%</span>`).join('') || 'No detection';
    el.innerHTML = `<a href="/get_snapshot?path=${encodeURIComponent(data.path)}" target="_blank" class="snap-preview-link">📸 View snapshot</a> ${pills}`;
  } catch (e) { document.getElementById('snap-result').textContent = '❌ Failed'; }
  btn.disabled = false; btn.textContent = '📸 Snapshot';
});

// ---- Image Upload ----
const imageInput = document.getElementById('image-input');
const imageResult = document.getElementById('image-result');
const imageLoading = document.getElementById('image-loading');
const imageBtn = document.getElementById('image-btn');

imageInput.addEventListener('change', () => {
  if (imageInput.files[0]) {
    document.getElementById('image-preview').textContent = `📁 ${imageInput.files[0].name}`;
    imageBtn.disabled = false;
  }
});

imageBtn.addEventListener('click', async () => {
  imageResult.classList.remove('show');
  imageLoading.classList.add('show');
  imageBtn.disabled = true;
  const fd = new FormData();
  fd.append('file', imageInput.files[0]);
  try {
    const data = await fetch('/upload_image', { method: 'POST', body: fd }).then(r => r.json());
    imageLoading.classList.remove('show');
    if (data.error) { alert(data.error); imageBtn.disabled = false; return; }
    if (data.annotated_image)
      document.getElementById('result-img').src = `/get_image?path=${encodeURIComponent(data.annotated_image)}&t=${Date.now()}`;
    document.getElementById('detection-pills').innerHTML = data.detections.length
      ? data.detections.map(d => `<span class="detection-pill pill-${d.class}">${d.class === 'fire' ? '🔥' : '💨'} ${d.class} — ${d.confidence}%</span>`).join('')
      : '<p style="color:var(--text-muted)">No fire or smoke detected.</p>';
    imageResult.classList.add('show');
  } catch (e) { imageLoading.classList.remove('show'); alert('Upload failed'); }
  imageBtn.disabled = false;
});

// ---- Video Upload ----
const videoInput = document.getElementById('video-input');
const videoResult = document.getElementById('video-result');
const videoLoading = document.getElementById('video-loading');
const videoBtn = document.getElementById('video-btn');

videoInput.addEventListener('change', () => {
  if (videoInput.files[0]) {
    document.getElementById('video-preview').textContent = `📁 ${videoInput.files[0].name}`;
    videoBtn.disabled = false;
  }
});

videoBtn.addEventListener('click', async () => {
  videoResult.classList.remove('show');
  videoLoading.classList.add('show');
  videoBtn.disabled = true;
  const fd = new FormData();
  fd.append('file', videoInput.files[0]);
  try {
    const data = await fetch('/upload_video', { method: 'POST', body: fd }).then(r => r.json());
    videoLoading.classList.remove('show');
    if (data.error) { alert(data.error); videoBtn.disabled = false; return; }
    document.getElementById('stat-frames').textContent = data.total_frames;
    document.getElementById('stat-total').textContent = data.total_detections;
    document.getElementById('stat-fire').textContent = data.fire_count;
    document.getElementById('stat-smoke').textContent = data.smoke_count;
    document.getElementById('stat-conf').textContent = `${data.avg_confidence}%`;
    const dl = document.getElementById('video-download');
    dl.style.display = 'inline-flex'; dl.href = '/get_video';
    videoResult.classList.add('show');
  } catch (e) { videoLoading.classList.remove('show'); alert('Upload failed'); }
  videoBtn.disabled = false;
});

// ---- Drag & Drop ----
document.querySelectorAll('.upload-area').forEach(area => {
  area.addEventListener('dragover', e => { e.preventDefault(); area.classList.add('drag-over'); });
  area.addEventListener('dragleave', () => area.classList.remove('drag-over'));
  area.addEventListener('drop', e => {
    e.preventDefault(); area.classList.remove('drag-over');
    const inp = area.querySelector('input[type="file"]');
    if (inp) { inp.files = e.dataTransfer.files; inp.dispatchEvent(new Event('change')); }
  });
});

// ---- Settings ----
const confSlider = document.getElementById('conf-slider');
const alertSlider = document.getElementById('alert-slider');
confSlider.addEventListener('input', () => document.getElementById('conf-val').textContent = confSlider.value);
alertSlider.addEventListener('input', () => document.getElementById('alert-val').textContent = alertSlider.value + 's');
document.getElementById('sound-toggle').addEventListener('change', e => { soundEnabled = e.target.checked; });

// Load current settings on start
fetch('/get_settings').then(r => r.json()).then(s => {
  confSlider.value = s.conf; document.getElementById('conf-val').textContent = s.conf;
  alertSlider.value = s.alert_seconds; document.getElementById('alert-val').textContent = s.alert_seconds + 's';
  document.getElementById('camera-select').value = s.camera_id;
  // Sync model selector
  if (s.active_model) {
    document.getElementById('model-select').value = s.active_model;
  }
  if (s.model_label) {
    document.getElementById('header-model-badge').textContent = 'Model: ' + s.model_label;
  }
}).catch(() => { });

// ---- Model Switcher ----
const modelSelect = document.getElementById('model-select');
const modelStatus = document.getElementById('model-switch-status');

modelSelect.addEventListener('change', async () => {
  const key = modelSelect.value;
  modelStatus.textContent = '⏳ Loading model...';
  modelStatus.style.color = '#fbbf24';
  try {
    const data = await fetch('/switch_model', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: key })
    }).then(r => r.json());

    if (data.ok) {
      modelStatus.textContent = `✅ Active: ${data.label}`;
      modelStatus.style.color = '#22c55e';
      document.getElementById('header-model-badge').textContent = 'Model: ' + data.label;
      // brief toast in settings-saved div
      const msg = document.getElementById('settings-saved');
      msg.textContent = `🤖 Model switched to: ${data.label}`;
      setTimeout(() => { msg.textContent = ''; }, 3000);
    } else {
      modelStatus.textContent = `❌ Error: ${data.error || 'Unknown'}`;
      modelStatus.style.color = '#ef4444';
    }
  } catch (e) {
    modelStatus.textContent = '❌ Network error';
    modelStatus.style.color = '#ef4444';
  }
  setTimeout(() => { modelStatus.textContent = ''; }, 5000);
});


document.getElementById('save-settings').addEventListener('click', async () => {
  const body = {
    conf: parseFloat(confSlider.value),
    alert_seconds: parseInt(alertSlider.value),
    camera_id: parseInt(document.getElementById('camera-select').value),
  };
  try {
    await fetch('/update_settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const msg = document.getElementById('settings-saved');
    msg.textContent = '✅ Settings saved!';
    setTimeout(() => { msg.textContent = ''; }, 2000);
  } catch (e) { alert('Failed to save settings'); }
});
