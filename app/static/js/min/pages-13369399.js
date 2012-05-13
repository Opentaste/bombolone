var b = b || {};
b.pages = {
    init: function() {},
    init_language: function() {  
        
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
            
            for (var i = b.pages.code_languages.length; i--;) {
                var lan = b.pages.code_languages[i];
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
            button_languages.html(b.pages.name_languages[code] + '<span class="caret"></span>');
        });
    },
    number_of_label: 0,
    code_languages: [],
    name_languages: {},
    init_change_label: function() {

        for (var i = 0, len_of_label = this.number_of_label; i < len_of_label; i++){
            b.pages.add_on_change(i);
        }
        
        this.number_of_label -= 1;

    },
    init_add_label: function() {

        t.get('.pages_add_label').on('click', function(e) {
            
            console.log(b.pages.number_of_label)
            
            b.pages.number_of_label += 1;
            t.ajax({
                'url': '/admin/pages/add_label/' + b.pages.number_of_label + '/',
                'success': function(data) {
                    for (var i = 0; i < b.pages.code_languages.length; i++) {
                        t.get('.pages_' + b.pages.code_languages[i]).before(data.split('__Bombolone__')[i])
                    }
                    b.pages.add_on_change(b.pages.number_of_label);
                    b.pages.init_remove_label();
                    b.pages.init_change_name_label();
                    
                    t.get('.label_' + b.pages.number_of_label + '_1').css({
                        'display': 'inline'
                    });
                }
            });
        });

    },
    init_remove_label: function() {

        t.get('.pages_remove_label').on('click', function(e) {
            var button_click = e.currentTarget.value;
            var num_label = t.get(this).attr('id');
            t.get('.section_num_' + num_label).destroy()
        });

    },
    init_change_name_label: function() {

        t.get('.name_label').on('keyup', function(e) {
            var label_press = e.currentTarget
            var label_value = label_press.value
            var label_num = label_press.className.split('_')[4]
            t.get('.label_en_name_' + label_num).value(label_value);
            t.get('.label_it_name_' + label_num).value(label_value);
        });

    },
    add_on_change: function(i) {

        t.get('.label_' + i + '_0').on('change', function(e) {
            var chosen = e.currentTarget.value;
            var chosen_num = e.currentTarget.name.split('_')[1];
            t.get('.label_' + chosen_num + '_1').css({
                'display': 'none'
            });
            t.get('.label_' + chosen_num + '_2').css({
                'display': 'none'
            });
            t.get('.label_' + chosen_num + '_3').css({
                'display': 'none'
            });
            
            t.get('.label_' + chosen_num + '_' + chosen).css({
                'display': 'inline'
            });
            
            t.get('.label_' + chosen_num + '_0').value(chosen)
        });

    },
    init_remove: function() {

        t.get('.remove_item').on('click', function(e) {
            var chosen = e.currentTarget.value;
            var item_id = e.currentTarget.className.split('_')[2];
            b.admin.check_remove(item_id, 'pages');
        });

    }
}
