/**
 * Popup script for AI Truth Detector extension
 * Handles settings and API health checks
 */

// DOM elements
const apiStatusEl = document.getElementById('api-status');
const apiUrlInput = document.getElementById('api-url');
const saveButton = document.getElementById('save-settings');
const saveMessage = document.getElementById('save-message');

/**
 * Initialize popup
 */
async function init() {
  // Load saved API URL
  const result = await chrome.storage.sync.get(['apiBaseUrl']);
  if (result.apiBaseUrl) {
    apiUrlInput.value = result.apiBaseUrl;
  }
  
  // Check API health
  checkApiHealth();
  
  // Set up event listeners
  saveButton.addEventListener('click', saveSettings);
  apiUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      saveSettings();
    }
  });
}

/**
 * Check API health status
 */
async function checkApiHealth() {
  apiStatusEl.className = 'status-indicator checking';
  apiStatusEl.innerHTML = '<div class="spinner"></div><span>Checking...</span>';
  
  try {
    const response = await chrome.runtime.sendMessage({ type: 'CHECK_API_HEALTH' });
    
    if (response.healthy) {
      apiStatusEl.className = 'status-indicator healthy';
      apiStatusEl.innerHTML = '<span class="icon-status">✓</span><span>Connected</span>';
    } else {
      apiStatusEl.className = 'status-indicator unhealthy';
      apiStatusEl.innerHTML = `<span class="icon-status">✗</span><span>Disconnected: ${response.error}</span>`;
    }
  } catch (error) {
    apiStatusEl.className = 'status-indicator unhealthy';
    apiStatusEl.innerHTML = `<span class="icon-status">✗</span><span>Error: ${error.message}</span>`;
  }
}

/**
 * Save settings to storage
 */
async function saveSettings() {
  const apiUrl = apiUrlInput.value.trim();
  
  // Validate URL
  if (!apiUrl) {
    showSaveMessage('Please enter a valid URL', 'error');
    return;
  }
  
  try {
    // Validate URL format
    new URL(apiUrl);
    
    // Save to storage
    await chrome.storage.sync.set({ apiBaseUrl: apiUrl });
    
    showSaveMessage('Settings saved successfully', 'success');
    
    // Re-check API health after saving
    setTimeout(() => {
      checkApiHealth();
    }, 500);
    
  } catch (error) {
    showSaveMessage('Invalid URL format', 'error');
  }
}

/**
 * Show save message
 * @param {string} message - Message to display
 * @param {string} type - Message type ('success' or 'error')
 */
function showSaveMessage(message, type) {
  saveMessage.textContent = message;
  saveMessage.className = `save-message ${type}`;
  
  // Clear message after 3 seconds
  setTimeout(() => {
    saveMessage.textContent = '';
    saveMessage.className = 'save-message';
  }, 3000);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
