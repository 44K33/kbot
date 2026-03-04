from enum import Enum
from vision import find_tree, is_inventory_full
from randomizer import random_reaction_delay, idle_time, random_delay, random_click_offset

# Enum so that i dont have to use string literals
class State(Enum):
    SEARCH_TREE = "search_tree"
    CLICK_TREE = "click_tree"
    WAIT_CHOP = "wait_chop"
    DROP_LOGS = "drop_logs"

#defines the states
class BotFSM:
    #standard state is search tree
    def __init__(self, input_handler, region=None, inventory_region=None, state_callback=None, log_callback=None):
        self.state = State.SEARCH_TREE
        self.input_handler = input_handler
        self.region = region
        self.inventory_region = inventory_region
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

            elif self.state == State.DROP_LOGS:
                self._drop_logs()

    #function that looks for the tree
    def _search_tree(self):
        # check inventory first before searching for a tree
        if self.inventory_region and is_inventory_full(self.inventory_region):
            self._log("Inventory full, dropping logs...")
            self._set_state(State.DROP_LOGS)
            return

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

    def _drop_logs(self):
        if not self.inventory_region:
            self._set_state(State.SEARCH_TREE)
            return

        inv_x, inv_y, inv_w, inv_h = self.inventory_region
        slot_w = inv_w / 4
        slot_h = inv_h / 7

        self._log("Dropping all logs...")
        self.input_handler.hold_shift()  # hold shift now

        for slot in range(28):
            col = slot % 4
            row = slot // 4
            slot_x = int(inv_x + col * slot_w + slot_w / 2)
            slot_y = int(inv_y + row * slot_h + slot_h / 2)

            slot_x, slot_y = random_click_offset(slot_x, slot_y, radius=3)
            self.input_handler.click((slot_x, slot_y))
            random_delay(mean=0.15, std_dev=0.03, min_delay=0.1, max_delay=0.3)

        self.input_handler.release_shift()  # release after all slots done
        self._log("Logs dropped, resuming...")
        random_delay(mean=1.0, std_dev=0.2, min_delay=0.8, max_delay=1.5)
        self._set_state(State.SEARCH_TREE)