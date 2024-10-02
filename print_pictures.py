import argparse
import subprocess
from PIL import Image
from zpl import Label

def png_to_zpl(image_quantities, zpl_output_path, borders):
    # Create a new ZPL label with the specified size (203 x 406 dots)
    total = 0
    for x in image_quantities.values():
        total += x

    lab_width = 50.8
    lab_height = 25.4 * total

    label = Label(width=lab_width, height=lab_height, dpmm=8)  # Full label size
    current_y = 1  # Start position with top margin (20 dots for 0.1 inch)

    for wagon_type, quantity in image_quantities.items():
        # Open the PNG file
        png_path = f"./WagonImages/Images/{wagon_type}.png"

        img = Image.open(png_path)

        # Convert the image to monochrome (1-bit pixels)
        if img.size[1] > img.size[0]:
            img = img.rotate(270, expand=True)

        scale = min([(25.4-2)*8 / img.size[1], (50.4-2) * 8 / img.size[0]])

        re_w = min(round(img.size[0] * scale), 250)
        re_h = round(img.size[1] * scale)

        img = img.resize((re_w, re_h))

        width, height = img.size

        width /= 8
        height /= 8

        left_edge = (50.8 - width)/2
        top_edge = (25.4 - height)/2

        img = img.convert("1")
        # Get the width and height of the image
        img.show()
        

        # Add each image the specified number of times
        for _ in range(quantity):

            if "-" not in wagon_type:
                wagon_type = wagon_type[:2] + "-" + wagon_type[2:]

            label.origin(50.4-10, current_y + 1.25)#+12.7-1*len(wagon_type))
            label.write_text(wagon_type, char_height=5, char_width=5, orientation='R')
            label.endorigin()

            if borders:
                label.origin(0.0, current_y)
                label.draw_box(50.8*8, 25.4*8, thickness=2, rounding=4)
                label.endorigin()

            # Create the ZPL image command
            label.origin(left_edge, current_y+1)
            label.write_graphic(img, img.size[0]/8.)
            label.endorigin()
            current_y += 25.4  # Move down for the next image, with a margin

    # Generate ZPL code
    zpl_code = label.dumpZPL()

    # Write the ZPL code to an output file
    with open(zpl_output_path, 'w') as f:
        f.write(zpl_code)

    print(f"ZPL code saved to {zpl_output_path}")

    label.preview()

    return zpl_output_path  # Return the output path for printing

def print_zpl(zpl_output_path, printer_name):
    try:
        subprocess.run(['lp', '-d', printer_name, zpl_output_path], check=True)
        print(f"Printed to {printer_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error printing: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generate ZPL labels from PNG images.')
    parser.add_argument('--wagontypes', nargs='+', help='Paths to PNG images.')
    parser.add_argument('--quantities', type=int, nargs='+', help='Quantities for each image, in the same order.')
    parser.add_argument('--output', default="wagon_images.zpl", help='Output file path for ZPL code.')
    parser.add_argument('--print', action='store_true', default=False, help='Print the generated ZPL using the lp command.')
    parser.add_argument('--printer', default='Zebra', help='Printer name (default: Zebra).')
    parser.add_argument('--borders', action='store_true', default=False, help='Add label outlines (default: False)')

    args = parser.parse_args()

    # Create a dictionary from images and quantities
    if args.quantities:
        image_quantities = {img: qty for img, qty in zip(args.wagontypes, args.quantities)}
    else:
        image_quantities = {img: 1 for img in args.wagontypes}  # Default to 1 if no quantities are provided

    print(image_quantities)

    # Generate ZPL
    zpl_file = png_to_zpl(image_quantities, args.output, args.borders)

    # Print if the flag is set
    if args.print:
        print_zpl(zpl_file, args.printer)

if __name__ == '__main__':
    main()
