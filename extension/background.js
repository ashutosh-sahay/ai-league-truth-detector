/**
 * Background service worker for AI Truth Detector extension
 * Handles context menu creation and claim verification API calls
 */

// API configuration - loads from storage or defaults to localhost
let API_BASE_URL = 'http://localhost:8000';

// Load API URL from storage on startup
chrome.storage.sync.get(['apiBaseUrl'], (result) => {
  if (result.apiBaseUrl) {
    API_BASE_URL = result.apiBaseUrl;
  }
});

// Listen for storage changes to update API URL
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'sync' && changes.apiBaseUrl) {
    API_BASE_URL = changes.apiBaseUrl.newValue;
  }
});

/**
 * Create context menu on extension installation
 */
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'verify-claim',
    title: 'Verify claim',
    contexts: ['selection']
  });
});

/**
 * Handle context menu clicks
 */
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'verify-claim' && info.selectionText) {
    const claim = info.selectionText.trim();
    
    console.log('Context menu clicked, claim:', claim);
    
    // Show loading notification to content script
    chrome.tabs.sendMessage(tab.id, {
      type: 'VERIFICATION_STARTED',
      claim: claim
    }).catch(error => {
      console.error('Failed to send VERIFICATION_STARTED message:', error);
      // Try injecting the content script if it's not loaded
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      }).then(() => {
        // Retry sending the message
        chrome.tabs.sendMessage(tab.id, {
          type: 'VERIFICATION_STARTED',
          claim: claim
        });
      }).catch(err => {
        console.error('Failed to inject content script:', err);
      });
    });
    
    // Verify the claim
    verifyClaim(claim, tab.id);
  }
});

/**
 * Verify a claim using the local API
 * @param {string} claim - The claim to verify
 * @param {number} tabId - The tab ID to send results to
 */
async function verifyClaim(claim, tabId) {
  try {
    console.log('Verifying claim:', claim);
    console.log('API URL:', `${API_BASE_URL}/api/v1/verify`);
    
    const response = await fetch(`${API_BASE_URL}/api/v1/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ claim })
    });

    console.log('API response status:', response.status);

    if (!response.ok) {
      throw new Error(`API returned ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    console.log('API result:', result);
    
    // Send result to content script
    chrome.tabs.sendMessage(tabId, {
      type: 'VERIFICATION_COMPLETE',
      claim: claim,
      result: result
    }).catch(error => {
      console.error('Failed to send VERIFICATION_COMPLETE message:', error);
    });
    
  } catch (error) {
    console.error('Verification error:', error);
    
    // Send error to content script
    chrome.tabs.sendMessage(tabId, {
      type: 'VERIFICATION_ERROR',
      claim: claim,
      error: error.message
    }).catch(err => {
      console.error('Failed to send VERIFICATION_ERROR message:', err);
    });
  }
}

/**
 * Handle messages from content script or popup
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'VERIFY_CLAIM') {
    verifyClaim(request.claim, sender.tab.id);
    sendResponse({ status: 'started' });
    return true;
  }
  
  if (request.type === 'CHECK_API_HEALTH') {
    checkApiHealth().then(sendResponse);
    return true;
  }
});

/**
 * Check if the API is reachable
 * @returns {Promise<Object>} Health check result
 */
async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
      method: 'GET'
    });
    
    if (!response.ok) {
      return { 
        healthy: false, 
        error: `API returned ${response.status}` 
      };
    }
    
    const data = await response.json();
    return { healthy: true, data };
    
  } catch (error) {
    return { 
      healthy: false, 
      error: error.message 
    };
  }
}
