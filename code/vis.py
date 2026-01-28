import os

from matplotlib.collections import LineCollection

from this_sucks_model import build_model, candidate_points, demand_coords, demand_indices, candidate_indices, poly, mask
import matplotlib.image as mpimg
import pyomo.environ as pyo
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from thing_playing_field import compute_coverage, mask, polygon
from shapely import MultiPoint
import math

def visualize_solution_with_image(
        img_path, img_extent,
        demand_points, candidate_points,
        selected_indices, assignments,
        dpi=110, fade=0.45, seed=123):

    # ––––– SET‑UP ––––– #
    rng = np.random.default_rng(seed)
    palette = plt.cm.get_cmap("tab10", len(selected_indices))

    img = mpimg.imread(img_path)
    h, w = img.shape[:2]
    fig, ax = plt.subplots(figsize=(12, 12*h/w), dpi=dpi)

    # background
    ax.imshow(img, extent=img_extent, alpha=fade, zorder=1)

    # pull out data in numpy for speed
    cand = np.asarray(candidate_points)
    if isinstance(demand_points, dict):
        dem   = np.asarray(list(demand_points.values()))
    else:
        dem   = np.asarray(demand_points)

    # ––––– DEMAND (tiny green) ––––– #
    ax.scatter(*dem.T, s=6, color="limegreen", zorder=20, label="Spirit Kill Points")

    # ––––– SELECTED FACILITIES ––––– #
    sel_xy = cand[selected_indices]
    ax.scatter(*sel_xy.T,
               s=80, color="red", edgecolor="k", linewidth=1.0, zorder=40,
               label="Optimal Counter Terrorist Positions",
               path_effects=[pe.Stroke(linewidth=3, foreground='white'), pe.Normal()]
               )

    # ––––– ASSIGNMENT LINES ––––– #
    # Build one segment list per facility (for colour‑coding)
    segs_by_fac = {j: [] for j in selected_indices}
    for dem_idx, fac_idx in assignments.items():
        segs_by_fac[fac_idx].append([dem[dem_idx], cand[fac_idx]])

    # Draw all facilities in one LineCollection each
    for k, (fac_idx, segs) in enumerate(segs_by_fac.items()):
        if not segs:   # in case a selected facility happened not to get demand
            continue
        lc = LineCollection(segs,
                            colors=[palette(k)],
                            linewidths=0.8,
                            linestyles="--",
                            alpha=0.5,
                            zorder=10)
        ax.add_collection(lc)

    # ––––– AESTHETICS ––––– #
    ax.set_xlim(img_extent[0], img_extent[1])
    ax.set_ylim(img_extent[2], img_extent[3])
    ax.set_title("Optimal Counter‑Terrorist Positions", fontsize=16, pad=30)

    lg = ax.legend(
        bbox_to_anchor=(0.02, 0.98), loc="upper left",
        framealpha=0.8, borderpad=0.8, fontsize=9
    )
    lg.get_frame().set_facecolor("white")

    ax.axis("off")          # map already has a frame
    plt.tight_layout()
    plt.show()

p = 5  # Number of facilities to open
lambda_param = 3.50 # Risk penalty coefficient 0.5901267 -- for average stuff

# Build and solve model
model = build_model(demand_indices, candidate_indices, p, lambda_param)
print("At Solver")
solver = pyo.SolverFactory('cbc')
print("Out of Solver")
print("Solving at solver.solve")
results = solver.solve(model, tee=True)
print("Out?")
# Extract results
selected_facilities = [j for j in model.J if pyo.value(model.Y[j]) > 0.5]
assignments = {
    i: [j for j in model.J if pyo.value(model.X[i,j]) > 0.5][0]
    for i in model.I
}

sel_x = [candidate_points[j][0] for j in selected_facilities]
sel_y = [candidate_points[j][1] for j in selected_facilities]

all_visited_sets = []
for x, y in zip(sel_x, sel_y):
    pts = compute_coverage(x, y, mask)
    all_visited_sets.append(pts)

img = mpimg.imread(r"de_ancient_radar_psd.png")
playable = polygon.buffer(0)

n = len(all_visited_sets)
cols = 2
rows = math.ceil(n/cols)

fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
axes = axes.flatten()

for ax, visited in zip(axes, all_visited_sets):
    # draw background
    ax.imshow(img, extent=(0, img.shape[1], img.shape[0], 0))
    ax.set_aspect("equal")
    ax.axis("off")

    if visited:
        xs, ys = zip(*visited)
        ax.scatter(xs, ys, s=1, alpha=0.5)

        hull = MultiPoint(visited).convex_hull
        covered = playable.intersection(hull)
        area = covered.area
        if not covered.is_empty and hasattr(covered, "exterior"):
            hx, hy = covered.exterior.xy
            ax.plot(hx, hy, linewidth=2)
            ax.fill(hx, hy, alpha=0.2)

    else:
        ax.text(.5, .5, "No points", ha="center", va="center", transform=ax.transAxes)

# turn off any extra subplots
for extra in axes[n:]:
    extra.axis("off")

plt.tight_layout()
plt.show()

visualize_solution_with_image(
    img_path="de_ancient_radar_psd.png",
    img_extent=[0, 1024, 1024, 0],  # Match your image coordinates
    demand_points=demand_coords,
    candidate_points=candidate_points,
    selected_indices=selected_facilities,
    assignments=assignments,
)
