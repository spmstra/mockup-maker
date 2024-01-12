#!/bin/bash

out_dir="$(pwd)/mockups"
if [ ! -d "$out_dir" ]; then
  mkdir "$out_dir"
fi
img_dir="$HOME/.bin/pic-mockups/img"
py_dir="$HOME/.bin/pic-mockups/mockups.py"

python3 "$py_dir" "$img_dir" "$out_dir" "$@"
