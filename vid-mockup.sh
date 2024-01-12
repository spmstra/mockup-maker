#!/bin/bash

# input is a base image file for which mockups are to be made
input=$1
# ensures outs are relative to execution pwd. makes output dir if absent
out_dir="$(pwd)/mockups"
if [ ! -d "$out_dir" ]; then
  mkdir "$out_dir"
fi

# location of stock frame image and python script to superimpose $input
# over stock frame
img_dir="$HOME/.bin/vid-mockup/frame.jpg"
py_dir="$HOME/.bin/vid-mockup/mockups.py"
vid1="$out_dir/zoom.mp4"
vid2="$HOME/.bin/vid-mockup/printing.mp4"
final_vid="$out_dir/video.mp4"

# makes composition of input in picture frame
python3 "$py_dir" "$img_dir" "$out_dir" "$1"
vid_framed_img="$out_dir/vid_framed.jpg"

# makes slow zoom video into framed image for 5 sec
ffmpeg -loop 1 -i $vid_framed_img -filter_complex "zoompan=z='min(zoom+0.0025,1.7)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080, fps=24" -t 5 -c:v libx264 -pix_fmt yuv420p $vid1

# discards framed image after video is made
rm $vid_framed_img

# composes zoom video with production video
ffmpeg -i $vid1 -i $vid2 -filter_complex \
"[0:v]format=pix_fmts=yuva420p,fade=t=out:st=3:d=1:alpha=1,setpts=PTS-STARTPTS[va0];\
 [1:v]format=pix_fmts=yuva420p,fade=t=in:st=0:d=1:alpha=1,setpts=PTS-STARTPTS[va1];\
 [va0][va1]xfade=transition=fade:duration=1:offset=3[vo]" \
-map "[vo]" $final_vid

# discards zoom video file
rm $vid1
