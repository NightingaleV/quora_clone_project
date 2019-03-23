const gulp = require('gulp');
const sass = require('gulp-sass');
const cssnano = require('gulp-cssnano');
const sourcemaps = require('gulp-sourcemaps');
const autoprefixer = require('gulp-autoprefixer');
const pixrem = require('gulp-pixrem');
const plumber = require('gulp-plumber');
const concat = require('gulp-concat');
const del = require('del');
const imagemin = require('gulp-imagemin');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify');
const runSequence = require('run-sequence');
const spawn = require('child_process').spawn;
const browserSync = require('browser-sync').create();
const reload = browserSync.reload;
const cache = require('gulp-cache');
const babel = require("gulp-babel");

const app = 'quora_clone';
const paths = {
    CSS: app + '/static/css',
    SASS: app + '/static/sass',
    JS: app + '/static/js',
    JS_MODULES: app + '/static/js/modules',
    IMAGES: app + '/static/images',
    TEMPLATES: app + '/templates',
};

// Compile SASS files
gulp.task('sass', function () {
    return gulp.src(paths.SASS + '/master.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePath: [paths.SASS]
        }).on('error', sass.logError))
        .pipe(plumber()) // Checks for errors
        .pipe(autoprefixer({browsers: ['last 2 versions']}))
        .pipe(pixrem())
        .pipe(gulp.dest(paths.CSS))
        .pipe(rename({suffix: '.min'}))
        .pipe(cssnano())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.CSS));
});

// Javascript minification
gulp.task('scripts', function () {
    return gulp.src([paths.JS_MODULES + '/ajax_csrf.js', paths.JS_MODULES + '/**/*.js'])
        .pipe(babel({
			presets: ['@babel/preset-env']
		}))
        .pipe(concat('master.js'))
        .pipe(plumber()) // Checks for errors
        .pipe(gulp.dest(paths.JS))
        .pipe(uglify()) // Minifies the js
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(paths.JS));
});

// Image compression
gulp.task('imgCompression', function () {
    return gulp.src(paths.IMAGES + '/*')
        .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(gulp.dest(paths.IMAGES))
});

// Run django server
gulp.task('runServer', function (cb) {
    var cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'});
    cmd.on('close', function (code) {
        console.log('runServer exited with code ' + code);
        cb(code);
    });
});

gulp.task('clearCache', function() {
  // Still pass the files to clear cache for
  // gulp.src('./lib/*.js')
  // .pipe(cache.clear());

  // Or, just call this for everything
  cache.clearAll();
});

// Browser sync server for live reload
gulp.task('browserSync', function () {
    browserSync.init(
        [paths.SASS + "/**/*.scss", paths.JS + "/**/*.js", paths.TEMPLATES + '/**/*.html'], {
            proxy: "localhost:8000"
        });
});

// Watcher
gulp.task('watcher', function () {
    gulp.watch(paths.SASS + '/**/*.scss', ['sass', 'clearCache']);
    gulp.watch(paths.JS + '/**/*.js', ['scripts', 'clearCache']).on("change", reload);
    gulp.watch(paths.IMAGES + '/*', ['imgCompression', 'clearCache']);
    gulp.watch(paths.TEMPLATES + '/**/*.html').on("change", reload);
});

// Default task
gulp.task('default', function () {
    runSequence(['sass', 'scripts', 'imgCompression'], ['runServer', 'browserSync', 'watcher']);
});