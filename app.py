from flask import Flask, render_template, request, jsonify
import re
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to extract coordinates from a list of text lines
def extract_coordinates(text_list):
    pattern = r"(-?\d+)\|(-?\d+)"
    coordinates = []
    for line in text_list:
        matches = re.findall(pattern, line)
        coordinates.extend([f"{int(x)}|{int(y)}" for x, y in matches])
        logging.info(f"Extracted matches from line '{line}': {matches}")
    return coordinates

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    # Get lists from the form and split into lines
    list1 = request.form.get("list1", "").strip().splitlines()
    list2 = request.form.get("list2", "").strip().splitlines()

    # Validate inputs
    if not list1 or not list2:
        return jsonify({"error": "Both lists must contain at least one line."}), 400

    # Extract coordinates from each list
    coords1 = extract_coordinates(list1)
    coords2 = extract_coordinates(list2)

    # Handle cases where no valid coordinates were found
    if not coords1 and not coords2:
        return jsonify({"error": "No valid coordinates found in either input."}), 400
    elif not coords1:
        return jsonify({"error": "No valid coordinates found in List 1."}), 400
    elif not coords2:
        return jsonify({"error": "No valid coordinates found in List 2."}), 400

    # Calculate common and unique coordinates
    common_items = set(coords1).intersection(coords2)
    unique_to_list1 = set(coords1) - set(coords2)
    unique_to_list2 = set(coords2) - set(coords1)

    logging.info(f"Common items: {common_items}")
    logging.info(f"Unique to List 1: {unique_to_list1}")
    logging.info(f"Unique to List 2: {unique_to_list2}")

    # Return comparison results with count details
    return jsonify({
        "common_items": list(common_items),
        "common_count": len(common_items),
        "unique_to_list1": list(unique_to_list1),
        "unique_to_list1_count": len(unique_to_list1),
        "unique_to_list2": list(unique_to_list2),
        "unique_to_list2_count": len(unique_to_list2)
    })

if __name__ == '__main__':
    app.run(debug=True)
