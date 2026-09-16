"""Build a phase-space locator for the q286 raw support-order target.

The current theorem target is pointwise and unnormalized:

    R_raw(N) = B_low_raw(N) - max(0, -T_high_raw(N)) > 0.

This receipt and companion HTML view expose the checked rows as a stress
locator: x=log(N), y=ordered strict-central pair count, z=raw margin, color by
q286 residue, brightness by distance from failure.  It is exploratory finite
evidence only, not an analytic estimate or proof.
"""

from __future__ import annotations

import html
import json
import math
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-residual-support-order-raw-scale-bridge.json"
OUT = EVIDENCE / "q286-residual-support-order-raw-bound-phase-space.json"
HTML_OUT = EVIDENCE / "q286-residual-support-order-raw-bound-phase-space.html"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    values = [float(value) for value in values]
    return {
        "count": len(values),
        "minimum": min(values),
        "mean": math.fsum(values) / len(values),
        "maximum": max(values),
    }


def pearson(xs, ys):
    xs = [float(x) for x in xs]
    ys = [float(y) for y in ys]
    mean_x = math.fsum(xs) / len(xs)
    mean_y = math.fsum(ys) / len(ys)
    x_var = math.fsum((x - mean_x) ** 2 for x in xs)
    y_var = math.fsum((y - mean_y) ** 2 for y in ys)
    if x_var == 0.0 or y_var == 0.0:
        return None
    return math.fsum(
        (x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)
    ) / math.sqrt(x_var * y_var)


def adverse_ratio(row):
    low = float(row["raw_low_order_base"])
    if low <= 0.0:
        return None
    return float(row["raw_adverse_drag"]) / low


def phase_space_row(row, max_margin):
    margin = float(row["raw_pointwise_margin"])
    ratio = adverse_ratio(row)
    return {
        "target": int(row["target"]),
        "x_log_N": math.log(int(row["target"])),
        "y_ordered_central_prime_pair_count": int(
            row["ordered_central_prime_pair_count"]),
        "z_raw_pointwise_margin": margin,
        "color_target_mod_286": int(row["target_mod_286"]),
        "color_target_mod_period": int(row["target_mod_period"]),
        "brightness_distance_from_failure": margin,
        "brightness_normalized_to_horizon": (
            margin / max_margin if max_margin else 0.0),
        "raw_low_order_base": float(row["raw_low_order_base"]),
        "raw_adverse_drag": float(row["raw_adverse_drag"]),
        "raw_high_order_tail": float(row["raw_high_order_tail"]),
        "adverse_drag_ratio_to_low_order": ratio,
        "normalized_pointwise_margin": float(
            row["normalized_pointwise_margin"]),
        "strict_central_total_weight": float(
            row["strict_central_total_weight"]),
        "principal_scale": float(row["principal_scale"]),
        "lift_index": int(row["lift_index"]),
        "base_target": int(row["base_target"]),
        "raw_domination_holds": bool(row["raw_domination_holds"]),
    }


def compact_row(row):
    return {
        "target": int(row["target"]),
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_period": int(row["target_mod_period"]),
        "lift_index": int(row["lift_index"]),
        "ordered_central_prime_pair_count": int(
            row["ordered_central_prime_pair_count"]),
        "strict_central_total_weight": float(
            row["strict_central_total_weight"]),
        "raw_low_order_base": float(row["raw_low_order_base"]),
        "raw_adverse_drag": float(row["raw_adverse_drag"]),
        "raw_high_order_tail": float(row["raw_high_order_tail"]),
        "raw_pointwise_margin": float(row["raw_pointwise_margin"]),
        "normalized_pointwise_margin": float(
            row["normalized_pointwise_margin"]),
        "adverse_drag_ratio_to_low_order": adverse_ratio(row),
    }


def build_receipt():
    raw = load_json(SOURCE)
    rows = raw["rows"]
    max_margin = max(float(row["raw_pointwise_margin"]) for row in rows)
    tight_margin = min(
        rows, key=lambda row: (
            float(row["raw_pointwise_margin"]), int(row["target"])))
    smallest_pair = min(
        rows, key=lambda row: (
            int(row["ordered_central_prime_pair_count"]), int(row["target"])))
    largest_adverse_ratio = max(
        rows, key=lambda row: (
            adverse_ratio(row) if adverse_ratio(row) is not None else -1.0,
            -int(row["target"])))
    largest_abs_tail = max(
        rows, key=lambda row: (
            abs(float(row["raw_high_order_tail"])), -int(row["target"])))

    log_targets = [math.log(int(row["target"])) for row in rows]
    log_margins = [
        math.log(float(row["raw_pointwise_margin"])) for row in rows]
    pair_counts = [
        int(row["ordered_central_prime_pair_count"]) for row in rows]
    log_weights = [
        math.log(float(row["strict_central_total_weight"])) for row in rows]

    phase_rows = [phase_space_row(row, max_margin) for row in rows]
    phase_rows.sort(key=lambda row: row["target"])

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_scale_bridge": str(SOURCE.relative_to(ROOT)),
        },
        "status": "CALIBRATION_raw_bound_phase_space_stress_locator",
        "status_boundary": (
            "finite phase-space stress locator only; no raw lower-bound "
            "theorem, positive-mass theorem, raw pointwise estimate, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "raw_lower_bound_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_pointwise_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "visual_schema": {
            "x": "log(target)",
            "y": "ordered strict-central prime-pair count",
            "z_default": "raw_pointwise_margin",
            "z_alternate": "adverse_drag_ratio_to_low_order",
            "color": "target_mod_286",
            "brightness": "raw_pointwise_margin as distance from failure",
            "animation_candidate": (
                "lift_index or successive target windows"),
            "linked_detail": (
                "target, residues, pair count, total weight, raw low, raw "
                "tail, adverse drag, margins, and scale"),
        },
        "finite_horizon": {
            "finite_evidence_is_acceptance_condition": False,
            "row_count": len(rows),
            "target_minimum": min(int(row["target"]) for row in rows),
            "target_maximum": max(int(row["target"]) for row in rows),
            "positive_raw_margin_rows": sum(
                float(row["raw_pointwise_margin"]) > 0.0 for row in rows),
            "raw_domination_failure_targets": [
                int(row["target"]) for row in rows
                if not row["raw_domination_holds"]],
            "negative_high_order_tail_rows": sum(
                float(row["raw_high_order_tail"]) < 0.0 for row in rows),
            "nonnegative_high_order_tail_rows": sum(
                float(row["raw_high_order_tail"]) >= 0.0 for row in rows),
            "target_mod_286_counts": {
                str(key): value
                for key, value in sorted(Counter(
                    int(row["target_mod_286"]) for row in rows).items())
            },
            "raw_margin_summary": finite_summary(
                row["raw_pointwise_margin"] for row in rows),
            "pair_count_summary": finite_summary(
                row["ordered_central_prime_pair_count"] for row in rows),
            "strict_central_total_weight_summary": finite_summary(
                row["strict_central_total_weight"] for row in rows),
            "adverse_ratio_summary": finite_summary(
                ratio for ratio in (adverse_ratio(row) for row in rows)
                if ratio is not None),
        },
        "stress_rows": {
            "tightest_raw_margin_row": compact_row(tight_margin),
            "smallest_pair_count_row": compact_row(smallest_pair),
            "largest_adverse_ratio_row": compact_row(largest_adverse_ratio),
            "largest_absolute_tail_row": compact_row(largest_abs_tail),
            "ten_tightest_raw_margin_rows": [
                compact_row(row)
                for row in sorted(
                    rows,
                    key=lambda row: (
                        float(row["raw_pointwise_margin"]),
                        int(row["target"])))[:10]
            ],
        },
        "shape_diagnostics": {
            "correlation_log_target_to_log_raw_margin": pearson(
                log_targets, log_margins),
            "correlation_pair_count_to_log_raw_margin": pearson(
                pair_counts, log_margins),
            "correlation_log_total_weight_to_log_raw_margin": pearson(
                log_weights, log_margins),
            "interpretation": (
                "On this finite horizon, raw margin is most tightly aligned "
                "with strict-central total weight.  That is useful for stress "
                "navigation, but it is also the warning: any universal proof "
                "must still create positive support or prove the raw witness "
                "directly, not just fit this correlation."),
        },
        "phase_space_points": phase_rows,
        "html_view": str(HTML_OUT.relative_to(ROOT)),
        "decision": (
            "The raw-bound phase space is a useful stress locator.  The "
            "tightest checked raw margin is target 44168, while the largest "
            "adverse/low-order ratio is target 164926.  The checked rows show "
            "strong finite alignment between raw margin and strict-central "
            "total weight, so the next analytic route should target a "
            "pointwise raw witness lower bound or a structured adverse-ratio "
            "bound in raw scale.  This visual/calibration artifact proves no "
            "universal estimate and is not an acceptance condition."),
    }


def script_json(value):
    return json.dumps(value, sort_keys=True).replace("<", "\\u003c")


def esc(value):
    return html.escape(str(value), quote=True)


def build_view_model(receipt):
    rows = []
    for point in receipt["phase_space_points"]:
        ratio = point["adverse_drag_ratio_to_low_order"]
        detail = dict(point)
        rows.append({
            "target": point["target"],
            "logN": point["x_log_N"],
            "pairCount": point["y_ordered_central_prime_pair_count"],
            "rawMargin": point["z_raw_pointwise_margin"],
            "adverseRatio": ratio if ratio is not None else 0.0,
            "residue286": point["color_target_mod_286"],
            "residuePeriod": point["color_target_mod_period"],
            "lift": point["lift_index"],
            "weight": point["strict_central_total_weight"],
            "rawLow": point["raw_low_order_base"],
            "rawAdverse": point["raw_adverse_drag"],
            "rawTail": point["raw_high_order_tail"],
            "brightness": point["brightness_normalized_to_horizon"],
            "positive": point["raw_domination_holds"],
            "detail": detail,
        })
    rows.sort(key=lambda row: row["target"])
    return {
        "receipt": receipt["status"],
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "generatedFromCommit": source_commit(),
        "decision": receipt["decision"],
        "boundary": receipt["status_boundary"],
        "schema": receipt["visual_schema"],
        "rows": rows,
    }


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>q286 raw-bound phase space</title>
<style>
:root {
  --bg: #f7f8fa;
  --panel: #ffffff;
  --ink: #16202a;
  --muted: #5c6675;
  --line: #d7dee8;
  --accent: #285f8f;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Segoe UI, Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
}
header {
  padding: 18px 22px 12px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}
h1 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 650;
}
.sub {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  max-width: 1180px;
}
main {
  display: grid;
  grid-template-columns: minmax(420px, 1.15fr) minmax(440px, 0.85fr);
  gap: 14px;
  padding: 14px;
}
.panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}
.plot-panel { min-height: 660px; }
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}
.toolbar label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
input[type="range"] { width: 115px; }
.segmented {
  display: inline-flex;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow: hidden;
  background: #f3f5f8;
}
.segmented button {
  border: 0;
  border-right: 1px solid var(--line);
  padding: 5px 9px;
  background: transparent;
  color: var(--muted);
  font: inherit;
  cursor: pointer;
}
.segmented button:last-child { border-right: 0; }
.segmented button.active {
  background: var(--accent);
  color: #fff;
}
#plot {
  display: block;
  width: 100%;
  height: 590px;
  cursor: crosshair;
}
.table-wrap {
  max-height: 335px;
  overflow: auto;
  border-bottom: 1px solid var(--line);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
th, td {
  padding: 7px 8px;
  border-bottom: 1px solid #edf0f5;
  text-align: right;
  white-space: nowrap;
}
th {
  position: sticky;
  top: 0;
  background: #f3f5f8;
  z-index: 1;
  font-weight: 600;
}
td:first-child, th:first-child { text-align: left; }
tr { cursor: pointer; }
tr.selected {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
  background: #eef5ff;
}
.detail { padding: 12px; }
.detail h2 {
  margin: 0 0 8px;
  font-size: 18px;
}
.kv {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 12px;
  margin-bottom: 10px;
  font-size: 12px;
}
.kv div {
  border-bottom: 1px dotted #d2d8e2;
  padding-bottom: 4px;
}
.kv span {
  display: block;
  color: var(--muted);
}
pre {
  margin: 0;
  max-height: 290px;
  overflow: auto;
  padding: 10px;
  background: #101722;
  color: #e8f0ff;
  border-radius: 6px;
  font-size: 11px;
  line-height: 1.45;
}
.footer {
  padding: 8px 12px 12px;
  color: var(--muted);
  font-size: 12px;
}
@media (max-width: 980px) {
  main { grid-template-columns: 1fr; }
  #plot { height: 500px; }
}
</style>
</head>
<body>
<header>
  <h1>q286 Raw-Bound Phase Space</h1>
  <p class="sub">Linked local navigation view. X = log N, Y = ordered strict-central pair count, Z = raw pointwise margin or adverse/low ratio. Color is q286 residue; brightness is distance from failure. This is a stress locator, not proof evidence.</p>
</header>
<main>
  <section class="panel plot-panel">
    <div class="toolbar">
      <label>rotate X <input id="rotX" type="range" min="-80" max="80" value="24"></label>
      <label>rotate Y <input id="rotY" type="range" min="-120" max="120" value="-34"></label>
      <label>zoom <input id="zoom" type="range" min="70" max="170" value="110"></label>
      <div class="segmented" aria-label="z axis mode">
        <button type="button" class="active" data-mode="margin">margin</button>
        <button type="button" data-mode="adverse">adverse ratio</button>
      </div>
      <span id="selectedLabel"></span>
    </div>
    <canvas id="plot"></canvas>
    <div class="footer" id="boundary"></div>
  </section>
  <section class="panel">
    <div class="table-wrap">
      <table id="pointTable">
        <thead>
          <tr>
            <th>N</th><th>mod286</th><th>lift</th><th>pairs</th>
            <th>weight</th><th>low</th><th>adv</th><th>adv/low</th><th>margin</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div class="detail">
      <h2 id="detailTitle">Select a point</h2>
      <div class="kv" id="summary"></div>
      <pre id="rawDetail"></pre>
    </div>
  </section>
</main>
<script id="view-data" type="application/json">__DATA__</script>
<script>
const view = JSON.parse(document.getElementById('view-data').textContent);
const rows = view.rows;
let selected = rows[0]?.target;
let zMode = 'margin';
let projected = [];

const palette = ['#20639b', '#3caea3', '#f6a01a', '#d1495b', '#5f4b8b', '#2f7d32'];
const residues = [...new Set(rows.map(row => row.residue286))].sort((a, b) => a - b);
const residueColor = new Map(residues.map((value, index) => [value, palette[index % palette.length]]));

const canvas = document.getElementById('plot');
const ctx = canvas.getContext('2d');
const tableBody = document.querySelector('#pointTable tbody');
const detailTitle = document.getElementById('detailTitle');
const summary = document.getElementById('summary');
const rawDetail = document.getElementById('rawDetail');
const selectedLabel = document.getElementById('selectedLabel');
document.getElementById('boundary').textContent = view.boundary;

function fmt(value, digits = 6) {
  if (value === null || value === undefined) return '';
  if (typeof value !== 'number') return value;
  if (Math.abs(value) >= 1000000) return value.toExponential(4);
  if (Math.abs(value) >= 1000) return value.toFixed(0);
  return value.toPrecision(digits);
}

function hexToRgb(hex) {
  const value = hex.replace('#', '');
  return [
    parseInt(value.slice(0, 2), 16),
    parseInt(value.slice(2, 4), 16),
    parseInt(value.slice(4, 6), 16),
  ];
}

function zValue(row) {
  return zMode === 'adverse' ? row.adverseRatio : Math.log(row.rawMargin);
}

function zLabel() {
  return zMode === 'adverse'
    ? 'adverse drag / low-order base'
    : 'log raw pointwise margin';
}

function norm(value, min, max) {
  if (Math.abs(max - min) < 1e-12) return 0;
  return (value - min) / (max - min) * 2 - 1;
}

function dims() {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(640, Math.floor(rect.width * dpr));
  canvas.height = Math.max(420, Math.floor(rect.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { w: rect.width, h: rect.height };
}

function rotate(point, ax, ay) {
  let [x, y, z] = point;
  const cx = Math.cos(ax), sx = Math.sin(ax);
  const cy = Math.cos(ay), sy = Math.sin(ay);
  let y1 = y * cx - z * sx;
  let z1 = y * sx + z * cx;
  let x2 = x * cy + z1 * sy;
  let z2 = -x * sy + z1 * cy;
  return [x2, y1, z2];
}

function project(p, w, h, zoom) {
  const scale = Math.min(w, h) * 0.29 * zoom;
  const depth = 2.8;
  const perspective = depth / (depth - p[2] * 0.45);
  return {
    x: w / 2 + p[0] * scale * perspective,
    y: h / 2 - p[1] * scale * perspective,
  };
}

function draw() {
  const { w, h } = dims();
  ctx.clearRect(0, 0, w, h);
  const pad = 72;
  const plotW = w - pad * 2;
  const plotH = h - pad * 2;
  const xs = rows.map(row => row.logN);
  const ys = rows.map(row => Math.log(row.pairCount));
  const zs = rows.map(row => zValue(row));
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const minZ = Math.min(...zs), maxZ = Math.max(...zs);
  const ax = Number(document.getElementById('rotX').value) * Math.PI / 180;
  const ay = Number(document.getElementById('rotY').value) * Math.PI / 180;
  const zoom = Number(document.getElementById('zoom').value) / 100;

  ctx.strokeStyle = '#d2d8e2';
  ctx.lineWidth = 1;
  ctx.strokeRect(pad, pad, plotW, plotH);
  ctx.fillStyle = '#5c6675';
  ctx.font = '12px Segoe UI, Arial';
  ctx.fillText('x log(N)', pad + 8, h - pad + 30);
  ctx.fillText('y log(pair count)', pad + 8, pad - 18);
  ctx.fillText(`z ${zLabel()}`, pad + 8, pad - 2);

  const axes = [
    { a: [-1,-1,-1], b: [1,-1,-1], label: 'log N' },
    { a: [-1,-1,-1], b: [-1,1,-1], label: 'pairs' },
    { a: [-1,-1,-1], b: [-1,-1,1], label: zMode === 'adverse' ? 'adv/low' : 'margin' },
  ];
  for (const axis of axes) {
    const a = rotate(axis.a, ax, ay);
    const b = rotate(axis.b, ax, ay);
    const pa = project(a, w, h, zoom);
    const pb = project(b, w, h, zoom);
    ctx.strokeStyle = '#aeb7c5';
    ctx.beginPath();
    ctx.moveTo(pa.x, pa.y);
    ctx.lineTo(pb.x, pb.y);
    ctx.stroke();
    ctx.fillStyle = '#5c6675';
    ctx.fillText(axis.label, pb.x + 4, pb.y - 4);
  }

  projected = rows.map(row => {
    const p = [
      norm(row.logN, minX, maxX),
      norm(Math.log(row.pairCount), minY, maxY),
      norm(zValue(row), minZ, maxZ)
    ];
    const r = rotate(p, ax, ay);
    const screen = project(r, w, h, zoom);
    const radius = 4 + 10 * row.brightness;
    return { row, x: screen.x, y: screen.y, z: r[2], radius };
  }).sort((a, b) => a.z - b.z);

  for (const item of projected) {
    const row = item.row;
    const [red, green, blue] = hexToRgb(residueColor.get(row.residue286));
    const alpha = 0.35 + 0.65 * row.brightness;
    ctx.beginPath();
    ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${red}, ${green}, ${blue}, ${alpha})`;
    ctx.fill();
    ctx.lineWidth = row.target === selected ? 4 : 1.25;
    ctx.strokeStyle = row.target === selected ? '#16202a' : '#ffffff';
    ctx.stroke();
    if (row.target === selected || row.rawMargin < 1.5e9 || row.adverseRatio > 0.08) {
      ctx.fillStyle = '#16202a';
      ctx.font = row.target === selected ? '700 12px Segoe UI, Arial' : '11px Segoe UI, Arial';
      ctx.fillText(String(row.target), item.x + item.radius + 4, item.y + 4);
    }
  }
}

function renderTable() {
  tableBody.innerHTML = '';
  const sorted = [...rows].sort((a, b) => a.rawMargin - b.rawMargin);
  for (const row of sorted) {
    const tr = document.createElement('tr');
    tr.dataset.target = row.target;
    tr.innerHTML = `
      <td>${row.target}</td>
      <td>${row.residue286}</td>
      <td>${row.lift}</td>
      <td>${row.pairCount}</td>
      <td>${fmt(row.weight)}</td>
      <td>${fmt(row.rawLow)}</td>
      <td>${fmt(row.rawAdverse)}</td>
      <td>${fmt(row.adverseRatio)}</td>
      <td>${fmt(row.rawMargin)}</td>`;
    tr.addEventListener('click', () => select(row.target));
    tableBody.appendChild(tr);
  }
}

function select(target) {
  selected = Number(target);
  for (const tr of tableBody.querySelectorAll('tr')) {
    tr.classList.toggle('selected', Number(tr.dataset.target) === selected);
  }
  const row = rows.find(candidate => candidate.target === selected);
  if (!row) return;
  selectedLabel.textContent = `selected N=${row.target}, mod286=${row.residue286}, margin=${fmt(row.rawMargin)}, adv/low=${fmt(row.adverseRatio)}`;
  detailTitle.textContent = `N = ${row.target}`;
  const items = [
    ['mod period', row.residuePeriod],
    ['lift', row.lift],
    ['log N', fmt(row.logN, 8)],
    ['pair count', row.pairCount],
    ['total weight', fmt(row.weight)],
    ['raw low', fmt(row.rawLow)],
    ['raw adverse', fmt(row.rawAdverse)],
    ['raw tail', fmt(row.rawTail)],
    ['raw margin', fmt(row.rawMargin)],
    ['adverse / low', fmt(row.adverseRatio)],
    ['brightness', fmt(row.brightness)],
    ['source', view.source],
  ];
  summary.innerHTML = items.map(([key, value]) => `<div><span>${key}</span>${value}</div>`).join('');
  rawDetail.textContent = JSON.stringify(row.detail, null, 2);
  draw();
}

canvas.addEventListener('click', event => {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  let best = null;
  for (const item of projected) {
    const distance = Math.hypot(item.x - x, item.y - y);
    if (distance <= item.radius + 8 && (!best || distance < best.distance)) {
      best = { item, distance };
    }
  }
  if (best) select(best.item.row.target);
});

for (const id of ['rotX', 'rotY', 'zoom']) {
  document.getElementById(id).addEventListener('input', draw);
}
for (const button of document.querySelectorAll('[data-mode]')) {
  button.addEventListener('click', () => {
    zMode = button.dataset.mode;
    for (const other of document.querySelectorAll('[data-mode]')) {
      other.classList.toggle('active', other === button);
    }
    draw();
  });
}
window.addEventListener('resize', draw);
renderTable();
select(selected);
</script>
</body>
</html>
"""


def write_html(receipt):
    view_model = build_view_model(receipt)
    HTML_OUT.write_text(
        HTML_TEMPLATE.replace("__DATA__", script_json(view_model)),
        encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_html(receipt)
    print(OUT.relative_to(ROOT))
    print(HTML_OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
