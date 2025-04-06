from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game


app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Temporary global instance (in production, use session/user-based handling)
game = Game()

# Helper to serialize grid state
def serialize_grid(grid):
    result = []
    for y in range(grid.height):
        row = []
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            if cell and cell.plant:
                row.append({
                    'type': cell.plant.name,
                    'growth_stage': cell.plant.growth_stage,
                    'health': cell.plant.health,  # Use health instead of water_level/fertilizer_level
                    'days_grown': cell.plant.days_grown
                })
            else:
                row.append(None)
        result.append(row)
    return result

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({
        'grid': serialize_grid(game.grid),
        'money': game.money,
        'day': game.timer.day,
        'season': game.timer.season,
        'remaining_turns': game.remaining_turns,
        'market_prices': game.economy.market_prices,
        'stock': game.stock,
        'seeds': game.seeds,
    })

@app.route('/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')

    if action == 'plant':
        return plant(data)
    elif action == 'water':
        return water(data)
    elif action == 'fertilize':
        return fertilize(data)
    elif action == 'check':
        return check(data)
    elif action == 'harvest':
        return harvest()
    else:
        return jsonify({'error': 'Invalid action'}), 400

@app.route('/advance', methods=['POST'])
def advance():
    game.advance_time()
    return jsonify({'message': 'Day advanced'})

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    plant_type = data.get('plant_type')
    quantity = int(data.get('quantity', 0))

    if plant_type not in game.plant_data:
        return jsonify({'error': 'Invalid plant type'}), 400

    price = game.economy.get_market_price(plant_type) * game.seed_price_multiplier
    cost = price * quantity

    if game.money < cost:
        return jsonify({'error': 'Not enough money'}), 400

    game.money -= cost
    game.seeds[plant_type] += quantity
    game.remaining_turns -= 1
    game.money -= game.action_cost

    return jsonify({'message': f'Bought {quantity} {plant_type} seeds'})

@app.route('/sell', methods=['POST'])
def sell():
    data = request.json
    plant_type = data.get('plant_type')
    quantity = int(data.get('quantity', 0))

    if plant_type not in game.plant_data:
        return jsonify({'error': 'Invalid plant type'}), 400

    if game.stock[plant_type] < quantity:
        return jsonify({'error': 'Not enough stock'}), 400

    price = game.economy.get_market_price(plant_type)
    revenue = price * quantity

    game.money += revenue
    game.stock[plant_type] -= quantity
    game.remaining_turns -= 1
    game.money -= game.action_cost

    return jsonify({'message': f'Sold {quantity} {plant_type} for ${revenue:.2f}'})

# --- Action Handlers ---
def plant(data):
    x = int(data.get('x', -1))
    y = int(data.get('y', -1))
    plant_type = data.get('plant_type')

    if not (0 <= x < 8 and 0 <= y < 8):
        return jsonify({'error': 'Invalid coordinates'}), 400

    if plant_type not in game.plant_data:
        return jsonify({'error': 'Invalid plant type'}), 400

    if game.seeds[plant_type] <= 0:
        return jsonify({'error': 'Not enough seeds'}), 400

    from plant import Plant
    plant_data = game.plant_data[plant_type]
    plant = Plant(plant_type, plant_data)

    if game.grid.plant(x, y, plant):
        game.seeds[plant_type] -= 1
        game.remaining_turns -= 1
        game.money -= game.action_cost
        return jsonify({'message': f'Planted {plant_type} at ({x}, {y})'})
    else:
        return jsonify({'error': 'Cannot plant here'}), 400

def water(data):
    x = int(data.get('x', -1))
    y = int(data.get('y', -1))
    cell = game.grid.get_cell(x, y)
    if cell and cell.plant:
        cell.plant.water()
        game.remaining_turns -= 1
        game.money -= game.action_cost
        return jsonify({'message': f'Watered plant at ({x}, {y})'})
    return jsonify({'error': 'No plant to water'}), 400

def fertilize(data):
    x = int(data.get('x', -1))
    y = int(data.get('y', -1))
    cell = game.grid.get_cell(x, y)
    if cell and cell.plant:
        cell.plant.fertilize()
        game.remaining_turns -= 1
        game.money -= game.action_cost
        return jsonify({'message': f'Fertilized plant at ({x}, {y})'})
    return jsonify({'error': 'No plant to fertilize'}), 400

def check(data):
    x = int(data.get('x', -1))
    y = int(data.get('y', -1))
    cell = game.grid.get_cell(x, y)
    if cell and cell.plant:
        status = cell.plant.status()
        game.remaining_turns -= 1
        game.money -= game.action_cost
        return jsonify({'status': status})
    return jsonify({'error': 'No plant at location'}), 400

def harvest():
    harvested_count = 0
    for y in range(game.grid.height):
        for x in range(game.grid.width):
            cell = game.grid.get_cell(x, y)
            if cell and cell.plant and cell.plant.growth_stage == 'mature':
                plant = cell.plant
                game.stock[plant.name] += 1
                game.grid.grid[y][x] = None
                harvested_count += 1

    if harvested_count > 0:
        game.remaining_turns -= 1
        game.money -= game.action_cost
        return jsonify({'message': f'Harvested {harvested_count} crops'})
    return jsonify({'message': 'No crops to harvest'})

if __name__ == '__main__':
    app.run(debug=True)