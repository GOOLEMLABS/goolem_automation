#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <unistd.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>

Display *display = NULL;

void sendkeyboardReleaseEvent(KeyCode keycode) {
    if (!display) return;
    XTestFakeKeyEvent(display, keycode, False, CurrentTime);
    XFlush(display);
}

void sendkeyboardPRessAndReleaseEvent(KeyCode keycode) {
    if (!display) return;
    XTestFakeKeyEvent(display, keycode, True, CurrentTime);
    XFlush(display);
    XTestFakeKeyEvent(display, keycode, False, CurrentTime);
    XFlush(display);
}

void sendkeyboardPressEvent(KeyCode keycode) {
    if (!display) return;
    XTestFakeKeyEvent(display, keycode, True, CurrentTime);
    XFlush(display);
}

extern "C" {

    int initialize_x_keyboard() {
        display = XOpenDisplay(NULL);
        if (!display) {
            fprintf(stderr, "Unable to open display for keyboard\n");
            return 1; // Indicate failure
        }
        return 0; // Indicate success
    }

    void close_x_keyboard() {
        if (display) {
            XCloseDisplay(display);
            display = NULL;
        }
    }

    int keyboard_press_extern(char *keyword) {
        if (!display) {
            fprintf(stderr, "Display not initialized for keyboard\n");
            return 1;
        }
        KeySym ksym = XStringToKeysym(keyword);
        KeyCode keycode = XKeysymToKeycode(display, ksym);
        if (keycode == NoSymbol) {
            fprintf(stderr, "Error: Could not find keycode for '%s'\n", keyword);
            return 1;
        }
        sendkeyboardPressEvent(keycode);
        return 0;
    }

    int keyboard_release_extern(char *keyword) {
        if (!display) {
            fprintf(stderr, "Display not initialized for keyboard\n");
            return 1;
        }
        KeySym ksym = XStringToKeysym(keyword);
        KeyCode keycode = XKeysymToKeycode(display, ksym);
        if (keycode == NoSymbol) {
            fprintf(stderr, "Error: Could not find keycode for '%s'\n", keyword);
            return 1;
        }
        sendkeyboardReleaseEvent(keycode);
        printf("called keyboard_release_extern: %s\n", keyword);
        return 0;
    }

    int keyboard_press_and_release_extern(char *keyword) {
        if (!display) {
            fprintf(stderr, "Display not initialized for keyboard\n");
            return 1;
        }
        KeySym ksym = XStringToKeysym(keyword);
        KeyCode keycode = XKeysymToKeycode(display, ksym);
        if (keycode == NoSymbol) {
            fprintf(stderr, "Error: Could not find keycode for '%s'\n", keyword);
            return 1;
        }
        sendkeyboardPRessAndReleaseEvent(keycode);
        printf("called keyboard_press_and_release_extern: %s\n", keyword);
        return 0;
    }
}