from enum import Enum
from vision import find_tree
from randomizer import random_reaction_delay, idle_time, random_delay

# Enum so that i dont have to use string literals
class State(Enum):
    SEARCH_TREE = "search_tree"
    CLICK_TREE = "click_tree"
    WAIT_CHOP = "wait_chop"

#defines the 3 states
class BotFSM:
    #standard state is search tree
    def __init__(self, input_handler, region=None, state_callback=None, log_callback=None):
        self.state = State.SEARCH_TREE
        self.input_handler = input_handler
        self.region = region
        self.state_callback = state_callback
        self.log_callback = log_callback
        self.tree_position = None
        self.running = True

    def stop(self):
        self.running = False

    def _set_state(self, state):
        self.state = state
        if self.state_callback:
            self.state_callback(state.value)

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    #main loop
    def run(self):
        while self.running:
            idle_time() #occasionally does nothing to seem more human

            if self.state == State.SEARCH_TREE:
                self._search_tree()

            elif self.state == State.CLICK_TREE:
                self._click_tree()

            elif self.state == State.WAIT_CHOP:
                self._wait_chop()

    #function that looks for the tree
    def _search_tree(self):
        #find_tree returns confidence aswell but we dont need it so it doesnt matter :)
        position, confidence = find_tree(region=self.region)

        if position:
            self.tree_position = position
            self._log(f"Tree found at {position}")
            self._set_state(State.CLICK_TREE)
        else:
            #no tree found
            self._log("No tree found, retrying...")
            random_delay(mean=0.5, std_dev=0.1, min_delay=0.3, max_delay=1.0)

    #function that clicks on tree
    def _click_tree(self):
        if self.tree_position:
            random_reaction_delay()
            #offset position by region origin
            if self.region:
                actual_x = self.tree_position[0] + self.region[0]
                actual_y = self.tree_position[1] + self.region[1]
                self.input_handler.click((actual_x, actual_y))
            else:
                self.input_handler.click(self.tree_position)
            self._log(f"Clicked tree at {self.tree_position}")
            self._set_state(State.WAIT_CHOP)
        else:
            self._set_state(State.SEARCH_TREE)

    #checks if the same tree is still there
    def _is_same_tree(self, tolerance=10):
        new_position, _ = find_tree(region=self.region)
        if new_position is None:
            return False
        dx = abs(new_position[0] - self.tree_position[0])
        dy = abs(new_position[1] - self.tree_position[1])
        return dx <= tolerance and dy <= tolerance

    def _wait_chop(self):
        random_delay(mean=4.0, std_dev=0.8, min_delay=2.0, max_delay=7.0)

        if self._is_same_tree():
            self._log("Tree still standing, waiting...")
            self._set_state(State.WAIT_CHOP)
        else:
            self._log("Tree chopped, searching for next...")
            self.tree_position = None
            self._set_state(State.SEARCH_TREE)