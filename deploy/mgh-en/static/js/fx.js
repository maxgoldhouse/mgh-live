function setCookie(key, value) {
            var expires = new Date();
            expires.setTime(expires.getTime() + (1 * 1 * 60 * 60 * 1000));
            document.cookie = key + '=' + value + ';secure;expires=' + expires.toUTCString();
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
   console.log('price_eur '+price_eur);
   price_gbp = (price_eur/rate);
   $(this).next('.price_gbp').html('(£'+Math.round(price_gbp).toLocaleString()+')');
});
}


//show the GBP prices
$(document).ready(function () {
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
});
function getmonthlypayment(cost,ltv,rate,years){
  var p = cost*ltv;
  var r = rate/100;
  var y = years;

  $('#monthlypaymentdetails').css('display','block')
  $('#mp').html('<b>'+Math.round(mortgagePayment(p,r/12,y*12),2)+'</b>')
  //return Math.round(mortgagePayment(p,r/12,y*12),2);
}

function mortgagePayment(p,r,y){
  return futureValue(p,r,y)/geomSeries(1+r,0,y-1);
}

function futureValue(p,r,y){
  return p*Math.pow(1+r,y);
}

function geomSeries(z,m,n){
  var amt;
  if (z == 1.0) amt = n + 1;
  else amt = (Math.pow(z,n + 1) - 1)/(z - 1);
  if (m >= 1) amt -= geomSeries(z,0,m-1);
  return amt;
}

function filterChars(s, charList){
  var s1 = "" + s; // force s1 to be a string data type
  var i;
  for (i = 0; i< s1.length; )
  {
    if (charList.indexOf(s1.charAt(i))< 0)
      s1 = s1.substring(0,i) + s1.substring(i+1, s1.length);
    else
      i++;
  }
  return s1;
}

function makeNumeric(s){
  return filterChars(s, "1234567890.-");
}





