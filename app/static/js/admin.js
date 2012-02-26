var b = b || {};
b.admin = {
    check_remove: function(item_id, module) {
        var div = t.make('div');
        div.attr('class', 'check_remove');
        var html = '<span>Are you sure you want to remove this item?</span>';
        html += '<span style="width:49%;display:inline-block;cursor:pointer;" ';
        html += 'onclick="b.admin.remove_item(true,\'' + item_id + '\', \'' + module + '\')">Yes</span>';
        html += '<span style="width:49%;text-align:right;display:inline-block;cursor:pointer;" ';
        html += 'onclick="b.admin.remove_item(false)">No</span>';
        div.html(html);
        t.get('.content').after(div);
    },
    check_remove_hidden: function() {
        t.get('.check_remove').destroy();
    },
    remove_item: function(check, item_id, module) {
        if (check) {
            t.ajax({
                'url': '/admin/' + module + '/remove/' + item_id + '/',
                'success': function(data) {
                    if (data == 'ok') {
                        t.get('.item_' + item_id).destroy();
                    }
                }
            });
        }
        b.admin.check_remove_hidden();
    }
}
