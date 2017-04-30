String.prototype.toProperCase = function() {
    return this.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};;
Gabra.loadLexeme = function(id, div) {
    $.ajax({
        url: Gabra.base_url + "lexemes/view/" + id + ".json",
        dataType: "json",
        type: "GET",
        success: function(data) {
            var out = Gabra.UI.lexeme(data.lexeme);
            $(div).html(out);
            $(div).removeClass('loading');
        },
        error: function(err) {
            console.log(err.responseJSON);
            $(div).removeClass('loading');
        }
    });
}
Gabra.loadWordForms = function(id, match, div, limit) {
    $.ajax({
        url: Gabra.base_url + "lexemes/wordforms/" + id + "/" + match + ".json",
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
                        out += '<a href="' + Gabra.base_url + 'lexemes/view/' + id + '">' + Gabra.i18n.x_more.replace("%s", remaining) + '...</a>';
                    break;
                }
            }
            $(div).html(out);
            $(div).removeClass('loading');
        },
        error: function(err) {
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
    wordForm: function(wordform, match) {
        var out = '';
        out += '<div class="word_form">';
        var sf_class = 'surface_form';
        var sf_title = '';
        out += '<span class="' + sf_class + '" ' + sf_title + '>' + Gabra.UI.highlight(wordform.surface_form, match) + '</span> ';
        out += '<span class="features">';
        out += Gabra.UI.maybeField(wordform, 'number', "%s.");
        out += Gabra.UI.maybeField(wordform, 'gender', "%s.");
        out += Gabra.UI.maybeField(wordform, 'phonetic', "/%s/");
        out += Gabra.UI.maybeField(wordform, 'pattern');
        out += Gabra.UI.maybeField(wordform, 'aspect');
        out += Gabra.UI.maybeAgr(wordform, 'subject');
        out += Gabra.UI.maybeAgr(wordform, 'dir_obj', "&middot; DO: %s");
        out += Gabra.UI.maybeAgr(wordform, 'ind_obj', "&middot; IO: %s");
        out += Gabra.UI.maybeField(wordform, 'polarity', "&middot; %s");
        out += '</span>';
        out += '</div>';
        return out;
    },
    highlight: function(haystack, needle) {
        var re = new RegExp("(" + needle + ")", "i");
        return (needle ? haystack.replace(re, "<mark>$1</mark>") : haystack);
    },
    maybeField: function(item, field, formatstring) {
        formatstring = typeof formatstring !== 'undefined' ? formatstring : "%s";
        var out = '';
        if (item[field]) {
            out += formatstring.replace("%s", item[field]) + " ";
        }
        return out;
    },
    maybeAgr: function(item, field, formatstring) {
        formatstring = typeof formatstring !== 'undefined' ? formatstring : "%s";
        var out = '';
        if (item[field]) {
            var agr = item[field];
            if (agr.person)
                out += agr.person.toUpperCase() + ' ';
            if (agr.gender)
                out += agr.gender + '. ';
            if (agr.number)
                out += agr.number + '. ';
        }
        if (out)
            return formatstring.replace("%s", out);
        else
            return '';
    },
};
$(document).ready(function() {
    $('select.filter').each(function() {
        var obj = $(this);
        var table = obj.parents('table');
        var opts = new Array();
        var index = obj.parent().index();
        table.find('tbody tr').find('td:eq(' + index + ')').each(function() {
            var value = $(this).text().trim();
            if (opts.indexOf(value)==-1) {
                opts.push(value);
            }
        });
        for (o in opts) {
            obj.append('<option>' + opts[o] + '</option>');
        }
        obj.change(function() {
            obj.parent().addClass('loading right');
            setTimeout(function() {
                table.find('tbody tr').show();
                $('select.filter').each(function() {
                    var _obj = $(this);
                    var _index = _obj.parent().index();
                    var _match = _obj.val();
                    table.find('tbody tr:visible').find('td:eq(' + _index + ')').each(function() {
                        var td = $(this);
                        if (td.text().trim() != _match)
                            td.parent().hide();
                    });
                });
                obj.parent().removeClass('loading right');
            }, 100);
        });
    });
    $('select.filter').first().trigger('change');
});;
$(document).ready(function() {
    var handler = function() {
        var anchor = $(this);
        var container = anchor.parent();
        var msg = container.find('.message');
        bootbox.prompt(Gabra.i18n.feedback_dialog_title, function(result) {
            if (!result) {
                return;
            }
            anchor.hide();
            msg.empty();
            container.addClass('loading right');
            $.ajax({
                url: anchor.attr('href'),
                data: {
                    message: result
                },
                dataType: "json",
                type: "GET",
                success: function(data) {
                    container.removeClass('loading right');
                    if (container.hasClass('lexeme')) {
                        msg.text(data.message);
                    } else {
                        container.hide();
                    }
                },
                error: function(err) {
                    container.removeClass('loading right');
                    msg.text(err.responseJSON.name);
                    anchor.show();
                }
            });
        });
        return false;
    };
    $('.lexeme.feedback a').click(handler);
});;
(function($, undefined) {
    $.fn.getCursorPosition = function() {
        var el = $(this).get(0);
        var pos = 0;
        if ('selectionStart'in el) {
            pos = el.selectionStart;
        } else if ('selection'in document) {
            el.focus();
            var Sel = document.selection.createRange();
            var SelLength = document.selection.createRange().text.length;
            Sel.moveStart('character', - el.value.length);
            pos = Sel.text.length - SelLength;
        }
        return pos;
    };
    $.fn.setCursorPosition = function(pos) {
        this.each(function(index, elem) {
            if (elem.setSelectionRange) {
                elem.setSelectionRange(pos, pos);
            } else if (elem.createTextRange) {
                var range = elem.createTextRange();
                range.collapse(true);
                range.moveEnd('character', pos);
                range.moveStart('character', pos);
                range.select();
            }
        });
        return this;
    };
    $.fn.insertAtCursor = function(s) {
        var el = $(this);
        var pos = $(el).getCursorPosition();
        var val = el.val();
        val = val.substring(0, pos) + s + val.substring(pos);
        el.val(val);
        el.setCursorPosition(pos + s.length);
        return this;
    };
})(jQuery);;
$(document).ready(function() {
    $('#add-field input').keydown(function(e) {
        if (e.keyCode == 13) {
            $('#add-field a').trigger('click');
            return false;
        }
    });
    $('#add-field a').click(function() {
        var name = $('#add-field input').val();
        if (!name)
            return false;
        var nameLC = name.toLowerCase();
        var nameSC = name.toProperCase();
        $('#add-field').before($('<div>').addClass("form-group").append('<label for="Lexeme' + nameSC + '">' + nameSC + '</label>').append('<input name="data[Lexeme][' + nameLC + ']" type="text" id="Lexeme' + nameSC + '" class="form-control"/>'));
        $('#add-field input').val(null);
        return false;
    });
});

