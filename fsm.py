from enum import Enum

from pyautogui import position
from vision import find_tree
from randomizer import random_reaction_delay, idle_time, random_delay

# Enum so that i dont have to use string literals
class State(Enum):
    SEARCH_TREE = "search_tree"
    CLICK_TREE = "click_tree"
    WAIT_CHOP = "wait_chop"

#defines the 3 states
class BotFSM:
    #standard state is seach tree
    def __init__(self, input_handler):
        self.state = State.SEARCH_TREE
        self.input_handler = input_handler
        self.tree_position = None
    #main loop
    def run(self):
        while True:
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
        position, confidence = find_tree()

        if position:
            self.tree_position = position
            self.state = State.CLICK_TREE
        else:
            #no tree found
            random_delay(mean=0.5, std_dev=0.1, min_delay=0.3, max_delay=1.0) #wait before trying again

        #function that clicks on tree
        def _click_tree(self):
            if self.tree_position:
                random_reaction_delay() #simulate human reaction
                self.input_handler.click(*self.tree_position)
                self.state = State.WAIT_CHOP
            else:
                self.state = State.SEARCH_TREE #if no tree position, go back to searching

        #function that waits for tree to vanish
    def _wait_chop(self):
        random_delay(mean=4.0, std_dev=0.8, min_delay=2.0, max_delay=7.0)
    
        #check if the tree is still there
        position, confidence = find_tree()
    
        if position:
        #tree still there, keep waiting
            self.state = State.WAIT_CHOP
        else:
            #tree is gone, find a new one
            self.tree_position = None
            self.state = State.SEARCH_TREE
