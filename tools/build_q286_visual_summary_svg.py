"""Render a compact SVG summary of the q286 visual evidence layers.

The SVG is a navigation aid.  It superimposes selected PCA positions,
role-based shapes, glow/heat, and component-vector arrows from generated JSON
receipts.  It is not a proof artifact.
"""

from __future__ import annotations

import html
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"

WIDTH = 1200
HEIGHT = 880


def load_json(path: Path):
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


def scale(value, source_min, source_max, target_min, target_max):
    if abs(source_max - source_min) < 1e-12:
        return (target_min + target_max) / 2.0
    fraction = (value - source_min) / (source_max - source_min)
    return target_min + fraction * (target_max - target_min)


def role_style(role):
    return {
        "boundary_failure": {"fill": "#d95f02", "stroke": "#7f2704"},
        "late_active_success": {"fill": "#1b9e77", "stroke": "#00441b"},
        "alignment_stress_success": {"fill": "#7570b3", "stroke": "#3f007d"},
    }.get(role, {"fill": "#666666", "stroke": "#222222"})


def point_shape(cx, cy, radius, shape, style, title):
    fill = style["fill"]
    stroke = style["stroke"]
    title_el = f"<title>{esc(title)}</title>"
    if shape == "down_triangle":
        points = [
            (cx, cy + radius),
            (cx - radius * 0.95, cy - radius * 0.65),
            (cx + radius * 0.95, cy - radius * 0.65),
        ]
        point_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        return (
            f'<polygon points="{point_text}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5" opacity="0.88">{title_el}</polygon>')
    if shape == "diamond":
        points = [
            (cx, cy - radius),
            (cx + radius, cy),
            (cx, cy + radius),
            (cx - radius, cy),
        ]
        point_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        return (
            f'<polygon points="{point_text}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5" opacity="0.88">{title_el}</polygon>')
    return (
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" '
        f'opacity="0.88">{title_el}</circle>')


def line(x1, y1, x2, y2, stroke="#777", width=1, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{stroke}" stroke-width="{width}"{dash_attr}/>')


def text(x, y, value, size=12, weight="400", anchor="start", fill="#222"):
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" '
        f'font-family="Arial, sans-serif" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}">{esc(value)}</text>')


def rect(x, y, width, height, fill="#f8f8f8", stroke="#ccc", opacity=1.0):
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" '
        f'height="{height:.2f}" fill="{fill}" stroke="{stroke}" '
        f'opacity="{opacity}"/>')


def render_scatter(pca, overlay):
    rows = pca["component_dataset"]["rows"]
    overlay_rows = overlay["target_rows"]
    x_values = [row["pc1"] for row in rows]
    y_values = [row["pc2"] for row in rows]
    x0, y0, w, h = 55, 95, 500, 360
    pad = 32
    xmin, xmax = min(x_values), max(x_values)
    ymin, ymax = min(y_values), max(y_values)
    pieces = [
        rect(x0, y0, w, h, "#ffffff", "#bbbbbb"),
        text(x0, y0 - 16, "Selected component PCA / SVD", 17, "500"),
        text(x0, y0 + h + 32, "PC1: boundary vs late component split", 12),
        text(x0 - 34, y0 + 16, "PC2", 12),
        line(x0 + pad, y0 + h - pad, x0 + w - pad, y0 + h - pad, "#999"),
        line(x0 + pad, y0 + pad, x0 + pad, y0 + h - pad, "#999"),
    ]
    zero_x = scale(0.0, xmin, xmax, x0 + pad, x0 + w - pad)
    zero_y = scale(0.0, ymin, ymax, y0 + h - pad, y0 + pad)
    pieces.append(line(zero_x, y0 + pad, zero_x, y0 + h - pad, "#cccccc", 1, "4 4"))
    pieces.append(line(x0 + pad, zero_y, x0 + w - pad, zero_y, "#cccccc", 1, "4 4"))
    for row in rows:
        target = str(row["target"])
        overlay_row = overlay_rows[target]
        cx = scale(row["pc1"], xmin, xmax, x0 + pad, x0 + w - pad)
        cy = scale(row["pc2"], ymin, ymax, y0 + h - pad, y0 + pad)
        radius = 7 + 8 * float(overlay_row.get("glow", 0.0))
        style = role_style(row["role"])
        title = (
            f"target {target}; role {row['role']}; "
            f"pc1 {row['pc1']:.3f}; pc2 {row['pc2']:.3f}; "
            f"glow {overlay_row.get('glow', 0.0):.3f}")
        pieces.append(point_shape(
            cx, cy, radius, overlay_row["shape"], style, title))
        pieces.append(text(cx + radius + 3, cy + 4, target, 11))
        actions = overlay_row.get("component_actions")
        if actions:
            dx = actions["(5,7)_centered"] * 170
            dy = -actions["(7,11)_centered"] * 170
            pieces.append(line(cx, cy, cx + dx, cy + dy, style["stroke"], 1.3))
            pieces.append(
                f'<circle cx="{cx + dx:.2f}" cy="{cy + dy:.2f}" r="2.4" '
                f'fill="{style["stroke"]}"/>')
    legend_y = y0 + h + 56
    legend_items = [
        ("down_triangle", "boundary failure", "boundary_failure"),
        ("circle", "late active success", "late_active_success"),
        ("diamond", "alignment stress success", "alignment_stress_success"),
    ]
    lx = x0
    for shape, label, role in legend_items:
        pieces.append(point_shape(
            lx + 10, legend_y - 5, 7, shape, role_style(role), label))
        pieces.append(text(lx + 24, legend_y, label, 11))
        lx += 160
    return pieces


def render_alignment_plot(pca, overlay):
    rows = pca["alignment_dataset"]["rows"]
    overlay_rows = overlay["target_rows"]
    x0, y0, w, h = 635, 95, 500, 250
    pieces = [
        rect(x0, y0, w, h, "#ffffff", "#bbbbbb"),
        text(x0, y0 - 16, "Alignment/complement selected PCA", 17, "500"),
        text(x0, y0 + h + 32, "PC1: certificate margin vs discrepancy size", 12),
    ]
    x_values = [row["pc1"] for row in rows]
    y_values = [row["pc2"] for row in rows]
    xmin, xmax = min(x_values), max(x_values)
    ymin, ymax = min(y_values), max(y_values)
    pad = 32
    pieces.append(line(x0 + pad, y0 + h - pad, x0 + w - pad, y0 + h - pad, "#999"))
    pieces.append(line(x0 + pad, y0 + pad, x0 + pad, y0 + h - pad, "#999"))
    for row in rows:
        target = str(row["target"])
        overlay_row = overlay_rows[target]
        cx = scale(row["pc1"], xmin, xmax, x0 + pad, x0 + w - pad)
        cy = scale(row["pc2"], ymin, ymax, y0 + h - pad, y0 + pad)
        radius = 5 + 7 * float(overlay_row.get("glow", 0.0))
        style = role_style(row["role"])
        pieces.append(point_shape(
            cx, cy, radius, overlay_row["shape"], style,
            f"target {target}; alignment PC1 {row['pc1']:.3f}; PC2 {row['pc2']:.3f}"))
        pieces.append(text(cx + radius + 2, cy + 4, target, 10))
    return pieces


def render_stack_bars(glow):
    x0, y0 = 635, 394
    pieces = [text(x0, y0 - 18, "Heat stacks: targets / mechanisms / theorem gaps", 17, "500")]

    sections = [
        ("Targets", glow["target_stacks"][:8], "#d95f02"),
        ("Mechanisms", glow["mechanism_stacks"][:5], "#1b9e77"),
        ("Theorem gaps", glow["theorem_gap_stacks"][:5], "#7570b3"),
    ]
    max_weight = max(
        row["stack_weight"]
        for _label, rows, _color in sections
        for row in rows)
    bar_h = 13
    y = y0
    for label, rows, color in sections:
        pieces.append(text(x0, y + 10, label, 12, "600"))
        y += 17
        for row in rows:
            bar_w = scale(row["stack_weight"], 0, max_weight, 0, 220)
            pieces.append(text(x0, y + 11, row["id"][:35], 10))
            pieces.append(rect(x0 + 225, y, 225, bar_h, "#eeeeee", "none"))
            pieces.append(rect(x0 + 225, y, bar_w, bar_h, color, "none", 0.78))
            pieces.append(text(x0 + 456, y + 11, f"{row['stack_weight']:.1f}", 10))
            y += 20
        y += 8
    return pieces


def main():
    glow = load_json(EVIDENCE / "q286-evidence-glow-map.json")
    overlay = load_json(EVIDENCE / "q286-target-vector-overlay.json")
    pca = load_json(EVIDENCE / "q286-target-vector-pca.json")
    commit = source_commit()
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-labelledby="title desc">',
        '<title id="title">q286 evidence glow and vector summary</title>',
        '<desc id="desc">Finite selected-target visualization. Brightness means overlapping evidence layers, not proof.</desc>',
        rect(0, 0, WIDTH, HEIGHT, "#fafafa", "none"),
        text(38, 42, "q286 Evidence Glow / Vector / PCA Summary", 24, "500"),
        text(38, 66, "Finite navigation layer only: glow is overlap, not proof. Boundary, endpoint, outer assembly, and signed prime correlation remain open.", 13),
        text(38, 855, f"generated from commit {commit}", 11, fill="#555"),
    ]
    pieces.extend(render_scatter(pca, overlay))
    pieces.extend(render_alignment_plot(pca, overlay))
    pieces.extend(render_stack_bars(glow))
    pieces.append("</svg>")
    out_path = EVIDENCE / "q286-visual-summary.svg"
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(pieces))
        handle.write("\n")
    print(out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
