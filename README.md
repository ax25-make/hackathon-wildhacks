# AI Farming Game - WildHacks 2025


# Overview


This project is a simple farming simulation game developed for the WildHacks 2025 hackathon. Players can manage a grid of land, plant seeds, water and fertilize their crops, harvest them, and sell them in a dynamic market. The goal is to grow your farm and accumulate wealth.


# Technologies Used


* **Frontend:**
   * React (JavaScript library for building user interfaces)
   * Axios (for making HTTP requests to the backend)
   * CSS (for styling)
   * Dependencies:npm install, npm install axios


* **Backend:**
   * Python 3
   * Flask (micro web framework for Python)
   * Flask-CORS (for handling Cross-Origin Resource Sharing)
   * Dependencies: pip3 install flask, python3 -m pip install python-dotenv, pip install google-genai




# How to Play


1.  **View Game State:** The current state of your farm (money, day, season, market prices, stock, seeds) is displayed at the top of the game page.
2.  **Perform Actions:** Use the buttons in the "Actions" section to interact with your farm:
   * **Plant:** Select "Plant" and then click on an empty grid cell. You will be prompted to enter the type of seed you want to plant (make sure you have seeds of that type in your stock). The first letter of the plant name will appear in the cell.
   * **Water:** Select "Water" and click on a planted cell to water the plant, improving its health.
   * **Fertilize:** Select "Fertilize" and click on a planted cell to fertilize the plant, further improving its health.
   * **Check:** Select "Check" and click on a grid cell to view the status (name, growth stage, health) of any plant in that cell. The status will be displayed below the action buttons.
   * **Harvest All:** Click this button to harvest all mature plants on your grid. Harvested crops will be added to your stock.
   * **Buy Seed:** Click this button and enter the plant type and quantity of seeds you want to purchase. The cost will be deducted from your money.
   * **Sell Crop:** Click this button and enter the plant type and quantity of crops you want to sell. The earnings will be added to your money based on the current market prices.
   * **Advance Day:** Click this button to advance to the next day. Plants will grow, seasons might change, and market prices may fluctuate. Your remaining turns for the day will also reset.
3.  **Manage Your Farm:** Strategically plant, water, and fertilize your crops to ensure healthy growth. Monitor the market prices to decide when to sell your harvested goods for the best profit. Buy seeds when you need them to continue planting.




# Credits


This game was developed by Alex (backend), Isaac (backend), Helmer (frontend) and Carlos (frontend) for the WildHacks 2025 hackathon.
