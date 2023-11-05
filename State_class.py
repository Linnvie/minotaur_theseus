class State():
    def __init__(self, game):
        self.game = game
        self.pre_state = None

    def update(self):
        pass
        
    def render(self, window):
        pass

    def enter_state(self):
        if len(self.game.state_stack)>1:
            self.pre_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
