var b = b || {};

b.home = {
    init: function() {
        t.get('.menu_account').on('click', function() {
            var attr = t.get('.menu_account').attr('class');
            if (attr == 'menu_account dropdown') {
                t.get('.menu_account').attr('class','open', true);
            } else {
                t.get('.menu_account').attr('class','menu_account dropdown');
            }
        });
    }
}

t.get(d).ready(function() {
    b.home.init();
    b.msg.close_msg();
    
})