//var totalslides=$(".thumb").length;var target=0;var autoslide;var onauto=0;$(".thumb").click(function(){$(".thumb").removeClass("current");$(this).addClass("current");var e=$(this).attr("src").replace("s35-p","s0");$("#show").attr("src",e).attr("showing",$(this).attr("slide"))});$(".forward").click(function(){current=eval($("#show").attr("showing"));if(current==totalslides){target=1}else{target=current+1}$("[slide="+target+"]").trigger("click")});$(".back").click(function(){current=eval($("#show").attr("showing"));if(current==1){target=totalslides}else{target=current-1}$("[slide="+target+"]").trigger("click")});$(".thumb, .forward, .pause").hover(function(){clearInterval(autoslide)},function(){if(onauto==1){$(".start").trigger("click")}});$(".start").click(function(){autoslide=setInterval(function(){$(".forward").trigger("click")},2500);onauto=1;$(".start").css("display","none");$(".pause").css("display","inline-block")});$(".pause").click(function(){clearInterval(autoslide);onauto=0;$(".pause").css("display","none");$(".start").css("display","inline-block")});$(document).ready(function(){$(".pause").trigger("click")});$(document).keydown(function(e){switch(e.which){case 37:$(".back").trigger("click");break;case 38:$(".start").trigger("click");break;case 39:$(".forward").trigger("click");break;case 40:$(".pause").trigger("click");break;default:return}e.preventDefault()})
function setbackbutton(){
 if(document.referrer.indexOf("maxgoldhouse.com") !== -1){
  $('#btn-property-back').attr('href',document.referrer)
}else{
  $('#btn-property-back').attr('href',window.location.protocol + "//" + window.location.host)
}
}
//form handler
        $.fn.serializeObject = function()
        {
          var o = {};
          var a = this.serializeArray();
          $.each(a, function() {
            if (o[this.name] !== undefined) {
              if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
              }
              o[this.name].push(this.value || '');
            } else {
              o[this.name] = this.value || '';
            }
          });
          o['url'] = location.protocol + '//' + location.host + location.pathname;
          return o;
        };
 $('form').submit(function() {

          var thedata = JSON.stringify($(this).serializeObject())
          var script = document.createElement('script');
          script.src = 'https://script.google.com/macros/s/AKfycbwFOPvfoJMpt-OgtwsC2PDo56pNWO7h5QQjJAgzbsRxBgucsFb9/exec?data='+thedata;
          document.body.appendChild(script);
          var enqname = $(this).find('input[name="name"]').val();
          var thankmsg = '<p>Dank u '+enqname+'. Iemand van ons kantoor zal contact met u op.</p>';
          $(this).html(thankmsg);
          return false;
        });
