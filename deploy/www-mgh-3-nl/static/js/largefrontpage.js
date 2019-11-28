screen = 'small';

function mediaqueryresponse(mql){
  console.log('mql is running');
 if(mql.matches){ // if media query matches
    screen = 'large';
    $('#quicklinks').html('<img src="//www.maxgoldhouse.com/img/laveleta2.jpg" style="max-width:100%;padding: 10px;"/>');
    $('#aftertop6').empty();
    $('#aftertop6').attr('screensize', 'large');
    $('#monbuts').load("inc/monbuts.html");

 }
 else{
    console.log('small')
 }
}

function setCookie(key, value) {
            var expires = new Date();
            expires.setTime(expires.getTime() + (1 * 1 * 60 * 60 * 1000));
            document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
        }

function getCookie(key) {
            var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
            return keyValue ? keyValue[2] : null;
        }

function getforexrate(callback) {
        return $.ajax({
        url: document.location.protocol + '//spreadsheets.google.com/feeds/cells/1JvVo4FI6KtE9aD6-CRCA8uwYre85zLY75nmwjHtTjwU/od6/public/basic/R1C1?alt=json',
        type: 'GET',
        cache: false,
        dataType: 'json'
    })
    .done(callback)
    .fail(function(jqXHR, textStatus, errorThrown) {
        // Handle error
    });
}

function setgbpPrices(rate){
var price_eur, price_gbp
 $( ".price_eur" ).each(function() {
   price_eur = $(this).html().replace(/,/g,'').replace('€','').replace(/ /g,'');
   price_gbp = (price_eur/rate);
   $(this).next('.price_gbp').html('(£'+Math.round(price_gbp).toLocaleString()+')');
});
}
function dogbprices(){
var currentrate = getCookie('gbpeur');
console.log('currentrate '+currentrate);
if(! currentrate){
  getforexrate(function(json) {
   var askprice = json.entry.content.$t;
    console.log('askprice from json '+askprice);
    setCookie('gbpeur', askprice)
    setgbpPrices(askprice)
  });
} else if(!isNaN(currentrate)){
  setgbpPrices(currentrate)
}
}

var mql = window.matchMedia("screen and (min-device-width: 900px)")
mediaqueryresponse(mql) // call listener function explicitly at run time
mql.addListener(mediaqueryresponse) // attach listener function to listen in on state changes


function moreprops(){
if($('#aftertop6').attr('screensize')=='large'){
   $("#aftertop6").load("allindex.html",function(){$(window).unbind(); dogbprices();});
  }
}

$(window).bind("scroll",function() {
    if ($('#aftertop6').is(':visible')) {
        moreprops();
    }
});

dogbprices();
//window.onload = function (screen){
	//show the GBP prices

//}
