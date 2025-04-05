class Timer:
    def __init__(self):
        self.day = 1
        self.seasons = ['spring', 'summer', 'autumn', 'winter']
        self.season_index = 0
        self.season = self.seasons[self.season_index]

    def advance_day(self):
        self.day += 1
        if self.day > 90:
            self.day = 1
            self.season_index = (self.season_index + 1) % len(self.seasons)
            self.season = self.seasons[self.season_index]