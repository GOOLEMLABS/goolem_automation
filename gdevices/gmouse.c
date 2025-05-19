#include <linux/uinput.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>

//https://docs.kernel.org/input/event-codes.html
//https://docs.kernel.org/input/uinput.html
//funciona en una raspberry
//SetCursorPos(int(x), int(y))
//mouse_event(2, 0, 0, 0,0)
#define O_RDONLY         00
#define O_WRONLY         01
#define O_RDWR           02
#define O_NONBLOCK          04000

//const int fd = open("/dev/uinput",  O_RDWR);//O_WRONLY | O_NONBLOCK);
int fd;

void init_fd() {
    fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK); //#O_RDWR);
}


void emit(int fd, int type, int code, int val)
{
   struct input_event ie;

   ie.type = type;
   ie.code = code;
   ie.value = val;
   ie.time.tv_sec = 0;
   ie.time.tv_usec = 0;

   write(fd, &ie, sizeof(ie));
}
int create(void)
{
   printf("init\n");
   struct uinput_setup usetup;
   int i = 50; //control de paso , sera variable
   printf("opening uinputn\n");
   //int fd = open("/dev/uinput",  O_RDWR);//O_WRONLY | O_NONBLOCK);

   ioctl(fd, UI_SET_EVBIT, EV_KEY);
   ioctl(fd, UI_SET_KEYBIT, BTN_LEFT);
   ioctl(fd, UI_SET_KEYBIT, BTN_RIGHT);
   ioctl(fd, UI_SET_EVBIT, EV_REL);
   ioctl(fd, UI_SET_RELBIT, REL_X);
   ioctl(fd, UI_SET_RELBIT, REL_Y);
   memset(&usetup, 0, sizeof(usetup));
   usetup.id.bustype = BUS_USB;
   usetup.id.vendor = 0x06cb; /* sample vendor */
   usetup.id.product = 0x0001;  /* sample product */
   strcpy(usetup.name, "goolem mouse");
   sleep(2);
   ioctl(fd, UI_DEV_SETUP, &usetup);
   sleep(2);
   ioctl(fd, UI_DEV_CREATE);


   sleep(5);
   return 0;
   }
int created_device ;//device creation

void init_createdev() {
    created_device = create();
}

int SetCursorPosABS(int x, int y )//que cojones
{
    emit(fd, EV_ABS, REL_X, x);
    emit(fd, EV_ABS, REL_Y, y);
    emit(fd, EV_SYN, SYN_REPORT, 0 );
 return 0;
}
int mouse_event(int _X, int _Y, int _LEFT, int _RIGHT ,int _SLEEP )
{
      usleep(_SLEEP);
      //printf("moving to %s %s and button \n",_X,_Y);
      if (_LEFT==1){
      printf("\n button left");
      emit(fd, EV_REL, BTN_LEFT, 1);
        };//BTN_LEFT
      printf("\n right moving %d",_X);
      printf("\n left moving %d",_Y);
      emit(fd, EV_ABS, REL_X, _X);//revisarEV_REL
      emit(fd, EV_ABS, REL_Y, _Y);
      emit(fd, EV_SYN, SYN_REPORT, 0);



   /*
    * Give userspace some time to read the events before we destroy the
    * device with UI_DEV_DESTROY

    */
   sleep(5);
   return 0;
 }

int destroy(void) {
   ioctl(fd, UI_DEV_DESTROY);
   close(fd);
   printf("remove\n");
   return 0;
}
int main()
{
    init_fd();
    printf
    create();
    sleep(2);
    destroy();
    return 0;
}

extern "C" {
    void create_device(){
    init_fd();
    printf("creating device");
    created_device=create();
    }

    int mouse_event_extern(int _X, int _Y, int _LEFT,int _RIGHT ,int _SLEEP ){
    printf("called mouse\n");
    printf("%d",_X);
    mouse_event(_X,_Y,_LEFT,_RIGHT,_SLEEP);
    printf("waiting\n");
    sleep(5);
    destroy();
    return 0;
    }
int get_mouse() {return 1;}
}