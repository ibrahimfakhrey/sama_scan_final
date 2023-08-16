var demo = function() {
  $(function() {
    closeNav();
    openNav();
    toggleCalendar();
    toggleChart();
    togglePanels();
    actionsAndAlerts();
    goFullScreen();
    showLog();
    toggleRightNav();
    stickyConfig();
   
  });
 
  var stickyConfig = function(){
     $("#top-buttons").sticky({
       topSpacing:25,
       zIndex: 'auto'
     });
  };
  
  var toggleRightNav = function(){
    $('#rightNavButton').on('click', function(){
      $('#rightMenu').css({'display': 'block'});
      $('#rightNavButton').hide();
    });
    $('#closeRightButton').on('click', function(){
      $('#rightMenu').css({'display': 'none'});
      $('#rightNavButton').show();
    });
    
  };
  
  var actionsAndAlerts = function() {
    $('#alerts').hide();
    $('#actionsLink').on('click', function() {
      $(this).addClass('active');
      $('#alertsLink').removeClass('active');
      $('#alerts').hide();
      $('#actions').show();
    });
    $('#alertsLink').on('click', function() {
      $(this).addClass('active');
      $('#actionsLink').removeClass('active');
      $('#actions').hide();
      $('#alerts').show();
    });

  };
  var showLog = function() {
    $('#showLog').prop('checked', true);
    $('#showLog').on('click', function() {
      if ($('#showLog').is(':checked')) {
        $('#actionsCard').show();
        $('.card-one').removeClass('col-lg-6').addClass('col-lg-5');
        $('.card-two').removeClass('col-lg-6').addClass('col-lg-4');
      } else {
        $('#actionsCard').hide();
        $('.card-one').removeClass('col-lg-5').addClass('col-lg-6');
        $('.card-two').removeClass('col-lg-4').addClass('col-lg-6');
      }
    });
  };
  var closeNav = function() {
    $('#closeNav').on('click', function() {
      $('#mySidenav').css({
        'width': '0'
      });
      $('#main').css({
        'margin-left': '0'
      });
      $('#openNav').show();

    })
  };
  var openNav = function() {
    $('#openNav').on('click', function() {
      $('#mySidenav').css({
        'width': '250px'
      });
      $('#main').css({
        'margin-left': '250px'
      });
      $('#openNav').hide();
    })
  };
  var togglePanels = function() {
    var collapsed = $('.card-block').parent('.collapse')

    $('.openCard').on('click', function() {
      if ($(this).children('i').hasClass('fa fa-plus')) {
        $(this).children('i').removeClass('fa fa-plus');
        $(this).children('i').addClass('fa fa-minus');
      } else {
        $(this).children('i').removeClass('fa fa-minus');
        $(this).children('i').addClass('fa fa-plus');
      }
    });
    $('.closeall').click(function() {
      $('.card-collapse.in')
        .collapse('hide');
      $('.closeall').prop("disabled", true);
      $('.openall').prop("disabled", false);
      $('.openCard').children('i').removeClass('fa fa-minus');
      $('.openCard').children('i').addClass('fa fa-plus');
    });

    $('.openall').click(function() {
      $('.card-collapse:not(".in")')
        .collapse('show');
      $('.openall').prop("disabled", true);
      $('.closeall').prop("disabled", false);
      $('.openCard').children('i').removeClass('fa fa-plus');
      $('.openCard').children('i').addClass('fa fa-minus');
    });
  };
  var toggleCalendar = function() {
    // Select a specified element
    $('.calendarOne').fullCalendar({
      // put your options and callbacks here
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month'
      },
      height: 600,
      defaultDate: '2016-09-12',
      defaultView: 'month',
      editable: true,
      events: [{
        id: 1,
        title: 'Repeating Event',
        start: '2016-09-09',
        color: 'yellow'
      }, {
        id: 2,
        title: 'DCM Event',
        start: '2016-09-16'
      }, {
        id: 3,
        title: 'Another Event',
        start: '2016-09-05',
        color: 'green'
      }]
    });
   
  };
  var toggleChart = function() {
    var ctx = $('#myChart');
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Votes'
            },
            ticks: {
              beginAtZero: true,
            }
          }],
          xAxes: [{
            scaleLabel:{
              display:true,
              labelString: 'Days(s)'
            }
          }]
        }
      }
    });
  };
  var goFullScreen = function() {
    $(".goFullScreen").click(function(e) {
      e.preventDefault();
      if ($(this).children('i').hasClass('fa fa-expand')) {
        $(this).children('i').removeClass('fa fa-expand');
        $(this).children('i').addClass('fa fa-compress');
      } else if ($(this).children('i').hasClass('fa fa-compress')) {
        $(this).children('i').removeClass('fa fa-compress');
        $(this).children('i').addClass('fa fa-expand');
      }
      $(this).closest('.card').toggleClass('panel-fullscreen');
    });
  };

}();