class Plant:
    def __init__(self, name, data):
        self.name = name
        self.fertilizer_requirement = data['fertilizer_requirement']
        self.water_requirement = data['water_requirement']
        self.growth_cycle = data['growth_cycle']
        self.health = 100
        self.growth_stage = 'planting'
        self.days_grown = 0
        self.symbol = data['symbol']

    def grow(self, season):
        if self.growth_stage == 'mature':
            return

        self.days_grown += 1
        if self.growth_stage == 'planting':
            if self.days_grown > 3:
                self.growth_stage = 'growing'
        elif self.growth_stage == 'growing':
            if self.days_grown >= self.growth_cycle[1]: # Use upper bound of growth cycle
                self.growth_stage = 'mature'

        # Health decrease
        if season != 'summer':
            self.health -= 5
            self.health = max(0, self.health)  # Ensure health doesn't go below 0

    def water(self):
        self.health += 20
        self.health = min(100, self.health)

    def fertilize(self):
        self.health += 30
        self.health = min(100, self.health)

    def status(self):
        return f"Plant: {self.name}, Stage: {self.growth_stage}, Health: {self.health}"

    @property
    def symbol(self):
        return self._symbol  # Access symbol using a property

    @symbol.setter
    def symbol(self, value):
        self._symbol = value