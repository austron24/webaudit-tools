// Simple analytics - logs events to console and could be extended
(function() {
    const toolName = document.title.split(' - ')[0] || 'Unknown Tool';
    
    // Log page view
    console.log('[Analytics] Page view:', toolName, window.location.href);
    
    // Track form submissions
    document.addEventListener('submit', function(e) {
        console.log('[Analytics] Form submit:', toolName);
    });
    
    // Track CTA clicks
    document.addEventListener('click', function(e) {
        if (e.target.href && e.target.href.includes('fiverr.com')) {
            console.log('[Analytics] Fiverr CTA click:', toolName);
        }
    });
    
    // Could add real analytics here (Google Analytics, Plausible, etc.)
    // Example for Google Analytics:
    // gtag('event', 'page_view', { page_title: toolName });
})();
