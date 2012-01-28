var hash_table = {
	init : function(){
		
		t.get('.remove_item').on('click', function(e){
		    var chosen = e.currentTarget.value;
            var item_id = e.currentTarget.className.split('_')[2];
		    b.check_remove('hash_table.remove_item',item_id);
        });
		
	},
	remove_item : function(check,item_id){
	    if (check) {
            t.ajax({
	            'url' : '/admin/hash_table/remove/'+item_id+'/',
	            'success' : function(data){
	                    if (data == 'ok') {
	                        t.get('.item_'+item_id).destroy();
	                    }
	            }
	        });
	    }
	    b.check_remove_hidden();
	}
}

t.get(d).ready(function(){
    
	hash_table.init();	
	
});