import json

path = "ros_server_v2/server/saved_accounts.json"
data = json.load(open(path, "r"))

# Update default
data["default"]["name"] = "TestPlayer"
data["default"]["char_type"] = 20001

seeded_items = [
    120901, 120902, 120903, 120904, 120905,
    142080, 142081, 142082, 140105,
    102568, 102413, 1102319,
    1111382, 1111383, 15, 16, 17,
    106500, 106501, 106502,
    104932, 104935,
    250175, 250153, 250156,
    270000, 270002, 270003
]

for gid in ["9547712472", "9000000001"]:
    inv_key = f"inventory:{gid}"
    gender_key = f"gender:{gid}"
    
    if inv_key not in data:
        data[inv_key] = {
            "yuanbao": 100000,
            "items": [],
            "outfit": {
                "body": [],
                "wear": [],
                "weapon": [120901, 120016],
                "vehicle": [142080],
                "theme": 270002
            }
        }
    
    current_items = set(data[inv_key].get("items", []))
    for it in seeded_items:
        current_items.add(it)
    data[inv_key]["items"] = sorted(list(current_items))
    data[inv_key]["yuanbao"] = max(data[inv_key].get("yuanbao", 0), 100000)
    
    if gender_key not in data:
        data[gender_key] = {"gender": 1, "body": {"1": [], "2": []}}

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Updated saved_accounts.json successfully.")
print(f"Total items for 9547712472: {len(data['inventory:9547712472']['items'])}")
print(f"Total items for 9000000001: {len(data['inventory:9000000001']['items'])}")
