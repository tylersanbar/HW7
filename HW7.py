from math import inf

class State:
    def __init__(self, x, y, value, term = False) -> None:
        self.x = x
        self.y = y
        self.term = term
        self.value = value
        self.actions = {"up" : None, "down" : None, "left" : None, "right" : None}

class World:
    def __init__(self, h, w, terminal_state, terminal_value) -> None:
        self.h = h
        self.w = w
        self.num_states = h * w
        self.states = self.populate(terminal_state, terminal_value)
        self.mapActions()

    def populate(self, terminal_state, terminal_value):
        states = []
        for i in range(self.num_states):
            if i == terminal_state:
                newState = State(i % self.w, int(i/self.h), terminal_value, True)
            else:
                newState = State(i % self.w, int(i/self.h), 0)
            states.append(newState)
        return states

    def mapActions(self):
        directions = {
        "up"   : [0, 1],
        "down" : [0,-1],
        "left" : [-1,0],
        "right": [1, 0]
        }
        for i in range(self.num_states):
            state = self.states[i]
            for direction in directions:
                nextState = self.getState(state.x + directions[direction][0], state.y + directions[direction][1])
                if nextState == None or state.term: nextState = state
                state.actions[direction] = nextState
    
    def getState(self, x, y):
        for state in self.states:
            if state.x == x and state.y == y: return state
        return None

    def printWorld(self):
        for y in reversed(range(self.h)):
            row = ""
            for x in range(self.w):
                row += str(self.getState(x, y).value) + " "
            print(row)
    
    def updateState(state, reward, discount):
        max_action_value = -inf
        if state.term: return state.value
        for action in state.actions:
            if action == "up" or "down":
                action_value = .8 * (reward + discount * state.actions[action].value) 
                + .1 * (reward + discount * state.actions["left"].value)
                + .1 * (reward + discount * state.actions["right"].value)
            else:
                action_value = .8 * (reward + discount * state.actions[action].value) 
                + .1 * (reward + discount * state.actions["up"].value)
                + .1 * (reward + discount * state.actions["down"].value)
            if action_value > max_action_value: 
                max_action_value = action_value
        return max_action_value

    def updateWorld(self, reward, discount):
        new_state_values = []
        for state in self.states:
            new_state_values.append(World.updateState(state, reward, discount))
        for i in range(self.num_states):
            self.states[i].value = new_state_values[i]
#6 7 8
#3 4 5
#0 1 2

reward = 0
k = 5
discount = .99

world = World(3, 3, 8, 10)
world.printWorld()
for i in range(k):
    print("Update: ", i)
    world.updateWorld(reward, discount)
    world.printWorld()



