import json

def get_enemy_menu(filepath="enemies.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        db = json.load(f)
    menu_list = []
    
    for i, a in db.items():
        enemy_id = i               
        enemy_name = a["name"] 
        menu_list.append((enemy_id, enemy_name))
        
    return menu_list

def load_anatomy(enemy_id, file_path="enemies.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    enemy_entry = db[enemy_id]
    critical_point = enemy_entry.get("critical_point", {})
    raw_anatomy = enemy_entry["anatomy"]
    
    final_anatomy = {}
    for organ, data in raw_anatomy.items():
        shape_type = data.get("type")
        
        if shape_type == "circle":
            final_anatomy[organ] = {
                "type": "circle",
                "x": float(data["x"]),
                "y": float(data["y"]),
                "r": float(data["r"])
            }
        elif shape_type == "rect":
            final_anatomy[organ] = {
                "type": "rect",
                "x_min": float(data["x_min"]),
                "x_max": float(data["x_max"]),
                "y_min": float(data["y_min"]),
                "y_max": float(data["y_max"])
            }
        elif shape_type == "poly":
            final_anatomy[organ] = {
                "type": "poly",
                "vertices": data["vertices"]
            }
            
    return {
        "critical_point": critical_point,
        "anatomy": final_anatomy
    }