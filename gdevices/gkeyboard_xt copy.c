#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <unistd.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>
//https://www.x.org/releases/X11R7.5/doc/man/man3/XSendEvent.3.html

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>

Display *display = NULL;

void sendkeyboardReleaseEvent(KeyCode keycode) {
    printf("kr");
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, keycode), False, CurrentTime);
    XFlush(display);

}

void sendkeyboardPRessAndReleaseEvent(KeyCode keycode){
    printf("kpkr");
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, keycode), True, CurrentTime);
    XFlush(display);
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, keycode), False, CurrentTime);
    XFlush(display);

}

void sendkeyboardPressEvent(KeySym ksym) {
    printf("kp");
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, XK_A), True, CurrentTime);
    XFlush(display);

}


extern "C" {

int keyboard_press_extern(char *keyword){

    Display *display;
    display = XOpenDisplay(NULL);
    KeySym ksym;

    if (!display) {
        fprintf(stderr, "Unable to open display\n");
        exit(EXIT_FAILURE);
    }
    Window root = DefaultRootWindow(display);
    root = DefaultRootWindow(display);
    ksym = XStringToKeysym(keyword);
    sendkeyboardPressEvent(display,ksym);
    printf("called keypress\n");
    XCloseDisplay(display);
    return 0;
    }

int keyboard_release_extern(char *keyword ){

        Display *display;
        display = XOpenDisplay(NULL);
        KeySym ksym;
    
        if (!display) {
            fprintf(stderr, "Unable to open display\n");
            exit(EXIT_FAILURE);
        }
        Window root = DefaultRootWindow(display);
        root = DefaultRootWindow(display);
        ksym = XStringToKeysym(keyword);
        sendkeyboardReleaseEvent(display,ksym);
        printf("called keypress\n");
        XCloseDisplay(display);
        return 0;
        }
    
int keyboard_press_and_release_extern(char *keyword){

    Display *display;
    display = XOpenDisplay(NULL);
    KeySym ksym;

    if (!display) {
        fprintf(stderr, "Unable to open display\n");
        exit(EXIT_FAILURE);
    }
    Window root = DefaultRootWindow(display);
    root = DefaultRootWindow(display);
    ksym = XStringToKeysym(keyword);
    sendkeyboardPRessAndReleaseEvent(display,ksym);
    printf("called keypress\n");
    XCloseDisplay(display);
    return 0;
    }
     
}