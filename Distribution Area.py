import math
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import json

#Pulling data from database
with open("weapons.json", "r", encoding="utf-8") as file:
    WEAPONS_DB = json.load(file)

with open("ammos.json", "r", encoding="utf-8") as file:
    AMMO_DB = json.load(file)

plt.style.use("dark_background")

# --- WEAPON & BALLISTICS SETUP ---
print("\n--- SİLAH SEÇİMİ ---")
weapon_keys = list(WEAPONS_DB.keys())

for i, s in enumerate(weapon_keys):
    print(f"{i+1} --- {WEAPONS_DB[s]["name"]}")
w_choice = int(input("seçmek istediğiniz silahın numarasını giriniz: ")) -1
s_weapon_key = weapon_keys[w_choice]
s_weapon = WEAPONS_DB[s_weapon_key]

distance = float(input("Atış mesafesini girin (Metre): "))
total_shots = int(input("Kaç el ateş edilecek?: "))
target_choice = input("Nereye nişan alıyorsun? (1: Gövde, 2: Kafa): ").strip()

delta_rifle = s_weapon["base_dispersion_angle"]
radius_dispersion = distance * math.tan(delta_rifle)

area = math.pi * (radius_dispersion**2)
sigma = radius_dispersion / 3

# Generate shot dispersions
x = np.random.normal(0, sigma, total_shots)
y = np.random.normal(0, sigma, total_shots)

# Selection of Aim (Anatomik & Taktiksel Oranlar)
# Selection of Aim (Tam Teğet & Çakışmasız Hiza)
if target_choice == "2":  # --- HEADSHOT SEÇİMİ ---
    head_x, head_y = 0.0, 0.0
    head_r = 0.12

    # Gövde tam kafanın altından (-0.12m) başlar
    torso_x_min, torso_x_max = -0.20, 0.20
    torso_y_min, torso_y_max = -0.82, -0.12

    # Kollar omuz hizasından başlar
    right_arm_x = (0.20, 0.32)
    right_arm_y = (-0.57, -0.12)
    left_arm_x = (-0.32, -0.20)
    left_arm_y = (-0.57, -0.12)

    # Bacaklar gövdenin altından başlar
    legs_x_min, legs_x_max = -0.20, 0.20
    legs_y_min, legs_y_max = -1.37, -0.82

else:  # --- BODYSHOT SEÇİMİ (Merkez Gövde) ---
    torso_x_min, torso_x_max = -0.20, 0.20
    torso_y_min, torso_y_max = -0.35, 0.35

    # Kafa tam gövdenin üstüne (+0.35m) teğet oturur
    head_x, head_y = 0.0, 0.47
    head_r = 0.12

    right_arm_x = (0.20, 0.32)
    right_arm_y = (-0.10, 0.35)
    left_arm_x = (-0.32, -0.20)
    left_arm_y = (-0.10, 0.35)

    legs_x_min, legs_x_max = -0.20, 0.20
    legs_y_min, legs_y_max = -0.90, -0.35


# --- HIT DETECTION LOGIC ---

# 1. Head
hit_head = ((x - head_x) ** 2 + (y - head_y) ** 2) <= (head_r**2)

# 2. Torso (Excluding head overlap)
hit_torso = (
    (x >= torso_x_min)
    & (x <= torso_x_max)
    & (y >= torso_y_min)
    & (y <= torso_y_max)
    & (~hit_head)
)

# 3. Arms (Excluding head & torso overlap)
hit_right_arm = (
    (x >= right_arm_x[0])
    & (x <= right_arm_x[1])
    & (y >= right_arm_y[0])
    & (y <= right_arm_y[1])
)
hit_left_arm = (
    (x >= left_arm_x[0])
    & (x <= left_arm_x[1])
    & (y >= left_arm_y[0])
    & (y <= left_arm_y[1])
)
hit_arms = (hit_right_arm | hit_left_arm) & (~hit_head) & (~hit_torso)

# 4. Legs (Excluding upper body overlap)
hit_legs = (
    (x >= legs_x_min)
    & (x <= legs_x_max)
    & (y >= legs_y_min)
    & (y <= legs_y_max)
    & (~hit_head)
    & (~hit_torso)
    & (~hit_arms)
)

# 5. Miss
hit_any = hit_head | hit_torso | hit_arms | hit_legs
miss = ~hit_any

# Hit counts
count_head = np.sum(hit_head)
count_torso = np.sum(hit_torso)
count_arms = np.sum(hit_arms)
count_legs = np.sum(hit_legs)
count_miss = np.sum(miss)


# --- STATISTICAL REPORT ---
print(
    f"""
--- SHOT DISPERSION REPORT ---
Total Shots : {total_shots}
Headshots   : {count_head} ({count_head / total_shots * 100:.2f}%)
Torso Hits  : {count_torso} ({count_torso / total_shots * 100:.2f}%)
Arm Hits    : {count_arms} ({count_arms / total_shots * 100:.2f})
Leg Hits    : {count_legs} ({count_legs / total_shots * 100:.2f})
Misses      : {count_miss} ({count_miss / total_shots * 100:.2f})
"""
)


# --- PLOT VISUALIZATION ---
fig, ax = plt.subplots()

plt.xlabel("X Deviation (Meters)", fontsize=11, color="white")
plt.ylabel("Y Deviation (Meters)", fontsize=11, color="white")

plt.title(
    f"{distance}m Shot Dispersion (R = {radius_dispersion:.2f}m, σ = {sigma:.3f}m)",
    fontsize=12,
    color="white",
    pad=15,
)

# Adding Patches
head_patch = plt.Circle(
    (head_x, head_y),
    head_r,
    edgecolor="red",
    facecolor="none",
    linewidth=2,
    label="Head",
    zorder=4,
)
ax.add_patch(head_patch)

torso_w = torso_x_max - torso_x_min
torso_h = torso_y_max - torso_y_min
torso_patch = patches.Rectangle(
    (torso_x_min, torso_y_min),
    torso_w,
    torso_h,
    edgecolor="red",
    facecolor="none",
    linewidth=2,
    label="Torso",
    zorder=4,
)
ax.add_patch(torso_patch)

r_arm_w = right_arm_x[1] - right_arm_x[0]
r_arm_h = right_arm_y[1] - right_arm_y[0]
r_arm_patch = patches.Rectangle(
    (right_arm_x[0], right_arm_y[0]),
    r_arm_w,
    r_arm_h,
    edgecolor="red",
    facecolor="none",
    linewidth=1.5,
    label="Arms",
    zorder=4,
)
ax.add_patch(r_arm_patch)

l_arm_w = left_arm_x[1] - left_arm_x[0]
l_arm_h = left_arm_y[1] - left_arm_y[0]
l_arm_patch = patches.Rectangle(
    (left_arm_x[0], left_arm_y[0]),
    l_arm_w,
    l_arm_h,
    edgecolor="red",
    facecolor="none",
    linewidth=1.5,
    zorder=4,
)
ax.add_patch(l_arm_patch)

legs_w = legs_x_max - legs_x_min
legs_h = legs_y_max - legs_y_min
legs_patch = patches.Rectangle(
    (legs_x_min, legs_y_min),
    legs_w,
    legs_h,
    edgecolor="magenta",
    facecolor="none",
    linewidth=1.5,
    label="Legs",
    zorder=4,
)
ax.add_patch(legs_patch)

plt.grid(True, linestyle=":", alpha=0.3, color="gray")

# Shots scatter & Crosshair
plt.scatter(x, y, s=15, alpha=0.15, color="orangered")
plt.plot(0, 0, "w+", markersize=10, markeredgewidth=1.5, zorder=6)

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.gca().set_aspect("equal")

plt.show()