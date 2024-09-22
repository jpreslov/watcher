import signal
import sys
import time

import pyautogui
import pygetwindow as gw

focused_time = 0
total_time = 0
start_time = time.time()


def signal_handler(sig, frame):
    elapsed_time = time.time() - start_time
    focus_percentage = (focused_time / total_time) * 100 if total_time > 0 else 0
    print(
        f"\nFocused Time: {focused_time} seconds, Total Time: {total_time} seconds, Focus Percentage: {focus_percentage:.2f}%"
    )
    sys.exit(0)


def get_running_apps():
    return [window.title for window in gw.getAllWindows() if window.title]


def choose_apps(tracked_apps):
    print("currently running applications:")
    running_apps = get_running_apps()

    for i, app in enumerate(running_apps):
        print(f"{i + 1}: {app}")

    print("\nEnter the number of the apps you want to track (comma-separated):")
    chosen_indices = input("Your choice: ").split(",")
    for index in chosen_indices:
        try:
            tracked_apps.append(running_apps[int(index) - 1])
        except (IndexError, ValueError):
            print(f"Invalid index: {index}")


def is_tracked_app(window_title, tracked_apps):
    return any(app.lower() in window_title.lower() for app in tracked_apps)


def log_mouse_activity(tracked_apps):
    global focused_time, total_time

    last_window_title = None

    while True:
        x, y = pyautogui.position()
        current_window = gw.getWindowsAt(x, y)

        if current_window:
            current_window_title = current_window[0].title
        else:
            current_window_title = None

        total_time += 1

        if current_window_title and is_tracked_app(current_window_title, tracked_apps):
            focused_time += 1

        if current_window_title != last_window_title:
            if current_window_title:
                print(f"Mouse moved to window: {current_window_title}")
            else:
                print(f"Mouse moved to empty area")

            last_window_title = current_window_title

        time.sleep(1)


if __name__ == "__main__":
    tracked_apps = []
    choose_apps(tracked_apps)

    if not tracked_apps:
        print("Nothing selected. Exiting")
    else:
        signal.signal(signal.SIGINT, signal_handler)
        log_mouse_activity(tracked_apps)
