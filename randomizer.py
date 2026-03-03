import random
import time

# gen random delay (i checked the average human reaction time to make the numbers seem plausible)
def random_delay(mean=0.52, std_dev=0.1, min_delay=0.2, max_delay=2):
    delay = random.gauss(mean, std_dev)
    delay = max(min_delay, min(max_delay, delay)) # clamp the delay to the specified range
    time.sleep(delay)

# gen random click position offset (Still need to test the proper radius)
def random_click_offset(x, y, radius=5):
    offset_x = int(random.gauss(0, radius))
    offset_y = int(random.gauss(0, radius))
    return x + offset_x, y + offset_y

#sim human reaction time
def random_reaction_delay(mean=0.52, std_dev=0.1):
    delay = random.gauss(mean, std_dev)
    delay = max(0.2, delay)# clamp the delay to a reasonable range
    time.sleep(delay)

#occasionally does nothing
def idle_time(chance=0.05, min_idle=1.0, max_idle=5.0): #5% chance that the bot does nothing
    if random.random() < chance: #random.random generates a random float between 0.0 and 1.0
        idle_duration = random.uniform(min_idle, max_idle)
        time.sleep(idle_duration)