# 🚀 Getting Started with AI Truth Detector Chrome Extension

Welcome! This guide will get you up and running in under 5 minutes.

## 📋 What You Need

- ✅ Chrome browser (version 88+)
- ✅ Python backend running (the main AI Truth Detector project)
- ✅ 2 minutes of your time

## 🎯 Quick Start (3 Steps)

### Step 1: Start Your Backend

Open a terminal and run:

```bash
cd /path/to/ai-league-truth-detector
python -m src.main
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Test it**: Open http://localhost:8000/docs in your browser

---

### Step 2: Install Extension

1. **Open** Chrome and type in address bar: `chrome://extensions/`

2. **Enable** "Developer mode" (toggle in top-right corner)

3. **Click** the "Load unpacked" button

4. **Navigate** to your project and select the `extension/` folder

5. **Done!** You should see the extension card appear

---

### Step 3: Test It!

**Option A: Use our test page**

1. Open `extension/test-page.html` in Chrome
2. Highlight any claim on the page
3. Right-click → "Verify claim"
4. Watch the magic happen! ✨

**Option B: Try on any website**

1. Go to Wikipedia, a news site, or any webpage
2. Highlight some text
3. Right-click → "Verify claim"
4. See the verification result

---

## 🎨 Optional: Add Icons

The extension works without custom icons (Chrome uses defaults), but if you want custom ones:

**Method 1: Auto-generate** (if you have Pillow installed)
```bash
pip install pillow
python extension/generate_icons.py
```

**Method 2: Add your own**
- Create 4 PNG files: 16×16, 32×32, 48×48, 128×128
- Name them: `icon16.png`, `icon32.png`, `icon48.png`, `icon128.png`
- Place in `extension/icons/` folder

Then reload the extension in Chrome.

---

## 📖 How to Use

### Basic Usage

```
1. SELECT text on any webpage
       ↓
2. RIGHT-CLICK on selected text
       ↓
3. CLICK "Verify claim"
       ↓
4. VIEW result in popup
```

### Result Indicators

- **✓ VERIFIED** (green) = Claim is true based on evidence
- **✗ NOT VERIFIED** (red) = Claim is false or unsupported

### Sources

- **RAG Store** = Answered from local knowledge base (fast!)
- **WEB** = Used web search (slower, but more comprehensive)

---

## 💡 Tips & Tricks

### Tip 1: Check Connection Status
Click the extension icon (puzzle piece in toolbar) to see if backend is connected.

### Tip 2: First Time is Slower
The first verification of a new topic uses web search (2-3 seconds). Subsequent similar queries are instant!

### Tip 3: Pin the Extension
Click the puzzle piece icon → Find "AI Truth Detector" → Click pin icon

### Tip 4: Highlight Whole Sentences
For best results, highlight complete claims/statements, not just keywords.

---

## 🔧 Troubleshooting

### Problem: Extension shows errors after loading

**Solution:**
- Check that all files exist in `extension/` folder
- Icon errors are OK (extension works without icons)
- Click "Clear" on any other errors and try reloading

---

### Problem: "Verify claim" doesn't appear in menu

**Solution:**
1. Make sure text is actually selected (highlighted)
2. Reload the extension in chrome://extensions/
3. Refresh the webpage you're testing on

---

### Problem: API Status shows "Disconnected"

**Solution:**
1. Make sure backend is running: `python -m src.main`
2. Test backend: `curl http://localhost:8000/api/v1/health`
3. Check Settings in extension popup has correct URL

---

### Problem: Popup shows error message

**Solution:**
- **"API returned 500"**: Check backend terminal for error logs
- **"Failed to fetch"**: Backend might not be running
- **"Network error"**: Check if backend is on correct port (8000)

---

### Problem: Result popup doesn't appear

**Solution:**
1. Open DevTools (press F12)
2. Check Console tab for errors
3. Try a shorter/simpler claim
4. Reload the extension

---

## 🧪 Testing

### Test Page

Open `extension/test-page.html` for ready-made test claims:

- ✅ **True claims** about Google (should verify)
- ❌ **False claims** (should not verify)
- 🌐 **General knowledge** (uses web search)

### Manual Testing Checklist

- [ ] Highlight text → right-click → menu appears
- [ ] Click "Verify claim" → loading popup shows
- [ ] After 1-3 seconds → result popup appears
- [ ] Result shows verdict (verified/not verified)
- [ ] Can close popup (X button, Escape, click outside)
- [ ] Extension popup shows "Connected" status

---

## ⚙️ Configuration

### Change API URL

If your backend runs on a different port:

1. Click extension icon (in toolbar)
2. Scroll to Settings section
3. Update "API Base URL" (e.g., `http://localhost:9000`)
4. Click "Save Settings"
5. Status indicator updates automatically

---

## 📚 Documentation

- **README.md** - Full documentation
- **QUICKSTART.md** - Ultra-quick 2-minute guide  
- **INSTALLATION.md** - Visual installation guide
- **CHECKLIST.md** - Complete testing checklist
- **EXTENSION_SUMMARY.md** - Technical details

---

## 🎓 Example Workflows

### Workflow 1: Reading News

1. Open a news article
2. See a suspicious claim
3. Highlight it → right-click → verify
4. Check if it's supported by evidence

### Workflow 2: Fact-Checking Social Media

1. See a claim on Twitter/Reddit
2. Copy and paste into any text field
3. Highlight → right-click → verify
4. Share the result with others

### Workflow 3: Research

1. Reading multiple sources
2. Highlight key claims as you read
3. Verify each one quickly
4. Build confidence in your understanding

---

## 🔒 Privacy & Security

- ✅ **100% Local**: All processing on your machine
- ✅ **No Tracking**: No analytics or telemetry
- ✅ **No External Calls**: Only talks to your local backend
- ✅ **Open Source**: All code is visible and auditable

---

## 🎯 Success!

If you've followed the steps above, you should now have:

- ✅ Extension loaded in Chrome
- ✅ Backend running locally
- ✅ Successfully verified at least one claim
- ✅ Seen the beautiful result popup

**Congratulations!** You're now ready to verify claims across the web! 🎉

---

## 🆘 Need Help?

1. Check **TROUBLESHOOTING** section above
2. Review **CHECKLIST.md** for detailed testing steps
3. Check browser console (F12) for error messages
4. Check backend terminal for API errors
5. Make sure CORS is enabled (it is by default)

---

## 🚀 Next Steps

- Try it on real websites (Wikipedia, news sites, blogs)
- Customize the styling in `content.js`
- Add custom icons with `generate_icons.py`
- Share with friends (just share the `extension/` folder)

---

**Happy Fact-Checking!** 🔍✨
