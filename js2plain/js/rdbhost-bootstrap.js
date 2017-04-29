var $L = $LAB
    .script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/util-bundle;rdbhost.js').wait(
        function() {

            if ( !Rdbhost.featuredetects.hasPromises() )
                $L = $L.script('https://www.rdbhost.com/vendor/es6-promises/dist/es6-promise.js');
            if ( !Rdbhost.featuredetects.hasFetch() )
                $L = $L.script('https://www.rdbhost.com/vendor/fetch/fetch.js').wait();
            $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-livereload.js');

            // -- uncomment these if you need them
            // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-emailing.js');
            // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-authenticate.js');
            // $L = $L.script('https://www.rdbhost.com/vendor/rdbhost/2.2/lib/js/rdb2-charge.js');


            // $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js');
            $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js');
            $L = $L.script('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js');
            // $L = $L.script('');

            $L = $L.script('js/example.js').wait(function() {

                Rdbhost.connect('www.rdbhost.com', 1866);
                var preauth_for_reloader = Rdbhost.preauth();
                Rdbhost.activate_reloader(preauth_for_reloader);

                run();

            });
        });
