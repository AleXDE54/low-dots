#!/usr/bin/env python3
import subprocess
import sys
import os
import random
from pathlib import Path

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def rgb_from_hex(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def print_palette():
    colors_file = os.path.expanduser("~/.cache/wal/colors")
    if not Path(colors_file).is_file():
        print("Palette: (no wal cache)")
        return
    with open(colors_file) as f:
        colors = [line.strip() for line in f if line.strip()]
    # Print 8 color blocks
    blocks = []
    for c in colors[:8]:
        r, g, b = rgb_from_hex(c)
        blocks.append(f"\033[48;2;{r};{g};{b}m  \033[0m")  # two spaces with background
    print("".join(blocks))

def init_shell(wallpaper=None):
    if not wallpaper:
        wallpaper = os.path.expanduser("~/Pictures/Wallpapers/active.jpg")
    run("awww-daemon &")
    run(f"awww img {wallpaper} --transition-type center")
    run(f"wal -i {wallpaper}")
    run("waybar &")
    print("Shell environment ready")

def set_wallpaper(target):
    if target == "random":
        wall_dir = os.path.expanduser("~/Pictures/Wallpapers")
        images = [f for f in Path(wall_dir).glob("*") if f.suffix in [".jpg", ".png", ".jpeg"]]
        if not images:
            print("No images found")
            sys.exit(1)
        target = str(random.choice(images))
    run(f"awww img {target} --transition-type center")
    run(f"wal -i {target}")
    run("killall -SIGUSR2 waybar")
    run("hyprctl reload")
    print(f"set wallpaper to {target}")
    print_palette()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: low-dots shell | low-dots wallpaper {random|/path/to/image}")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "shell":
        init_shell()
    elif cmd == "wallpaper" and len(sys.argv) == 3:
        set_wallpaper(sys.argv[2])
    else:
        print("Invalid command")
