#!/usr/bin/env python3
"""
Simple automated page capture using AppleScript to control the browser.
Works with any browser - no ChromeDriver needed!
"""

import os
import time
import subprocess
from PIL import Image

def capture_with_applescript(num_pages, delay=3):
    """
    Use AppleScript to capture screenshots and flip pages.
    
    Args:
        num_pages: Number of pages to capture
        delay: Seconds to wait between pages (for animations)
    """
    output_folder = os.path.expanduser("~/Documents/Textbook_Download")
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a temp folder for intermediate PNG files
    temp_folder = os.path.join(output_folder, ".temp_pages")
    os.makedirs(temp_folder, exist_ok=True)
    
    # Generate unique filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"textbook_{timestamp}.pdf"
    
    print(f"\n=== AUTOMATED CAPTURE STARTING ===")
    print(f"Will capture {num_pages} pages")
    print(f"Final PDF will be saved to: {output_folder}/{pdf_filename}")
    print(f"\nInstructions:")
    print("1. Make sure your textbook is open in the browser")
    print("2. Position the browser window so the page is fully visible")
    print("3. Click on the browser window to make sure it's active")
    print("4. The script will start in 5 seconds...")
    print("5. DO NOT move your mouse or type during capture!\n")
    
    time.sleep(5)
    
    for page_num in range(1, num_pages + 1):
        # Deselect any selected text before capturing
        subprocess.run([
            "osascript", "-e",
            'tell application "System Events"\n'
            '    key code 53\n'  # Escape key to deselect
            'end tell'
        ])
        time.sleep(0.2)
        
        # Take screenshot using screencapture
        screenshot_path = os.path.join(temp_folder, f"page_{page_num:04d}.png")
        temp_screenshot = os.path.join(temp_folder, f"temp_{page_num:04d}.png")
        
        # Capture full screen
        subprocess.run(["screencapture", "-x", temp_screenshot])
        
        # Crop to just the white textbook page (centered)
        # MacBook Pro 13" screen: white page is centered
        # White page dimensions: ~650px wide, ~900px tall
        # Centered on 1440x900 screen: x=395, y=150
        subprocess.run([
            "sips", "--cropToHeightWidth", "1200", "900",
            "--cropOffset", "460", "1050",  # y=150, x=395
            temp_screenshot,
            "--out", screenshot_path
        ])
        
        # Remove temp file
        if os.path.exists(temp_screenshot):
            os.remove(temp_screenshot)
        print(f"Captured page {page_num}/{num_pages}")
        
        # Wait for next page action
        time.sleep(delay)
        
        # Click the next button (adjust coordinates as needed)
        # Common locations for next buttons:
        # Right side of screen: x=1400, y=500 (adjust for your screen)
        # Bottom right: x=1300, y=800
        # Arrow key also works for many viewers
        
        # Click on right side of screen to flip page
        # Try multiple common next button locations
        # Right side of book viewer (adjust based on your screen)
        subprocess.run([
            "osascript", "-e",
            f'tell application "Safari" to activate\n'
            f'delay 0.3\n'
            f'tell application "System Events"\n'
            f'    key code 124\n'  # Try right arrow key
            f'end tell\n'
            f'delay 0.5'
        ])
        
        # Small delay for page flip animation
        time.sleep(1)
    
    print(f"\n✓ Capture complete! {num_pages} pages saved.")
    print(f"Location: {temp_folder}")
    return temp_folder, output_folder, pdf_filename

def combine_images_to_pdf(input_folder, output_folder, output_filename):
    """Combine all captured images into a single PDF and clean up temp files."""
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(image_extensions)]
    images.sort()
    
    if not images:
        print(f"No images found in {input_folder}")
        return
    
    print(f"\nCombining {len(images)} images into PDF...")
    
    first_image_path = os.path.join(input_folder, images[0])
    first_image = Image.open(first_image_path)
    
    if first_image.mode != 'RGB':
        first_image = first_image.convert('RGB')
    
    other_images = []
    for img_name in images[1:]:
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        other_images.append(img)
    
    output_path = os.path.join(output_folder, output_filename)
    first_image.save(
        output_path,
        save_all=True,
        append_images=other_images,
        resolution=150.0
    )
    
    print(f"✓ PDF saved: {output_path}")
    print(f"Total pages: {len(images)}")
    
    # Clean up temp folder and individual PNG files
    print(f"\nCleaning up temporary files...")
    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        os.remove(img_path)
    os.rmdir(input_folder)
    print(f"✓ Temporary files cleaned up")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Quick textbook capture')
    parser.add_argument('--pages', type=int, required=True, help='Number of pages to capture')
    parser.add_argument('--delay', type=float, default=3, help='Delay between pages in seconds')
    parser.add_argument('--combine', action='store_true', help='Combine existing images into PDF')
    parser.add_argument('--name', type=str, help='Custom name for the PDF file (optional)')
    
    args = parser.parse_args()
    
    if args.combine:
        temp_folder = os.path.expanduser("~/Documents/Textbook_Download/.temp_pages")
        output_folder = os.path.expanduser("~/Documents/Textbook_Download")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"textbook_{timestamp}.pdf"
        combine_images_to_pdf(temp_folder, output_folder, pdf_filename)
    else:
        temp_folder, output_folder, pdf_filename = capture_with_applescript(args.pages, args.delay)
        
        # Override filename if custom name provided
        if args.name:
            pdf_filename = args.name if args.name.endswith('.pdf') else f"{args.name}.pdf"
        
        # Automatically combine images into PDF
        print("\nAutomatically combining images into PDF...")
        combine_images_to_pdf(temp_folder, output_folder, pdf_filename)

if __name__ == '__main__':
    main()
