var d = document;
var b = {
    msg: {
        close_msg: function() {
            t.get('.msg .close').on('click', function() {
                t.get('.msg').attr('class', 'msg-hidden');
            });
        }
    }
}


if (!Modernizr.input.placeholder) {

/*
    TO DO 
    Cross Browser HTML5 Placeholder with Tiramisu Js
    http://webdesignerwall.com/tutorials/cross-browser-html5-placeholder-text
    */

}
