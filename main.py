import cv2
import numpy as np
import pyautogui

# Constants
ROI_X = 400
ROI_Y = 550
ROI_WIDTH = 255
ROI_HEIGHT = 250
THRESHOLD_MIN_B = 5000
THRESHOLD_MIN_W=1000
THRESHOLD_MAX = 30000
WAIT_KEY_DELAY = 10  # Milliseconds

while True:
    # Capture screen
    screen = pyautogui.screenshot(region=(ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT))
    frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Count black and white pixels
    black_px_count = np.sum(gray_frame < 100)
    white_px_count = np.sum(gray_frame > 100)

    # Print pixel counts
    print(white_px_count, ROI_X,black_px_count)

    # Perform action based on pixel counts
    if THRESHOLD_MIN_B < black_px_count < THRESHOLD_MAX or THRESHOLD_MIN_W < white_px_count < THRESHOLD_MAX:
        pyautogui.press("up")
        ROI_X += 2

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(WAIT_KEY_DELAY) & 0xFF == ord('q'):
        break

# Close all windows
cv2.destroyAllWindows()
