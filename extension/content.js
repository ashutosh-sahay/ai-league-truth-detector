/**
 * Content script for AI Truth Detector extension
 * Displays verification results as an overlay on the page
 */

/**
 * Create and show the result popup
 * @param {Object} data - Verification data
 */
function showResultPopup(data) {
  // Remove any existing popup
  removeResultPopup();
  
  // Create popup container
  const popup = document.createElement('div');
  popup.id = 'ai-truth-detector-popup';
  popup.className = 'ai-truth-detector-popup';
  
  // Determine verdict status
  const hasEvidence = data.result.evidence_source && data.result.evidence_source !== 'unknown';
  const claimVerdict = data.result.claim_verdict;
  
  let statusClass, statusIcon, statusText, statusEmoji;
  
  if (!hasEvidence) {
    // Inconclusive - no sufficient evidence
    statusClass = 'inconclusive';
    statusIcon = '?';
    statusText = 'INCONCLUSIVE';
    statusEmoji = '❓';
  } else if (claimVerdict === true) {
    // Claim is TRUE
    statusClass = 'true';
    statusIcon = '✓';
    statusText = 'TRUE';
    statusEmoji = '✅';
  } else {
    // Claim is FALSE
    statusClass = 'false';
    statusIcon = '✗';
    statusText = 'FALSE';
    statusEmoji = '❌';
  }
  
  // Build source URLs section
  let sourcesHtml = '';
  if (data.result.source_urls && data.result.source_urls.length > 0) {
    const sourcesList = data.result.source_urls.map(url => 
      `<li><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(truncateUrl(url))}</a></li>`
    ).join('');
    sourcesHtml = `
      <div class="ai-truth-detector-sources">
        <strong>Sources</strong>
        <ul class="ai-truth-detector-sources-list">
          ${sourcesList}
        </ul>
      </div>
    `;
  }
  
  // Build popup content
  popup.innerHTML = `
    <div class="ai-truth-detector-header">
      <div class="ai-truth-detector-title">
        <span class="ai-truth-detector-icon">🔍</span>
        <span>AI Truth Detector</span>
      </div>
      <button class="ai-truth-detector-close" aria-label="Close">×</button>
    </div>
    
    <div class="ai-truth-detector-body">
      <div class="ai-truth-detector-claim">
        <strong>Claim</strong>
        <p>"${escapeHtml(data.claim)}"</p>
      </div>
      
      <div class="ai-truth-detector-verdict">
        <div class="ai-truth-detector-verdict-badge ${statusClass}">
          <span class="ai-truth-detector-verdict-emoji">${statusEmoji}</span>
          <span class="ai-truth-detector-verdict-text">${statusText}</span>
        </div>
      </div>
      
      <div class="ai-truth-detector-analysis">
        <strong>Analysis</strong>
        <p>${escapeHtml(data.result.verification_data)}</p>
      </div>
      
      ${sourcesHtml}
      
      <div class="ai-truth-detector-footer">
        <span class="ai-truth-detector-source-badge">
          ${data.result.evidence_source === 'WEB' ? '🌐' : '📚'} 
          ${escapeHtml(data.result.evidence_source || 'Unknown')}
        </span>
      </div>
    </div>
  `;
  
  // Add styles
  addStyles();
  
  // Add to page
  document.body.appendChild(popup);
  
  // Add close button listener
  const closeBtn = popup.querySelector('.ai-truth-detector-close');
  closeBtn.addEventListener('click', removeResultPopup);
  
  // Close on outside click
  setTimeout(() => {
    document.addEventListener('click', handleOutsideClick);
  }, 100);
  
  // Close on Escape key
  document.addEventListener('keydown', handleEscapeKey);
}

/**
 * Truncate URL for display
 * @param {string} url - Full URL
 * @returns {string} Truncated URL
 */
function truncateUrl(url) {
  try {
    const urlObj = new URL(url);
    const domain = urlObj.hostname.replace('www.', '');
    const path = urlObj.pathname.length > 30 
      ? urlObj.pathname.substring(0, 30) + '...' 
      : urlObj.pathname;
    return domain + path;
  } catch {
    return url.length > 50 ? url.substring(0, 50) + '...' : url;
  }
}

/**
 * Show loading popup
 * @param {string} claim - The claim being verified
 */
function showLoadingPopup(claim) {
  removeResultPopup();
  
  const popup = document.createElement('div');
  popup.id = 'ai-truth-detector-popup';
  popup.className = 'ai-truth-detector-popup';
  
  popup.innerHTML = `
    <div class="ai-truth-detector-header">
      <div class="ai-truth-detector-title">
        <span class="ai-truth-detector-icon">🔍</span>
        AI Truth Detector
      </div>
      <button class="ai-truth-detector-close" aria-label="Close">×</button>
    </div>
    
    <div class="ai-truth-detector-body">
      <div class="ai-truth-detector-claim">
        <strong>Claim:</strong> "${escapeHtml(claim)}"
      </div>
      
      <div class="ai-truth-detector-loading">
        <div class="ai-truth-detector-spinner"></div>
        <p>Verifying claim...</p>
      </div>
    </div>
  `;
  
  addStyles();
  document.body.appendChild(popup);
  
  const closeBtn = popup.querySelector('.ai-truth-detector-close');
  closeBtn.addEventListener('click', removeResultPopup);
}

/**
 * Show error popup
 * @param {string} claim - The claim that failed verification
 * @param {string} error - Error message
 */
function showErrorPopup(claim, error) {
  removeResultPopup();
  
  const popup = document.createElement('div');
  popup.id = 'ai-truth-detector-popup';
  popup.className = 'ai-truth-detector-popup';
  
  popup.innerHTML = `
    <div class="ai-truth-detector-header">
      <div class="ai-truth-detector-title">
        <span class="ai-truth-detector-icon">🔍</span>
        AI Truth Detector
      </div>
      <button class="ai-truth-detector-close" aria-label="Close">×</button>
    </div>
    
    <div class="ai-truth-detector-body">
      <div class="ai-truth-detector-claim">
        <strong>Claim:</strong> "${escapeHtml(claim)}"
      </div>
      
      <div class="ai-truth-detector-error">
        <span class="ai-truth-detector-error-icon">⚠️</span>
        <strong>Error:</strong>
        <p>${escapeHtml(error)}</p>
        <p class="ai-truth-detector-error-hint">
          Make sure the API server is running at http://localhost:8000
        </p>
      </div>
    </div>
  `;
  
  addStyles();
  document.body.appendChild(popup);
  
  const closeBtn = popup.querySelector('.ai-truth-detector-close');
  closeBtn.addEventListener('click', removeResultPopup);
}

/**
 * Remove the result popup
 */
function removeResultPopup() {
  const popup = document.getElementById('ai-truth-detector-popup');
  if (popup) {
    popup.remove();
  }
  document.removeEventListener('click', handleOutsideClick);
  document.removeEventListener('keydown', handleEscapeKey);
}

/**
 * Handle clicks outside the popup
 */
function handleOutsideClick(event) {
  const popup = document.getElementById('ai-truth-detector-popup');
  if (popup && !popup.contains(event.target)) {
    removeResultPopup();
  }
}

/**
 * Handle Escape key press
 */
function handleEscapeKey(event) {
  if (event.key === 'Escape') {
    removeResultPopup();
  }
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Add CSS styles to the page
 */
function addStyles() {
  if (document.getElementById('ai-truth-detector-styles')) {
    return;
  }
  
  const style = document.createElement('style');
  style.id = 'ai-truth-detector-styles';
  style.textContent = `
    .ai-truth-detector-popup {
      position: fixed;
      top: 20px;
      right: 20px;
      width: 440px;
      max-width: calc(100vw - 40px);
      max-height: calc(100vh - 40px);
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.05);
      z-index: 2147483647;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      color: #1a1a1a;
      overflow: hidden;
      animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      backdrop-filter: blur(10px);
    }
    
    @keyframes slideIn {
      from {
        transform: translateX(100%) scale(0.95);
        opacity: 0;
      }
      to {
        transform: translateX(0) scale(1);
        opacity: 1;
      }
    }
    
    .ai-truth-detector-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 24px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
      position: relative;
      overflow: hidden;
    }
    
    .ai-truth-detector-header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
      pointer-events: none;
    }
    
    .ai-truth-detector-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
      font-size: 17px;
      color: white;
      z-index: 1;
      text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .ai-truth-detector-icon {
      font-size: 22px;
      filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
    }
    
    .ai-truth-detector-close {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: white;
      font-size: 24px;
      line-height: 1;
      cursor: pointer;
      padding: 0;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 1;
    }
    
    .ai-truth-detector-close:hover {
      background: rgba(255, 255, 255, 0.25);
      transform: rotate(90deg);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .ai-truth-detector-body {
      padding: 24px;
      max-height: calc(100vh - 140px);
      overflow-y: auto;
      scrollbar-width: thin;
      scrollbar-color: rgba(0,0,0,0.2) transparent;
    }
    
    .ai-truth-detector-body::-webkit-scrollbar {
      width: 6px;
    }
    
    .ai-truth-detector-body::-webkit-scrollbar-track {
      background: transparent;
    }
    
    .ai-truth-detector-body::-webkit-scrollbar-thumb {
      background: rgba(0,0,0,0.2);
      border-radius: 3px;
    }
    
    .ai-truth-detector-body::-webkit-scrollbar-thumb:hover {
      background: rgba(0,0,0,0.3);
    }
    
    .ai-truth-detector-claim {
      margin-bottom: 20px;
      padding: 16px;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      border-radius: 12px;
      border: 1px solid rgba(0,0,0,0.05);
    }
    
    .ai-truth-detector-claim strong {
      display: block;
      margin-bottom: 8px;
      color: #495057;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    
    .ai-truth-detector-claim p {
      margin: 0;
      color: #212529;
      font-size: 15px;
      line-height: 1.6;
      font-weight: 500;
    }
    
    .ai-truth-detector-verdict {
      margin-bottom: 20px;
      display: flex;
      justify-content: center;
    }
    
    .ai-truth-detector-verdict-badge {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 16px 28px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      animation: scaleIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
    }
    
    @keyframes scaleIn {
      from {
        transform: scale(0.9);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }
    
    .ai-truth-detector-verdict-emoji {
      font-size: 24px;
    }
    
    .ai-truth-detector-verdict-badge.true {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: white;
      border: 2px solid rgba(255,255,255,0.3);
    }
    
    .ai-truth-detector-verdict-badge.false {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      color: white;
      border: 2px solid rgba(255,255,255,0.3);
    }
    
    .ai-truth-detector-verdict-badge.inconclusive {
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      color: white;
      border: 2px solid rgba(255,255,255,0.3);
    }
    
    .ai-truth-detector-analysis {
      margin-bottom: 20px;
      padding: 16px;
      background: white;
      border-radius: 12px;
      border: 1px solid #e5e7eb;
    }
    
    .ai-truth-detector-analysis strong,
    .ai-truth-detector-sources strong {
      display: block;
      margin-bottom: 10px;
      color: #374151;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    
    .ai-truth-detector-analysis p {
      margin: 0;
      line-height: 1.7;
      color: #4b5563;
      font-size: 14px;
    }
    
    .ai-truth-detector-sources {
      margin-bottom: 20px;
      padding: 16px;
      background: #f9fafb;
      border-radius: 12px;
      border: 1px solid #e5e7eb;
    }
    
    .ai-truth-detector-sources-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    
    .ai-truth-detector-sources-list li {
      margin-bottom: 8px;
      padding-left: 20px;
      position: relative;
    }
    
    .ai-truth-detector-sources-list li:last-child {
      margin-bottom: 0;
    }
    
    .ai-truth-detector-sources-list li::before {
      content: '→';
      position: absolute;
      left: 0;
      color: #6366f1;
      font-weight: bold;
    }
    
    .ai-truth-detector-sources-list a {
      color: #6366f1;
      text-decoration: none;
      font-size: 13px;
      transition: all 0.2s;
      display: inline-block;
    }
    
    .ai-truth-detector-sources-list a:hover {
      color: #4f46e5;
      text-decoration: underline;
      transform: translateX(2px);
    }
    
    .ai-truth-detector-footer {
      padding-top: 16px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      justify-content: flex-end;
    }
    
    .ai-truth-detector-source-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      color: #6b7280;
      border: 1px solid rgba(0,0,0,0.05);
    }
    
    .ai-truth-detector-loading {
      text-align: center;
      padding: 30px 20px;
    }
    
    .ai-truth-detector-spinner {
      width: 40px;
      height: 40px;
      margin: 0 auto 16px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .ai-truth-detector-loading p {
      margin: 0;
      color: #6c757d;
    }
    
    .ai-truth-detector-error {
      padding: 16px;
      background: #fff3cd;
      border-radius: 8px;
      border-left: 3px solid #ffc107;
    }
    
    .ai-truth-detector-error-icon {
      font-size: 20px;
      margin-right: 8px;
    }
    
    .ai-truth-detector-error strong {
      color: #856404;
    }
    
    .ai-truth-detector-error p {
      margin: 8px 0 0 0;
      color: #856404;
    }
    
    .ai-truth-detector-error-hint {
      font-size: 12px;
      margin-top: 12px !important;
      padding-top: 12px;
      border-top: 1px solid #ffc107;
      opacity: 0.8;
    }
  `;
  
  document.head.appendChild(style);
}

/**
 * Listen for messages from background script
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Content script received message:', request.type);
  
  if (request.type === 'VERIFICATION_STARTED') {
    console.log('Showing loading popup for claim:', request.claim);
    showLoadingPopup(request.claim);
    sendResponse({ status: 'loading shown' });
  }
  
  if (request.type === 'VERIFICATION_COMPLETE') {
    console.log('Showing result popup');
    showResultPopup(request);
    sendResponse({ status: 'result shown' });
  }
  
  if (request.type === 'VERIFICATION_ERROR') {
    console.log('Showing error popup:', request.error);
    showErrorPopup(request.claim, request.error);
    sendResponse({ status: 'error shown' });
  }
  
  return true; // Keep message channel open for async response
});

// Log when content script loads
console.log('AI Truth Detector content script loaded');
