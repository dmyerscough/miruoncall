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
      colors: [App.color.warning],
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
          ajax: {
            url: '/incidents/' + teamID + '/?since=' + dateSince+"&until="+dateUntil,
            dataSrc: "incidents"
          },
          columnDefs: [
            {
              targets: -1, data: null,  defaultContent: '', orderable: false, className: 'select-checkbox'
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
            
          }
        });
  
        var headers = $(".group-start");
            
            for (var h=0; h<headers.length; h++) {
              console.log(headers[0].innerText);
              if (headers[0].innerText == "acknowledged") {$(headers[h]).html('<td class="warning" colspan="5"><span class="icon mdi mdi-alert-triangle text-warning"></span> Acknowledged</td>')};
            //if (cells[0].innerText == "triggered") {$(headers[h]).html('<td class="danger" colspan="5"><span class="icon mdi mdi-notifications text-danger"></span> Triggered</td>')};
            //if (cells[0].innerText == "resolved") {$(headers[h]).html('<td class="success" colspan="5"><span class="icon mdi mdi-info text-success"></span> Resolved</td>')};
           // if (cells[0].innerText == "acknowledged") {$("td", row).eq(0).html('<td class="warning" colspan="5"><span class="icon mdi mdi-alert-triangle text-warning"></span> Acknowledged</td>')};
          }
      }
      
  };

  return App;
})(App || {});
