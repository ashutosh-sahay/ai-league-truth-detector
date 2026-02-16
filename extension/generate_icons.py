#!/usr/bin/env python3
"""
Generate placeholder icons for the Chrome extension using PIL/Pillow.

This creates simple colored icons with the magnifying glass emoji.
Run this if you want quick placeholder icons instead of designing custom ones.

Requirements: pip install pillow
Usage: python generate_icons.py
"""

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    
    def create_icon(size: int, output_path: Path):
        """Create a simple icon with gradient background."""
        # Create image with gradient purple background
        img = Image.new('RGB', (size, size), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw gradient-like circles for background
        center = size // 2
        for i in range(5, 0, -1):
            radius = int(center * (i / 5))
            color_val = int(102 + (118 - 102) * (i / 5))
            color = (color_val, 126, 234)
            draw.ellipse([center - radius, center - radius, 
                         center + radius, center + radius], 
                        fill=color)
        
        # Draw magnifying glass
        # Circle (lens)
        lens_radius = int(size * 0.25)
        lens_x, lens_y = int(size * 0.4), int(size * 0.4)
        draw.ellipse([lens_x - lens_radius, lens_y - lens_radius,
                     lens_x + lens_radius, lens_y + lens_radius],
                    outline='white', width=max(2, size // 32))
        
        # Handle
        handle_start_x = int(lens_x + lens_radius * 0.7)
        handle_start_y = int(lens_y + lens_radius * 0.7)
        handle_end_x = int(size * 0.75)
        handle_end_y = int(size * 0.75)
        draw.line([handle_start_x, handle_start_y, handle_end_x, handle_end_y],
                 fill='white', width=max(2, size // 32))
        
        img.save(output_path)
        print(f"Created {output_path.name} ({size}x{size})")
    
    def main():
        """Generate all required icon sizes."""
        script_dir = Path(__file__).parent
        icons_dir = script_dir / 'icons'
        icons_dir.mkdir(exist_ok=True)
        
        sizes = [16, 32, 48, 128]
        for size in sizes:
            output_path = icons_dir / f'icon{size}.png'
            create_icon(size, output_path)
        
        print("\n✅ All icons generated successfully!")
        print("Icons are located in: extension/icons/")
        print("\nReload your extension in Chrome to see the new icons.")
    
    if __name__ == '__main__':
        main()

except ImportError:
    print("❌ PIL/Pillow not installed")
    print("\nTo generate icons, install Pillow:")
    print("  pip install pillow")
    print("\nThen run:")
    print("  python extension/generate_icons.py")
    print("\nOr add your own PNG files to extension/icons/:")
    print("  - icon16.png (16x16)")
    print("  - icon32.png (32x32)")
    print("  - icon48.png (48x48)")
    print("  - icon128.png (128x128)")
    print("\nThe extension will work without icons (Chrome uses defaults).")
