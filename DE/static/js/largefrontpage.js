screen = 'small';

function mediaqueryresponse(mql){
 if(mql.matches){ // if media query matches
    screen = 'large';
    $('#quicklinks').html('<img src="//www.maxgoldhouse.com/img/laveleta2.jpg" style="max-width:100%"/>');
    $('#aftertop6').empty();
    $('#aftertop6').attr('screensize', 'large');
    $('#monbuts').load("inc/monbuts.html");

 }
 else{
    console.log('small')
 }
}

var mql = window.matchMedia("screen and (min-device-width: 900px)")
mediaqueryresponse(mql) // call listener function explicitly at run time
mql.addListener(mediaqueryresponse) // attach listener function to listen in on state changes

window.onload = function (screen){
 if($('#aftertop6').attr('screensize') == 'large'){
      $('#aftertop6').load("allindex.html");
 }
}