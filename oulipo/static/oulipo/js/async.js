// Load stuff using AJAX

Gabra.loadLexeme = function(id, div) {
    $.ajax({
        url: Gabra.base_url+"lexemes/view/"+id+".json",
        dataType: "json",
        type: "GET",
        success: function(data) {
            var out = Gabra.UI.lexeme(data.lexeme);
            $(div).html(out);
            $(div).removeClass('loading');
        },
        error: function(err){
            console.log(err.responseJSON);
            $(div).removeClass('loading');
        }
    });
}

Gabra.loadWordForms = function(id, match, div, limit) {
    $.ajax({
        url: Gabra.base_url+"lexemes/wordforms/"+id+"/"+match+".json",
        dataType: "json",
        type: "GET",
        success: function(data) {
            var match2 = decodeURIComponent(match);
            var out = '';
            var seen = 0;
            for (i in data.wordforms) {
                var wf = data.wordforms[i]['Wordform'];
                out += Gabra.UI.wordForm(wf, match2);
                seen += 1;
                if (seen >= limit) {
                    var remaining = data.wordforms.length - seen;
                    if (remaining > 0)
                        out += '<a href="'+Gabra.base_url+'lexemes/view/'+id+'">'+Gabra.i18n.x_more.replace("%s", remaining)+'...</a>';
                    break;
                }
            }
            $(div).html(out);
            $(div).removeClass('loading');
        },
        error: function(err){
            console.log(err.responseJSON);
            $(div).removeClass('loading');
        }
    });
}

Gabra.UI = {

    lexeme: function(lexeme) {
        var out = '';
        out += '<div class="lexeme">';
        out += Gabra.UI.maybeField(lexeme.Lexeme, 'pos', "%s");
        out += Gabra.UI.maybeField(lexeme.Lexeme, 'form', " Form %s");
        if (lexeme.Lexeme['root']) {
            out += '<span class="root">';
            out += lexeme.Lexeme['root'].radicals;
            if (lexeme.Lexeme['root'].variant)
                out += ' <sup>' + lexeme.Lexeme['root'].variant + '</sup> ';
            out += "</span> ";
        }
        if (lexeme.Lexeme['gloss']) {
            out += '<div class="gloss">';
            out += lexeme.Lexeme['gloss'].replace(/\n/g, ", ");
            out += "</div>";
        }
        out += Gabra.UI.maybeField(lexeme.Lexeme, 'source', "(%s)");

        if (lexeme.Wordforms) {
	    out += lexeme.Wordforms.length + " wordforms";
        }

        out += '</div>';
        return out;
    },

    wordForm : function(wordform, match) {
        var out = '';
        out += '<div class="word_form">';
        var sf_class = 'surface_form';// + wordform.feedback;
        var sf_title = '';//(wordform.feedback=='incorrect') ? 'title="'+Gabra.i18n.marked_as_incorrect+'"' : '';
        out += '<span class="'+sf_class+'" '+sf_title+'>'+ Gabra.UI.highlight(wordform.surface_form, match)+'</span> ';
        out += '<span class="features">';

        // Noun
        out += Gabra.UI.maybeField(wordform, 'number', "%s.");
        out += Gabra.UI.maybeField(wordform, 'gender', "%s.");
        out += Gabra.UI.maybeField(wordform, 'phonetic', "/%s/");
        out += Gabra.UI.maybeField(wordform, 'pattern');

        // Verb
        out += Gabra.UI.maybeField(wordform, 'aspect');
        out += Gabra.UI.maybeAgr(wordform, 'subject');
        out += Gabra.UI.maybeAgr(wordform, 'dir_obj', "&middot; DO: %s");
        out += Gabra.UI.maybeAgr(wordform, 'ind_obj', "&middot; IO: %s");
        out += Gabra.UI.maybeField(wordform, 'polarity', "&middot; %s");

        out += '</span>';
        out += '</div>';
        return out;
    },

    highlight : function(haystack, needle) {
        var re = new RegExp("("+needle+")","i");
        return (needle ? haystack.replace(re,"<mark>$1</mark>") : haystack);
    },

    maybeField : function(item, field, formatstring) {
        formatstring = typeof formatstring !== 'undefined' ? formatstring : "%s";
        var out = '';
        if (item[field]) {
            out += formatstring.replace("%s", item[field]) + " ";
        }
        return out;
    },

    maybeAgr : function(item, field, formatstring) {
        formatstring = typeof formatstring !== 'undefined' ? formatstring : "%s";
        var out = '';
        if (item[field]) {
            var agr = item[field];
            if (agr.person) out += agr.person.toUpperCase() + ' ';
            if (agr.gender) out += agr.gender + '. ';
            if (agr.number) out += agr.number + '. ';
        }
        if (out)
            return formatstring.replace("%s", out);
        else
            return '';
    },
}
