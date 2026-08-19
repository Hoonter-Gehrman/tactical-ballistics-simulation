import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np

def render(anatomy):
    for organ_name, data in anatomy.items():
        
        if data.get("type") == "rect":
            x_min = data["x_min"]
            x_max = data["x_max"]
            y_min = data["y_min"]
            y_max = data["y_max"]
            
            xs = [x_min, x_min, x_max, x_max, x_min]
            ys = [y_min, y_max, y_max, y_min, y_min]
            
            plt.plot(xs, ys, color="red")
            
        elif data.get("type") == "circle":
            cx = data["x"]
            cy = data["y"]
            r = data["r"]
            circle = patches.Circle((cx, cy), r, edgecolor="red", facecolor="none")
            plt.gca().add_patch(circle)
            
        elif data.get("type") == "poly":
            vertices = data["vertices"]
            xs = []
            ys = []
            for i in vertices:
                xs.append(i[0])
                ys.append(i[1])
            xs.append(vertices[0][0])
            ys.append(vertices[0][1])
            
            plt.plot(xs, ys, color="red")
            
def calculate_hits(anatomy, x, y):
    hit_results = {}
    total_hits = 0
    
    for organ, data in anatomy.items():
        shape_type = data.get("type")
        
        if shape_type == "circle":
            hits = (x - data["x"])**2 + (y - data["y"])**2 <= data["r"]**2
            
        elif shape_type == "rect":
            hits = (x >= data["x_min"]) & (x <= data["x_max"]) & (y >= data["y_min"]) & (y <= data["y_max"])
            
        elif shape_type == "poly":
            points = np.column_stack((x, y))
            hits = Path(data["vertices"]).contains_points(points)
        else:
            hits = np.zeros(len(x), dtype=bool)
            
        count = int(np.sum(hits))
        hit_results[organ] = count
        total_hits += count
        
    hit_results["Miss"] = len(x) - total_hits
    return hit_results