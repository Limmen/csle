$(function() {

    // $('.collapse').collapse('hide');
    $('.list-group-item.active').parent().parent('.collapse').collapse('show');

    $.ajaxSetup({cache: true});

    var fuzzyhound = new FuzzySearch();

    function setsource(url, keys) {
        $.getJSON(url).then(function (response) {
            fuzzyhound.setOptions({
                source: response,
                keys: keys
            })
        });
    }

    setsource(baseurl + '/search.json', ["title"]);

    $('#search-box').typeahead({
        minLength: 0,
        highlight: true
    }, {
        name: 'pages',
        display: 'title',
        source: fuzzyhound
    });

    $('#search-box').bind('typeahead:select', function(ev, suggestion) {
        window.location.href = suggestion.url;
    });


    // Markdown plain out to bootstrap style
    $('#markdown-content-container table').addClass('table');
    $('#markdown-content-container img').addClass('img-responsive');


});
