var marks_new = []

var items = Array("Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.",
"We should abandon Youtube. Toolassisted speedruns uploaded to video sites like Nico Nico Douga , YouTube or TASVideos may be described as a new world record by TASsan , who is said to have the superhuman memory and reflexes",
"The internet brings more harm than good. Source the Internet except as noted for items from the 1999 censusREF.",
"The internet brings more harm than good. Some of Sarcones artworks such as The Other Face of ParisREF or Flashing StarREF have gone viral on the Internet.",
"Science is a major threat. In the final section, that dealing with moral philosophy or ethics in seven lessons, Debono discusses religion, happiness as humans highest end, the duties of scientists ,on right behaviour especially moderation, duties in general, genuine ethical mistakes, and the principal reason for acquiring knowledge and science.",
"Newspapers are outdated. Bahrains Information Affairs Authority reported that the number of newspapers in 1999 was four which were published in Arabic and English languages.",
"We should not subsidize single parents. In the United States , 80.6 of single parents are mothers.",
"Suicide should be a criminal offence. It is suspected that Francis committed suicide having been faced with being murdered over his large debt to Johnny Boy.",
"Religion does more harm than good. Morriss early academic work was in the field of modern British religious history, looking in particular at the impact of urbanization and industrialization on religious change.",
"Child labor should be legalized .Officials investigated several cases of child labor in all instances, offenders were issued compliance orders in accordance with the 2007 Labor Act, but were not arrested or otherwise penalized.",
"We should disband the United Nations. The United Nations condemned the killings in the strongest possible terms, and the French Council of the Muslim Faith also condemned the attacks",
"Academic freedom is not absolute. All major Canadian universities are now publicly funded but maintain institutional autonomy, with the ability to decide on admission, tuition and governance.",
"Coaching brings more harm than good. He is coaching junior tennis players while simultaneously going to school and working to receive his massage therapy license.",
"The alternative vote is advantageous. The President is directly elected by secret ballot under the system of the Alternative Vote.",
"We should protect endangered species. Centaurea pinnata is an endangered species of plant present in this mountain range.",
"We should ban Greyhound racing. The stadium opened to greyhound racing in March 1948 and just five months later a new totalisator was brought into the track.",
"We should adopt vegetarianism. There are several categories for which the food entry can be classified Appetizers, Soups and Salads, Seafood, Entrees, Vegetarian Entree, Desserts, and the coined Best Damned Dish.");
var item = items[Math.floor(Math.random()*items.length)];

$(function() {

    $('#text_to_parse').val(item)

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

	    /*$(".d-input__option__box").each(function() {            
    		$(this).prop( "checked", true );            
	    });*/

	    $.post( "/label_text", { username: document.getElementById("text_to_parse").value , classifier: document.getElementById("model").value } )
	    .done(function( data ) {
		    console.log( "JSON Data: " + data )
            marks = JSON.parse(data)
            marks_new = marks

            console.log(marks_new);

	        const displacy = new displaCyENT('https://api.explosion.ai/displacy/ent/', {
	            container: '#displacy'
	            });
	        text = document.getElementById("text_to_parse").value
	        //ents = ['premise', 'claim', 'person', 'org', 'gpe', 'loc', 'product', 'misc']
	        ents = []
            $(".d-input__option__box").each(function() {
                if( $(this).prop('checked') ) {
		            ents.push($(this).val());
                }
            });

	        //displacy.render(text, marks_new, ents);
	        
	        //marks_new = [{"type": "CLAIM", "start": 3, "end": 36}, {"type": "PREMISE", "start": 42, "end": 111}, {"type": "ORG", "start": 42, "end": 56}, {"type": "PREMISE", "start": 113, "end": 115}, {"type": "ORG", "start": 22, "end": 36}, {"type": "ORG", "start": 121, "end": 155}];
	        //text = "We should disband the United Nations. The United Nations condemned the killings in the strongest possible terms, and the French Council of the Muslim Faith also condemned the attacks";
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

$("#more_labels").click(function(){
    if ($("#more_labels_box").is(":visible")){
        $("#more_labels").text("+ more labels");
    } else {
        $("#more_labels").text("- more labels");
    }
    $("#more_labels_box").toggle();
});


function do_label_arg(marks) {
    marks_new = []
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
            // End Label
            if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                if (marks[i].type.substring(0,1) != marks[i+1].type.substring(0,1)) {
                    var mark = marks_new.pop() 
                    mark.end = marks[i].end
                    marks_new.push(mark)
                }
            }
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
            // End Label
            if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                if (marks[i].type.substring(0,1) != marks[i+1].type.substring(0,1)) {
                    var mark = marks_new.pop() 
                    mark.end = marks[i].end
                    marks_new.push(mark)
                }
             }
        }
        else if (i == 0 && i+1 == marks.length ) {
            // End Label
            if ((marks[i].type.substring(0,1) == "P" || marks[i].type.substring(0,1) == "C")) {
                mark.end = marks[i]
                marks_new.push(mark)
            }
        }
    }
    return marks_new
}


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
