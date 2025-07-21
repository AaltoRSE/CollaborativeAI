const CACHE_NAME = 'floorplan-v1';
const ASSETS = [
  '/',
  '../index.html',
  '/images/bed.png',
  '/images/chair.png',
  '/images/table.png',
  '/styles.css',
  '../src/index.css',
  '../src/main.jsx'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  console.log('service worker installed and assets cached');
  self.skipWaiting();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(res => res || fetch(event.request))
  );
});

self.addEventListener('activate', event => {
  console.log('service worker Activated');
  clients.claim();
});