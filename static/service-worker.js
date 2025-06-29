// Finla - Service Worker for PWA functionality

const CACHE_NAME = 'finla-v1.0.0';
const STATIC_CACHE_NAME = 'finla-static-v1.0.0';
const DYNAMIC_CACHE_NAME = 'finla-dynamic-v1.0.0';

// Files to cache immediately
const STATIC_ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/js/scripts.js',
    '/static/js/charts.js',
    '/manifest.json',
    // Bootstrap and external libraries from CDN
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap'
];

// API routes to cache
const API_ROUTES = [
    '/api/chart_data'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Service Worker: Installation complete');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Service Worker: Installation failed', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE_NAME && 
                            cacheName !== DYNAMIC_CACHE_NAME) {
                            console.log('Service Worker: Deleting old cache', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Activation complete');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip cross-origin requests and non-GET requests
    if (url.origin !== location.origin || request.method !== 'GET') {
        return;
    }
    
    // Handle API requests
    if (API_ROUTES.some(route => url.pathname.includes(route))) {
        event.respondWith(networkFirstStrategy(request));
        return;
    }
    
    // Handle static assets
    if (STATIC_ASSETS.some(asset => url.pathname === asset || request.url === asset)) {
        event.respondWith(cacheFirstStrategy(request));
        return;
    }
    
    // Handle navigation requests
    if (request.mode === 'navigate') {
        event.respondWith(networkFirstStrategy(request));
        return;
    }
    
    // Default strategy for other requests
    event.respondWith(staleWhileRevalidateStrategy(request));
});

// Caching strategies
async function cacheFirstStrategy(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.error('Cache first strategy failed:', error);
        return createOfflineResponse();
    }
}

async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('Network first: falling back to cache', request.url);
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        return createOfflineResponse(request);
    }
}

async function staleWhileRevalidateStrategy(request) {
    try {
        const cachedResponse = await caches.match(request);
        const networkResponsePromise = fetch(request);
        
        // Update cache in background
        networkResponsePromise.then(networkResponse => {
            if (networkResponse.ok) {
                const cache = caches.open(DYNAMIC_CACHE_NAME);
                cache.then(c => c.put(request, networkResponse.clone()));
            }
        }).catch(error => {
            console.log('Background update failed:', error);
        });
        
        return cachedResponse || networkResponsePromise;
    } catch (error) {
        console.error('Stale while revalidate failed:', error);
        return createOfflineResponse();
    }
}

// Create offline response
function createOfflineResponse(request) {
    if (request && request.mode === 'navigate') {
        return new Response(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Finla - Offline</title>
                <style>
                    body {
                        font-family: 'Inter', sans-serif;
                        background: linear-gradient(135deg, #000000, #1a1a1a);
                        color: #f8f9fa;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                        text-align: center;
                    }
                    .offline-container {
                        max-width: 400px;
                        padding: 2rem;
                        border: 2px solid #FFD700;
                        border-radius: 12px;
                        background: rgba(255, 215, 0, 0.05);
                    }
                    .gold-text { color: #FFD700; }
                    .btn {
                        background: #FFD700;
                        color: #000;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 6px;
                        cursor: pointer;
                        font-weight: 600;
                        margin-top: 1rem;
                    }
                    .btn:hover { background: #DAA520; }
                    .icon { font-size: 3rem; margin-bottom: 1rem; }
                </style>
            </head>
            <body>
                <div class="offline-container">
                    <div class="icon">🌐</div>
                    <h2 class="gold-text">You're Offline</h2>
                    <p>Finla is currently unavailable. Please check your internet connection and try again.</p>
                    <button class="btn" onclick="window.location.reload()">
                        Retry Connection
                    </button>
                    <p style="margin-top: 1rem; font-size: 0.9rem; color: #adb5bd;">
                        Your data is safe and will sync when you're back online.
                    </p>
                </div>
            </body>
            </html>
        `, {
            status: 200,
            headers: {
                'Content-Type': 'text/html',
                'Cache-Control': 'no-cache'
            }
        });
    }
    
    // For API requests, return JSON
    return new Response(JSON.stringify({
        error: 'Offline',
        message: 'This feature requires an internet connection'
    }), {
        status: 503,
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }
    });
}

// Background sync for offline transactions
self.addEventListener('sync', event => {
    console.log('Service Worker: Background sync triggered', event.tag);
    
    if (event.tag === 'sync-transactions') {
        event.waitUntil(syncTransactions());
    }
});

async function syncTransactions() {
    try {
        // Check if there are pending transactions in IndexedDB
        const pendingTransactions = await getPendingTransactions();
        
        if (pendingTransactions.length > 0) {
            console.log('Syncing', pendingTransactions.length, 'pending transactions');
            
            for (const transaction of pendingTransactions) {
                await submitTransaction(transaction);
            }
            
            await clearPendingTransactions();
            console.log('All pending transactions synced');
        }
    } catch (error) {
        console.error('Failed to sync transactions:', error);
    }
}

// Placeholder functions for offline transaction storage
async function getPendingTransactions() {
    // Implementation would use IndexedDB to store offline transactions
    return [];
}

async function submitTransaction(transaction) {
    // Implementation would submit transaction to server
    console.log('Submitting transaction:', transaction);
}

async function clearPendingTransactions() {
    // Implementation would clear IndexedDB
    console.log('Clearing pending transactions');
}

// Push notification handling
self.addEventListener('push', event => {
    console.log('Service Worker: Push notification received');
    
    const options = {
        body: 'Check your latest spending insights!',
        icon: '/static/icon-192x192.png',
        badge: '/static/icon-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: '2'
        },
        actions: [
            {
                action: 'explore',
                title: 'View Analytics',
                icon: '/static/icon-192x192.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/icon-192x192.png'
            }
        ]
    };
    
    const title = event.data ? event.data.text() : 'Finla Finance Tracker';
    
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    console.log('Service Worker: Notification clicked');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/analytics')
        );
    } else if (event.action === 'close') {
        // Just close the notification
    } else {
        // Default action - open app
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Message handling from main app
self.addEventListener('message', event => {
    console.log('Service Worker: Message received', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_TRANSACTION') {
        // Cache transaction for offline submission
        cacheTransactionOffline(event.data.transaction);
    }
});

async function cacheTransactionOffline(transaction) {
    try {
        // Store transaction in IndexedDB for later sync
        console.log('Caching transaction for offline sync:', transaction);
        
        // Request background sync
        await self.registration.sync.register('sync-transactions');
    } catch (error) {
        console.error('Failed to cache transaction:', error);
    }
}

// Periodic background sync (if supported)
self.addEventListener('periodicsync', event => {
    if (event.tag === 'daily-sync') {
        event.waitUntil(performDailySync());
    }
});

async function performDailySync() {
    try {
        console.log('Performing daily background sync');
        
        // Sync any pending data
        await syncTransactions();
        
        // Refresh cache for frequently used data
        const cache = await caches.open(DYNAMIC_CACHE_NAME);
        await cache.add('/api/chart_data');
        
        console.log('Daily sync completed');
    } catch (error) {
        console.error('Daily sync failed:', error);
    }
}

// Update notification
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'UPDATE_AVAILABLE') {
        event.ports[0].postMessage({
            type: 'UPDATE_AVAILABLE',
            message: 'A new version of Finla is available!'
        });
    }
});

console.log('🔧 Finla Service Worker Loaded');
