import pyvista as pv
import numpy as np

# -----------------------------
# Cone geometry parameters
# -----------------------------
H = 100.0                      # height (depth)
R_outer_top = 25.0
R_outer_bottom = 10.0
R_inner_top = 20.0
R_inner_bottom = 17.0

# -----------------------------
# Create hollow cone
# -----------------------------
outer_cone = pv.Cone(
    center=(0, 0, H/2),
    direction=(0, 0, 1),
    height=H,
    radius=R_outer_top,
    resolution=120
).triangulate()

inner_cone = pv.Cone(
    center=(0, 0, H/2),
    direction=(0, 0, 1),
    height=H,
    radius=R_inner_top,
    resolution=120
).triangulate()

# scale inner cone to match bottom radius
scale_factor = R_inner_bottom / R_inner_top
inner_cone.scale([scale_factor, scale_factor, 1.0], inplace=True)

# boolean subtraction
hollow_cone = outer_cone.boolean_difference(inner_cone)


# -----------------------------
# Helper function
# -----------------------------
def inner_radius_at_z(z):
    return R_inner_top + (R_inner_bottom - R_inner_top) * (z / H)

# -----------------------------
# Create synthetic voids
# -----------------------------
voids = []
void_params = [
    (30, np.pi/4, 3.0),
    (55, np.pi,   4.0),
    (75, 3*np.pi/2, 2.5),
]

for z, theta, r in void_params:
    r_z = inner_radius_at_z(z)
    x = r_z * np.cos(theta)
    y = r_z * np.sin(theta)
    voids.append(pv.Sphere(radius=r, center=(x, y, z)))

# -----------------------------
# Create synthetic cracks
# -----------------------------
cracks = []
crack_params = [
    (40, np.pi/2, 8.0),
    (65, 5*np.pi/4, 10.0),
]

for z, theta, length in crack_params:
    r_z = inner_radius_at_z(z)
    x = r_z * np.cos(theta)
    y = r_z * np.sin(theta)

    cracks.append(
        pv.Cylinder(
            center=(x, y, z),
            direction=(0, 0, 1),
            radius=0.7,
            height=length
        )
    )

# -----------------------------
# Visualization
# -----------------------------
plotter = pv.Plotter()

plotter.add_mesh(
    hollow_cone,
    color="gold",
    opacity=0.35,
    smooth_shading=True
)

for v in voids:
    plotter.add_mesh(v, color="red")

for c in cracks:
    plotter.add_mesh(c, color="blue")

plotter.add_axes()
plotter.show_grid()
plotter.show()
