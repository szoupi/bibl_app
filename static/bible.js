// delete object dialog
function fConfirm() {
	if (confirm('Should I delete it?') == false) {
		event.preventDefault()
	}
}

// it is use for the fetch API (favorite)
// using jQuery
function getCookie(name) {
	var cookieValue = null
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';')
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i])
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
				break
			}
		}
	}
	return cookieValue
}

var csrftoken = getCookie('csrftoken')

// ============= service worker ===========
if ('serviceWorker' in navigator) {
	window.addEventListener('load', function () {
		navigator.serviceWorker.register('sw.js')
			// navigator.serviceWorker.register('sw.js')
			.then(function (registration) {
				// Registration was successful 
				console.log('ServiceWorker registration successful with scope: ', registration.scope)
			},
			function (err) {
				// registration failed
				console.log('ServiceWorker registration failed: ', err)
			})
	})
}