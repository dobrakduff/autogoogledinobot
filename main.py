import cv2
import numpy as np
import pyautogui
import multiprocessing

# Constants
ROI_X = 400
ROI_Y = 625
ROI_WIDTH = 250
ROI_HEIGHT = 250
THRESHOLD_MAX_B = 59000
THRESHOLD_MAX_W=10000
THRESHOLD_MIN_B=10000
THRESHOLD_MIN_W=1500
WAIT_KEY_DELAY = 10  # Milliseconds
jumps_count = 0


def screen_capture(queue):
    while True:
        screen = pyautogui.screenshot(region=(ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT))
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        queue.put(frame)


def process_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    black_px_count = np.sum(gray_frame < 100)
    return black_px_count


if __name__ == '__main__':
    # Create a queue to share data between processes
    queue = multiprocessing.Queue()

    # Create and start the screen capture process
    screen_capture_process = multiprocessing.Process(target=screen_capture, args=(queue,))
    screen_capture_process.start()

    while True:
        # Retrieve the captured frame from the queue
        frame = queue.get()

        # Process the frame
        black_px_count = process_frame(frame)

        # Print pixel counts
        print("Black Pixel Count:", black_px_count)

        # Perform action based on pixel counts
        if THRESHOLD_MIN_B < black_px_count < THRESHOLD_MAX_B or THRESHOLD_MIN_W < black_px_count < THRESHOLD_MAX_W:
            pyautogui.press("up")
            jumps_count += 1

        # Display the frame
        cv2.imshow('frame', frame)

        if jumps_count == 5:
            jumps_count = 0
            ROI_X += 5

        # Exit if 'q' is pressed
        if cv2.waitKey(WAIT_KEY_DELAY) & 0xFF == ord('q'):
            break

    # Terminate the screen capture process
    screen_capture_process.terminate()

    # Close all windows
    cv2.destroyAllWindows()
