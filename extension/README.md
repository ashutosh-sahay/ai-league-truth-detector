# AI Truth Detector Chrome Extension

A Chrome extension that allows you to verify claims directly from any webpage using the AI Truth Detector backend.

## Features

- **Right-click verification**: Highlight any text and verify it with a single click
- **Beautiful popup UI**: Clean, modern interface for displaying verification results
- **Real-time results**: Instant verification using your local AI backend
- **Smart fallback**: Uses local RAG knowledge base first, then falls back to web search
- **Configurable**: Change API endpoint from the extension popup
- **Status indicator**: Always know if your backend is running

## Installation

### Step 1: Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top-right corner)
3. Click **Load unpacked**
4. Select the `extension/` folder from this project
5. The AI Truth Detector extension should now appear in your extensions list

### Step 2: Add Extension Icons (Optional)

The extension needs icon files in the `extension/icons/` directory. You can:

**Option A: Use placeholder icons (quick start)**
The extension will work without custom icons, Chrome will use default placeholders.

**Option B: Add custom icons**
Create or download icons and place them in `extension/icons/`:
- `icon16.png` (16x16)
- `icon32.png` (32x32)
- `icon48.png` (48x48)
- `icon128.png` (128x128)

You can use any icon generator tool or create them manually. Recommended: a magnifying glass or shield icon.

### Step 3: Start Your Backend

Make sure your AI Truth Detector backend is running:

```bash
# From the project root
python -m src.main
```

The backend should be running at `http://localhost:8000`

## How to Use

1. **Navigate to any webpage** with text content
2. **Highlight text** you want to verify (e.g., a claim, fact, or statement)
3. **Right-click** on the selected text
4. **Click "Verify claim"** from the context menu
5. **View the result** in the popup that appears in the top-right corner

The popup will show:
- The claim being verified
- Verification status (✓ VERIFIED or ✗ NOT VERIFIED)
- Detailed analysis from the AI
- Evidence source (RAG Store or WEB)

## Configuration

### Changing the API URL

If your backend is running on a different port or host:

1. Click the extension icon in Chrome toolbar
2. Find the **Settings** section
3. Update the **API Base URL**
4. Click **Save Settings**
5. The status indicator will update automatically

Default: `http://localhost:8000`

## Extension Structure

```
extension/
├── manifest.json       # Extension configuration (Manifest V3)
├── background.js       # Service worker (handles API calls)
├── content.js          # Content script (displays results on page)
├── popup.html          # Extension popup UI
├── popup.css           # Popup styles
├── popup.js            # Popup logic
└── icons/              # Extension icons
    ├── icon16.png
    ├── icon32.png
    ├── icon48.png
    └── icon128.png
```

## Technical Details

### Architecture

- **Manifest V3**: Uses the latest Chrome extension standard
- **Service Worker**: Background script handles all API communication
- **Content Script**: Injected into web pages to display results
- **Message Passing**: Communication between components via Chrome messaging API

### Permissions

- `contextMenus`: Add "Verify claim" to right-click menu
- `activeTab`: Access to current tab for result display
- `storage`: Save user settings (API URL)
- `http://localhost:8000/*`: Access to local API

### API Integration

The extension calls these backend endpoints:
- `POST /api/v1/verify` - Verify a claim
- `GET /api/v1/health` - Check API status

### Security

- No external dependencies
- All processing done on your local backend
- No data sent to third parties
- Content Security Policy enforced

## Troubleshooting

### Extension won't load
- Make sure Developer mode is enabled
- Check that all files are present in the `extension/` folder
- Look for errors in Chrome's extension management page

### "Disconnected" status
- Verify backend is running: `python -m src.main`
- Check the API URL in settings matches your backend
- Ensure CORS is configured (already done in the FastAPI app)
- Check browser console for error messages

### Right-click menu not appearing
- Try reloading the extension
- Refresh the webpage you're testing on
- Make sure text is actually selected

### Popup shows error
- Check that backend is running and accessible
- Verify the claim isn't too long (should be reasonable length)
- Look at backend logs for any errors

## Development

### Testing Changes

1. Make changes to extension files
2. Go to `chrome://extensions/`
3. Click the refresh icon on the AI Truth Detector card
4. Test your changes on a webpage

### Debugging

**Background Script:**
- Go to `chrome://extensions/`
- Click "Inspect views: service worker"
- View console logs and network requests

**Content Script:**
- Open DevTools on any webpage (F12)
- Check Console tab for content script logs

**Popup:**
- Right-click the extension icon
- Click "Inspect popup"
- Debug like a normal webpage

## Keyboard Shortcuts

Currently, the extension uses the context menu. To add keyboard shortcuts:

1. Edit `manifest.json` and add a `commands` section
2. Update `background.js` to handle command events

Example:
```json
"commands": {
  "verify-claim": {
    "suggested_key": {
      "default": "Ctrl+Shift+V"
    },
    "description": "Verify selected text"
  }
}
```

## Future Enhancements

Potential features to add:
- [ ] Keyboard shortcuts for verification
- [ ] History of verified claims
- [ ] Batch verification
- [ ] Export results
- [ ] Custom styling themes
- [ ] Confidence score visualization
- [ ] Source citation links
- [ ] Firefox/Safari versions

## License

Same license as the main AI Truth Detector project.

## Support

For issues related to:
- **Backend**: See main project README
- **Extension**: Check browser console and extension service worker logs
