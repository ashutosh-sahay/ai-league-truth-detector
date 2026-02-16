# Chrome Extension Usage Guide

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. SELECT TEXT                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Any Webpage                                        │    │
│  │                                                     │    │
│  │  "Google was founded on September 4, 1998"         │    │
│  │   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^          │    │
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

                           ↓

┌─────────────────────────────────────────────────────────────┐
│  2. RIGHT-CLICK                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Context Menu:                                      │    │
│  │  ├─ Copy                                            │    │
│  │  ├─ Search Google                                   │    │
│  │  ├─ Translate                                       │    │
│  │  └─ 🔍 Verify claim  ← Click this!                 │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

                           ↓

┌─────────────────────────────────────────────────────────────┐
│  3. VIEW RESULT                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  🔍 AI Truth Detector                           [×] │    │
│  │  ─────────────────────────────────────────────────│    │
│  │  Claim: "Google was founded on September 4, 1998"  │    │
│  │                                                     │    │
│  │  ✓ VERIFIED                                         │    │
│  │                                                     │    │
│  │  Analysis:                                          │    │
│  │  The evidence confirms that Google was founded      │    │
│  │  on September 4, 1998, by Larry Page and Sergey    │    │
│  │  Brin while they were PhD students at Stanford.    │    │
│  │                                                     │    │
│  │  Source: RAG Store                                  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Installation Steps

### 1. Open Chrome Extensions Page

Type in address bar:
```
chrome://extensions/
```

Or: Menu (⋮) → Extensions → Manage Extensions

### 2. Enable Developer Mode

Look for a toggle switch in the top-right corner labeled "Developer mode" and turn it ON.

### 3. Load Extension

1. Click the **"Load unpacked"** button (appears after enabling Developer mode)
2. Navigate to your project folder
3. Select the `extension/` folder
4. Click "Select Folder" or "Open"

### 4. Verify Installation

You should see:
- Extension card with "AI Truth Detector" title
- Status: "Errors" should be 0
- A puzzle piece icon in your Chrome toolbar (you can pin it)

### 5. Start Backend

In terminal:
```bash
cd /path/to/ai-league-truth-detector
python -m src.main
```

Backend should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Test It!

1. Go to any website (e.g., Wikipedia, news site)
2. Highlight some text
3. Right-click → "Verify claim"
4. Watch the magic happen! ✨

## Troubleshooting

### Extension icon shows with errors
- Check that all files are in the `extension/` folder
- Look at the error details in chrome://extensions/
- Try reloading the extension

### "Verify claim" doesn't appear in menu
- Make sure you've selected/highlighted text first
- Reload the extension
- Refresh the webpage

### "Disconnected" status in popup
- Check backend is running: `python -m src.main`
- Verify it's on port 8000
- Check Settings in extension popup

### Result popup doesn't show
- Open browser DevTools (F12) and check Console for errors
- Verify backend received the request (check backend logs)
- Try reloading the extension

## Tips

- **Pin the extension**: Click the puzzle piece icon in Chrome toolbar, then click the pin icon next to "AI Truth Detector"
- **Check API status**: Click the extension icon to see if backend is connected
- **Configure API URL**: If backend runs on different port, update it in extension settings
- **View detailed logs**: Right-click extension icon → Inspect popup for debugging

## Examples to Try

1. **Wikipedia** - Highlight any fact and verify it
2. **News articles** - Check claims in recent news
3. **Social media** - Verify statements from posts
4. **Blog posts** - Fact-check technical claims

The first time you verify a claim about a new topic, it may take 2-3 seconds (web search). Subsequent verifications on the same topic are instant (local RAG).
