#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <unistd.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>

Display *display = NULL;

void setPointerFocus() {
    if (!display) return;
    printf("Setting the focus\n");
    Window root = DefaultRootWindow(display);
    printf("display ",display);
    Window returned_root, returned_child;
    int root_x, root_y, win_x, win_y;
    unsigned int mask;

    XQueryPointer(display, root, &returned_root, &returned_child,
                  &root_x, &root_y, &win_x, &win_y, &mask);

    if (returned_child != None) {
        XSetInputFocus(display, returned_child, RevertToPointerRoot, CurrentTime);
        XFlush(display);
        printf("display ",display);
    }
}

void sendMouseEvent( unsigned int button, int isPress) {
    if (!display) return;
    printf("display ",display);
    printf("\n mouse event control button:%d press:%d \n", button, isPress);
    usleep(100000);
    setPointerFocus();
    if (isPress == 1) {
        printf("ButtonPress<<<<<<<<<<<<<%d\n", button);
        XTestFakeButtonEvent(display, button, True, CurrentTime);
        usleep(100000);
        XFlush(display);
    } else {
        printf("\n<<<<<<<<<<<<ButtonRelease:%d\n", button);
        XTestFakeButtonEvent(display, button, False, CurrentTime);
        usleep(100000);
        XFlush(display);
    }
}

void moveMouse(int x, int y) {
    if (!display) return;
    XTestFakeMotionEvent(display, -1, x, y, CurrentTime);
    usleep(100000);
    XFlush(display);
}

extern "C" {

    int initialize_x() {
        display = XOpenDisplay(NULL);
        if (!display) {
            fprintf(stderr, "Unable to open display\n");
            return 1; // Indicate failure
        }
        return 0; // Indicate success
    }

    void close_x() {
        if (display) {
            XCloseDisplay(display);
            display = NULL;
        }
    }

    int mouse_move_extern(int _X, int _Y) {
        printf("display ",display);
        if (!display) {
            fprintf(stderr, "Display not initialized\n");
            return 1;
        }
        printf("called mouse move\n");
        printf("X %d Y %d\n", _X, _Y);
        moveMouse(_X, _Y);
        printf("waiting mouse move\n");
        usleep(100000); 
        XFlush(display);
        return 0;
    }

    int mouse_event_extern(unsigned int _uiBUTTON, int _iISPRESS) {
        if (!display) {
            fprintf(stderr, "Display not initialized\n");
            return 1;
        }
        printf("\ncalled mouse event\n");
        printf("ISPRESS CHECK %d\n", _iISPRESS);

        int screen = DefaultScreen(display);
        printf("\n mouse event button:%d isPress:%d screen:%d\n", _uiBUTTON, _iISPRESS, screen);

        printf("\n Calling mouse event\n");
        sendMouseEvent(_uiBUTTON, _iISPRESS); // Press left button
        printf("\nwaiting mouse event 2\n");
        usleep(100000); // Reduced sleep
        XFlush(display);
        return 0;
    }
}