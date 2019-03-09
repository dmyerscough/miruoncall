var App = (function () {
  'use strict';
  
  App.charts = function( ){
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }
    // Date range picker

    $(".daterange").daterangepicker();

    $(".datetimerange").daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        locale: {
            format: 'MM/DD/YYYY h:mm A'
        }
    });

    var start = moment().subtract(7, 'days');
    var end = moment();

    function cb(start, end) {
        $('.reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $('.reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(7, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

    $("#previous").click(function() {
      $('.reportrange').daterangepicker({
        startDate: moment().subtract(14, 'days'),
        endDate: moment().subtract(7, 'days')
      });
    });

    // Get data for given date range using the teamID
    
    $('.reportrange').on('apply.daterangepicker', function(ev, picker) {
      var teamID = $("#teams").find(":selected").val();
      var dateSince = picker.startDate.format('YYYY-MM-DD');
      var dateUntil = picker.endDate.format('YYYY-MM-DD');
      $.ajax({
        method: 'GET',
        url: '../incidents/' + teamID,
        dataType: "json",
        data: {"since": dateSince, "until": dateUntil},
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
         },
        success: function(incidents) {         
          loadIncidentGraph(incidents.incident_count);
          loadTable(incidents, dateSince, dateUntil);
        },
        error: function(jqXHR, exception) {
          var errorMsg = jqXHR.responseJSON;
          if(errorMsg){
            console.log(errorMsg);
          } else {
            error = "Something has gone wrong.";
          }
        }
      });
     
    });

    // Load incident graph
    function loadIncidentGraph(incident){
      
      var series = Object.keys(incident).map(function(data){
        return [data,incident[data]];
      });
      var color1 = "#ff7f00";

    	var plot_statistics = $.plot($("#incidents-graph"), [
	    	{
	        data: series,
	        label: "Incidents"
	      }
      ], {
        series: {
          bars: {
          	align: 'center',
            show: true,
            barWidth: 0.35, 
            fill: true,
            fillColor: {
              colors: [{
                opacity: 1
              }, {
                opacity: 1
              }
              ]
            } 
          }
        },
        legend:{
          show: false
        },
        grid: {
          margin: {
            left: 23,
            right: 30,
            top: 20,
            bottom: 40
          },
        	labelMargin: 10,
          axisMargin: 200,
          hoverable: true,
          clickable: true,
          tickColor: "rgba(0,0,0,0.15)",
          borderWidth: 1,
          borderColor: "rgba(0,0,0,0.15)"
        },
        colors: [color1],
        xaxis: {
          mode: "categories",
          showTicks: false,
          gridLines: false
        }
      });
    }

    function loadInitialGraph(incident) {
      var incidentData = Object.keys(incident).map(function(data){
        return [data,incident[data]];
      });
      var color1 = "#ff7f00";

		$.plot("#incidents-graph", [ incidentData ], {
			series: {
				bars: {
					show: true,
					barWidth: 0.35,
          align: "center",
          fill: true,
            fillColor: {
              colors: [{
                opacity: 1
              }, {
                opacity: 1
              }
              ]
            } 
				}
      },
      colors: [color1],
			xaxis: {
				mode: "categories",
				showTicks: false,
				gridLines: false
      },
      grid: {
        borderWidth: 1,
        borderColor: "rgba(0,0,0,0.15)"
      }
		});
    }

    function loadIncidents() {
      var start = moment().subtract(7, 'days').format('MMMM D, YYYY');
      var end = moment().format('MMMM D, YYYY');
      
      var teamID = $("#teams").find(":selected").val();
      
      // Load initial graph
      $.ajax({
        method: 'GET',
        url: '../incidents/' + teamID,
        dataType: "json",
        data: {"since": start, "until": end},
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
        success: function(incidents) {
          
          loadInitialGraph(incidents.incident_count);
        },
        error: function(jqXHR, exception) {
          var errorMsg = jqXHR.responseJSON;
          if(errorMsg){
            console.log(errorMsg);
          } else {
            error = "Something has gone wrong.";
          }
        }
      });
    }
    loadIncidents();

      // Team picker
      $(".select2").select2({
        width: '100%',
        placeholder: "Select your team",
        ajax: {
          url: '../teams',
          dataType: 'json',
          processResults: function (data) {
            var data = $.map(data.teams, function (obj) {
              obj.text = obj.text || obj.name; 
              return obj;
            });
            return {
              results: data
            };
          }
        }
      });
  
      $('#teams').on('select2:select', function (e) {
        var data = e.params.data;
        var start = moment().subtract(7, 'days').format('YYYY-MM-DD');
        var end = moment().format('YYYY-MM-DD');
        var teamName = $("#teams").find(":selected").text();
        $("#team-name").html(teamName);
 
        loadTable(data, start, end);
        loadIncidents();
    });
    
      function loadTable(data, dateSince, dateUntil) {
        var teamID = $("#teams").find(":selected").val();
        
        var nameType = $.fn.dataTable.absoluteOrder({
          value: 'resolved', position: 'bottom'
        });
        $("#table1").dataTable({
          destroy: true,
          rowId: 'id',
          ajax: {
            url: '/incidents/' + teamID + '/?since=' + dateSince+"&until="+dateUntil,
            dataSrc: "incidents"
          },
          preDrawCallback: function(settings) {
            $("div.be-loading").addClass("be-loading-active");

          },
          stateLoaded: function (settings, data) {
            $("div.be-loading").removeClass("be-loading-active");
          },

          initComplete: function(settings, json) {
            console.log("initComplete app-charts");
            $("div.be-loading").removeClass("be-loading-active");
    
             // Enable Add Annotation button if a checkbox is selected
            $('input[type=checkbox]').change(function () {
             
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
              },  defaultContent: '', orderable: false,
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
            }
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
                  }, orderable: false}
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
            }
        }
        });

        $('#table1').on( 'draw.dt', function () {        
          $("div.be-loading").removeClass("be-loading-active");
        });
  
      }

      $('#annotateModal').on('show.bs.modal', function (e) {
      
        $("#addNewAnnotation").on("click", function (e) {
          var id = [];
          var teamID = $("#teams").find(":selected").val();
  
          var selected_rows = $("input:checkbox:checked");
          // Iterate over all selected checkboxes
          $.each(selected_rows, function(index, el){
            var tr = $(el).closest("tr");
            id.push($(tr).attr("id"));
          });
          // Remove the "select all" checkbox from array
          id.shift();
          console.log(id);
          $.ajax({
            type: "POST",
            url: "/incidents/"+teamID+"/",
            data: { 
                incident_ids: id.join(","),
                annotation: $("#annotateEditInput").val() ,
                actionable: $("#teamaction").val() == "on" ? true : false
            },
            beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
             },
            success: function(result) {
                loadTable();
            },
            error: function(result) {
                alert('error');
            }
        });
  
        })
        
      });
      
  };

  return App;
})(App || {});
