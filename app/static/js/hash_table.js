var b = b || {};
b.hash_table = {
    init: function() {
        
        // Main element to change language
        var button_languages = t.get('.button-lng');
        var list_languages_in_menu = t.get('.dropdown-lng .dropdown-menu li');
                    
        // Open languages menu
        button_languages.on('click', function() {
            var attr = t.get('.dropdown-lng').attr('class');
            if (attr == 'span2 dropdown-lng') {
                t.get('.dropdown-lng').attr('class', 'open', true);
            } else {
                t.get('.dropdown-lng').attr('class', 'span2 dropdown-lng');
            }
        });

        // Change language
        list_languages_in_menu.on('click', function(e) {
            
            var li_press = e.currentTarget;
            var code = li_press.className.split('_')[0];

            for (var i = b.hash_table.code_languages.length; i--;) {
                var lan = b.hash_table.code_languages[i];
                t.get('.section_' + lan).css({
                    'display': 'none'
                });
                t.get('li.' + lan + '_lan').attr('class', lan + '_lan');
            }

            t.get('.section_' + code).css({
                'display': 'block'
            });
            t.get('.dropdown-lng').attr('class', 'span2 dropdown-lng');
            t.get('li.' + code + '_lan').attr('class', code + '_lan active');
            button_languages.html(b.hash_table.name_languages[code] + '<span class="caret"></span>');
        });

    },
    init_remove: function() {

        t.get('.remove_item').on('click', function(e) {
            var chosen = e.currentTarget.value;
            var item_id = e.currentTarget.className.split('_')[2];
            b.admin.check_remove(item_id, 'hash_table');
        });

    },
    number_document: 0,
    init_num_field: function() {

        this.number_document = parseInt(t.get('.name_key').length / 2);

    },
    code_languages: [],
    name_languages: {},
    init_add_label: function() {

        t.get('.hash_add_label').on('click', function(e) {
            b.hash_table.number_document += 1;
            var num = b.hash_table.number_document
            for (var i = b.hash_table.code_languages.length; i--;) {
                var lan = b.hash_table.code_languages[i];
                var label = '<div class="control-group section_num_' + num + ' row-fluid">';
                label += '<input type="text" name="label_name_' + lan + '_' + num + '" value="" ';
                label += 'class="span3 name_key label_name_' + lan + '_' + num + '" maxlength="30" />';
                label += '<textarea name="label_' + lan + '_' + num + '"';
                label += 'tabindex="{{ j }}" class="span6 label_' + lan + '_' + num + '"></textarea>';
                label += '<span class="hash_remove_label button button_remove button-red span2" id="' + num + '">- Remove field</span>';
                label += '</div>';

                t.get('.language_' + lan).before(label);
            }
            b.hash_table.init_remove_label();
            b.hash_table.init_change_name_label();
        });


    },
    init_remove_label: function() {

        t.get('.hash_remove_label').on('click', function(e) {
            var button_click = e.currentTarget.value;
            var num_label = t.get(this).attr('id');
            t.get('.section_num_' + num_label).destroy()
        });

    },
    init_change_name_label: function() {

        t.get('.name_key').on('keyup', function(e) {

            var label_press = e.currentTarget
            var label_value = label_press.value
            var label_num = label_press.className.split('_')[4]

            for (var i = b.hash_table.code_languages.length; i--;) {
                var lan = b.hash_table.code_languages[i];
                t.get('.label_name_' + lan + '_' + label_num).value(label_value);
            }
        });

    }
}
