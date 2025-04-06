import os
import interface
from data import PLANT_DATA

class Economy():
    def __init__(self):
        self.market_prices = {plant_type: 2.0 for plant_type in PLANT_DATA}

    def simulate_market(self, season):
        plant_names = ", ".join(PLANT_DATA.keys())
        input_prompt = f"Simulate the market prices for {plant_names} for the {season} season. Provide a table of updated market prices. Include the following columns: Plant, Price. Format as CSV"
        response = interface.generate_content(interface.chat, input_prompt)

        if response:
            self.parse_gemini_output(response)
        else:
            print("Error simulating market.")

    def parse_gemini_output(self, gemini_output):
        lines = gemini_output.split('\n')
        for line in lines:
            parts = line.split(',')
            if len(parts) == 2:
                plant, price = parts[0].strip(), parts[1].strip()
                if plant == "Plant":  
                    continue
                try:
                    self.market_prices[plant] = float(price)
                except ValueError:
                    print(f"Could not parse price for {plant}")
                except KeyError:
                    print(f"Plant type {plant} not found in market prices")

    def get_market_price(self, plant_type):
        return self.market_prices.get(plant_type, 1.0)  # Default price of 1.0 if not found