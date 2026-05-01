#!/usr/bin/env python3
"""Generate Warp-branded Slack icons for incident creation.

Outputs:
  warp_incident_icon.png      – 512x512 (primary)
  warp_incident_icon_128.png  – 128x128 (small/thumbnail)

Brand tokens used:
  Background: #121212 (Warp black)
  Alert:      #C6372A (Warp red – error/destructive states)
  Accent:     #A43787 (Warp pink – primary expressive accent)
"""

from PIL import Image, ImageDraw
import math

# Warp brand tokens
BLACK = "#121212"
RED = "#C6372A"
PINK = "#A43787"


def inset_triangle(verts, px):
    """Shrink a triangle toward its centroid by px pixels."""
    cx = sum(v[0] for v in verts) / 3
    cy = sum(v[1] for v in verts) / 3
    result = []
    for x, y in verts:
        dx, dy = cx - x, cy - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            result.append((x, y))
        else:
            result.append((x + dx / dist * px, y + dy / dist * px))
    return result


def generate_icon(size, output_path):
    """Generate the incident icon at a given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded-rect background (Slack crops to rounded square)
    corner_radius = int(size * 0.156)  # ~80/512
    draw.rounded_rectangle(
        [(0, 0), (size - 1, size - 1)],
        radius=corner_radius,
        fill=BLACK,
    )

    # Warning triangle
    pad = int(size * 0.156)
    tri_top = pad + int(size * 0.02)
    tri_bottom = size - pad - int(size * 0.04)
    tri_left = pad
    tri_right = size - pad
    tri_cx = size // 2

    vertices = [
        (tri_cx, tri_top),
        (tri_left, tri_bottom),
        (tri_right, tri_bottom),
    ]

    # Outer triangle (filled red)
    draw.polygon(vertices, fill=RED)

    # Inner triangle (cut out to make outline)
    inset = int(size * 0.055)
    inner_verts = inset_triangle(vertices, inset)
    draw.polygon(inner_verts, fill=BLACK)

    # Exclamation mark
    exc_cx = tri_cx
    exc_top = tri_top + int(size * 0.254)
    exc_bar_bottom = tri_bottom - int(size * 0.215)
    exc_dot_top = tri_bottom - int(size * 0.156)
    exc_dot_bottom = tri_bottom - int(size * 0.107)
    bar_hw = int(size * 0.031)
    dot_r = int(size * 0.035)

    draw.rounded_rectangle(
        [(exc_cx - bar_hw, exc_top), (exc_cx + bar_hw, exc_bar_bottom)],
        radius=max(2, int(size * 0.016)),
        fill=RED,
    )
    draw.ellipse(
        [(exc_cx - dot_r, exc_dot_top), (exc_cx + dot_r, exc_dot_bottom)],
        fill=RED,
    )

    # Subtle pink accent line at bottom
    accent_y = size - int(size * 0.082)
    accent_margin = int(size * 0.273)
    draw.rounded_rectangle(
        [(accent_margin, accent_y), (size - accent_margin, accent_y + max(2, int(size * 0.006)))],
        radius=max(1, int(size * 0.004)),
        fill=PINK,
    )

    img.save(output_path, "PNG")
    print(f"Saved {size}x{size} icon to {output_path}")


if __name__ == "__main__":
    generate_icon(512, "/workspace/.github/warp_incident_icon.png")
    generate_icon(128, "/workspace/.github/warp_incident_icon_128.png")
