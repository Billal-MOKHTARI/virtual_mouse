import numpy as np
import win32gui, win32com.client

"""Transform given string in format of list or tuple to those respectively."""
def str_preprocessing(string, to=list):    
    """to : determine if the given string will be transformed to a list or tuple."""
    assert to == list or to == tuple

    if to == list :
        stripper = ']['
    else:
        stripper = ')('

    lst = string.strip(stripper).split(',')
    length = len(lst)
    lst = [int(lst[i]) for i in range(length)]

    if to == tuple:
        lst = tuple(lst)

    return lst

"""Get the given finger's position"""
def fingerPosition(finger, lmList, xxp, yxp, xfp, yfp):
    # Get position of the index (so as to move the mouse pointer)
    x_val = lmList[finger][0]
    y_val = lmList[finger][1]

    # Interpolation : We wanna transform the xp scale to fp scale
    xp = {'x_interpol' :xxp, 'y_interpol' :yxp}
    fp = {'x_interpol' :xfp, 'y_interpol' :yfp}
    
    x_val = int(np.interp(x_val, xp['x_interpol'], fp['x_interpol']))
    y_val = int(np.interp(y_val, xp['y_interpol'], fp['y_interpol']))

    return x_val, y_val

def bringWinToFront(title):
    hwnd = win32gui.FindWindowEx(0, 0, 0, title)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)