# Quick Start Guide

## Install the Extension (2 minutes)

1. **Open Chrome Extensions**
   - Type `chrome://extensions/` in address bar
   - Enable "Developer mode" (top right toggle)

2. **Load Extension**
   - Click "Load unpacked"
   - Navigate to and select the `extension/` folder
   - Extension is now installed!

3. **Start Backend**
   ```bash
   python -m src.main
   ```

## Use It

1. Go to any website
2. Highlight text you want to verify
3. Right-click → "Verify claim"
4. See result popup

That's it! 🎉

## Note on Icons

The extension will work without custom icons (Chrome uses defaults). To add custom icons:

1. Create 4 PNG files: 16x16, 32x32, 48x48, 128x128
2. Name them: `icon16.png`, `icon32.png`, `icon48.png`, `icon128.png`
3. Place in `extension/icons/` folder
4. Reload extension

Recommended icon: magnifying glass 🔍 or shield 🛡️
