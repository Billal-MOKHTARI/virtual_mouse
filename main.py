from threading import Thread
import pyautogui
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from playsound import playsound
from os.path import join
import configparser
from functions import *

# Load configuration file
config = configparser.ConfigParser()
config.read('./configfile.ini')

# Load each section to a variable
fingers = config['fingers']
hand_det_params = config['hand_detector_parameters']
scr_rnd_name = config['screenshot_random_name']
right_hand = config['right_hand']
left_hand = config['left_hand']
threshold_line = config['threshold_line']
extra = config['extra']

"""Constants : it's divided into nine sections :
    1. Get the landmarks from "hand detector landmarks.png" to see which one correspons to each finger
    2. Screen Size and image display size
    3. Hand detector parameters
    4. Random generation numbers
    5. Right hand gestures
    6. Left hand gestures
    7. Paths
    8. Threshold line
    9. Additional parameters
"""
THUMB = int(fingers['THUMB']) 
INDEX = int(fingers['INDEX'])
MIDDLE = int(fingers['MIDDLE'])
RING = int(fingers['RING'])
PINKY = int(fingers['PINKY'])

SCREEN_WIDTH = pyautogui.size().width
SCREEN_HEIGHT = pyautogui.size().height 
WIDTH = 300
HEIGHT = int(WIDTH*SCREEN_HEIGHT/SCREEN_WIDTH)
TITLE = 'Cam'

DETECTION_CONFIDENCE = float(hand_det_params['DETECTION_CONFIDENCE'])
MAX_HANDS = int(hand_det_params['MAX_HANDS'])

MIN_VALUE = scr_rnd_name['MIN_VALUE']
MAX_VALUE = scr_rnd_name['MAX_VALUE']

MOVE_POINTER = str_preprocessing(right_hand['MOVE_POINTER'])
DRAG = str_preprocessing(right_hand['DRAG'])
LEFT_CLICK = str_preprocessing(right_hand['LEFT_CLICK'])
RIGHT_CLICK = str_preprocessing(right_hand['RIGHT_CLICK'])
DOUBLE_CLICK = str_preprocessing(right_hand['DOUBLE_CLICK'])
SCROLL_UP = str_preprocessing(right_hand['SCROLL_UP'])
SCROLL_DOWN = str_preprocessing(right_hand['SCROLL_DOWN'])
SCROLL_LEFT = str_preprocessing(right_hand['SCROLL_LEFT'])
SCROLL_RIGHT = str_preprocessing(right_hand['SCROLL_RIGHT'])

SCREENSHOT = str_preprocessing(left_hand['SCREENSHOT'])
COPY = str_preprocessing(left_hand['COPY'])
CUT = str_preprocessing(left_hand['CUT'])
PASTE = str_preprocessing(left_hand['PASTE'])
SELECT_ALL = str_preprocessing(left_hand['SELECT_ALL'])
QUIT = str_preprocessing(left_hand['QUIT'])
ENTER = str_preprocessing(left_hand['ENTER'])

SCREENSHOT_PATH = 'C:\\Users\\Billal\\Pictures\\Screenshots\\'+str(np.random.randint(MIN_VALUE, MAX_VALUE))+'.png'
SOUND_PATH = 'assets/sounds'
IMAGE_PATH = 'assets/images'
SINGLE_CLICK_PATH = join(SOUND_PATH, 'single_click.mp3')
DOUBLE_CLICK_PATH = join(SOUND_PATH, 'double_click.mp3')
COPY_PATH = join(SOUND_PATH, 'copy.wav')
PASTE_PATH = join(SOUND_PATH, 'paste.wav')
SCREENSHOT_SOUND_PATH = join(SOUND_PATH, 'screenshot.wav')
CURSOR_TRIGGER_PATH = join(IMAGE_PATH, 'mouse_cursor_1.png')
KEYBOARD_PRESS_PATH = join(SOUND_PATH, 'keyboard_press.mp3')

THRESHOLD = int(threshold_line['THRESHOLD'])
COLOR = str_preprocessing(threshold_line['COLOR'], to = tuple)

BUTTON_DELAY = int(extra['BUTTON_DELAY'])
SCROLL_SPEED = int(extra['SCROLL_SPEED'])

SMOOTHING = int(extra['SMOOTHING'])
# Set the video capture
cap = cv2.VideoCapture(0)
cap.set(3, SCREEN_WIDTH)
cap.set(4, SCREEN_HEIGHT)

# Hand Detector 
detector = HandDetector(detectionCon=DETECTION_CONFIDENCE, maxHands=MAX_HANDS)

# Delay management
button_pressed = False
button_counter = 0

"""Interpolation parameters :
    - xxp --> xfp
    - yxp --> yfp
"""
xxp = [SCREEN_WIDTH//2-200, SCREEN_WIDTH-400]
yxp = [200, SCREEN_HEIGHT-300]
xfp = [0, SCREEN_WIDTH]
yfp = [0, SCREEN_HEIGHT]
plocX = 0
plocY = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, flipType=False)        # Detect and show hands on the image 
    cv2.line(frame, (0, THRESHOLD), (SCREEN_WIDTH, THRESHOLD), COLOR, 3)
    img = cv2.resize(frame, (WIDTH, HEIGHT))

    # We test if there is any detected hand
    if hands and not button_pressed:
        # Get the center of the hand
        hand = hands[0]
        cx, cy = hand['center']

        # Get the fingers up of the detected hand
        fingers = detector.fingersUp(hand)
        fingers[0] = int(not bool(fingers[0]))
 
        # Get the list of landmarks
        lmList = hand['lmList']
        
        """The right hand will trigger the mouse events."""
        if hand['type'] == 'Right':
            x_val, y_val = fingerPosition(INDEX, lmList, xxp, yxp, xfp, yfp)
            x_val = plocX + (x_val - plocX) / SMOOTHING
            y_val = plocY + (y_val - plocY) / SMOOTHING
            # Move the pointer
            if fingers == MOVE_POINTER:
                try :
                    pyautogui.moveTo(x_val, y_val)
                    plocX, plocY = x_val, y_val

                except :
                    print('There is a problem in pyautogui !!')
            # # Drag
            # if fingers == DRAG:
            #     pyautogui.dragTo(x_val, y_val)

            # Click management
            if cy <= THRESHOLD :
                # window.set_mouse_cursor(cursor_trigger)

                # Left click
                if fingers == LEFT_CLICK:
                    button_pressed = True
                    pyautogui.leftClick()
                    playsound(SINGLE_CLICK_PATH)

                # Right click
                if fingers == RIGHT_CLICK:
                    button_pressed = True
                    pyautogui.rightClick()
                    playsound(SINGLE_CLICK_PATH)

                # Double click
                if fingers == DOUBLE_CLICK :
                    button_pressed = True
                    pyautogui.doubleClick()
                    playsound(DOUBLE_CLICK_PATH)

                # Scroll up
                if fingers == SCROLL_UP:
                    pyautogui.vscroll(SCROLL_SPEED)

                # Scroll down
                if fingers == SCROLL_DOWN:
                    pyautogui.vscroll(-SCROLL_SPEED)

                """The left and the right scrolling is just supported by Linux Currently."""
                # Scroll to left
                if fingers == SCROLL_LEFT:
                    pyautogui.hscroll(-SCROLL_SPEED)

                #  Scroll to right
                if fingers == SCROLL_RIGHT:
                    pyautogui.hscroll(SCROLL_SPEED)

        if hand['type'] == 'Left':
            if cy <= THRESHOLD :
                
                # Take creenshot
                if fingers == SCREENSHOT:
                    button_pressed = True
                    pyautogui.screenshot(SCREENSHOT_PATH)
                    playsound(SCREENSHOT_SOUND_PATH)


                # Copy
                if fingers == COPY :
                    button_pressed = True
                    pyautogui.hotkey('ctrl', 'c')
                    playsound(COPY_PATH)

                # Cut
                if fingers == CUT :
                    button_pressed = True
                    pyautogui.hotkey('ctrl', 'x')
                    playsound(COPY_PATH)

                # Paste
                if fingers == PASTE :
                    button_pressed = True
                    pyautogui.hotkey('ctrl', 'v')
                    playsound(PASTE_PATH)

                # Select all
                if fingers == SELECT_ALL :
                    button_pressed = True
                    pyautogui.hotkey('ctrl', 'a')

                # Quit
                if fingers == QUIT :
                    button_pressed = True
                    pyautogui.hotkey('alt', 'f4')
                
                # Enter
                if fingers == ENTER :
                    button_pressed = True
                    pyautogui.hotkey('enter')
                    playsound(KEYBOARD_PRESS_PATH)

    # Button Pressed iterations
    if button_pressed:
        button_counter += 1
        if button_counter > BUTTON_DELAY:
            button_counter = 0
            button_pressed = False
        
    # Show the frames
    cv2.imshow(TITLE, img)
    # bringWinToFront(TITLE)

    # Quit if "q" is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break