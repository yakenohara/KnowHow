var jQueryCrayon=jQuery;(function(a){a(document).ready(function(){CrayonUtil.init()});CrayonUtil=new function(){var c=this;var b=null;c.init=function(){b=CrayonSyntaxSettings;c.initGET()};c.addPrefixToID=function(d){return d.replace(/^([#.])?(.*)$/,"$1"+b.prefix+"$2")};c.removePrefixFromID=function(e){var d=new RegExp("^[#.]?"+b.prefix,"i");return e.replace(d,"")};c.cssElem=function(d){return a(c.addPrefixToID(d))};c.setDefault=function(e,f){return(typeof e=="undefined")?f:e};c.setMax=function(e,d){return e<=d?e:d};c.setMin=function(d,e){return d>=e?d:e};c.setRange=function(e,f,d){return c.setMax(c.setMin(e,f),d)};c.initFancybox=function(){if(fancyboxInit){fancyboxInit(window,document,a,"crayonFancybox")}};c.getExt=function(e){if(e.indexOf(".")==-1){return undefined}var d=e.split(".");if(d.length){d=d[d.length-1]}else{d=""}return d};c.initGET=function(){window.currentURL=window.location.protocol+"//"+window.location.host+window.location.pathname;window.currentDir=window.currentURL.substring(0,window.currentURL.lastIndexOf("/"));function d(e){e=e.split("+").join(" ");var h={},g,f=/[?&]?([^=]+)=([^&]*)/g;while(g=f.exec(e)){h[decodeURIComponent(g[1])]=decodeURIComponent(g[2])}return h}window.GET=d(document.location.search)};c.getAJAX=function(d,e){d.version=b.version;a.get(b.ajaxurl,d,e)};c.postAJAX=function(d,e){d.version=b.version;a.post(b.ajaxurl,d,e)};c.reload=function(){var d="?";for(var e in window.GET){d+=e+"="+window.GET[e]+"&"}window.location=window.currentURL+d};c.escape=function(d){if(typeof encodeURIComponent=="function"){return encodeURIComponent(d)}else{if(typeof escape!="function"){return escape(d)}else{return d}}};c.log=function(d){if(typeof console!="undefined"&&b.debug){console.log(d)}};c.decode_html=function(d){return String(d).replace(/&amp;/g,"&").replace(/&lt;/g,"<").replace(/&gt;/g,">")};c.encode_html=function(d){return String(d).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")};c.getReadableColor=function(g,f){f=a.extend({amount:0.5,xMulti:1,yMulti:1.5,normalizeHue:[20,180],normalizeHueXMulti:1/2.5,normalizeHueYMulti:1},f);var d=tinycolor(g);var e=d.toHsv();var j={x:e.s,y:1-e.v};j.x*=f.xMulti;j.y*=f.yMulti;if(f.normalizeHue&&e.h>f.normalizeHue[0]&&e.h<f.normalizeHue[1]){j.x*=f.normalizeHueXMulti;j.y*=f.normalizeHueYMulti}var h=Math.sqrt(Math.pow(j.x,2)+Math.pow(j.y,2));if(h<f.amount){e.v=0}else{e.v=1}e.s=0;return tinycolor(e).toHexString()};c.removeChars=function(e,f){var d=new RegExp("["+e+"]","gmi");return f.replace(d,"")}};a.fn.bindFirst=function(c,e){this.bind(c,e);var b=this.data("events")[c.split(".")[0]];var d=b.pop();b.splice(0,0,d)};a.keys=function(d){var c=[];for(var b in d){c.push(b)}return c};RegExp.prototype.execAll=function(c){var f=[];var b=null;while((b=this.exec(c))!=null){var e=[];for(var d in b){if(parseInt(d)==d){e.push(b[d])}}f.push(e)}return f};RegExp.prototype.escape=function(b){return b.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,"\\$&")};String.prototype.sliceReplace=function(d,b,c){return this.substring(0,d)+c+this.substring(b)};String.prototype.escape=function(){var b={"&":"&amp;","<":"&lt;",">":"&gt;"};return this.replace(/[&<>]/g,function(c){return b[c]||c})};String.prototype.linkify=function(b){b=typeof b!="undefined"?b:"";return this.replace(/(http(s)?:\/\/(\S)+)/gmi,'<a href="$1" target="'+b+'">$1</a>')};String.prototype.toTitleCase=function(){var b=this.split(/\s+/);var c="";a.each(b,function(e,d){if(d!=""){c+=d.slice(0,1).toUpperCase()+d.slice(1,d.length);if(e!=b.length-1&&b[e+1]!=""){c+=" "}}});return c}})(jQueryCrayon);jqueryPopup=Object();jqueryPopup.defaultSettings={centerBrowser:0,centerScreen:0,height:500,left:0,location:0,menubar:0,resizable:0,scrollbars:0,status:0,width:500,windowName:null,windowURL:null,top:0,toolbar:0,data:null,event:"click"};(function(a){popupWindow=function(d,c,f,b){f=typeof f!=="undefined"?f:null;b=typeof b!=="undefined"?b:null;if(typeof d=="string"){d=jQuery(d)}if(!(d instanceof jQuery)){return false}var e=jQuery.extend({},jqueryPopup.defaultSettings,c||{});d.handler=jQuery(d).bind(e.event,function(){if(f){f()}var g="height="+e.height+",width="+e.width+",toolbar="+e.toolbar+",scrollbars="+e.scrollbars+",status="+e.status+",resizable="+e.resizable+",location="+e.location+",menuBar="+e.menubar;e.windowName=e.windowName||jQuery(this).attr("name");var h=jQuery(this).attr("href");if(!e.windowURL&&!(h=="#")&&!(h=="")){e.windowURL=jQuery(this).attr("href")}var j,k;var l=null;if(e.centerBrowser){if(jQuery.browser.msie){j=(window.screenTop-120)+((((document.documentElement.clientHeight+120)/2)-(e.height/2)));k=window.screenLeft+((((document.body.offsetWidth+20)/2)-(e.width/2)))}else{j=window.screenY+(((window.outerHeight/2)-(e.height/2)));k=window.screenX+(((window.outerWidth/2)-(e.width/2)))}l=window.open(e.windowURL,e.windowName,g+",left="+k+",top="+j)}else{if(e.centerScreen){j=(screen.height-e.height)/2;k=(screen.width-e.width)/2;l=window.open(e.windowURL,e.windowName,g+",left="+k+",top="+j)}else{l=window.open(e.windowURL,e.windowName,g+",left="+e.left+",top="+e.top)}}if(l!=null){l.focus();if(e.data){l.document.write(e.data)}}if(b){b()}});return e};popdownWindow=function(b,c){if(typeof c=="undefined"){c="click"}b=jQuery(b);if(!(b instanceof jQuery)){return false}b.unbind(c,b.handler)}})(jQueryCrayon);(function(f){f.fn.exists=function(){return this.length!==0};f.fn.style=function(C,F,B){var E=this.get(0);if(typeof E=="undefined"){return}var D=E.style;if(typeof C!="undefined"){if(typeof F!="undefined"){B=typeof B!="undefined"?B:"";if(typeof D.setProperty!="undefined"){D.setProperty(C,F,B)}else{D[C]=F}}else{return D[C]}}else{return D}};var d="crayon-pressed";var a="";var o="div.crayon-syntax";var e=".crayon-toolbar";var c=".crayon-info";var x=".crayon-plain";var p=".crayon-main";var n=".crayon-table";var w=".crayon-loading";var h=".crayon-code";var q=".crayon-title";var m=".crayon-tools";var b=".crayon-nums";var k=".crayon-num";var r=".crayon-line";var g="crayon-wrapped";var t=".crayon-nums-content";var v=".crayon-nums-button";var l=".crayon-wrap-button";var j=".crayon-expand-button";var u="crayon-expanded crayon-toolbar-visible";var z="crayon-placeholder";var y=".crayon-popup-button";var s=".crayon-copy-button";var A=".crayon-plain-button";f(document).ready(function(){CrayonSyntax.init()});CrayonSyntax=new function(){var J=this;var O=new Object();var ah;var I;var H=0;var aa;J.init=function(){if(typeof O=="undefined"){O=new Object()}ah=CrayonSyntaxSettings;I=CrayonSyntaxStrings;f(o).each(function(){J.process(this)})};J.process=function(aE,aF){aE=f(aE);var at=aE.attr("id");if(at=="crayon-"){at+=Y()}aE.attr("id",at);CrayonUtil.log(at);if(typeof aF=="undefined"){aF=false}if(!aF&&!ab(at)){return}var av=aE.find(e);var aD=aE.find(c);var aq=aE.find(x);var ar=aE.find(p);var aC=aE.find(n);var ak=aE.find(h);var aH=aE.find(q);var aB=aE.find(m);var az=aE.find(b);var aw=aE.find(t);var aA=aE.find(v);var an=aE.find(l);var ap=aE.find(j);var aG=aE.find(y);var au=aE.find(s);var am=aE.find(A);O[at]=aE;O[at].toolbar=av;O[at].plain=aq;O[at].info=aD;O[at].main=ar;O[at].table=aC;O[at].code=ak;O[at].title=aH;O[at].tools=aB;O[at].nums=az;O[at].nums_content=aw;O[at].numsButton=aA;O[at].wrapButton=an;O[at].expandButton=ap;O[at].popup_button=aG;O[at].copy_button=au;O[at].plainButton=am;O[at].numsVisible=true;O[at].wrapped=false;O[at].plainVisible=false;O[at].toolbar_delay=0;O[at].time=1;f(x).css("z-index",0);var ax=ar.style();O[at].mainStyle={height:ax&&ax.height||"","max-height":ax&&ax.maxHeight||"","min-height":ax&&ax.minHeight||"",width:ax&&ax.width||"","max-width":ax&&ax.maxWidth||"","min-width":ax&&ax.minWidth||""};O[at].mainHeightAuto=O[at].mainStyle.height==""&&O[at].mainStyle["max-height"]=="";var al;var ay=0;O[at].loading=true;O[at].scrollBlockFix=false;aA.click(function(){CrayonSyntax.toggleNums(at)});an.click(function(){CrayonSyntax.toggleWrap(at)});ap.click(function(){CrayonSyntax.toggleExpand(at)});am.click(function(){CrayonSyntax.togglePlain(at)});au.click(function(){CrayonSyntax.copyPlain(at)});C(at);var ao=function(){if(az.filter('[data-settings~="hide"]').length!=0){aw.ready(function(){CrayonUtil.log("function"+at);CrayonSyntax.toggleNums(at,true,true)})}else{ad(at)}if(typeof O[at].expanded=="undefined"){if(Math.abs(O[at].main.outerWidth()-O[at].table.outerWidth())<10){O[at].expandButton.hide()}else{O[at].expandButton.show()}}if(ay==5){clearInterval(al);O[at].loading=false}ay++};al=setInterval(ao,300);D(at);f(k,O[at]).each(function(){var aK=f(this).attr("data-line");var aJ=f("#"+aK);var aI=aJ.style("height");if(aI){aJ.attr("data-height",aI)}});ar.css("position","relative");ar.css("z-index",1);aa=(aE.filter('[data-settings~="touchscreen"]').length!=0);if(!aa){ar.click(function(){B(at,"",false)});aq.click(function(){B(at,"",false)});aD.click(function(){B(at,"",false)})}if(aE.filter('[data-settings~="no-popup"]').length==0){O[at].popup_settings=popupWindow(aG,{height:screen.height-200,width:screen.width-100,top:75,left:50,scrollbars:1,windowURL:"",data:""},function(){G(at)},function(){})}aq.css("opacity",0);O[at].toolbarVisible=true;O[at].hasOneLine=aC.outerHeight()<av.outerHeight()*2;O[at].toolbarMouseover=false;if(av.filter('[data-settings~="mouseover"]').length!=0&&!aa){O[at].toolbarMouseover=true;O[at].toolbarVisible=false;av.css("margin-top","-"+av.outerHeight()+"px");av.hide();if(av.filter('[data-settings~="overlay"]').length!=0&&!O[at].hasOneLine){av.css("position","absolute");av.css("z-index",2);if(av.filter('[data-settings~="hide"]').length!=0){ar.click(function(){U(at,undefined,undefined,0)});aq.click(function(){U(at,false,undefined,0)})}}else{av.css("z-index",4)}if(av.filter('[data-settings~="delay"]').length!=0){O[at].toolbar_delay=500}aE.mouseenter(function(){U(at,true)}).mouseleave(function(){U(at,false)})}else{if(aa){av.show()}}if(aE.filter('[data-settings~="minimize"]').length==0){J.minimize(at)}if(aq.length!=0&&!aa){if(aq.filter('[data-settings~="dblclick"]').length!=0){ar.dblclick(function(){CrayonSyntax.togglePlain(at)})}else{if(aq.filter('[data-settings~="click"]').length!=0){ar.click(function(){CrayonSyntax.togglePlain(at)})}else{if(aq.filter('[data-settings~="mouseover"]').length!=0){aE.mouseenter(function(){CrayonSyntax.togglePlain(at,true)}).mouseleave(function(){CrayonSyntax.togglePlain(at,false)});aA.hide()}}}if(aq.filter('[data-settings~="show-plain-default"]').length!=0){CrayonSyntax.togglePlain(at,true)}}var aj=aE.filter('[data-settings~="expand"]').length!=0;if(!aa&&aE.filter('[data-settings~="scroll-mouseover"]').length!=0){ar.css("overflow","hidden");aq.css("overflow","hidden");aE.mouseenter(function(){N(at,true,aj)}).mouseleave(function(){N(at,false,aj)})}if(aj){aE.mouseenter(function(){E(at,true)}).mouseleave(function(){E(at,false)})}if(aE.filter('[data-settings~="disable-anim"]').length!=0){O[at].time=0}if(aE.filter('[data-settings~="wrap"]').length!=0){O[at].wrapped=true}O[at].mac=aE.hasClass("crayon-os-mac");ad(at);ac(at);Z(at)};var ab=function(aj){CrayonUtil.log(O);if(typeof O[aj]=="undefined"){O[aj]=f("#"+aj);CrayonUtil.log("make "+aj);return true}CrayonUtil.log("no make "+aj);return false};var Y=function(){return H++};var G=function(aj){if(typeof O[aj]=="undefined"){return ab(aj)}var ak=O[aj].popup_settings;if(ak.data){return}var am=O[aj].clone(true);am.removeClass("crayon-wrapped");if(O[aj].wrapped){f(k,am).each(function(){var ap=f(this).attr("data-line");var ao=f("#"+ap);var an=ao.attr("data-height");an=an?an:"";if(typeof an!="undefined"){ao.css("height",an);f(this).css("height",an)}})}am.find(p).css("height","");var al="";if(O[aj].plainVisible){al=am.find(x)}else{al=am.find(p)}ak.data=J.getAllCSS()+'<body class="crayon-popup-window" style="padding:0; margin:0;"><div class="'+am.attr("class")+' crayon-popup">'+J.removeCssInline(J.getHtmlString(al))+"</div></body>"};J.minimize=function(am){var al=f('<div class="crayon-minimize crayon-button"><div>');O[am].tools.append(al);O[am].origTitle=O[am].title.html();if(!O[am].origTitle){O[am].title.html(I.minimize)}var ak="crayon-minimized";var aj=function(){O[am].toolbarPreventHide=false;al.remove();O[am].removeClass(ak);O[am].title.html(O[am].origTitle);var an=O[am].toolbar;if(an.filter('[data-settings~="never-show"]').length!=0){an.remove()}};O[am].toolbar.click(aj);al.click(aj);O[am].addClass(ak);O[am].toolbarPreventHide=true;U(am,undefined,undefined,0)};J.getHtmlString=function(aj){return f("<div>").append(aj.clone()).remove().html()};J.removeCssInline=function(al){var ak=/style\s*=\s*"([^"]+)"/gmi;var aj=null;while((aj=ak.exec(al))!=null){var am=aj[1];am=am.replace(/\b(?:width|height)\s*:[^;]+;/gmi,"");al=al.sliceReplace(aj.index,aj.index+aj[0].length,'style="'+am+'"')}return al};J.getAllCSS=function(){var al="";var ak=f('link[rel="stylesheet"]');var aj=[];if(ak.length==1){aj=ak}else{aj=ak.filter('[href*="crayon-syntax-highlighter"], [href*="min/"]')}aj.each(function(){var am=J.getHtmlString(f(this));al+=am});return al};J.copyPlain=function(al,am){if(typeof O[al]=="undefined"){return ab(al)}var ak=O[al].plain;J.togglePlain(al,true,true);U(al,true);var aj=O[al].mac?"\u2318":"CTRL";var an=I.copy;an=an.replace(/%s/,aj+"+C");an=an.replace(/%s/,aj+"+V");B(al,an);return false};var B=function(ak,am,aj){if(typeof O[ak]=="undefined"){return ab(ak)}var al=O[ak].info;if(typeof am=="undefined"){am=""}if(typeof aj=="undefined"){aj=true}if(M(al)&&aj){al.html("<div>"+am+"</div>");al.css("margin-top",-al.outerHeight());al.show();R(ak,al,true);setTimeout(function(){R(ak,al,false)},5000)}if(!aj){R(ak,al,false)}};var C=function(aj){if(window.devicePixelRatio>1){var ak=f(".crayon-button-icon",O[aj].toolbar);ak.each(function(){var am=f(this).css("background-image");var al=am.replace(/\.(?=[^\.]+$)/g,"@2x.");f(this).css("background-size","48px 128px");f(this).css("background-image",al)})}};var M=function(aj){var ak="-"+aj.outerHeight()+"px";if(aj.css("margin-top")==ak||aj.css("display")=="none"){return true}else{return false}};var R=function(am,al,ak,ao,an,aq){var aj=function(){if(aq){aq(am,al)}};var ap="-"+al.outerHeight()+"px";if(typeof ak=="undefined"){if(M(al)){ak=true}else{ak=false}}if(typeof ao=="undefined"){ao=100}if(ao==false){ao=false}if(typeof an=="undefined"){an=0}al.stop(true);if(ak==true){al.show();al.animate({marginTop:0},ai(ao,am),aj)}else{if(ak==false){if(al.css("margin-top")=="0px"&&an){al.delay(an)}al.animate({marginTop:ap},ai(ao,am),function(){al.hide();aj()})}}};J.togglePlain=function(am,an,ak){if(typeof O[am]=="undefined"){return ab(am)}var aj=O[am].main;var al=O[am].plain;if((aj.is(":animated")||al.is(":animated"))&&typeof an=="undefined"){return}af(am);var ap,ao;if(typeof an!="undefined"){if(an){ap=aj;ao=al}else{ap=al;ao=aj}}else{if(aj.css("z-index")==1){ap=aj;ao=al}else{ap=al;ao=aj}}O[am].plainVisible=(ao==al);O[am].top=ap.scrollTop();O[am].left=ap.scrollLeft();O[am].scrollChanged=false;D(am);ap.stop(true);ap.fadeTo(ai(500,am),0,function(){ap.css("z-index",0)});ao.stop(true);ao.fadeTo(ai(500,am),1,function(){ao.css("z-index",1);if(ao==al){if(ak){al.select()}else{}}ao.scrollTop(O[am].top+1);ao.scrollTop(O[am].top);ao.scrollLeft(O[am].left+1);ao.scrollLeft(O[am].left)});ao.scrollTop(O[am].top);ao.scrollLeft(O[am].left);ac(am);U(am,false);return false};J.toggleNums=function(an,am,aj){if(typeof O[an]=="undefined"){ab(an);return false}if(O[an].table.is(":animated")){return false}var ap=Math.round(O[an].nums_content.outerWidth()+1);var ao="-"+ap+"px";var al;if(typeof am!="undefined"){al=false}else{al=(O[an].table.css("margin-left")==ao)}var ak;if(al){ak="0px";O[an].numsVisible=true}else{O[an].table.css("margin-left","0px");O[an].numsVisible=false;ak=ao}if(typeof aj!="undefined"){O[an].table.css("margin-left",ak);ad(an);return false}var aq=(O[an].table.outerWidth()+K(O[an].table.css("margin-left"))>O[an].main.outerWidth());var ar=(O[an].table.outerHeight()>O[an].main.outerHeight());if(!aq&&!ar){O[an].main.css("overflow","hidden")}O[an].table.animate({marginLeft:ak},ai(200,an),function(){if(typeof O[an]!="undefined"){ad(an);if(!aq&&!ar){O[an].main.css("overflow","auto")}}});return false};J.toggleWrap=function(aj){O[aj].wrapped=!O[aj].wrapped;Z(aj)};J.toggleExpand=function(aj){var ak=!CrayonUtil.setDefault(O[aj].expanded,false);E(aj,ak)};var Z=function(aj,ak){ak=CrayonUtil.setDefault(ak,true);if(O[aj].wrapped){O[aj].addClass(g)}else{O[aj].removeClass(g)}F(aj);if(!O[aj].expanded&&ak){W(aj)}O[aj].wrapTimes=0;clearInterval(O[aj].wrapTimer);O[aj].wrapTimer=setInterval(function(){if(O[aj].is(":visible")){P(aj);O[aj].wrapTimes++;if(O[aj].wrapTimes==5){clearInterval(O[aj].wrapTimer)}}},200)};var ae=function(aj){if(typeof O[aj]=="undefined"){ab(aj);return false}};var K=function(ak){if(typeof ak!="string"){return 0}var aj=ak.replace(/[^-0-9]/g,"");if(aj.length==0){return 0}else{return parseInt(aj)}};var ad=function(aj){if(typeof O[aj]=="undefined"||typeof O[aj].numsVisible=="undefined"){return}if(O[aj].numsVisible){O[aj].numsButton.removeClass(a);O[aj].numsButton.addClass(d)}else{O[aj].numsButton.removeClass(d);O[aj].numsButton.addClass(a)}};var F=function(aj){if(typeof O[aj]=="undefined"||typeof O[aj].wrapped=="undefined"){return}if(O[aj].wrapped){O[aj].wrapButton.removeClass(a);O[aj].wrapButton.addClass(d)}else{O[aj].wrapButton.removeClass(d);O[aj].wrapButton.addClass(a)}};var X=function(aj){if(typeof O[aj]=="undefined"||typeof O[aj].expanded=="undefined"){return}if(O[aj].expanded){O[aj].expandButton.removeClass(a);O[aj].expandButton.addClass(d)}else{O[aj].expandButton.removeClass(d);O[aj].expandButton.addClass(a)}};var ac=function(aj){if(typeof O[aj]=="undefined"||typeof O[aj].plainVisible=="undefined"){return}if(O[aj].plainVisible){O[aj].plainButton.removeClass(a);O[aj].plainButton.addClass(d)}else{O[aj].plainButton.removeClass(d);O[aj].plainButton.addClass(a)}};var U=function(ak,aj,am,al){if(typeof O[ak]=="undefined"){return ab(ak)}else{if(!O[ak].toolbarMouseover){return}else{if(aj==false&&O[ak].toolbarPreventHide){return}else{if(aa){return}}}}var an=O[ak].toolbar;if(typeof al=="undefined"){al=O[ak].toolbar_delay}R(ak,an,aj,am,al,function(){O[ak].toolbarVisible=aj})};var S=function(al,aj){var ak=f.extend({},al);ak.width+=aj.width;ak.height+=aj.height;return ak};var Q=function(al,aj){var ak=f.extend({},al);ak.width-=aj.width;ak.height-=aj.height;return ak};var V=function(aj){if(typeof O[aj].initialSize=="undefined"){O[aj].toolbarHeight=O[aj].toolbar.outerHeight();O[aj].innerSize={width:O[aj].width(),height:O[aj].height()};O[aj].outerSize={width:O[aj].outerWidth(),height:O[aj].outerHeight()};O[aj].borderSize=Q(O[aj].outerSize,O[aj].innerSize);O[aj].initialSize={width:O[aj].main.outerWidth(),height:O[aj].main.outerHeight()};O[aj].initialSize.height+=O[aj].toolbarHeight;O[aj].initialOuterSize=S(O[aj].initialSize,O[aj].borderSize);O[aj].finalSize={width:O[aj].table.outerWidth(),height:O[aj].table.outerHeight()};O[aj].finalSize.height+=O[aj].toolbarHeight;O[aj].finalSize.width=CrayonUtil.setMin(O[aj].finalSize.width,O[aj].initialSize.width);O[aj].finalSize.height=CrayonUtil.setMin(O[aj].finalSize.height,O[aj].initialSize.height);O[aj].diffSize=Q(O[aj].finalSize,O[aj].initialSize);O[aj].finalOuterSize=S(O[aj].finalSize,O[aj].borderSize);O[aj].initialSize.height+=O[aj].toolbar.outerHeight()}};var E=function(am,ap){if(typeof O[am]=="undefined"){return ab(am)}if(typeof ap=="undefined"){return}var ak=O[am].main;var ar=O[am].plain;if(ap){if(typeof O[am].expanded=="undefined"){V(am);O[am].expandTime=CrayonUtil.setRange(O[am].diffSize.width/3,300,800);O[am].expanded=false;var aq=O[am].finalOuterSize;O[am].placeholder=f("<div></div>");O[am].placeholder.addClass(z);O[am].placeholder.css(aq);O[am].before(O[am].placeholder);O[am].placeholder.css("margin",O[am].css("margin"));f(window).bind("resize",L)}var an={height:"auto","min-height":"none","max-height":"none"};var aj={width:"auto","min-width":"none","max-width":"none"};O[am].outerWidth(O[am].outerWidth());O[am].css({"min-width":"none","max-width":"none"});var ao={width:O[am].finalOuterSize.width};if(!O[am].mainHeightAuto&&!O[am].hasOneLine){ao.height=O[am].finalOuterSize.height;O[am].outerHeight(O[am].outerHeight())}ak.css(an);ak.css(aj);O[am].stop(true);O[am].animate(ao,ai(O[am].expandTime,am),function(){O[am].expanded=true;X(am)});O[am].placeholder.show();f("body").prepend(O[am]);O[am].addClass(u);L()}else{var at=O[am].initialOuterSize;var al=O[am].toolbar_delay;if(at){O[am].stop(true);if(!O[am].expanded){O[am].delay(al)}var ao={width:at.width};if(!O[am].mainHeightAuto&&!O[am].hasOneLine){ao.height=at.height}O[am].animate(ao,ai(O[am].expandTime,am),function(){ag(am)})}else{setTimeout(function(){ag(am)},al)}O[am].placeholder.hide();O[am].placeholder.before(O[am]);O[am].css({left:"auto",top:"auto"});O[am].removeClass(u)}af(am);if(ap){Z(am,false)}};var L=function(){for(uid in O){if(O[uid].hasClass(u)){O[uid].css(O[uid].placeholder.offset())}}};var ag=function(aj){O[aj].expanded=false;W(aj);X(aj);if(O[aj].wrapped){Z(aj)}};var N=function(am,ak,an){if(typeof O[am]=="undefined"){return ab(am)}if(typeof ak=="undefined"||an||O[am].expanded){return}var aj=O[am].main;var al=O[am].plain;if(ak){aj.css("overflow","auto");al.css("overflow","auto");if(typeof O[am].top!="undefined"){visible=(aj.css("z-index")==1?aj:al);visible.scrollTop(O[am].top-1);visible.scrollTop(O[am].top);visible.scrollLeft(O[am].left-1);visible.scrollLeft(O[am].left)}}else{visible=(aj.css("z-index")==1?aj:al);O[am].top=visible.scrollTop();O[am].left=visible.scrollLeft();aj.css("overflow","hidden");al.css("overflow","hidden")}O[am].scrollChanged=true;D(am)};var D=function(aj){O[aj].table.style("width","100%","important");var ak=setTimeout(function(){O[aj].table.style("width","");clearInterval(ak)},10)};var W=function(al){var ak=O[al].main;var aj=O[al].mainStyle;ak.css(aj);O[al].css("height","auto");O[al].css("width",aj.width);O[al].css("max-width",aj["max-width"]);O[al].css("min-width",aj["min-width"])};var af=function(aj){O[aj].plain.outerHeight(O[aj].main.outerHeight())};var P=function(aj){f(k,O[aj]).each(function(){var am=f(this).attr("data-line");var al=f("#"+am);var ak=null;if(O[aj].wrapped){al.css("height","");ak=al.outerHeight();ak=ak?ak:""}else{ak=al.attr("data-height");ak=ak?ak:"";al.css("height",ak)}f(this).css("height",ak)})};var ai=function(aj,ak){if(aj=="fast"){aj=200}else{if(aj=="slow"){aj=600}else{if(!T(aj)){aj=parseInt(aj);if(isNaN(aj)){return 0}}}}return aj*O[ak].time};var T=function(aj){return typeof aj=="number"}}})(jQueryCrayon);var CSSJSON=new function(){var c=this;c.init=function(){String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")};String.prototype.repeat=function(p){return new Array(1+p).join(this)}};c.init();var h=/([^\s\;\{\}][^\;\{\}]*)\{/g;var n=/\}/g;var d=/([^\;\{\}]*)\;/g;var l=/\/\*[\s\S]*?\*\//g;var g=/([^\:]+):([^\;]*);/;var o=/(\/\*[\s\S]*?\*\/)|([^\s\;\{\}][^\;\{\}]*(?=\{))|(\})|([^\;\{\}]+\;(?!\s*\*\/))/gmi;var j=1;var f=2;var b=3;var k=4;var e=function(p){return typeof p=="undefined"||p.length==0||p==null};c.toJSON=function(r,x){var s={children:{},attributes:{}};var u=null;var v=0;if(typeof x=="undefined"){var x={ordered:false,comments:false,stripComments:false,split:false}}if(x.stripComments){x.comments=false;r=r.replace(l,"")}while((u=o.exec(r))!=null){if(!e(u[j])&&x.comments){var C=u[j].trim();s[v++]=C}else{if(!e(u[f])){var p=u[f].trim();var A=c.toJSON(r,x);if(x.ordered){var t={};t.name=p;t.value=A;t.type="rule";s[v++]=t}else{if(x.split){var B=p.split(",")}else{var B=[p]}for(i in B){var q=B[i].trim();if(q in s.children){for(var y in A.attributes){s.children[q].attributes[y]=A.attributes[y]}}else{s.children[q]=A}}}}else{if(!e(u[b])){return s}else{if(!e(u[k])){var D=u[k].trim();var w=g.exec(D);if(w){var p=w[1].trim();var z=w[2].trim();if(x.ordered){var t={};t.name=p;t.value=z;t.type="attr";s[v++]=t}else{s.attributes[p]=z}}else{s[v++]=D}}}}}}return s};c.toCSS=function(r,t,q){var p="";if(typeof t=="undefined"){t=0}if(typeof q=="undefined"){q=false}if(r.attributes){for(i in r.attributes){p+=a(i,r.attributes[i],t)}}if(r.children){var s=true;for(i in r.children){if(q&&!s){p+="\n"}else{s=false}p+=m(i,r.children[i],t)}}return p};var a=function(p,q,r){return"\t".repeat(r)+p+": "+q+";\n"};var m=function(p,r,s){var q="\t".repeat(s)+p+" {\n";q+=c.toCSS(r,s+1);q+="\t".repeat(s)+"}\n";return q}};