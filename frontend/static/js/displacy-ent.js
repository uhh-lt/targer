//- ----------------------------------
//- 💥 DISPLACY ENT
//- ----------------------------------

'use strict';

class displaCyENT {
    constructor (api, options) {
        this.api = api;
        this.container = document.querySelector(options.container || '#displacy');

        this.defaultText = options.defaultText || 'When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.';
        this.defaultModel = options.defaultModel || 'en';
        this.defaultEnts = options.defaultEnts || ['person', 'org', 'gpe', 'loc', 'product'];

        this.onStart = options.onStart || false;
        this.onSuccess = options.onSuccess || false;
        this.onError = options.onError || false;
        this.onRender = options.onRender || false;

    }

    parse(text = this.defaultText, model = this.defaultModel, ents = this.defaultEnts) {
        if(typeof this.onStart === 'function') this.onStart();

        let xhr = new XMLHttpRequest();
        xhr.open('POST', this.api, true);
        xhr.setRequestHeader('Content-type', 'text/plain');
        xhr.onreadystatechange = () => {
            if(xhr.readyState === 4 && xhr.status === 200) {
                if(typeof this.onSuccess === 'function') this.onSuccess();
                this.render(text, JSON.parse(xhr.responseText), ents);
            }

            else if(xhr.status !== 200) {
                if(typeof this.onError === 'function') this.onError(xhr.statusText);
            }
        }

        xhr.onerror = () => {
            xhr.abort();
            if(typeof this.onError === 'function') this.onError();
        }

        xhr.send(JSON.stringify({ text, model }));
    }

    render_old(text, spans, ents) {
        this.container.innerHTML = '';
        let offset = 0;

        spans.forEach(({ type, start, end }) => {
            const entity = text.slice(start, end);
            const fragments = text.slice(offset, start).split('\n');

            fragments.forEach((fragment, i) => {
                this.container.appendChild(document.createTextNode(fragment));
                if(fragments.length > 1 && i != fragments.length - 1) this.container.appendChild(document.createElement('br'));
            });

            if(ents.includes(type.toLowerCase())) {
                const mark = document.createElement('mark');
                mark.setAttribute('data-entity', type.toLowerCase());
                mark.appendChild(document.createTextNode(entity));
                this.container.appendChild(mark);
            }

            else {
                this.container.appendChild(document.createTextNode(entity));
            }

            offset = end;
        });

        this.container.appendChild(document.createTextNode(text.slice(offset, text.length)));

        console.log(`%c💥  HTML markup\n%c<div class="entities">${this.container.innerHTML}</div>`, 'font: bold 16px/2 arial, sans-serif', 'font: 13px/1.5 Consolas, "Andale Mono", Menlo, Monaco, Courier, monospace');

        if(typeof this.onRender === 'function') this.onRender();
    }

    render(text, spans, ents) {

        var text_copy = text
        var offset = 0        

        for (var i = 0; i < text.length; i++) {
            var start_tags = spans.filter( span => span.start === i );
            var end_tags = spans.filter( span => span.end === i );

            start_tags.forEach(function(tag){
                if(ents.includes(tag.type.toLowerCase())) {
                    var entity_string = "<mark data-entity='" + tag.type.toLowerCase() + "'>"
                    text_copy = text_copy.slice(0, offset+i) + entity_string + text_copy.slice(offset+i);
                    offset = offset + entity_string.length
                }
            })

            end_tags.forEach(function(tag){
                if(ents.includes(tag.type.toLowerCase())) {
                    var entity_string = "</mark>"
                    text_copy = text_copy.slice(0, offset+i) + entity_string + text_copy.slice(offset+i);
                    offset = offset + entity_string.length
                }
            })
            /*if (end_tag) {
                var entity_string = "</mark>"
                text_copy = text_copy.slice(0, offset+i) + entity_string + text_copy.slice(offset+i);
                offset = offset + entity_string.length
            }*/

        }

        //this.container.appendChild(document.createTextNode(text_copy));

        while (this.container.firstChild) {
            this.container.removeChild(this.container.firstChild);
        }

        var e = document.createElement('div');
        e.innerHTML = text_copy;
        this.container.appendChild(e)

        if(typeof this.onRender === 'function') this.onRender();
    }

    search_render(text, spans, ents) {

        var text_copy = text
        var offset = 0        

        for (var i = 0; i < text.length; i++) {
            var start_tags = spans.filter( span => span.start === i );
            var end_tags = spans.filter( span => span.end === i );

            start_tags.forEach(function(tag){
                if(ents.includes(tag.type.toLowerCase())) {
                    var entity_string = "<mark data-entity='" + tag.type.toLowerCase() + "'>"
                    text_copy = text_copy.slice(0, offset+i) + entity_string + text_copy.slice(offset+i);
                    offset = offset + entity_string.length
                }
            })

            end_tags.forEach(function(tag){
                if(ents.includes(tag.type.toLowerCase())) {
                    var entity_string = "</mark>"
                    text_copy = text_copy.slice(0, offset+i) + entity_string + text_copy.slice(offset+i);
                    offset = offset + entity_string.length
                }
            })
        }
        return text_copy
    }
}
