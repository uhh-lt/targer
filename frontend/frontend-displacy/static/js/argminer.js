            var marks_new = []

$(function() {

    $('#text_to_parse').val("Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.")

    $('.d-input__option').bind('click', function() {

        var chkArray = [];
	    $(".d-input__option__box").each(function() {
            if( $(this).prop('checked') ) {
    		    chkArray.push($(this).val());
            }
	    });
        console.log(chkArray)
        show_entity_labels(chkArray);
    });

    $('#button_send').bind('click', function() {

        marks_new = []

	    $(".d-input__option__box").each(function() {            
    		$(this).prop( "checked", true );            
	    });

	    $.post( "/label_text", { username: document.getElementById("text_to_parse").value , classifier: document.getElementById("model").value } )
	    .done(function( data ) {
		    console.log( "JSON Data: " + data );

            marks = JSON.parse(data)



            for (var i = 0; i < marks.length; i++) {
                if (marks[i].type == "P-B") {
                    var mark = {'type': "PREMISE", 'start': marks[i].start}
                    marks_new.push(mark)
                }
                else if (marks[i].type == "C-B") {
                    var mark = {'type': "CLAIM", 'start': marks[i].start}
                    marks_new.push(mark)
                }
                else if (marks[i].type == "P-I" || marks[i].type == "C-I") {

                    if (i+1 < marks.length) {
                        if (marks[i].type != marks[i+1].type) {

                            mark = marks_new.pop()
                            mark.end = marks[i].end
                            marks_new.push(mark)
                        }
                    } else {
                        mark = marks_new.pop()
                        mark.end = marks[i].end
                        marks_new.push(mark)
                    }
                }
                else {
                    marks_new.push(marks[i])
                }
            }

            console.log(marks_new );

	        const displacy = new displaCyENT('https://api.explosion.ai/displacy/ent/', {
	            container: '#displacy'
	            });
	        text = document.getElementById("text_to_parse").value
	        spans = JSON.parse(data)
	        ents = ['premise', 'claim'];
	        displacy.render(text, marks_new, ents);
	    })
	    .fail(function( jqxhr, textStatus, error ) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );
	    });
	
	    return false;
      });
    });
    const displacy = new displaCyENT('https://api.explosion.ai/displacy/ent/', {
    container: '#displacy'
});

function show_entity_labels(labels) {


    console.log(marks_new );

    const displacy = new displaCyENT('https://api.explosion.ai/displacy/ent/', {
        container: '#displacy'
        });
    text = document.getElementById("text_to_parse").value
    
    ents = labels;
    displacy.render(text, marks_new, ents);

	
	return false;
      
}
