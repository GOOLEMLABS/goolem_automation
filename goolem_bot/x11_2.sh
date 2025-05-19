"x11.sh" 17 lines, 1041 bytes written
root@goolem:/home/goolem/scripts# ps ax |gre vfb
bash: gre: command not found
root@goolem:/home/goolem/scripts# ps ax |grep vfb
   2462 pts/1    S+     0:00 grep vfb
root@goolem:/home/goolem/scripts# cd scripts/^C
root@goolem:/home/goolem/scripts# cat x11.sh
export DISPLAY=:1
Xvfb $DISPLAY -screen 0 1024x768x32 &
icewm &

#x11vnc -display $DISPLAY -bg -forever -nopw -quiet -listen localhost -xkb
# x11vnc -rfbport 5900 -no6 -rawfb /dev/fb0 -verbose -cursor none -nodragging -pipeinput UINPUT:direct_abs=/dev/uinput,accel=1.0 -forever
#x11vnc -rfbport 5900 -no6 -rawfb /dev/fb0 -verbose -listen localhost -cursor none -nodragging -forever
#x11vnc -permitfiletransfer -nopw -rawfb +/dev/fb0 -forever -noxrecord -noxfixes -noxdamage -xrandr -bg -shared -pipeinput UINPUT:accel=0.7,reset=0 -cursor none -nodragging
#x11vnc -display $DISPLAY -bg -forever -nopw -quiet -listen localhost -xkb -rawfb  console

#x11vnc -rfbport 5900 -no6 -rawfb /dev/fb0 -verbose -listen localhost -cursor none -nodragging -forever

#x11vnc -display $DISPLAY  -noipv6 -clip 500x500+0+0 -rawfb /dev/fb0 -listen localhost -pipeinput UINPUT:direct_abs=/dev/input/uinput
xset r rate 200 30
#x11vnc -usepw  -repeat -pipeinput UINPUT
#x11vnc  -pipeinput UINPUT:direct_abs=/dev/input/uinput -dk -dp
x11vnc -dk -dp -depth 32
