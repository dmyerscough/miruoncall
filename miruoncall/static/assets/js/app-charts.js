var App = (function () {
  'use strict';
  
  App.charts = function( ){

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

        var count = new CountUp(_el.get(0), start, end, decimals, duration, { 
          suffix: suffix,
          prefix: prefix,
        });

        count.start();
      });
    }

    //Bar Chart 2
    function widget_barchart2(){

      var color1 = App.color.success;
      var color2 = tinycolor( App.color.success ).lighten( 22 ).toString();

    	var plot_statistics = $.plot($("#bar-chart2"), [
	    	{
	        data: [
	        	["Jan 12", 7], ["Jan 13", 13], [2, 17], [3, 20], [4, 22], [5,15], [6,18]
	        ],
	        label: "Page Views"
	      }
      ], {
        series: {
          bars: {
          	order: 2,
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
          },
          shadowSize: 2
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
          ticks: 11,
          tickDecimals: 0
        },
        yaxis: {
          ticks: 4,
          tickDecimals: 0
        }
      });
    }

    //row 1
      //widget_linechart2();
	    widget_barchart2();
  };

  return App;
})(App || {});
