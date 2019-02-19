var App = (function () {
  'use strict';
  
  App.charts = function( ){
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }

    function randValue() {
      return (Math.floor(Math.random() * (1 + 50 - 20))) + 10;
    }

    //Counter
    function counter(){

      $('[data-toggle="counter"]').each(function(i, e){
        var _el       = $(this);
        var prefix    = '';
        var suffix    = '';
        var start     = 0;
        var end       = 0;
        var decimals  = 0;
        var duration  = 2.5;

        if( _el.data('prefix') ){ prefix = _el.data('prefix'); }

        if( _el.data('suffix') ){ suffix = _el.data('suffix'); }

        if( _el.data('start') ){ start = _el.data('start'); }

        if( _el.data('end') ){ end = _el.data('end'); }

        if( _el.data('decimals') ){ decimals = _el.data('decimals'); }

        if( _el.data('duration') ){ duration = _el.data('duration'); }

      });
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
          console.log(incidents);
          
          loadIncidentGraph(incidents.incident_count);
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
      var color1 = App.color.success;
      var color2 = tinycolor( App.color.success ).lighten( 22 ).toString();

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
            lineWidth: 1, 
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
            botttom: 40
          },
        	labelMargin: 10,
          axisMargin: 200,
          hoverable: true,
          clickable: true,
          tickColor: "rgba(0,0,0,0.15)",
          borderWidth: 1,
          borderColor: "rgba(0,0,0,0.15)"
        },
        colors: [color1, color2],
        xaxis: {
          mode: "categories",
          showTicks: false,
          gridLines: false
        }
      });
    }

    function loadInitialGraph() {
      var data = [ ["January", 10], ["February", 8], ["March", 4], ["April", 13], ["May", 17], ["June", 9] ];

		$.plot("#incidents-graph", [ data ], {
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
      colors: [App.color.success],
			xaxis: {
				mode: "categories",
				showTicks: false,
				gridLines: false
      },
      grid: {borderWidth: 1}
		});
    }
	    loadInitialGraph();
  };

  return App;
})(App || {});
