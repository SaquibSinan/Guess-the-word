class OfflineScoring:
    def __init__(self,level):
        self.level=level
    def calculate_points(self,game_state):
        if game_state.won:
            return self.win_points(game_state.hints_used)
        if game_state.forfeited:
            return self.forfeit_points()
        return 0
    def win_points(self,hints_used):
        base_point=self.level*100
        penalty=hints_used*0.15
        points=base_point*(1-penalty)
        return int(points)
    def forfeit_points(self):
        return int(-(self.level*25))