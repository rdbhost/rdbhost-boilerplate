
function run() {

    var tpl = $('#guest-list .entry').remove();

    var preauth = Rdbhost.preauth();

    function add_table(tablename) {

        var q = "\
CREATE TABLE guests ( \n\
  name VARCHAR(120), \n\
  tstamp TIMESTAMP WITH TIME ZONE DEFAULT now() \n\
); \n\
GRANT SELECT, UPDATE, INSERT ON guests TO {};".replace('{}', Rdbhost.roleid('p'));

        var p = Rdbhost.super().query(q)
            .get_data();
        return p;
    }

    function _go() {

        var p = preauth.clone().query('SELECT name, tstamp FROM guests;')
            .get_data();

        return p.then(function(d) {

                $('#guest-list').empty();

                var results = d.result_sets[0];
                if (results.row_count[0] === 0)
                    return;

                for (var _row in results.records.rows) {

                    var row = results.records.rows[_row],
                        tr = tpl[0].outerHTML.replace('{{name}}', row.name)
                            .replace('{{date}}', moment(row.tstamp).fromNow()); // format('MMMM Do YYYY, h:mm:ss'));

                    $('#guest-list').append(tr);

                }
            })
            .catch(function(e) {

                var errMsg = e.message;
                if (errMsg.substr(0, 5) === '42P01') {

                    var m = /relation "([^"]+)" does not exist/.exec(errMsg);
                    if (m) {
                        var missing_tablename = m[1];
                        return add_table(missing_tablename)
                            .then(function() {
                                return _go();
                            });
                    }
                }
                else
                    throw e;
            })
    }

    $('#add').click(function(e) {

        var guestname = $('#guestname').val();
        if (!guestname || guestname.length === 0)
            return;

        var p = preauth.clone().query('INSERT INTO guests (name) VALUES (%s);').params([guestname])
            .get_data();

        p.then(_go);
    });


    return _go();

}
