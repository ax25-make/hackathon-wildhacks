import os
import interface

class Economy():
    def __init__(self):
        self.market_prices = {
            "Wheat": 2.0,
            "Beans": 5.0,
            "Potatoes": 3.0,
            "Corn": 4.0
        }

    def simulate_market(self, season):
        input_prompt = f"Simulate the market prices for Wheat, Beans, Potatoes, and Corn for the {season} season.  Provide a table of updated market prices. Include the following columns: Plant, Price. Format as CSV"
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
                if plant == "Plant":  # Skip header
                    continue
                try:
                    self.market_prices[plant] = float(price)
                except ValueError:
                    print(f"Could not parse price for {plant}")
                except KeyError:
                    print(f"Plant type {plant} not found in market prices")

    def get_market_price(self, plant_type):
        return self.market_prices.get(plant_type, 1.0)  # Default price of 1.0 if not found