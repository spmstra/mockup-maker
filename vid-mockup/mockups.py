import sys
import random
from PIL import Image, ImageDraw, ImageFont

def process_images(img_dir, out_dir, art_path):

    art = Image.open(art_path)

    # Make framed image
    print(f"Creating mockup for zoom video of framed image.")
    
    frame_img = Image.open(f"{img_dir}")
    resized_art = art.resize((1301,1321), Image.BICUBIC)
    position = (343, 345)
    frame_img.paste(resized_art, position)
    
    # Save the thumbnail image with a specific file name
    output_filename = f"{out_dir}/vid_framed.jpg"
    frame_img.save(output_filename)
    print(f"Saved: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mockups.py art.jpg")
        sys.exit(1)
    img_dir = sys.argv[1]
    out_dir = sys.argv[2]
    art_path = sys.argv[3]
    process_images(img_dir, out_dir, art_path)
