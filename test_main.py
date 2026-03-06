import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock OpenCV and MediaPipe
sys.modules['cv2'] = MagicMock()
sys.modules['mediapipe'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()

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
        actual_center = self.controller.calculate_palm_center(mock_hand_landmarks, frame_width, frame_height)

        # Allow for small floating point inaccuracies
        self.assertAlmostEqual(actual_center[0], expected_center[0])
        self.assertAlmostEqual(actual_center[1], expected_center[1])

if __name__ == '__main__':
    unittest.main()