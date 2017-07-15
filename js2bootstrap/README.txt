
The JavaScript v2 boilerplate module is very lean,
including an html file with links to server hosted
JavaScript, and to Content Distribution Network (CDN)
urls for vendor libraries.

It is a working app, though, and something to build
on developing a new app.

The root directory of this module includes a nodejs/gulp
based build system.  Read the README.md file for how
to set that up.  Alternatively, copy the client subdir
into a local server of your choice.

When you run `gulp serve`, a working copy of the site is
generated in build\dev, and opened in your browser.

When you wish to deploy to Rdbhost, you can upload the
build\dev contents to your Rdbhost account.
Alternatively, you can run `gulp build:dist` and create
an optimized 'production' build for deployment to
Rdbhost or any static web server available to you.
