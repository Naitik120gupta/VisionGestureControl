import cv2
import mediapipe as mp
import pyautogui
import subprocess
import argparse
import time


class GestureController:
    def __init__(self, target="desktop", adb_path="adb", swipe_duration_ms=250):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.scroll_cooldown = 0.4  # seconds between scroll actions
        self.last_action_time = time.time()
        self.prev_hand_position = None

        # Gesture thresholds
        self.scroll_threshold = 0.05
        self.target = target
        self.adb_path = adb_path
        self.swipe_duration_ms = swipe_duration_ms
        self._screen_size = None

    def detect_gestures(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = frame.shape

        results = self.hands.process(rgb_frame)

        gesture = "none"

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            # Draw landmarks on the frame
            self.mp_drawing.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
            )

            palm_center = self.calculate_palm_center(
                hand_landmarks, frame_width, frame_height
            )

            if self.prev_hand_position is not None:
                vertical_movement = palm_center[1] - self.prev_hand_position[1]

                current_time = time.time()
                if current_time - self.last_action_time > self.scroll_cooldown:
                    if vertical_movement > self.scroll_threshold * frame_height:
                        gesture = "scroll_down"
                        self.last_action_time = current_time
                    elif vertical_movement < -self.scroll_threshold * frame_height:
                        gesture = "scroll_up"
                        self.last_action_time = current_time

                cv2.putText(
                    frame,
                    f"V-Move: {vertical_movement:.2f}",
                    (10, 60),
                    cv2.FONT_HERSHEY_PLAIN,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            # Update previous hand position
            self.prev_hand_position = palm_center

            cv2.circle(
                frame, (int(palm_center[0]), int(palm_center[1])), 10, (0, 255, 0), -1
            )
        else:
            self.prev_hand_position = None

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 30),
            cv2.FONT_HERSHEY_PLAIN,
            0.7,
            (0, 0, 255),
            2,
        )

        return frame, gesture

    def calculate_palm_center(self, hand_landmarks, frame_width, frame_height):
        """Calculate the center of the palm based on hand landmarks."""

        palm_points = [0, 1, 5, 9, 13, 17]

        x_sum = sum(hand_landmarks.landmark[point].x for point in palm_points)
        y_sum = sum(hand_landmarks.landmark[point].y for point in palm_points)

        return [
            (x_sum * frame_width) / len(palm_points),
            (y_sum * frame_height) / len(palm_points),
        ]

    def execute_action(self, gesture):
        """Execute the action corresponding to the detected gesture."""
        if gesture == "scroll_down":
            self._perform_scroll("down")
        elif gesture == "scroll_up":
            self._perform_scroll("up")

    def _perform_scroll(self, direction):
        if self.target == "android":
            self._android_swipe(direction)
            print(f"Swiping {direction} on Android")
        else:
            if direction == "down":
                pyautogui.scroll(-100)
            else:
                pyautogui.scroll(100)
            print(f"Scrolling {direction}")

    def _get_android_screen_size(self):
        if self._screen_size is not None:
            return self._screen_size

        result = subprocess.run(
            [self.adb_path, "shell", "wm", "size"],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in result.stdout.splitlines():
            if "Physical size:" in line:
                size_text = line.split(":", 1)[1].strip()
                width_text, height_text = size_text.split("x", 1)
                self._screen_size = (int(width_text), int(height_text))
                return self._screen_size

        raise RuntimeError("Unable to determine Android screen size from adb")

    def _android_swipe(self, direction):
        screen_width, screen_height = self._get_android_screen_size()
        x = screen_width // 2
        start_y = int(screen_height * 0.75)
        end_y = int(screen_height * 0.25)

        if direction == "down":
            start_y, end_y = end_y, start_y

        subprocess.run(
            [
                self.adb_path,
                "shell",
                "input",
                "swipe",
                str(x),
                str(start_y),
                str(x),
                str(end_y),
                str(self.swipe_duration_ms),
            ],
            check=True,
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hand gesture scroll controller")
    parser.add_argument(
        "--target",
        choices=["desktop", "android"],
        default="desktop",
        help="Where the gesture should scroll",
    )
    parser.add_argument(
        "--adb-path",
        default="adb",
        help="ADB executable path when target is android",
    )
    parser.add_argument(
        "--swipe-duration-ms",
        type=int,
        default=250,
        help="Swipe duration in milliseconds for Android scrolling",
    )
    args = parser.parse_args(argv)

    controller = GestureController(
        target=args.target,
        adb_path=args.adb_path,
        swipe_duration_ms=args.swipe_duration_ms,
    )

    cap = cv2.VideoCapture(0)

    print("=== Hand Gesture Social Media Controller ===")
    print("Hold your hand in front of the camera")
    print("Move your hand up/down to scroll")
    if args.target == "android":
        print("Android mode enabled: requires USB debugging and adb")
    print("Press 'q' to quit")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to capture video")
            break

        # Validate frame dimensions to prevent downstream processing errors
        if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print("Invalid video frame received")
            continue

        frame = cv2.flip(frame, 1)

        frame, gesture = controller.detect_gestures(frame)

        controller.execute_action(gesture)

        cv2.imshow("Hand Gesture Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
