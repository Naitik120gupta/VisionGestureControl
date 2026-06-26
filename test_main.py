import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock OpenCV and MediaPipe
sys.modules["cv2"] = MagicMock()
sys.modules["mediapipe"] = MagicMock()
sys.modules["pyautogui"] = MagicMock()

from main import GestureController


class TestGestureController(unittest.TestCase):
    def setUp(self):
        self.controller = GestureController()

    def test_calculate_palm_center(self):
        # Create a mock hand_landmarks object
        mock_hand_landmarks = MagicMock()
        mock_hand_landmarks.landmark = []
        for i in range(21):
            mock_landmark = MagicMock()
            mock_landmark.x = i * 0.1
            mock_landmark.y = i * 0.2
            mock_hand_landmarks.landmark.append(mock_landmark)

        frame_width = 100
        frame_height = 200

        # palm_points = [0, 1, 5, 9, 13, 17]
        # x_sum = (0*0.1) + (1*0.1) + (5*0.1) + (9*0.1) + (13*0.1) + (17*0.1)
        #       = 0 + 0.1 + 0.5 + 0.9 + 1.3 + 1.7 = 4.5
        # (x_sum * frame_width) / 6 = (4.5 * 100) / 6 = 450 / 6 = 75.0

        # y_sum = (0*0.2) + (1*0.2) + (5*0.2) + (9*0.2) + (13*0.2) + (17*0.2)
        #       = 0 + 0.2 + 1.0 + 1.8 + 2.6 + 3.4 = 9.0
        # (y_sum * frame_height) / 6 = (9.0 * 200) / 6 = 1800 / 6 = 300.0

        expected_center = [75.0, 300.0]
        actual_center = self.controller.calculate_palm_center(
            mock_hand_landmarks, frame_width, frame_height
        )

        # Allow for small floating point inaccuracies
        self.assertAlmostEqual(actual_center[0], expected_center[0])
        self.assertAlmostEqual(actual_center[1], expected_center[1])

    @patch("main.cv2")
    def test_main_invalid_frame_handled(self, mock_cv2):
        from main import main

        # Mock the VideoCapture to return an invalid frame then stop
        mock_cap = MagicMock()
        mock_cv2.VideoCapture.return_value = mock_cap

        # isOpened will return True once, then False
        mock_cap.isOpened.side_effect = [True, False]

        # mock frame as an object with empty shape
        mock_frame = MagicMock()
        mock_frame.shape = (0, 0, 3)
        mock_cap.read.return_value = (True, mock_frame)

        # This shouldn't raise any exceptions
        try:
            main([])
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__} unexpectedly!")

        # Verify that cv2.flip wasn't called because we hit `continue`
        mock_cv2.flip.assert_not_called()

    @patch("main.pyautogui.scroll")
    def test_perform_scroll_desktop(self, mock_scroll):
        self.controller.target = "desktop"

        self.controller._perform_scroll("down")
        mock_scroll.assert_called_with(-100)

        self.controller._perform_scroll("up")
        mock_scroll.assert_called_with(100)

    @patch("main.subprocess.run")
    def test_android_swipe_command(self, mock_run):
        controller = GestureController(target="android", adb_path="adb", swipe_duration_ms=300)

        mock_run.side_effect = [
            MagicMock(stdout="Physical size: 1080x2400\n"),
            MagicMock(),
        ]

        controller._android_swipe("up")

        self.assertEqual(mock_run.call_count, 2)
        first_call_args = mock_run.call_args_list[1][0][0]
        self.assertEqual(first_call_args[:4], ["adb", "shell", "input", "swipe"])
        self.assertEqual(first_call_args[-1], "300")
        self.assertEqual(first_call_args[4:8], ["540", "1800", "540", "600"])

    @patch("main.subprocess.run")
    def test_get_android_screen_size_runtime_error(self, mock_run):
        controller = GestureController(target="android")
        mock_run.return_value = MagicMock(stdout="Some other output\nNo size info here\n")

        with self.assertRaises(RuntimeError) as context:
            controller._get_android_screen_size()

        self.assertEqual(str(context.exception), "Unable to determine Android screen size from adb")


if __name__ == "__main__":
    unittest.main()
