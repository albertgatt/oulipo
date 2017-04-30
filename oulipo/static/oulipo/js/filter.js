// Logic for drop-down filters on large tables.. all JS baby!
$(document).ready(function(){
    $('select.filter').each(function(){
        var obj = $(this);
        var table = obj.parents('table');

        // Traverse columns and populate select with options
        var opts = new Array(); //Array('');
        var index = obj.parent().index();
        table.find('tbody tr').find('td:eq('+index+')').each(function(){
            var value = $(this).text().trim();
            if (opts.indexOf(value) == -1) {
                opts.push(value);
            }
        });
        for (o in opts) {
            obj.append('<option>'+opts[o]+'</option>');
        }

        // Filtering action - always apply all filters
        obj.change(function(){
            obj.parent().addClass('loading right');
            setTimeout(function() {

              table.find('tbody tr').show();
              $('select.filter').each(function(){
                  var _obj = $(this);
                  var _index = _obj.parent().index();
                  var _match = _obj.val();
                  // if (_match!='') {
                      // table.find('tbody tr').find('td:eq('+_index+'):not(:contains("'+_match+'"))').parent().hide();
                      // table.find('tbody tr').find('td:eq('+_index+'):not(.'+_match+')').parent().hide();
                      table.find('tbody tr:visible').find('td:eq('+_index+')').each(function(){
                          var td = $(this);
                          if (td.text().trim()!=_match)
                              td.parent().hide();
                      });
                  // }
              });
              // console.log("Showing "+table.find('tbody tr:visible').length+" rows");
              obj.parent().removeClass('loading right');

            }, 100); // to ensure spinner is visible
        });
    });
    $('select.filter').first().trigger('change');
});
