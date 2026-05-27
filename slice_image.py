import os
import math
from PIL import Image

def main():
    image_path = "Guha_landing Page.jpg"
    output_dir = "slices"
    target_width = 1920
    slice_height = 2000
    quality = 82

    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    print(f"Opening {image_path}...")
    # Open the image, allowing large images
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    print(f"Original size: {orig_w}x{orig_h}")

    # Calculate new height to maintain aspect ratio
    scale = target_width / orig_w
    target_height = int(round(orig_h * scale))
    print(f"Target size (scaled to {target_width}px width): {target_width}x{target_height}")

    print("Resizing image...")
    # Resize the image using high quality LANCZOS filter
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    print("Resizing complete.")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    num_slices = math.ceil(target_height / slice_height)
    print(f"Slicing into {num_slices} parts of max {slice_height}px height...")

    img_tags = []

    for i in range(num_slices):
        y_start = i * slice_height
        y_end = min(y_start + slice_height, target_height)
        
        # Crop region: (left, upper, right, lower)
        crop_box = (0, y_start, target_width, y_end)
        slice_img = img_resized.crop(crop_box)
        
        slice_filename = f"slice_{i}.jpg"
        slice_path = os.path.join(output_dir, slice_filename)
        
        print(f"Saving {slice_filename} ({y_start} to {y_end} px)...")
        # Save slice with high JPEG compression/quality
        slice_img.save(slice_path, "JPEG", quality=quality, optimize=True)
        
        # Build img tag (lazy load lower slices)
        loading_attr = 'loading="lazy"' if i >= 2 else 'loading="eager"'
        img_tags.append(f'<img src="slices/{slice_filename}" alt="Guha Realty section {i+1}" {loading_attr} class="site-slice" width="{target_width}" height="{y_end - y_start}">')

    print("\nSlice generation complete!")
    print("\n--- HTML Code to Copy ---")
    for tag in img_tags:
        print(tag)

if __name__ == "__main__":
    main()
