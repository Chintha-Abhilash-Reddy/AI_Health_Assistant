/**
 * Service Worker for AI Health Assistant PWA
 * Handles offline caching, background sync, and app installation
 */

const CACHE_NAME = 'ai-health-v1';
const RUNTIME_CACHE = 'ai-health-runtime-v1';
const OFFLINE_PAGE = '/offline.html';

const ASSETS_TO_CACHE = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js',
  '/static/js/chatbot.js',
  '/static/js/doctor_chat.js',
  '/manifest.webmanifest',
  '/static/images/icon-192x192.png',
  '/static/images/icon-512x512.png'
];

// Install event - cache essential files
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Install event triggered');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[ServiceWorker] Caching essential files');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.warn('[ServiceWorker] Some assets failed to cache:', err);
        // Don't fail installation if some assets can't be cached
        return Promise.resolve();
      });
    })
  );
  
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activate event triggered');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
            console.log('[ServiceWorker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip external URLs
  if (url.origin !== location.origin) {
    return;
  }

  // Skip API calls and authentication routes
  if (url.pathname.startsWith('/api/') ||
      url.pathname.includes('/login') ||
      url.pathname.includes('/logout') ||
      url.pathname.includes('/register')) {
    return event.respondWith(
      fetch(request).catch(() => {
        return new Response(
          JSON.stringify({ error: 'You are offline. Please check your internet connection.' }),
          { status: 503, statusText: 'Service Unavailable', headers: { 'Content-Type': 'application/json' } }
        );
      })
    );
  }

  // Cache-first strategy for static assets
  if (url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|woff|woff2|ttf)$/)) {
    return event.respondWith(
      caches.match(request).then(response => {
        if (response) {
          return response;
        }
        
        return fetch(request).then(response => {
          if (!response || response.status !== 200) {
            return response;
          }
          
          // Cache the new response
          const responseClone = response.clone();
          caches.open(RUNTIME_CACHE).then(cache => {
            cache.put(request, responseClone);
          });
          
          return response;
        }).catch(() => {
          // Return a cached version or offline page
          return caches.match(request) || new Response('Resource not found', { status: 404 });
        });
      })
    );
  }

  // Network-first strategy for HTML pages
  event.respondWith(
    fetch(request)
      .then(response => {
        // Don't cache error responses
        if (!response || response.status >= 400) {
          return response;
        }

        // Cache successful responses
        const responseClone = response.clone();
        caches.open(RUNTIME_CACHE).then(cache => {
          cache.put(request, responseClone);
        });

        return response;
      })
      .catch(() => {
        // Fallback to cache if offline
        return caches.match(request).then(response => {
          if (response) {
            return response;
          }
          
          // Show offline page for HTML requests
          if (request.headers.get('accept').includes('text/html')) {
            return caches.match(OFFLINE_PAGE);
          }
          
          return new Response('Offline - Resource unavailable', { 
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
      })
  );
});

// Handle messages from clients
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Background sync for offline data
self.addEventListener('sync', event => {
  if (event.tag === 'sync-health-data') {
    event.waitUntil(syncHealthData());
  }
});

async function syncHealthData() {
  try {
    // Sync any pending data when connection is restored
    console.log('[ServiceWorker] Syncing health data...');
    // Add your sync logic here
  } catch (error) {
    console.error('[ServiceWorker] Sync failed:', error);
  }
}
