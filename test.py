import time
import numpy as np
from randomizer import random_delay, random_click_offset, random_reaction_delay
from vision import screen_capture, find_tree, check_xp_drop

passed = 0
failed = 0

def test(name, fn):
    global passed, failed
    try:
        fn()
        print(f"[PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"[FAIL] {name} — {e}")
        failed += 1

# ── randomizer tests ──────────────────────────────────────────

def test_random_delay():
    start = time.time()
    random_delay(mean=0.5, std_dev=0.1, min_delay=0.2, max_delay=1.0)
    elapsed = time.time() - start
    assert 0.2 <= elapsed <= 1.0, f"Delay out of range: {elapsed:.3f}s"

def test_random_delay_clamped():
    # run 20 times and check it never goes below min or above max
    for _ in range(20):
        start = time.time()
        random_delay(mean=0.3, std_dev=0.5, min_delay=0.1, max_delay=0.5)
        elapsed = time.time() - start
        assert 0.1 <= elapsed <= 0.6, f"Delay out of range: {elapsed:.3f}s"

def test_random_reaction_delay():
    start = time.time()
    random_reaction_delay()
    elapsed = time.time() - start
    assert 0.1 <= elapsed <= 1.0, f"Reaction delay out of range: {elapsed:.3f}s"

def test_random_click_offset_range():
    for _ in range(100):
        x, y = random_click_offset(100, 100, radius=5)
        assert 85 <= x <= 115, f"x out of range: {x}"
        assert 85 <= y <= 115, f"y out of range: {y}"

def test_random_click_offset_type():
    x, y = random_click_offset(200, 300, radius=10)
    assert isinstance(x, int), f"x is not int: {type(x)}"
    assert isinstance(y, int), f"y is not int: {type(y)}"

# ── vision tests ──────────────────────────────────────────────

def test_screen_capture_returns_array():
    img = screen_capture()
    assert img is not None
    assert isinstance(img, np.ndarray)

def test_screen_capture_shape():
    img = screen_capture()
    assert len(img.shape) == 3, f"Expected 3 dimensions, got {len(img.shape)}"
    assert img.shape[2] == 3, f"Expected 3 channels (BGR), got {img.shape[2]}"

def test_screen_capture_with_region():
    img = screen_capture(region=(0, 0, 200, 200))
    assert img is not None
    assert isinstance(img, np.ndarray)

def test_find_tree_returns_tuple():
    position, confidence = find_tree()
    assert isinstance(confidence, float), f"Confidence is not float: {type(confidence)}"
    if position is not None:
        assert isinstance(position, tuple), f"Position is not tuple: {type(position)}"
        assert len(position) == 2, f"Position should have 2 values: {position}"

def test_find_tree_confidence_range():
    _, confidence = find_tree()
    assert 0.0 <= confidence <= 1.0, f"Confidence out of range: {confidence}"

def test_check_xp_drop_returns_bool():
    result = check_xp_drop(xp_region=(0, 0, 100, 50))
    assert isinstance(result, bool), f"Expected bool, got {type(result)}"

# ── run all tests ─────────────────────────────────────────────

print("
=== Running Tests ===
")

test("random_delay stays within bounds", test_random_delay)
test("random_delay clamps correctly", test_random_delay_clamped)
test("random_reaction_delay stays within bounds", test_random_reaction_delay)
test("random_click_offset stays within range", test_random_click_offset_range)
test("random_click_offset returns integers", test_random_click_offset_type)
test("screen_capture returns numpy array", test_screen_capture_returns_array)
test("screen_capture has correct shape", test_screen_capture_shape)
test("screen_capture works with region", test_screen_capture_with_region)
test("find_tree returns correct types", test_find_tree_returns_tuple)
test("find_tree confidence in range 0-1", test_find_tree_confidence_range)
test("check_xp_drop returns bool", test_check_xp_drop_returns_bool)

print(f"
=== Results: {passed} passed, {failed} failed ===")