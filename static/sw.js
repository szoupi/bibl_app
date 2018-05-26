importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.2.0/workbox-sw.js');

if (workbox) {
	console.log(`Yay! Workbox is loaded`);
} else {
	console.log(`Boo! Workbox didn't load`);
}

// workbox.routing.registerRoute(
// 	new RegExp('.*\.js'),
// 	workbox.strategies.networkFirst()
// );



// Cache JS/CSS files
workbox.routing.registerRoute(
	/\.(?:js|html|css)$/,
	// Use cache but update in the background ASAP
	workbox.strategies.staleWhileRevalidate({
		// Use a custom cache name
		cacheName: 'static-resources',
	}),
);

workbox.routing.registerRoute(
	// Cache image files
	/.*\.(?:png|jpg|jpeg|svg|gif|webp)/,
	// Use the cache if it's available
	workbox.strategies.cacheFirst({
		// Use a custom cache name
		cacheName: 'image-cache',
		plugins: [
			new workbox.expiration.Plugin({
				// Cache only 60 images
				maxEntries: 80,
				// Cache for a maximum of a week
				maxAgeSeconds: 7 * 24 * 60 * 60,
			})
		],
	})
);


workbox.routing.registerRoute(
	new RegExp('https://fonts.(?:googleapis|gstatic).com/(.*)'),
	workbox.strategies.cacheFirst({
		cacheName: 'googleapis',
		plugins: [
			new workbox.expiration.Plugin({
				maxEntries: 10,
			}),
		],
	}),
);
