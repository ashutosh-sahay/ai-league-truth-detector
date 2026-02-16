# Debugging the Extension

## Step-by-Step Debugging Process

### 1. Reload the Extension

After making changes:
1. Go to `chrome://extensions/`
2. Find "AI Truth Detector"
3. Click the **reload icon** (circular arrow)
4. Check for any errors

### 2. Check Service Worker Console

To see background script logs:
1. Go to `chrome://extensions/`
2. Find "AI Truth Detector"
3. Click **"service worker"** link (or "Inspect views: service worker")
4. A DevTools window opens showing the background script console

**Expected logs when you click "Verify claim":**
```
Context menu clicked, claim: <your text>
Verifying claim: <your text>
API URL: http://localhost:8000/api/v1/verify
API response status: 200
API result: {claim_verdict: true, ...}
```

### 3. Check Content Script Console

To see content script logs:
1. Go to the webpage where you're testing
2. Press **F12** or right-click → Inspect
3. Go to **Console** tab
4. Look for messages starting with "AI Truth Detector"

**Expected logs when extension loads:**
```
AI Truth Detector content script loaded
```

**Expected logs when you click "Verify claim":**
```
Content script received message: VERIFICATION_STARTED
Showing loading popup for claim: <your text>
Content script received message: VERIFICATION_COMPLETE
Showing result popup
```

### 4. Common Issues & Solutions

#### Issue: Content script not loaded

**Symptoms:**
- Service worker logs show message sent
- No logs in page console
- Error: "Could not establish connection"

**Solution:**
1. Refresh the webpage (F5)
2. Try on a different page (not chrome:// pages)
3. Check console for content script errors

---

#### Issue: API connection fails

**Symptoms:**
- Error message in popup: "Failed to fetch"
- Service worker shows network error

**Solution:**
1. Make sure backend is running: `python -m src.main`
2. Test manually: `curl http://localhost:8000/api/v1/health`
3. Check CORS is enabled (it should be by default)

---

#### Issue: Popup doesn't appear

**Symptoms:**
- Logs show messages sent and received
- No visual popup on page

**Solution:**
1. Check page console for JavaScript errors
2. Look for CSP (Content Security Policy) errors
3. Try on a simple page first (like the test-page.html)
4. Check if `document.body` exists

---

#### Issue: Extension doesn't work on certain pages

**Some pages block extensions:**
- Chrome internal pages (`chrome://`)
- Chrome Web Store
- Some secure banking sites

**Solution:** Test on regular websites like Wikipedia or the included test-page.html

---

### 5. Testing Checklist

Do these in order:

- [ ] Extension loaded without errors in chrome://extensions/
- [ ] Service worker console opens (no errors)
- [ ] Open test-page.html in browser
- [ ] Backend is running (`python -m src.main`)
- [ ] Test backend: `curl http://localhost:8000/api/v1/health`
- [ ] Refresh test-page.html
- [ ] Check page console shows "AI Truth Detector content script loaded"
- [ ] Highlight text on the page
- [ ] Right-click → "Verify claim" appears
- [ ] Click "Verify claim"
- [ ] Check service worker logs for API call
- [ ] Check page console for message received
- [ ] Visual popup should appear

---

### 6. Quick Test Commands

**Test backend health:**
```bash
curl http://localhost:8000/api/v1/health
```

**Test verification endpoint:**
```bash
curl -X POST http://localhost:8000/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "Google was founded in 1998"}'
```

---

### 7. Manual Test Without Extension

To verify backend is working:

1. Open browser DevTools (F12)
2. Go to Console tab
3. Paste this code:

```javascript
fetch('http://localhost:8000/api/v1/verify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ claim: 'Google was founded in 1998' })
})
.then(r => r.json())
.then(d => console.log('Result:', d))
.catch(e => console.error('Error:', e));
```

Should log the verification result.

---

### 8. Force Refresh Everything

If nothing works:

1. **Reload extension:** chrome://extensions/ → reload icon
2. **Refresh page:** F5 or Ctrl+R
3. **Clear cache:** Ctrl+Shift+Delete → Clear cached files
4. **Restart browser**
5. **Restart backend server**

---

### 9. Check for Conflicting Extensions

Some extensions can interfere:

1. Disable other extensions temporarily
2. Test again
3. Re-enable one by one to find conflict

---

### 10. Verify File Contents

Make sure all files are present:

```bash
ls -la extension/
```

Should show:
- manifest.json
- background.js
- content.js
- popup.html
- popup.css
- popup.js

---

## Expected Behavior

### Successful Flow:

1. **User highlights text** → Text selected on page
2. **User right-clicks** → Context menu shows "Verify claim"
3. **User clicks menu item** → Loading popup appears immediately
4. **Backend processes** → Takes 1-3 seconds
5. **Result appears** → Popup updates with verdict

### What You Should See:

**Loading State:**
```
┌─────────────────────────────┐
│ 🔍 AI Truth Detector    [×] │
├─────────────────────────────┤
│ Claim: "Your selected text" │
│                             │
│      ⟲ (spinner)            │
│   Verifying claim...        │
└─────────────────────────────┘
```

**Result State:**
```
┌─────────────────────────────┐
│ 🔍 AI Truth Detector    [×] │
├─────────────────────────────┤
│ Claim: "Your selected text" │
│                             │
│ ✓ VERIFIED                  │
│                             │
│ Analysis:                   │
│ <AI analysis text...>       │
│                             │
│ Source: RAG Store          │
└─────────────────────────────┘
```

---

## Still Not Working?

### Share These Details:

1. **Service worker console logs** (full output)
2. **Page console logs** (full output)
3. **Backend terminal output** (any errors?)
4. **Chrome version** (chrome://version/)
5. **Which page you're testing on**
6. **Screenshot of chrome://extensions/** (showing extension status)

### Try Minimal Test:

1. Open `extension/test-page.html` in Chrome
2. Highlight "Google was founded in 1998"
3. Right-click → Verify claim
4. Should work on this simple page

If it works on test-page.html but not other sites, the issue is page-specific (CSP, iframe, etc.).
