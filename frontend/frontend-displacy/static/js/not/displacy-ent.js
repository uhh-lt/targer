"use strict";
(function() {
    "use strict";
    var e = "https://api.explosion.ai";

    function t(e) {
        var t = arguments.length <= 1 || arguments[1] === undefined ? "" : arguments[1];
        var n = arguments.length <= 2 || arguments[2] === undefined ? [] : arguments[2];
        var r = arguments.length <= 3 || arguments[3] === undefined ? [] : arguments[3];
        var a = [];
        var i = 0;
        r.forEach(function(r) {
            var s = r.label;
            var o = r.type;
            var l = r.start;
            var u = r.end;
            var d = s || o;
            var h = t.slice(l, u);
            var c = t.slice(i, l).split("\n");
            c.forEach(function(t, n) {
                a.push(t);
                if (c.length > 1 && n != c.length - 1) {
                    a.push(e("br"))
                }
            });
            if (n.includes(d.toLowerCase())) {
                var p = {
                    "data-entity": d.toLowerCase()
                };
                a.push(e("mark", {
                    attrs: p
                }, h))
            } else {
                a.push(h)
            }
            i = u
        });
        a.push(t.slice(i, t.length));
        return e("div", a)
    }

    function n(e) {
        var t = window.location.search.substring(1);
        var n = t.split("&").map(function(e) {
            return e.split("=")
        });
        var r = true;
        var a = false;
        var i = undefined;
        try {
            for (var s = n[Symbol.iterator](), o; !(r = (o = s.next()).done); r = true) {
                var l = o.value;
                if (l[0] == e) {
                    return decodeURIComponent(l[1])
                }
            }
        } catch (e) {
            a = true;
            i = e
        } finally {
            try {
                if (!r && s.return) {
                    s.return()
                }
            } finally {
                if (a) {
                    throw i
                }
            }
        }
        return false
    }

    function r(e, t) {
        var n, r;
        var a = Object.keys(e).map(function(t) {
            return t + "=" + encodeURIComponent(e[t])
        });
        var i = [e, null, "?" + a.join("&")];
        if (t)(n = history).replaceState.apply(n, i);
        else(r = history).pushState.apply(r, i)
    }
    var a = new Vue({
        el: '[data-demo="displacy-ent"]',
        data: {
            api: e + "/displacy/",
            text: "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other. I know it better.",
            renderText: "",
            model: "en_core_web_sm",
            ents: ["person", "org", "gpe", "loc", "product", "norp", "date", "per", "misc"],
            models: [],
            spans: [],
            loading: false
        },
        components: {
            entities: {
                functional: true,
                props: ["text", "ents", "spans"],
                render: function e(n, r) {
                    var a = r.props;
                    var i = a.text;
                    var s = a.ents;
                    var o = a.spans;
                    return t(n, i, s, o)
                }
            }
        },
        beforeMount: function e() {
            window.addEventListener("popstate", this.init);
            this.init()
        },
        methods: {
            init: function e() {
                var t = this;
                this.loading = true;
                var r = n("text");
                var a = n("model");
                var i = n("ents");
                var s = i ? i.split(",") : null;
                fetch(this.api + "models").then(function(e) {
                    return e.json()
                }).then(function(e) {
                    t.loading = false;
                    t.models = e;
                    t.parse(r, a, s, true)
                })
            },
            parse: function e(t, n, a) {
                var i = this;
                var s = arguments.length <= 3 || arguments[3] === undefined ? false : arguments[3];
                this.loading = true;
                this.text = t || this.text;
                this.model = n || this.model;
                this.ents = a || this.ents;
                var o = {
                    Accept: "application/json",
                    "Content-Type": "application/json"
                };
                var l = "same-origin";
                var u = JSON.stringify({
                    text: this.text,
                    model: this.model
                });
                fetch(this.api + "ent", {
                    method: "POST",
                    headers: o,
                    credentials: l,
                    body: u
                }).then(function(e) {
                    return e.json()
                }).then(function(e) {
                    i.spans = e;
                    i.renderText = i.text;
                    i.loading = false;
                    if (!s) {
                        r({
                            text: i.text,
                            model: i.model,
                            ents: i.ents
                        })
                    }
                })
            },
            submit: function e(t) {
                this.parse(this.text, this.model, this.ents)
            },
            showLabel: function e(t) {
                var n = this.model == "en_core_web_sm";
                var r = !n && ["per", "org", "loc", "misc"].includes(t);
                return n && !["per", "misc"].includes(t) || r
            },
            selectAll: function e() {
                var t = Object.keys(this.$refs);
                this.ents = this.ents.length == t.length ? [] : t
            }
        }
    })
})();

/*
    $(function() {
      $('a#button_send').bind('click', function() {
	$.post( "/label_text", { username: document.getElementById("text_to_parse").value } )
	.done(function( data ) {
		console.log( "JSON Data: " + data );
		const displacy = new displaCyENT('https://api.explosion.ai/displacy/ent/', {
		    container: '#displacy'
		});
		text = document.getElementById("text_to_parse").value
 		spans = JSON.parse(data)
		ents = ['p-b', 'p-i', 'c-b', 'c-i'];
		displacy.render(text, spans, ents);
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
*/
