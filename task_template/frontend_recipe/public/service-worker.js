self.addEventListener('install', event => {
  console.log('service worker installed');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('service worker Activated');
  clients.claim();
});