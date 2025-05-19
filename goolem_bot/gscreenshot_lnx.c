#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <png.h>
#include <stdio.h>
#include <stdlib.h>

//gcc -o gscreenshot_lnx gscreenshot_lnx.c -lX11 -lpng

// Function to save the screenshot as a 24-bit PNG file
void save_png(const char *filename, unsigned char *buffer, int width, int height) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        perror("File opening for PNG failed");
        return;
    }

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) {
        perror("png_create_write_struct failed");
        fclose(fp);
        return;
    }

    png_infop info = png_create_info_struct(png);
    if (!info) {
        perror("png_create_info_struct failed");
        fclose(fp);
        png_destroy_write_struct(&png, NULL);
        return;
    }

    if (setjmp(png_jmpbuf(png))) {
        perror("Error during PNG creation");
        fclose(fp);
        png_destroy_write_struct(&png, &info);
        return;
    }

    png_init_io(png, fp);

    // Write header for 24-bit RGB image
    png_set_IHDR(png, info, width, height, 8, PNG_COLOR_TYPE_RGB, PNG_INTERLACE_NONE,
                 PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png, info);

    // Write image data (8 bits per channel, RGB)
    for (int y = 0; y < height; y++) {
        png_write_row(png, &buffer[y * width * 3]);  // 3 channels (RGB), 8 bits each
    }

    // End write
    png_write_end(png, NULL);
    png_destroy_write_struct(&png, &info);
    fclose(fp);
}

int main() {
    Display *display = XOpenDisplay(NULL);
    if (!display) {
        fprintf(stderr, "Unable to open X display\n");
        return EXIT_FAILURE;
    }

    // Get the root window (the entire screen)
    Window root = DefaultRootWindow(display);

    // Get the screen width and height
    int screen = DefaultScreen(display);
    int width = DisplayWidth(display, screen);
    int height = DisplayHeight(display, screen);

    // Capture the screenshot as a 24-bit XImage (ZPixmap)
    XImage *image = XGetImage(display, root, 0, 0, width, height, AllPlanes, ZPixmap);
    if (image->depth != 24 && image->depth != 32) {
        fprintf(stderr, "Unsupported image depth: %d (only 24 and 32 supported)\n", image->depth);
        XDestroyImage(image);
        XCloseDisplay(display);
        return EXIT_FAILURE;
    }

    // Allocate memory for storing the screenshot in 24-bit RGB format (3 bytes per pixel)
    unsigned char *buffer = (unsigned char *)malloc(width * height * 3);  // 3 bytes per pixel (RGB)
    if (!buffer) {
        fprintf(stderr, "Unable to allocate memory for screenshot\n");
        XDestroyImage(image);
        XCloseDisplay(display);
        return EXIT_FAILURE;
    }

    // Convert XImage to RGB format (XImage uses BGRA or BGR depending on depth)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            unsigned long pixel = XGetPixel(image, x, y);
            buffer[(y * width + x) * 3 + 0] = (pixel & image->red_mask) >> 16;  // Red
            buffer[(y * width + x) * 3 + 1] = (pixel & image->green_mask) >> 8;  // Green
            buffer[(y * width + x) * 3 + 2] = (pixel & image->blue_mask);         // Blue
        }
    }

    // Save the screenshot as a PNG file in RGB format (24-bit)
    save_png("/dev/shm/gscreenshot.png", buffer, width, height);

    // Clean up
    free(buffer);
    XDestroyImage(image);
    XCloseDisplay(display);

    printf("Screenshot saved to dev shm\n");
    return 0;
}
