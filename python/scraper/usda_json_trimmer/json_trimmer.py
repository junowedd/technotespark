import json
import csv
import sys

def main():
    print("[json_trimmer] Starting USDA JSON trimming")

    # Determine input file
    input_file = "FoodData_Central_foundation_food_json_2025-04-24.json"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print(f"[json_trimmer] Using input file: {input_file}")

    # Load JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    foods = data.get("FoundationFoods", [])
    print(f"[json_trimmer] Number of foods found: {len(foods)}")

    target_nutrients = [
        "Protein",
        "Total lipid (fat)",
        "Carbohydrate, by difference",
        "Energy"
    ]

    filtered_data = []

    for food in foods:
        nutrients = food.get("foodNutrients", [])
        entry = {"description": food.get("description", "")}

        for n in nutrients:
            name = n.get("nutrient", {}).get("name")
            if name in target_nutrients:
                entry[name] = n.get("amount")

        if any(k in entry for k in target_nutrients):
            filtered_data.append(entry)

    print(f"[json_trimmer] Filtered foods count: {len(filtered_data)}")

    # Write JSON output
    with open("usda_filtered_foods.json", "w", encoding="utf-8") as jf:
        json.dump(filtered_data, jf, indent=2)

    # Write CSV output
    fieldnames = ["description"] + target_nutrients
    with open("usda_filtered_foods.csv", "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        for row in filtered_data:
            writer.writerow(row)

    print("[json_trimmer] Output written:")
    print("  - usda_filtered_foods.json")
    print("  - usda_filtered_foods.csv")
    print("[json_trimmer] Done.")

if __name__ == "__main__":
    main()
