$(document).ready( function() {
    $('.first').click( function() {
      $('#chart-1').toggle( 'slow' );
      $('#chart-2').toggle( 'slow' );
      $('#chart-3').toggle( 'slow' );
      $('#chart-4').toggle( 'slow' );
      $('#chart-5').toggle( 'slow' );
      $('#chart-6').toggle( 'slow' );
      $('.second').removeClass('changeBc');
      $('.first').addClass('changeBc');
    });
    $('.second').click( function() {
        $('#chart-1').toggle( 'slow' );
        $('#chart-2').toggle( 'slow' );
        $('#chart-3').toggle( 'slow' );
        $('#chart-4').toggle( 'slow' );
        $('#chart-5').toggle( 'slow' );
        $('#chart-6').toggle( 'slow' );
        $('.first').removeClass('changeBc');
        $('.second').addClass('changeBc');
    });
  });