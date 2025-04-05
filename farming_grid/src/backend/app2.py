import os
import random
from dotenv import load_dotenv
import re
import json
from google import genai

load_dotenv()

# API keys
API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
if not API_KEY_1:
    raise ValueError("GEMINI_API_KEY_1 not found. Make sure it's in the .env file!")
API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
if not API_KEY_2:
    raise ValueError("GEMINI_API_KEY_2 not found. Make sure it's in the .env file!")

plantation = ""
grid_size = 8

# - Defining the character model and states
conversation_history = []

# - Initiate the client
client_1 = genai.Client(api_key=API_KEY_1)
client_2 = genai.Client(api_key=API_KEY_2)
client = client_1

# - Set the model name
MODEL_NAME = "gemini-2.0-flash"

# - Generate grid
def initial_game():
    global plantation
    plantation = "Plantation"

    plant_cells = [[None for _ in range(grid_size)] for _ in range(grid_size)]

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

# add plant - look up plant in files ## add later
def create_plant(plant_type="Wheat"):
    return {
        "type": "plant",  
        "plant_type": plant_type,
        "growth_stage": "planting",
        "health": 100,
        "water_level": 0,
        "fertilizer_level": 0,
        "days_planted": 0,
    }

def grid_to_string(game_state):
    """Converts the grid to a text representation."""
    grid_str = "  " + " ".join([chr(ord('A') + i) for i in range(grid_size)]) + "\n"
    for row in range(grid_size):
        grid_str += str(row + 1) + " "
        for col in range(grid_size):
            cell = game_state["plant_cells"][row][col]
            if cell["type"] == "dirt":
                grid_str += ". "
            else:
                grid_str += cell["plant_type"][0].upper() + " "  # First letter of plant type
        grid_str += "\n"
    return grid_str

def get_gemini_response(user_query, game_state, history, client):
    """Gets a response from Gemini, managing conversation history and client rotation."""

    grid_string = grid_to_string(game_state)  # Get the current farm state

    conversation_context = history[:]
    # conversation_context = [{"role": "system", "parts": [{"text": f"You are a helpful assistant helping a user manage their farm." + grid_string}]}]
    # Adding the current grid to the system prompt
    conversation_context.extend(history)
    conversation_context.append({"role": "user", "parts": [{"text": user_query + grid_string}]})
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation_context,
        )
        client = client_2 if client == client_1 else client_1  # Alternate the client for the next call

        gemini_response = response.text.strip()
        print(f"gemini_response: {gemini_response}")
        # Update conversation history and reduce questions
        history.append({"role": "user", "parts": [{"text": user_query}]})
        history.append({"role": "model", "parts": [{"text": gemini_response}]})

        return gemini_response, history

    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response from AI."  # changed


def main():
    global client
    game_state = initial_game()
    history = []

    while True:
        grid_string = grid_to_string(game_state)
        print("\nFarm State:\n" + grid_string)

        user_input = input(f"Enter your command (type 'exit'): ")

        if user_input.lower() == "exit":
            print("Exiting.")
            break

        gemini_response, history = get_gemini_response(user_input, game_state, history, client) # Passing client

        print(f"Gemini's Response: {gemini_response}")

        if "plant wheat" in gemini_response.lower():
            print("Gemini suggested planting wheat. Attempting to plant in a random empty cell...")
            empty_cells = []
            for row in range(grid_size):
                for col in range(grid_size):
                    if game_state["plant_cells"][row][col]["type"] == "dirt":
                        empty_cells.append((row, col))

            if empty_cells:
                row, col = random.choice(empty_cells)
                game_state["plant_cells"][row][col] = create_plant("Wheat")
                print(f"Planted wheat at {chr(ord('A') + col)}{row + 1}")
            else:
                print("No empty cells to plant in!")

if __name__ == "__main__":
    main()