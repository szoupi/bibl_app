// TODO: INSTALL NPM, MODIFY THIS FILE, EDIT PACKAGE.JSON etc 
var gulp = require('gulp')
var browserSync = require('browser-sync').create()
var responsive = require('gulp-responsive')


// dist is the distribution folder
var paths = {

	images: {
		src: './img-raw/**/*.{jpg,png}',
		dest: './media'
	},

}


function watch() {
	//watch the styles folder and execute styles func
	// gulp.watch(paths.styles.src, styles).on('change', browserSync.reload)
	gulp.watch('./**/*.{html,js,css}').on('change', browserSync.reload)

}

function browserSyncInit() {
	browserSync.init({
		server: {
			baseDir: './'
			// baseDir: './dist/' // for production
		}
	})
}


// MAKE IMAGES RESPONSIVE
function responsiveImages() {
	return gulp
		.src(paths.images.src)
		.pipe(responsive({
			// Resize jpg in various sizes
			'*.jpg': [{
				width: 64,
				rename: {
					suffix: '-64w'
				}
			},
			{
				width: 128,
				rename: {
					suffix: '-128w'
				}
			},
			{
				width: 400,
				rename: {
					suffix: '-400w'
				}
			},
			{
				width: 500,
				rename: {
					suffix: '-500w'
				}
			},
			{ // rename original img
				rename: {
					suffix: ''
				}
			}
			],
			// Resize all PNG images (currently the logo) to be retina ready    
			'*.png': [{
				width: 48,
				height: 48,
				rename: {
					suffix: '-48x48'
				},
			},
			{
				width: 96,
				height: 96,
				rename: {
					suffix: '-96x96'
				},
			},
			{
				width: 144,
				height: 144,
				rename: {
					suffix: '-144x144'
				},
			},
			{
				width: 192,
				height: 192,
				rename: {
					suffix: '-192x192'
				},
			},
			{
				width: 512,
				height: 512,
				rename: {
					suffix: '-512x512'
				},
			},
			{
				width: 250 * 2,
				rename: {
					suffix: '-250x250@2x'
				},
			}
			],
		}, {
			// Global configuration for all images
			// The output quality for JPEG, WebP and TIFF output formats
			quality: 70,
			// Use progressive (interlace) scan for JPEG and PNG output
			progressive: true,
			// Strip all metadata
			withMetadata: false
		}))
		.pipe(cleanDest(paths.images.dest))
		.pipe(gulp.dest(paths.images.dest))
}




// gulp.task('default', gulp.series(styles, gulp.parallel(watch, browserSyncInit)))
gulp.task('default', gulp.series(gulp.parallel(watch, browserSyncInit)))
gulp.task('images', gulp.series(responsiveImages));
