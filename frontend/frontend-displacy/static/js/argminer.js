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

	    $.post( "/arg-mining-ltcpu/label_text", { username: document.getElementById("text_to_parse").value , classifier: document.getElementById("model").value } )
	    .done(function( data ) {
		    console.log( "JSON Data: " + data );

            marks = JSON.parse(data)



            for (var i = 0; i < marks.length; i++) {
                if (i > 0 && i+1 < marks.length) {
                    // Start Label
                    if (marks[i].type.substring(0,1) == "P" && marks[i-1].type.substring(0,1) != marks[i].type.substring(0,1)) {
                        var mark = {'type': "PREMISE", 'start': marks[i].start}
                        marks_new.push(mark)
                    }
                    else if (marks[i].type.substring(0,1) == "C" && marks[i-1].type.substring(0,1) != marks[i].type.substring(0,1)) {
                        var mark = {'type': "CLAIM", 'start': marks[i].start}
                        marks_new.push(mark)
                    }
                    /*else if (marks[i].type.substring(0,1) == "O") {
                        var mark = marks[i]
                        marks_new.push(mark)
                    }*/
                    // End Label
                    if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                        if (marks[i].type.substring(0,1) != marks[i+1].type.substring(0,1)) {
                            var mark = marks_new.pop() 
                            mark.end = marks[i].end
                            marks_new.push(mark)
                        }
                    } /* else if (marks[i].type.substring(0,1) == "O") {
                        mark = marks[i]
                        marks_new.push(mark)
                    } */
                }
                else if (i == 0 && i+1 < marks.length ) {
                    // Start Label
                    if (marks[i].type.substring(0,1) == "P") {
                        var mark = {'type': "PREMISE", 'start': marks[i].start}
                        marks_new.push(mark)
                    }
                    else if (marks[i].type.substring(0,1) == "C") {
                        var mark = {'type': "CLAIM", 'start': marks[i].start}
                        marks_new.push(mark)
                    }
                    /* else if (marks[i].type.substring(0,1) == "O") {
                        var mark = marks[i]
                        marks_new.push(mark)
                    } */
                    // End Label
                    if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                        if (marks[i].type.substring(0,1) != marks[i+1].type.substring(0,1)) {
                            var mark = marks_new.pop() 
                            mark.end = marks[i].end
                            marks_new.push(mark)
                        }
                     } /* else if (marks[i].type.substring(0,1) == "O") {
                        var mark = marks_new.pop() 
                        mark.end = marks[i].end
                        marks_new.push(mark)
                    } */
                }
                else if (i == 0 && i+1 == marks.length ) {
                    // End Label
                    if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                        mark.end = marks[i]
                        marks_new.push(mark)
                    } /* else if (marks[i].type.substring(0,1) == "O") {
                        mark.end = marks[i]
                        marks_new.push(mark)
                    } */
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
