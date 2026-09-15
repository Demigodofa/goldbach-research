"""Build a linked 3D phase-space viewer for the q286 stress receipt.

The HTML is a local navigation aid: canvas scatter, linked table, and exact
row-detail panel all come from the checked JSON receipt.  It is intentionally
dependency-free so it opens directly from the evidence directory.
"""

from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-active-lane-strict-closure-post-discovery-stress.json"
OUT = EVIDENCE / "q286-active-lane-strict-closure-phase-space.html"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def esc(value):
    return html.escape(str(value), quote=True)


def script_json(value):
    """Encode JSON for a non-executable script tag."""
    return json.dumps(value, sort_keys=True).replace("<", "\\u003c")


def build_view_model(receipt):
    rows = []
    points = {
        int(point["target"]): point
        for point in receipt["phase_space_points"]
    }
    for target_text, row in receipt["target_rows"].items():
        target = int(target_text)
        point = points[target]
        maximum_channel = (
            receipt["calibrated_normalized_real_channel_linf_bound"]
            - row["channel_margin_to_calibrated_linf_bound"])
        combined_driver = (
            receipt["calibrated_combined_floor_driver_floor"]
            + row["driver_margin_to_calibrated_floor"])
        detail = dict(row)
        detail["derived_combined_floor_driver_to_principal_ratio"] = (
            combined_driver)
        detail["derived_maximum_normalized_real_channel_sum"] = (
            maximum_channel)
        detail["fixed_conductor_pair"] = point["fixed_conductor_pair"]
        detail["calibrated_constants"] = {
            "combined_floor_driver_floor": receipt[
                "calibrated_combined_floor_driver_floor"],
            "normalized_real_channel_linf_bound": receipt[
                "calibrated_normalized_real_channel_linf_bound"],
            "real_channel_l1_to_principal_mean": receipt[
                "calibrated_real_channel_l1_to_principal_mean"],
        }
        rows.append({
            "target": target,
            "block": row["block_index_after_discovery"],
            "logN": point["x_log_N"],
            "driverMargin": row["driver_margin_to_calibrated_floor"],
            "strictMargin": row[
                "strict_closure_margin_to_calibrated_endpoint"],
            "channelContribution": row[
                "channel_margin_contribution_to_strict_closure"],
            "channelMargin": row["channel_margin_to_calibrated_linf_bound"],
            "maximumNormalizedChannel": maximum_channel,
            "combinedDriver": combined_driver,
            "fullAction": row["full_action_to_principal_ratio"],
            "firstTwo": row["source_first_two_modes_to_principal_ratio"],
            "firstThree": row["source_first_three_modes_to_principal_ratio"],
            "residue286": row["source_target_mod_286"],
            "residue143": row["source_target_mod_143"],
            "residue13": row["source_target_mod_13"],
            "dominant": row["dominant_strict_margin_source"],
            "positive": row["strict_closure_margin_positive"],
            "brightness": point["brightness_normalized_to_sample"],
            "detail": detail,
        })
    rows.sort(key=lambda item: item["block"])
    return {
        "receipt": receipt["receipt"],
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "generatedFromCommit": source_commit(),
        "decision": receipt["decision"],
        "boundary": receipt["status_boundary"],
        "schema": receipt["phase_space_visual_schema"],
        "rows": rows,
    }


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>q286 strict-closure phase space</title>
<style>
:root {{
  --bg: #f7f8fa;
  --panel: #ffffff;
  --ink: #17202a;
  --muted: #596575;
  --line: #d8dee8;
  --fail: #c43c35;
  --pass: #1d7f58;
  --accent: #335c99;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: Segoe UI, Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
}}
header {{
  padding: 18px 22px 12px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}}
h1 {{
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 650;
}}
.sub {{
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  max-width: 1180px;
}}
main {{
  display: grid;
  grid-template-columns: minmax(420px, 1.15fr) minmax(440px, 0.85fr);
  gap: 14px;
  padding: 14px;
}}
.panel {{
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}}
.plot-panel {{
  min-height: 660px;
}}
.toolbar {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}}
.toolbar label {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}
input[type="range"] {{ width: 115px; }}
#plot {{
  display: block;
  width: 100%;
  height: 590px;
  cursor: crosshair;
}}
.table-wrap {{
  max-height: 335px;
  overflow: auto;
  border-bottom: 1px solid var(--line);
}}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}}
th, td {{
  padding: 7px 8px;
  border-bottom: 1px solid #edf0f5;
  text-align: right;
  white-space: nowrap;
}}
th {{
  position: sticky;
  top: 0;
  background: #f3f5f8;
  z-index: 1;
  font-weight: 600;
}}
td:first-child, th:first-child {{
  text-align: left;
}}
tr {{
  cursor: pointer;
}}
tr.selected {{
  outline: 2px solid var(--accent);
  outline-offset: -2px;
  background: #eef5ff;
}}
.pill {{
  display: inline-block;
  min-width: 44px;
  padding: 2px 6px;
  border-radius: 999px;
  color: #fff;
  text-align: center;
  font-weight: 600;
}}
.pass {{ background: var(--pass); }}
.fail {{ background: var(--fail); }}
.detail {{
  padding: 12px;
}}
.detail h2 {{
  margin: 0 0 8px;
  font-size: 18px;
}}
.kv {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 12px;
  margin-bottom: 10px;
  font-size: 12px;
}}
.kv div {{
  border-bottom: 1px dotted #d2d8e2;
  padding-bottom: 4px;
}}
.kv span {{
  display: block;
  color: var(--muted);
}}
pre {{
  margin: 0;
  max-height: 290px;
  overflow: auto;
  padding: 10px;
  background: #101722;
  color: #e8f0ff;
  border-radius: 6px;
  font-size: 11px;
  line-height: 1.45;
}}
.footer {{
  padding: 8px 12px 12px;
  color: var(--muted);
  font-size: 12px;
}}
@media (max-width: 980px) {{
  main {{ grid-template-columns: 1fr; }}
  #plot {{ height: 500px; }}
}}
</style>
</head>
<body>
<header>
  <h1>q286 Strict-Closure Phase Space</h1>
  <p class="sub">Linked local navigation view. X = log N, Y = driver margin, Z = strict closure margin. Color is pass/fail with residue labels; brightness is distance from the zero boundary. This is a falsifier locator, not proof evidence.</p>
</header>
<main>
  <section class="panel plot-panel">
    <div class="toolbar">
      <label>rotate X <input id="rotX" type="range" min="-80" max="80" value="22"></label>
      <label>rotate Y <input id="rotY" type="range" min="-120" max="120" value="-36"></label>
      <label>zoom <input id="zoom" type="range" min="70" max="160" value="108"></label>
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
            <th>N</th><th>block</th><th>status</th><th>mod286</th>
            <th>driver</th><th>channel</th><th>strict</th><th>full</th>
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
<script id="view-data" type="application/json">{DATA}</script>
<script>
const view = JSON.parse(document.getElementById('view-data').textContent);
const rows = view.rows;
let selected = rows[0]?.target;
let projected = [];

const canvas = document.getElementById('plot');
const ctx = canvas.getContext('2d');
const tableBody = document.querySelector('#pointTable tbody');
const detailTitle = document.getElementById('detailTitle');
const summary = document.getElementById('summary');
const rawDetail = document.getElementById('rawDetail');
const selectedLabel = document.getElementById('selectedLabel');
document.getElementById('boundary').textContent = view.boundary;

function fmt(value, digits = 6) {{
  if (typeof value !== 'number') return value;
  if (Math.abs(value) >= 1000) return value.toFixed(0);
  return value.toPrecision(digits);
}}

function norm(value, min, max) {{
  if (Math.abs(max - min) < 1e-12) return 0;
  return (value - min) / (max - min) * 2 - 1;
}}

function dims() {{
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(640, Math.floor(rect.width * dpr));
  canvas.height = Math.max(420, Math.floor(rect.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return {{ w: rect.width, h: rect.height }};
}}

function rotate(point, ax, ay) {{
  let [x, y, z] = point;
  const cx = Math.cos(ax), sx = Math.sin(ax);
  const cy = Math.cos(ay), sy = Math.sin(ay);
  let y1 = y * cx - z * sx;
  let z1 = y * sx + z * cx;
  let x2 = x * cy + z1 * sy;
  let z2 = -x * sy + z1 * cy;
  return [x2, y1, z2];
}}

function draw() {{
  const {{ w, h }} = dims();
  ctx.clearRect(0, 0, w, h);
  const pad = 72;
  const plotW = w - pad * 2;
  const plotH = h - pad * 2;
  const xs = rows.map(r => r.logN);
  const ys = rows.map(r => r.driverMargin);
  const zs = rows.map(r => r.strictMargin);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const minZ = Math.min(...zs), maxZ = Math.max(...zs);
  const ax = Number(document.getElementById('rotX').value) * Math.PI / 180;
  const ay = Number(document.getElementById('rotY').value) * Math.PI / 180;
  const zoom = Number(document.getElementById('zoom').value) / 100;

  ctx.strokeStyle = '#d2d8e2';
  ctx.lineWidth = 1;
  ctx.strokeRect(pad, pad, plotW, plotH);
  ctx.fillStyle = '#596575';
  ctx.font = '12px Segoe UI, Arial';
  ctx.fillText('x log(N)', pad + 8, h - pad + 30);
  ctx.fillText('y driver margin', pad + 8, pad - 18);
  ctx.fillText('z strict margin: red below zero, green above', pad + 8, pad - 2);

  const axes = [
    {{ a: [-1,-1,-1], b: [1,-1,-1], label: 'log N' }},
    {{ a: [-1,-1,-1], b: [-1,1,-1], label: 'driver' }},
    {{ a: [-1,-1,-1], b: [-1,-1,1], label: 'strict' }},
  ];
  for (const axis of axes) {{
    const a = rotate(axis.a, ax, ay);
    const b = rotate(axis.b, ax, ay);
    const pa = project(a, w, h, zoom);
    const pb = project(b, w, h, zoom);
    ctx.strokeStyle = '#aeb7c5';
    ctx.beginPath();
    ctx.moveTo(pa.x, pa.y);
    ctx.lineTo(pb.x, pb.y);
    ctx.stroke();
    ctx.fillStyle = '#596575';
    ctx.fillText(axis.label, pb.x + 4, pb.y - 4);
  }}

  projected = rows.map(row => {{
    const p = [
      norm(row.logN, minX, maxX),
      norm(row.driverMargin, minY, maxY),
      norm(row.strictMargin, minZ, maxZ)
    ];
    const r = rotate(p, ax, ay);
    const screen = project(r, w, h, zoom);
    const radius = 7 + 8 * row.brightness;
    return {{ row, x: screen.x, y: screen.y, z: r[2], radius }};
  }}).sort((a, b) => a.z - b.z);

  for (const item of projected) {{
    const row = item.row;
    const alpha = 0.55 + 0.45 * row.brightness;
    ctx.beginPath();
    ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);
    ctx.fillStyle = row.positive
      ? `rgba(29, 127, 88, ${{alpha}})`
      : `rgba(196, 60, 53, ${{alpha}})`;
    ctx.fill();
    ctx.lineWidth = row.target === selected ? 4 : 1.5;
    ctx.strokeStyle = row.target === selected ? '#17202a' : '#ffffff';
    ctx.stroke();
    ctx.fillStyle = '#17202a';
    ctx.font = row.target === selected ? '700 12px Segoe UI, Arial' : '11px Segoe UI, Arial';
    ctx.fillText(String(row.target), item.x + item.radius + 4, item.y + 4);
  }}
}}

function project(p, w, h, zoom) {{
  const scale = Math.min(w, h) * 0.29 * zoom;
  const depth = 2.8;
  const perspective = depth / (depth - p[2] * 0.45);
  return {{
    x: w / 2 + p[0] * scale * perspective,
    y: h / 2 - p[1] * scale * perspective,
  }};
}}

function renderTable() {{
  tableBody.innerHTML = '';
  for (const row of rows) {{
    const tr = document.createElement('tr');
    tr.dataset.target = row.target;
    tr.innerHTML = `
      <td>${{row.target}}</td>
      <td>${{row.block}}</td>
      <td><span class="pill ${{row.positive ? 'pass' : 'fail'}}">${{row.positive ? 'pass' : 'fail'}}</span></td>
      <td>${{row.residue286}}</td>
      <td>${{fmt(row.driverMargin)}}</td>
      <td>${{fmt(row.channelContribution)}}</td>
      <td>${{fmt(row.strictMargin)}}</td>
      <td>${{fmt(row.fullAction)}}</td>`;
    tr.addEventListener('click', () => select(row.target));
    tableBody.appendChild(tr);
  }}
}}

function select(target) {{
  selected = Number(target);
  for (const tr of tableBody.querySelectorAll('tr')) {{
    tr.classList.toggle('selected', Number(tr.dataset.target) === selected);
  }}
  const row = rows.find(r => r.target === selected);
  if (!row) return;
  selectedLabel.textContent = `selected N=${{row.target}}, mod286=${{row.residue286}}, strict=${{fmt(row.strictMargin)}}`;
  detailTitle.textContent = `N = ${{row.target}}`;
  const items = [
    ['block', row.block],
    ['residues', `mod13=${{row.residue13}}, mod143=${{row.residue143}}, mod286=${{row.residue286}}`],
    ['log N', fmt(row.logN, 8)],
    ['status', row.positive ? 'strict endpoint positive' : 'strict endpoint falsifier'],
    ['first two', fmt(row.firstTwo)],
    ['first three', fmt(row.firstThree)],
    ['driver margin', fmt(row.driverMargin)],
    ['channel contribution', fmt(row.channelContribution)],
    ['channel margin', fmt(row.channelMargin)],
    ['max normalized channel', fmt(row.maximumNormalizedChannel)],
    ['strict margin', fmt(row.strictMargin)],
    ['full action', fmt(row.fullAction)],
    ['dominant source', row.dominant],
    ['fixed conductors', row.detail.fixed_conductor_pair.join(', ')],
  ];
  summary.innerHTML = items.map(([k, v]) => `<div><span>${{k}}</span>${{v}}</div>`).join('');
  rawDetail.textContent = JSON.stringify(row.detail, null, 2);
  draw();
}}

canvas.addEventListener('click', event => {{
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  let best = null;
  for (const item of projected) {{
    const d = Math.hypot(item.x - x, item.y - y);
    if (d <= item.radius + 8 && (!best || d < best.d)) best = {{ item, d }};
  }}
  if (best) select(best.item.row.target);
}});

for (const id of ['rotX', 'rotY', 'zoom']) {{
  document.getElementById(id).addEventListener('input', draw);
}}
window.addEventListener('resize', draw);
renderTable();
select(selected);
</script>
</body>
</html>
"""


def main():
    view_model = build_view_model(load_json(SOURCE))
    html_text = HTML_TEMPLATE.format(DATA=script_json(view_model))
    OUT.write_text(html_text, encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
