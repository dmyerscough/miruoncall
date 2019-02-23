var App = (function () {
  'use strict';

  App.dataTables = function( ){

    //We use this to apply style to certain elements
    $.extend( true, $.fn.dataTable.defaults, {
      dom:
        "<'row be-datatable-header'<'col-sm-6'l><'col-sm-6'f>>" +
        "<'row be-datatable-body'<'col-sm-12'tr>>" +
        "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>"
    } );

    var nameType = $.fn.dataTable.absoluteOrder( {
      value: 'resolved', position: 'bottom'
  } );

    var start = moment().subtract(7, 'days');
    var end = moment();
    var teamID = $("#teams").find(":selected").val();

    $("#table1").dataTable({
      ajax: {
        
        url: "/incidents/"+ teamID+ "/?since="+start.format('YYYY-MM-DD')+"&until="+end.format('YYYY-MM-DD'),
        dataSrc: "incidents",
        
      },
      columnDefs: [
        {
          targets: -1, data: "Icon",  defaultContent: '', orderable: false, className: 'select-checkbox',
          render : function (data, type, row) { 
            return "<span id='" 
                    + row.id 
                    + "' class='icon mdi mdi-comment-edit' data-toggle='modal' data-target='#annotateModal' title='Add Annotation'></span>" }
        },
        { targets: 2, type: nameType, orderable: false,
          "createdCell": function (td, cellData, rowData, row, col) {
            if ( $(td).text() == "triggered" ) {
              $(td).html('<span class="label label-danger">Triggered</span>')
            }
            if ( $(td).text() == "acknowledged" ) {
              $(td).html('<span class="label label-warning">Acknowledged</span>')
            }
            if ( $(td).text() == "resolved" ) {
              $(td).html('<span class="label label-success">Resolved</span>')
            }
          } 
        },

          {targets: 3, "createdCell": function (td, cellData, rowData, row, col) {
            var d = moment(cellData).format("dddd, MMMM Do YYYY, h:mm:ss a");
            $(td).html(d);
          } 
        }
    ],
    select: {
      style:    'os',
      selector: 'td:first-child'
  },
      columns: [
        { data: 'incident_id', orderable: false},
        { data: 'title', orderable: false},
        { data: 'status', orderable: false},
        { data: 'created_at', orderable: false},
        { data: {
                _:    "annotation.annotation",
                sort: "annotation.created_at"
              }, orderable: false}
      ],
      order: [[2, 'desc']],
      rowGroup: {dataSrc: 'status'},
      createdRow: function( row, data, index, cells ) {
        for ( var i in data.incidents ) {
          var label;
                if (incident.status=="resolved") {
                    label = '<span class="label label-success">'+incident.status.toUpperCase()+'</span>';
                    return label;
                }
                else if (incident.status=="acknowledged") {
                    label = '<span class="label label-primary">'+incident.status.toUpperCase()+'</span>';
                    return label;
                }
                else if (incident.status=="triggered") {
                    label = '<span class="label label-warning">'+incident.status.toUpperCase()+'</span>';
                    return label;
                }
                
        }
        var headers = $(".group-start");
        for (var h=0; h<headers.length; h++) {
          if (cells[0].innerText == "acknowledged") {$(headers[h]).html('<td class="warning" colspan="5"><span class="icon mdi mdi-alert-triangle text-warning"></span> Acknowledged</td>')};
          //if (cells[0].innerText == "triggered") {$(headers[h]).html('<td class="danger" colspan="5"><span class="icon mdi mdi-notifications text-danger"></span> Triggered</td>')};
          //if (cells[0].innerText == "resolved") {$(headers[h]).html('<td class="success" colspan="5"><span class="icon mdi mdi-info text-success"></span> Resolved</td>')};
         // if (cells[0].innerText == "acknowledged") {$("td", row).eq(0).html('<td class="warning" colspan="5"><span class="icon mdi mdi-alert-triangle text-warning"></span> Acknowledged</td>')};
        }
        
      }
    });

    $(".mdi-comment-edit").modal('show');

  };

  return App;
})(App || {});
