(function(undefined) {
    
    function hasPromises() {
        var e = window;
        return "Promise" in e &&
            "resolve" in e.Promise && "reject" in e.Promise &&
            "all" in e.Promise && "race" in e.Promise &&
            function () {
                var n;
                new e.Promise(function (e) {
                    n = e
                });
                return "function" == typeof n;
            }()
    }
    function hasFetch() {
        return "fetch" in window;
    }

    var $L = window.$L = $LAB;
    
    if ( !hasPromises() )
          $L = $L.script('https://www.rdbhost.com/vendor/es6-promises/dist/es6-promise.js').wait();
    if ( !hasFetch() )
          $L = $L.script('https://www.rdbhost.com/vendor/fetch/fetch.js').wait();

    if ( !window.Rdbhost || !window.Rdbhost.preauth ) {     
        $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/util-bundle;rdbhost.js').wait();

    // -- uncomment these if you need them
    // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-emailing.js');
    // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-authenticate.js');
    // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-charge.js');

    // $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.js');
    // $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js');
    // $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.4/lodash.min.js');
    // $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js');
    $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js');
    $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js');
    // $L = $L.script('');

    $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-livereload.js').wait();    

    $L = $L.script('js/app.js').wait(function() {

        Rdbhost.connect(/* HOST_NAME */'www.rdbhost.com', /* ACCOUNT_NUMBER */1866);
        var preauth_for_reloader = Rdbhost.preauth();
        Rdbhost.activate_reloader(preauth_for_reloader);
        run();
    });
})();
