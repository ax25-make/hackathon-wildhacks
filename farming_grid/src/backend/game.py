import os
from grid import Grid
from plant import Plant
from economy import Economy
from timer_time import Timer
from data import PLANT_DATA

class Game:
    def __init__(self):
        self.grid = Grid(8, 8)
        self.economy = Economy()
        self.timer = Timer()
        self.plant_data = PLANT_DATA
        self.money = 100  #Starting money
        self.turns_per_day = 3  # Number of actions allowed per day
        self.remaining_turns = self.turns_per_day
        self.stock = {plant_type: 0 for plant_type in PLANT_DATA} # Initialize stock

    def run(self):
        while True:
            self.grid.display()
            print(f"Day: {self.timer.day}, Season: {self.timer.season}, Money: ${self.money:.2f}")
            print(f"Remaining turns: {self.remaining_turns}")
            self.display_stock()
            self.display_player_actions()
            action = input("What do you want to do? ").lower()

            if action == 'plant':
                self.plant_prompt()
            elif action == 'water':
                self.water_prompt()
            elif action == 'fertilize':
                self.fertilize_prompt()
            elif action == 'check':
                self.check_prompt()
            elif action == 'harvest':
                self.harvest_prompt()
            elif action == 'advance':
                self.advance_time()
            elif action == 'sell':
                self.sell_prompt()
            elif action == 'exit':
                print("Exiting game.")
                break
            else:
                print("Invalid action.")

            if self.remaining_turns == 0:
                self.advance_time()
                self.remaining_turns = self.turns_per_day

    def display_player_actions(self):
        print("Available actions: Plant, Water, Fertilize, Check, Harvest, Advance, Sell, Exit")
    
    def display_stock(self):
        print("--- Stock ---")
        for plant_type, quantity in self.stock.items():
            print(f"{plant_type}: {quantity}")
        print("-------------")

    def plant_prompt(self):
        try:
            x = int(input("Enter X coordinate to plant (0-7): "))
            y = int(input("Enter Y coordinate to plant (0-7): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return

        if not (0 <= x <= 7 and 0 <= y <= 7):
            print("Invalid coordinates.")
            return

        plant_type = input(f"Select a plant to plant ({', '.join(self.plant_data.keys())}): ")
        if plant_type not in self.plant_data:
            print("Invalid plant type.")
            return

        plant_data = self.plant_data[plant_type]
        plant = Plant(plant_type, plant_data)

        if self.grid.plant(x, y, plant):
            print(f"Planted {plant_type} at ({x}, {y}).")
            self.remaining_turns -= 1
        else:
            print("Cannot plant here.")

    def water_prompt(self):
        try:
            x = int(input("Enter X coordinate to water (0-7): "))
            y = int(input("Enter Y coordinate to water (0-7): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return

        if not (0 <= x <= 7 and 0 <= y <= 7):
            print("Invalid coordinates.")
            return

        cell = self.grid.get_cell(x, y)
        if cell and cell.plant:
            cell.plant.water()
            #water(self)
            print(f"Watered plant at ({x}, {y})")
            self.remaining_turns -= 1
        else:
            print("No plant to water at this location.")

    def fertilize_prompt(self):
        try:
            x = int(input("Enter X coordinate to fertilize (0-7): "))
            y = int(input("Enter Y coordinate to fertilize (0-7): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return

        if not (0 <= x <= 7 and 0 <= y <= 7):
            print("Invalid coordinates.")
            return

        cell = self.grid.get_cell(x, y)
        if cell and cell.plant:
            cell.plant.fertilize()
            print(f"Fertilized plant at ({x}, {y})")
            self.remaining_turns -= 1
            #fertilize(self)
        else:
            print("No plant to fertilize at this location.")

    def check_prompt(self):
        try:
            x = int(input("Enter X coordinate to check (0-7): "))
            y = int(input("Enter Y coordinate to check (0-7): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return

        if not (0 <= x <= 7 and 0 <= y <= 7):
            print("Invalid coordinates.")
            return

        cell = self.grid.get_cell(x, y)
        if cell and cell.plant:
            print(cell.plant.status())
            self.remaining_turns -= 1
        else:
            print("No plant at this location.")

    def advance_time(self):
        self.timer.advance_day()
        self.grid.tick(self.timer.season)
        print(f"Advanced to day {self.timer.day}, Season: {self.timer.season}")
        self.economy.simulate_market(self.timer.season)
        self.remaining_turns = self.turns_per_day

    def harvest_prompt(self):
        if self.remaining_turns <= 0:
            print("No turns left for today. Advance to the next day.")
            return

        harvested_count = 0
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell and cell.plant and cell.plant.growth_stage == 'mature':
                    plant = cell.plant
                    self.stock[plant.name] += 1  # Increase stock
                    self.grid.grid[y][x] = None  # Clear the cell
                    harvested_count += 1

        if harvested_count > 0:
            print(f"Harvested {harvested_count} crops.")
            self.remaining_turns -= 1
        else:
            print("No mature crops to harvest.")

    def sell_prompt(self):
        plant_type = input(f"Select plant to sell ({', '.join(self.plant_data.keys())}): ")
        if plant_type not in self.plant_data:
            print("Invalid plant type.")
            return

        if self.stock[plant_type] <= 0:
            print(f"You have no {plant_type} in stock to sell.")
            return

        try:
            quantity = int(input("Enter quantity to sell: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if quantity > self.stock[plant_type]:
            print(f"You only have {self.stock[plant_type]} {plant_type} in stock.")
            return

        price = self.economy.get_market_price(plant_type)
        revenue = price * quantity
        self.money += revenue
        self.stock[plant_type] -= quantity #Decrease stocks here
        print(f"Sold {quantity} {plant_type} for ${revenue:.2f}")

if __name__ == "__main__":
    game = Game()
    game.run()