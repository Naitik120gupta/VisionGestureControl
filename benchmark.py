import time
import timeit

def original():
    last_action_time = 0
    scroll_cooldown = 0.4
    scroll_threshold = 0.05
    frame_height = 480
    vertical_movement = 50

    if time.time() - last_action_time > scroll_cooldown:
        if vertical_movement > scroll_threshold * frame_height:
            gesture = "scroll_down"
            last_action_time = time.time()
        elif vertical_movement < -scroll_threshold * frame_height:
            gesture = "scroll_up"
            last_action_time = time.time()

def optimized():
    last_action_time = 0
    scroll_cooldown = 0.4
    scroll_threshold = 0.05
    frame_height = 480
    vertical_movement = 50

    current_time = time.time()
    if current_time - last_action_time > scroll_cooldown:
        if vertical_movement > scroll_threshold * frame_height:
            gesture = "scroll_down"
            last_action_time = current_time
        elif vertical_movement < -scroll_threshold * frame_height:
            gesture = "scroll_up"
            last_action_time = current_time

if __name__ == "__main__":
    t_orig = timeit.timeit(original, number=1000000)
    t_opt = timeit.timeit(optimized, number=1000000)

    print(f"Original:  {t_orig:.4f} seconds")
    print(f"Optimized: {t_opt:.4f} seconds")
    if t_orig > t_opt:
        print(f"Improvement: {(t_orig - t_opt) / t_orig * 100:.2f}%")
