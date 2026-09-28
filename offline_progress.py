class OfflineProgress:
    def __init__(self):
        self.points = 0
        self.level = 1

    def add_points(self, points):
        self.points += points
        self.update_level()

    def update_level(self):
        if self.points>=5500 and self.level<7:
            self.level=7
        elif self.points>=4200 and self.level<6 :
            self.level=6
        elif self.points>=3000 and self.level<5:
            self.level=5
        elif self.points>=2000 and self.level<4:
            self.level=4
        elif self.points>=1200 and self.level<3:
            self.level=3
        elif self.points>=500 and self.level<2:
            self.level=2
    
    def can_play(self,level):
        return level<=self.level
