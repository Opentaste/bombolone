var d = document;

(function(){
	var admin = {
		
	}
	
	t.get(d).ready(function(){
	    
	    // to do
		
	})
		
})();


bombolone = {
    check_remove : function(callback, item_id){
        var div = t.make('div');
        div.attr('class', 'check_remove');
        var html = '<span>Are you sure you want to remove this item?</span>';
            html += '<span style="width:49%;display:inline-block;cursor:pointer;" ';
            html += 'onclick="'+callback+'(true,\''+item_id+'\')">Yes</span>';
            html += '<span style="width:49%;text-align:right;display:inline-block;cursor:pointer;" ';
            html += 'onclick="'+callback+'(false,\''+item_id+'\')">No</span>';
        div.html(html);
        t.get('.content').after(div);
    },
    check_remove_hidden : function(){
        t.get('.check_remove').destroy();
    },
}

b = bombolone;