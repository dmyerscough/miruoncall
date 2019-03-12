var App = (function () {
  'use strict';

  App.dataTables = function( ){
    const csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

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
    var teamName = $("#teams").find(":selected").text();
    $("#team-name").html(teamName);

    var table = $("#table1").dataTable({
      rowId: 'id',
      ajax: {
        
        url: "/incidents/"+ teamID+ "/?since="+start.format('YYYY-MM-DD')+"&until="+end.format('YYYY-MM-DD'),
        dataSrc: "incidents",      
      },
      
      initComplete: function(settings, json) {
        console.log("initComplete app-tables-datatables");
        $("div.be-loading").removeClass("be-loading-active");
        
         // Enable Add Annotation button if a checkbox is selected
        $("#table1").on('click', 'input[type="checkbox"]', function () {
         
        if ($("input:checkbox:checked").length > 0) {
          $("#addAnnotation").prop('disabled', false);
          console.log($("input:checkbox:checked").length);
        }
        else {
          $("#addAnnotation").prop('disabled', true);
        }
      });
      },  
      columnDefs: [
        {
          targets: -1, data: {
            _:    "annotation.annotation",
            sort: "annotation.created_at"
          },  defaultContent: '',
          "createdCell": function (td, cellData, rowData, row, col) {
            if ( $(td).text() ) {
              $(td).html('<i class="icon icon-left mdi mdi-comment-text" data-toggle="modal" data-target="#annotateEditModal"></i>')
            }
          }
          },
        { targets: 3, type: nameType, orderable: false,
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

          {targets: 4, "createdCell": function (td, cellData, rowData, row, col) {
            var d = moment(cellData).format("dddd, MMMM Do YYYY, h:mm:ss a");
            $(td).html(d);
          } 
        },
    ],
    select: {
      style:    'multi'
  },
      columns: [
        {
          'data': 'id',
          'checkboxes': {
             'selectRow': true
          }
       },
        { data: 'incident_id', orderable: false},
        { data: 'title', orderable: false},
        { data: 'status', orderable: false},
        { data: 'created_at', orderable: false},
        { data: {
                _:    "annotation.annotation",
                sort: "annotation.created_at"
              }}
      ],
      order: [[4, 'desc'], [ 3, 'desc' ]],
      rowGroup: {
        dataSrc: 'status',
        startRender: function(rows, group) {
          var label;
                if (group=="resolved") {
                    label = '<span class="label label-success">'+group.toUpperCase()+'</span>';
                    return label;
                }
                else if (group=="acknowledged") {
                    label = '<span class="label label-warning">'+group.toUpperCase()+'</span>';
                    return label;
                }
                else if (group=="triggered") {
                    label = '<span class="label label-danger">'+group.toUpperCase()+'</span>';
                    return label;
                }
                $(".mdi-info").closest("td").addClass("success");


      }
    }
    });
 
    // Trigger checkbox select when row is selected
    $('#table1 tbody').on( 'click', 'tr', function () {
      var checkbox = $(this).find("input");
      //checkbox.trigger('click');
      checkbox.prop('checked', true);
      console.log($("input:checkbox:checked").length);
  } );
   
    $("#addAnnotation").on("click", function(e) {
      var selected_rows = $("input:checkbox:checked");
      if (selected_rows.length == 0) {
        $("#addAnnotation").prop('disabled', true);
        $("#annotateModal").modal('hide');
        $("#annotateInfo").modal();
      }

      if (selected_rows.length<=2 &&  selected_rows>=1) {
        $("#addAnnotation").prop('disabled', false);
        var tr = $("input:checkbox:checked")[1].closest("tr");
        var incident_id = $(tr).attr("id");

        $.ajax({
          type: "GET",
          url: "/incident/"+teamID+"/"+incident_id,
          
          success: function(result) {
              // Set annotation values in popup modal
              modal.find("input#annotateEditInput").val(result.annotation.annotation);
              
          },
          error: function(result) {
              console.log(result);
          }
        });
      }
    });
      
      
      $("#addNewAnnotation").on("click", function (e) {
        var id;
        var selected_rows = $("input:checkbox:checked");
        // Iterate over all selected checkboxes
        $.each(selected_rows, function(index, el){
          var tr = $(el).closest("tr");
          id = $(tr).attr("id");
        });
        // Remove the "select all" checkbox from array
        //id.shift();

        $.ajax({
          type: "POST",
          url: "/incidents/"+teamID+"/",
          data: { 
              incident_ids: id,
              annotation: $("#annotateEditInput").val() ,
              actionable: $("#teamaction").val() == "on" ? true : false
          },
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
           },
          success: function(result) {
            table.DataTable({
              ajax: {
        
                url: "/incidents/"+ teamID+ "/?since="+start.format('YYYY-MM-DD')+"&until="+end.format('YYYY-MM-DD'),      
              }
            }).ajax.reload();
            //http://192.168.1.144:8080/incidents/7f9021ed-cc15-4323-865b-6886f8e68263/?since=undefined&until=undefined&_=1552284420904
          },
          error: function(result) {
              alert('error');
          }
      });

     
      
    });

    $('#annotateEditModal').on('show.bs.modal', function (e) {
      var icon = $(e.relatedTarget);
      var tr = $(icon).closest("tr");
      var incident_id = $(tr).attr("id");
      var modal = $(this);
      $.ajax({
        type: "GET",
        url: "/incident/"+teamID+"/"+incident_id,
        
        success: function(result) {
            // Set annotation values in popup modal
            modal.find("input#annotateEditInput").val(result.annotation.annotation);
            
        },
        error: function(result) {
            alert('error');
        }
    });

    });

  };

  return App;
})(App || {});
