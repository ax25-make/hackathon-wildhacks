from flask import Flask, request, jsonify
from google import genai
import os
import random
from dotenv import load_dotenv
from flask_cors import CORS
import json
import re

load_dotenv()

# - API keys to search
API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
if not API_KEY_1:
    raise ValueError("GEMINI_API_KEY_1 not found. Make sure it's in the .env file!")
API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
if not API_KEY_2:
    raise ValueError("GEMINI_API_KEY_2 not found. Make sure it's in the .env file!")

app = Flask(__name__)
CORS(app)  

plantation = ""
grid_size = 8

def initial_game():
    global plantation
    plantation = "Plantation"

    plant_cells = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    # - Empty cell essentially
    barren_dirt = {
        "type": "dirt",
        "description": "Barren land, ready to be cultivated.",
        "growth_stage": "barren",
        "plant_type": "dirt" 
    }

    plant_cells = [[barren_dirt for _ in range(grid_size)] for _ in range(grid_size)]

    initial_grid = {
        "plantation": plantation,
        "plant_cells": plant_cells
    }

    return initial_grid

# - can change later
def create_plant(plant_type="Wheat"):
    return {
        "plant_type": plant_type,   
        "growth_stage": "planting", 
        "health": 100,               
        "water_level": 0,
        "fertilizer_level": 0,
        "days_planted": 0,
    }

def generate_ai_prompt(game_state, row, col):
    plant = game_state["plant_cells"][row][col]
    plantation_name = game_state["plantation"]

    if plant["type"] == "dirt":
        prompt = f"The cell at row {row}, column {col} in {plantation_name} is empty. Describe the empty plot of land and what could be planted here."
    else:
        plant_type = plant["plant_type"]
        growth_stage = plant["growth_stage"]
        health = plant["health"]

        prompt = (
            f"In {plantation_name}, at row {row}, column {col}, there is a {plant_type} plant in the {growth_stage} stage."
            f"Its health is {health}. Describe the plant's appearance, its current needs (water, fertilizer), "
            f"and the potential consequences if those needs are not met."
        )

    return prompt

def get_gemini_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash") 

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response from AI."

def cell_to_row_col(cell):
    """Converts a cell string (e.g., 'A1') to row and column indices (0-based)."""
    match = re.match(r"([A-Za-z]+)(\d+)", cell)
    if not match:
        raise ValueError("Invalid cell format. Use A1, B2, etc.")

    col_str = match.group(1).upper()
    row = int(match.group(2)) - 1  

    col = 0
    for i, char in enumerate(reversed(col_str)):
        col += (ord(char) - ord('A') + 1) * (26 ** i)

    return row, col - 1 

def plant_cells_in_range(grid, start_cell, end_cell, plant_type="Wheat"):
    """Plants the specified plant type in all cells within the given range."""
    try:
        start_row, start_col = cell_to_row_col(start_cell)
        end_row, end_col = cell_to_row_col(end_cell)
    except ValueError as e:
        print(f"Error parsing cell coordinates: {e}")
        return

    # Determine the range of rows and columns to plant in
    min_row = min(start_row, end_row)
    max_row = max(start_row, end_row)
    min_col = min(start_col, end_col)
    max_col = max(start_col, end_col)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if 0 <= row < grid_size and 0 <= col < grid_size:
                grid["plant_cells"][row][col] = create_plant(plant_type)
            else:
                print(f"Cell {chr(col + ord('A'))}{row + 1} is out of bounds.")  

@app.route('/plant', methods=['POST'])
def plant():
    data = request.get_json()
    start_cell = data.get('start_cell')  
    end_cell = data.get('end_cell')    
    plant_type = data.get('plant_type', "Wheat") 

    game_state = initial_game()  
    plant_cells_in_range(game_state, start_cell, end_cell, plant_type)
    return jsonify({"message": f"Planted {plant_type} from {start_cell} to {end_cell}"})

@app.route('/cell_info', methods=['POST'])
def get_cell_info():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    game_state = initial_game() 
    prompt = generate_ai_prompt(game_state, row, col)
    api_key = random.choice([API_KEY_1, API_KEY_2])
    response_text = get_gemini_response(prompt, api_key)

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)