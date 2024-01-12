import sys
import random
from PIL import Image, ImageDraw, ImageFont

def shift():
    return random.randint(-10,10)

def process_images(img_dir, out_dir, art_path, sizes):
    # Load the background image
    #bg_img = Image.open("small.jpg")
    #  Load the art image
    art = Image.open(art_path)

    for size_str in sizes:
        size = size_str.split('x')
        small = int(size[0]) < 9
        scale = 84 if small else 65

        # Parse the dimensions from the size string (e.g., "12x12")
        dims = tuple( map( lambda x: int(x) * scale, size ) )
        print(f"Creating mockup for {size[0]}\" x {size[1]}\" print")

        # Determine what size bg to use and set parameters
        # small = int(size[0]) < 15
        position = (630+shift(), 1615-dims[1]+shift()) if small else (540+shift(), 1830-dims[1]+shift())
        bg_path = f"{img_dir}/small.jpg" if small else f"{img_dir}/medium.jpg"
        bg_img = Image.open(bg_path)

        # Resize the image to proper size in context of mockup image
        resized_art = art.resize(dims, Image.BICUBIC)

        # Create a copy of the background image to paste onto
        mockup_img = bg_img.copy()

        # Calculate the position at NW corner of art at 600x1500)
        # position = ( 600, 1615 - dims[1] )  

        # Paste the resized image onto the background image
        mockup_img.paste(resized_art, position)

        # Puts text indicating size at NW of mockup imag
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 170, encoding="unic")
        text = f"{size[0]}\" x {size[1]}\""
        font_color = (50,20,20)
        
        # Create an ImageDraw object
        draw = ImageDraw.Draw(mockup_img)

        # Draw the text in the NW corner with specified font and color
        text_position = (8, -30)
        draw.text(text_position, text, font=font, fill=font_color)

        # Save the composited image with a specific file name
        output_filename = f"{out_dir}/{size_str}.jpg"
        mockup_img.save(output_filename)
        print(f"Saved: {output_filename}")


    # Make framed image
    print(f"Creating mockup for framed image.")
    
    frame_img = Image.open(f"{img_dir}/frame.jpg")
    resized_art = art.resize((1301,1321), Image.BICUBIC)
    position = (593, 345)
    frame_img.paste(resized_art, position)
    
    # Save the thumbnail image with a specific file name
    output_filename = f"{out_dir}/framed.jpg"
    frame_img.save(output_filename)
    print(f"Saved: {output_filename}")


    # Make main image
    print(f"Creating mockup for main/thumbnail image.")
    
    frame_img = Image.open(f"{img_dir}/main.jpg")
    resized_art = art.resize((1950,1950), Image.BICUBIC)
    position = (275, 25)
    frame_img.paste(resized_art, position)
    
    # Save the thumbnail image with a specific file name
    output_filename = f"{out_dir}/main.jpg"
    frame_img.save(output_filename)
    print(f"Saved: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mockups.py art.jpg size1 size2 ...")
        sys.exit(1)
    img_dir = sys.argv[1]
    out_dir = sys.argv[2]
    art_path = sys.argv[3]
    sizes = sys.argv[4:]
    process_images(img_dir, out_dir, art_path, sizes)
