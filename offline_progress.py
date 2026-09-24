class OfflineProgress:
    def __init__(self):
        self.points=0
        self.level=1
    def add_points(self,points):
        self.points+=points
        self.update_level()
    def update_level(self):
        if self.points>=5500:
            self.level=7
        elif self.points>=4200:
            self.level=6
        elif self.points>=3000:
            self.level=5
        elif self.points>=2000:
            self.level=4
        elif self.points>=1200:
            self.level=3
        elif self.points>=500:
            self.level=2
        else:
            self.level=1
    def can_play(self,level):
        return level<=self.level