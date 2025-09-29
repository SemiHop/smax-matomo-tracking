// Matomo tracking for SMAX
var _paq = window._paq = window._paq || [];

/* tracker methods like "setCustomDimension" should be called before "trackPageView" */
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);

(function() {
    var u="https://microfocus.matomo.cloud/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; 
    g.src='https://cdn.matomo.cloud/microfocus.matomo.cloud/matomo.js'; 
    s.parentNode.insertBefore(g,s);
})();

// Enhanced tracking for SMAX Single Page Application
console.log('SMAX Matomo Tracking Initialized');

var lastUrl = location.href;
var lastTitle = document.title;

// Track URL changes in SMAX (SPA behavior)
setInterval(function() {
    if (location.href !== lastUrl || document.title !== lastTitle) {
        console.log('SMAX Page Change Detected:', location.href);
        lastUrl = location.href;
        lastTitle = document.title;
        
        _paq.push(['setCustomUrl', location.href]);
        _paq.push(['setDocumentTitle', document.title]);
        _paq.push(['trackPageView']);
    }
}, 2000);

// Track browser back/forward navigation
window.addEventListener('popstate', function() {
    console.log('SMAX Navigation (popstate):', location.href);
    _paq.push(['setCustomUrl', location.href]);
    _paq.push(['setDocumentTitle', document.title]);
    _paq.push(['trackPageView']);
});

// Track hash changes (if SMAX uses them)
window.addEventListener('hashchange', function() {
    console.log('SMAX Hash Change:', location.href);
    _paq.push(['setCustomUrl', location.href]);
    _paq.push(['setDocumentTitle', document.title]);
    _paq.push(['trackPageView']);
});

console.log('SMAX Matomo Tracking Ready');
