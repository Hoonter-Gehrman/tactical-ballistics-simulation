import math
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import json

import hitboxloader
import hitboxrenderer


#Pulling data from database
with open("weapons.json", "r", encoding="utf-8") as file:
    WEAPONS_DB = json.load(file)

with open("ammos.json", "r", encoding="utf-8") as file:
    AMMO_DB = json.load(file)
    
    
# Getting creature anatomical hitbox data    
print("\n--- HEDEF SEÇİMİ ---")
creature_menu = hitboxloader.get_enemy_menu()
for i, (enemy_id, enemy_name) in enumerate(creature_menu):
    print(f"{i+1} --- {enemy_name}")
    
e_choice_index = int(input("Hedef numarasını giriniz: ")) - 1
selected_id = creature_menu[e_choice_index][0]

enemy_data = hitboxloader.load_anatomy(selected_id)
critical_point = enemy_data["critical_point"]
anatomy = enemy_data["anatomy"]


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


# Dynamic aim menu
print("\n--- NİŞAN ALMA TERCİHİ ---")
print(f"1 --- Gövde (Merkez: 0.0, 0.0)")
print(f"2 --- {critical_point['name']} (Kritik Nokta: X={critical_point['x']}, Y={critical_point['y']})")
target_choice = int(input("Nişan alacağınız noktayı seçin (1 veya 2): "))

if target_choice == 2:
    center_x = critical_point["x"]
    center_y = critical_point["y"]
elif target_choice == 1:
    center_x = 0.0
    center_y = 0.0
    

#Shooting distribution
delta_rifle = s_weapon["base_dispersion_angle"]
radius_dispersion = distance * math.tan(delta_rifle)

area = math.pi * (radius_dispersion**2)
sigma = radius_dispersion / 3

x = np.random.normal(loc=center_x, scale=sigma, size=total_shots)
y = np.random.normal(loc=center_y, scale=sigma, size=total_shots)


#Statistics
hit_stats = hitboxrenderer.calculate_hits(anatomy, x, y)
print("\n--- ATIŞ RAPORU ---")
print(f"Toplam Mermi: {total_shots}")
for organ, hits in hit_stats.items():
    pct = (hits / total_shots) * 100
    print(f"{organ:<12}: {hits:>5} (%{pct:5.1f})")


#Hitbox Rendering
hitboxrenderer.render(anatomy)


# Shots scatter & Crosshair
plt.style.use("dark_background")
plt.scatter(x, y, s=15, alpha=0.15, color="orangered")
plt.plot(center_x, center_y, "w+", markersize=10, markeredgewidth=1.5, zorder=6)

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.gca().set_aspect("equal")

plt.show()