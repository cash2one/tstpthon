$(function () {
	
	
	/*--------------------------------------------------
	Plugin: Slider
	--------------------------------------------------*/
		
	/* Increment Slider */
	$( "#incrementSlider" ).slider({
		range: "min",
		value:150,
		min: 0,
		max: 500,
		step: 50,
		slide: function( event, ui ) {
			$( "#incrementAmount" ).text ( "$" + ui.value );
		}
	});
		
	$( "#incrementAmount" ).text ( "$" + $( "#incrementSlider" ).slider( "value" ) );
		
		
	
	/* Min Value Slider */
	$( "#rangeMinSlider" ).slider({
		range: "min",
		value: 100,
		min: 50,
		max: 700,
		slide: function( event, ui ) {
			$( "#rangeMinAmount" ).text ( "$" + ui.value );
		}
	});
	
	$( "#rangeMinAmount" ).text ( "$" + $( "#rangeMinSlider" ).slider( "value" ) );
		
		
	/* Default Slider */
	$( ".slider-demo" ).each (function () {
		$(this).slider({ value: randomFromInterval (10, 100), range: 'min' });
	})
	
	
	
	/* Vertical Slider */	
	$("#eq > span").each(function() {
		var value = parseInt($(this).text());
		$(this).empty().slider({
			value: value,
			range: "min",
			animate: true,
			orientation: "vertical"
		});
	});
    
/*
	*//* Horizontal Slider *//*
	$( "#rangeSlider" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount" ).text( "$" + $( "#rangeSlider" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider2" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount2" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount2" ).text( "$" + $( "#rangeSlider2" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider2" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider3" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount3" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount3" ).text( "$" + $( "#rangeSlider3" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider3" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider4" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount4" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount4" ).text( "$" + $( "#rangeSlider4" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider4" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider5" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount3" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount5" ).text( "$" + $( "#rangeSlider5" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider5" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider6" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount6" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount6" ).text( "$" + $( "#rangeSlider6" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider6" ).slider( "values", 1 )  +"M");

	*//* Horizontal Slider *//*
	$( "#rangeSlider7" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount7" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount7" ).text( "$" + $( "#rangeSlider7" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider7" ).slider( "values", 1 )  +"M");
	
	*//* Horizontal Slider *//*
	$( "#rangeSlider8" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 750, 2500 ],
		slide: function( event, ui ) {
			$( "#amount8" ).text ( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ] +"M" );
		}
	});
				
	$( "#amount8" ).text( "$" + $( "#rangeSlider8" ).slider( "values", 0 ) +
		"M - $" + $( "#rangeSlider8" ).slider( "values", 1 )  +"M");
	
	*/
	
});

function randomFromInterval(from,to)
{
    return Math.floor(Math.random()*(to-from+1)+from);
}