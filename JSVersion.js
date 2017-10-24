function get_json(url, callback) {
    http.get(url, function(res) {
        var body = '';
        res.on('data', function(chunk) {
            body += chunk;
        });

        res.on('end', function() {
            var response = JSON.parse(body);
// call function ----v
            callback(response);
        });
    });
}

         // -----------the url---v         ------------the callback---v
var mydata = get_json("http://vejr.eu/api.php?location=Roskilde&degree=C", function (resp) {
    console.log(resp);
});