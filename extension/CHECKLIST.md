# Extension Installation Checklist

## ✅ Pre-Installation

- [ ] Backend is working (test with `curl http://localhost:8000/api/v1/health`)
- [ ] Python environment is activated
- [ ] Backend server is running (`python -m src.main`)
- [ ] You can access http://localhost:8000/docs in browser

## ✅ Installation Steps

- [ ] Open Chrome browser
- [ ] Navigate to `chrome://extensions/`
- [ ] Enable "Developer mode" (toggle in top-right)
- [ ] Click "Load unpacked" button
- [ ] Navigate to the project folder
- [ ] Select the `extension/` folder
- [ ] Click "Select Folder" or "Open"
- [ ] Extension card appears with no errors

## ✅ Verification Steps

- [ ] Extension appears in `chrome://extensions/` list
- [ ] Extension icon appears in Chrome toolbar (puzzle piece area)
- [ ] Click extension icon → popup opens
- [ ] API Status shows "Connected" (green checkmark)
- [ ] Settings section shows `http://localhost:8000`

## ✅ Functionality Test

- [ ] Open `extension/test-page.html` in Chrome (or any webpage)
- [ ] Highlight any text
- [ ] Right-click on highlighted text
- [ ] "Verify claim" option appears in context menu
- [ ] Click "Verify claim"
- [ ] Loading popup appears immediately
- [ ] After 1-3 seconds, result popup shows with verdict
- [ ] Can close popup by clicking X or Escape key
- [ ] Can click outside popup to close it

## ✅ Test Different Claims

- [ ] Test a true claim (should show ✓ VERIFIED)
- [ ] Test a false claim (should show ✗ NOT VERIFIED)
- [ ] Test a claim not in KB (should use web search)
- [ ] Verify "Source" shows "RAG Store" or "WEB"

## ✅ Error Handling Test

- [ ] Stop backend server (Ctrl+C)
- [ ] Try to verify a claim
- [ ] Error popup should appear with helpful message
- [ ] Extension popup should show "Disconnected" status
- [ ] Restart backend
- [ ] Extension popup should show "Connected" again

## ✅ Settings Test

- [ ] Click extension icon
- [ ] Change API Base URL to `http://localhost:9999`
- [ ] Click "Save Settings"
- [ ] Success message appears
- [ ] Try to verify claim → should show error (wrong port)
- [ ] Change back to `http://localhost:8000`
- [ ] Save again
- [ ] Verify claim works again

## 🎯 Success Indicators

✅ Extension loads without errors  
✅ Right-click menu works  
✅ Result popups display correctly  
✅ API connection is stable  
✅ Settings persist after browser restart  

## 🐛 If Something Doesn't Work

1. **Extension won't load**
   - Check all files exist in `extension/` folder
   - Look for red error text in chrome://extensions/
   - Reload the extension

2. **No right-click menu**
   - Reload extension in chrome://extensions/
   - Refresh the webpage
   - Make sure text is actually selected

3. **Popup doesn't appear**
   - Open DevTools (F12) → Console tab
   - Check for JavaScript errors
   - Check Network tab for failed API calls

4. **"Disconnected" status**
   - Verify backend: `curl http://localhost:8000/api/v1/health`
   - Check backend logs for errors
   - Verify CORS is configured (it is by default)

5. **Popup appears but no result**
   - Check browser console (F12)
   - Check backend terminal for errors
   - Try with a simpler claim

## 📋 Quick Test Commands

```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Test verify endpoint
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Google was founded in 1998"}'

# Start backend (if not running)
cd /path/to/ai-league-truth-detector
python -m src.main
```

## 🎉 You're Done!

If all checkboxes are checked, your Chrome extension is working perfectly!

Try it on real websites:
- Wikipedia articles
- News sites  
- Blog posts
- Social media (Twitter, Reddit, etc.)

Enjoy verifying claims with AI! 🔍✨
