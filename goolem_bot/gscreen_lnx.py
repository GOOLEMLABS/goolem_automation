import ctypes
from ctypes import Structure, c_int, POINTER
from ctypes.util import find_library
import os

# Load the Xlib library root@goolem:/home/goolem/scripts# sh x11.sh

# Define XWindowAttributes structure
import ctypes
import ctypes.util

# Load the X11 library
x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library('X11'))

# Define necessary structures and functions
class XDisplay(ctypes.Structure):
    pass

class XRootWindowAttributes(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("border_width", ctypes.c_int),
                ("depth", ctypes.c_int)]

class XWindowAttributes(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("border_width", ctypes.c_int),
                ("depth", ctypes.c_int),
                ("visual", ctypes.c_void_p),
                ("root", ctypes.c_ulong),
                ("class", ctypes.c_int),
                ("bit_gravity", ctypes.c_int),
                ("win_gravity", ctypes.c_int),
                ("backing_store", ctypes.c_int),
                ("backing_planes", ctypes.c_ulong),
                ("backing_pixel", ctypes.c_ulong),
                ("save_under", ctypes.c_int),
                ("colormap", ctypes.c_ulong),
                ("map_installed", ctypes.c_int),
                ("map_state", ctypes.c_int),
                ("all_event_masks", ctypes.c_long),
                ("your_event_mask", ctypes.c_long),
                ("do_not_propagate_mask", ctypes.c_long),
                ("override_redirect", ctypes.c_int),
                ("screen", ctypes.c_void_p)]

class XWindow(ctypes.Structure):
    pass

class XQueryPointerReply(ctypes.Structure):
    _fields_ = [("root_return", ctypes.c_ulong),
                ("child_return", ctypes.c_ulong),
                ("root_x", ctypes.c_int),
                ("root_y", ctypes.c_int),
                ("win_x", ctypes.c_int),
                ("win_y", ctypes.c_int),
                ("mask_return", ctypes.c_uint)]





class window_attributes():
    # Define function prototypes
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.POINTER(XDisplay)

    x11.XRootWindow.argtypes = [ctypes.POINTER(XDisplay), ctypes.c_int]
    x11.XRootWindow.restype = ctypes.c_ulong

    x11.XQueryPointer.argtypes = [ctypes.POINTER(XDisplay), ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
                                  ctypes.POINTER(ctypes.c_ulong),
                                  ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                  ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                  ctypes.POINTER(ctypes.c_uint)]
    x11.XQueryPointer.restype = ctypes.c_int
    def __init__(self):
        pass



    def get_mouse_position(self):
        # Open display
        display = x11.XOpenDisplay(None)
        if not display:
            raise Exception("Unable to open display")

        # Get the root window
        root_window = x11.XRootWindow(display, 0)

        # Prepare the result variables
        root_return = ctypes.c_ulong()
        child_return = ctypes.c_ulong()
        root_x = ctypes.c_int()
        root_y = ctypes.c_int()
        win_x = ctypes.c_int()
        win_y = ctypes.c_int()
        mask_return = ctypes.c_uint()

        # Query pointer
        x11.XQueryPointer(display, root_window, ctypes.byref(root_return), ctypes.byref(child_return),
                          ctypes.byref(root_x), ctypes.byref(root_y), ctypes.byref(win_x), ctypes.byref(win_y),
                          ctypes.byref(mask_return))

        # Return the position

    def get_window_attributes(self):
        # Check if DISPLAY environment variable is set
        display_env = os.getenv("DISPLAY")
        if not display_env:
            raise Exception("DISPLAY environment variable is not set")

        # Open display
        display = x11.XOpenDisplay(None)
        if not display:
            raise Exception("Unable to open display. DISPLAY environment variable: {}".format(display_env))

        # Get the root window
        root_window = x11.XRootWindow(display, 0)

        # Get window attributes
        attributes = XWindowAttributes()
        if not x11.XGetWindowAttributes(display, root_window, ctypes.byref(attributes)):
            raise Exception("Unable to get window attributes")

        # Return the size
        return attributes

