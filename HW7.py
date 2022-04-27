from math import inf

class State:
    def __init__(self, x, y, value, term = False) -> None:
        self.x = x
        self.y = y
        self.term = term
        self.value = value
        self.actions = {"up" : None, "down" : None, "left" : None, "right" : None}
    
    def __repr__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"

class World:
    def __init__(self, h, w, terminal_state, terminal_value, discount, reward, policy, transitionModel) -> None:
        self.h = h
        self.w = w
        self.num_states = h * w
        self.states = self.populate(terminal_state, terminal_value)
        self.discount = discount
        self.reward = reward
        self.policy = policy
        self.transitionModel = transitionModel
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
    #6 7 8
    #3 4 5
    #0 1 2
    def printWorld(self):
        for y in reversed(range(self.h)):
            row = ""
            for x in range(self.w):
                row += str(self.getState(x, y).value) + " "
            print(row)

    def maxActionValue(self, state):
        max_action_value = -inf
        if state.term: return state.value
        for action in state.actions:
            action_value = self.actionValue(state, action)
            if action_value > max_action_value: max_action_value = action_value
        return max_action_value
    
    def maxAction(self, state):
        max_action_value = -inf
        max_action = None
        if state.term: return "exit"
        for action in state.actions:
            action_value = self.actionValue(state, action)
            if action_value > max_action_value: 
                max_action_value = action_value
                max_action = action
        return max_action

    def actionValue(self, state, action):
        if state.term: return state.value
        action_value = 0
        for next_state in self.states:
            action_value += self.transitionModel(state, action, next_state) * (self.reward + self.discount * next_state.value) 
        return action_value

    def updateWorld(self):
        new_state_values = []
        for state in self.states:
            new_state_values.append(self.actionValue(state, self.policy(self, state)))
        for i in range(self.num_states):
            self.states[i].value = new_state_values[i]
    
    def updatePolicy(self):
        for state in self.policyMap.keys():
            self.policyMap[state] = self.maxAction(state)
    
    def printPolicy(self):
        for state in self.policyMap.keys():
            print("State: ", state, ", Action: ", self.policyMap[state])

def transitionModel(state, action, nextState):
    if action == "up" or action ==  "down":
        if state.actions[action] == nextState: return .8
        elif state.actions["left"] == nextState or state.actions["right"] == nextState: return .1
        else: return 0
    else:
        if state.actions[action] == nextState: return .8
        elif state.actions["up"] == nextState or state.actions["down"] == nextState: return .1
        else: return 0

def maxPolicy(self, state):
    return self.maxAction(state)

def eastPolicy(self, state):
    try:
        return self.policyMap[state]
    except:
        self.policyMap = { key : "right" for key in self.states }
        return self.policyMap[state]

def exercise1a():
    k = 5
    discount = .99
    for reward in [10, 0, -100]:
        print("Reward = ", reward)
        world = World(3, 3, 8, 10, discount, reward, maxPolicy, transitionModel)
        world.printWorld()
        for i in range(k):
            print("Update: ", i)
            world.updateWorld()
            world.printWorld()

def exercise1b():
    k = 2
    discount = .99
    reward = 0
    world = World(3, 3, 8, 10, discount, reward, eastPolicy, transitionModel)
    world.printWorld()
    world.updateWorld()
    world.printWorld()
    world.updatePolicy()
    world.printPolicy()

exercise1b()