import time
import numpy as np
import pytest
from randomizer import random_delay, random_click_offset, random_reaction_delay
from vision import screen_capture, find_tree, check_xp_drop

# ── randomizer tests ──────────────────────────────────────────

def test_random_delay_within_bounds():
    start = time.time()
    random_delay(mean=0.5, std_dev=0.1, min_delay=0.2, max_delay=1.0)
    elapsed = time.time() - start
    assert 0.2 <= elapsed <= 1.0

def test_random_delay_clamped():
    for _ in range(20):
        start = time.time()
        random_delay(mean=0.3, std_dev=0.5, min_delay=0.1, max_delay=0.5)
        elapsed = time.time() - start
        assert 0.1 <= elapsed <= 0.6

def test_random_reaction_delay_within_bounds():
    start = time.time()
    random_reaction_delay()
    elapsed = time.time() - start
    assert 0.1 <= elapsed <= 1.0

def test_random_click_offset_range():
    for _ in range(100):
        x, y = random_click_offset(100, 100, radius=5)
        assert 85 <= x <= 115
        assert 85 <= y <= 115

def test_random_click_offset_returns_integers():
    x, y = random_click_offset(200, 300, radius=10)
    assert isinstance(x, int)
    assert isinstance(y, int)

# ── vision tests ──────────────────────────────────────────────

def test_screen_capture_returns_array():
    img = screen_capture()
    assert img is not None
    assert isinstance(img, np.ndarray)

def test_screen_capture_correct_shape():
    img = screen_capture()
    assert len(img.shape) == 3
    assert img.shape[2] == 3

def test_screen_capture_with_region():
    img = screen_capture(region=(0, 0, 200, 200))
    assert img is not None
    assert isinstance(img, np.ndarray)

def test_find_tree_returns_correct_types():
    position, confidence = find_tree()
    assert isinstance(confidence, float)
    if position is not None:
        assert isinstance(position, tuple)
        assert len(position) == 2

def test_find_tree_confidence_in_range():
    _, confidence = find_tree()
    assert 0.0 <= confidence <= 1.0

def test_check_xp_drop_returns_bool():
    result = check_xp_drop(xp_region=(0, 0, 100, 50))
    assert isinstance(result, bool)