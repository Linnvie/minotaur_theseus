from State_class import State

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta_time, actions):
        self.game.reset_keys()
    
    def render(self, window):
        window.fill((255,255,255))
        self.game.draw_text(window, "Game_state", (0,0,0), 720/2, 360/2)