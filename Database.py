# ---------------------------------------------------------
# SİLAH VERİTABANI
# ---------------------------------------------------------
WEAPONS_DB = {
    "handgun_compact": {
        "name": "Kısa Namlu Tabanca",
        "barrel_length_cm": 10.0,
        "base_dispersion_angle": 0.045,  # ~2.5 derece (25m'de ~1.1m yarıçaplı koni)
        "fire_rate_rpm": 300,
        "accepted_calibers": ["9x19mm"]
    },
    "carbine_rifle": {
        "name": "Taktik Karabina",
        "barrel_length_cm": 40.0,
        "base_dispersion_angle": 0.012,  # ~0.45 derece (100m'de ~0.8m yarıçaplı dar koni)
        "fire_rate_rpm": 700,
        "accepted_calibers": ["5.56x45mm"]
    }
}

# ---------------------------------------------------------
# MÜHİMMAT VERİTABANI
# ---------------------------------------------------------
AMMO_DB = {
    # 9x19mm
    "9mm_standard_fmj": {
        "name": "9x19mm Standart FMJ",
        "caliber": "9x19mm",
        "base_damage": 22.0,
        "base_penetration": 14.0,
        "ideal_barrel_cm": 15.0,
        "drag_rate": 0.008
    },
    "9mm_armor_piercing": {
        "name": "9x19mm Zırh Delici (AP)",
        "caliber": "9x19mm",
        "base_damage": 18.0,
        "base_penetration": 32.0,
        "ideal_barrel_cm": 18.0,
        "drag_rate": 0.007
    },

    # 5.56x45mm
    "556_standard_ball": {
        "name": "5.56x45mm Standart Ball",
        "caliber": "5.56x45mm",
        "base_damage": 42.0,
        "base_penetration": 35.0,
        "ideal_barrel_cm": 45.0,
        "drag_rate": 0.0025
    },
    "556_armor_piercing": {
        "name": "5.56x45mm Zırh Delici (AP)",
        "caliber": "5.56x45mm",
        "base_damage": 28.0,
        "base_penetration": 68.0,
        "ideal_barrel_cm": 50.0,
        "drag_rate": 0.0020
    }
}
