var browserLayoutManager_loggingMsgCount=0;
var browserLayoutManager_isDebugging=false;
var browserLayoutManager_horizontalExpandDirection="left";
var browserLayoutManager_FlashContainers=new Array();
var browserLayoutManager_FlashObjects=new Array();
var browserLayoutManager_onResizeIntervalTimeout;
var browserLayoutManager_onResizeIntervalTime=100;
var browserLayoutManager_debugPanel;
function browserLayoutManager_registerFlashContainerForLayout(_1){
browserLayoutManager_FlashContainers.push(_1);
}
function browserLayoutManager_registerFlashObjectForLayout(_2){
browserLayoutManager_FlashObjects.push(_2);
browserLayoutManager_Resize();
}
function browserLayoutManager_GetControllableDivs(){
return browserLayoutManager_FlashContainers;
}
function browserLayoutManager_GetControllableSwfs(){
return browserLayoutManager_FlashObjects;
}
function browserLayoutManager_DimObject(w,h,_5,_6){
this.width=w;
this.height=h;
this.widthMax=_5;
this.heightMax=_6;
}
function browserLayoutManager_getMaxHeight(){
var _7;
if(arguments[0]!=undefined){
_7=arguments[0];
}else{
_7=browserLayoutManager_FlashContainers[0];
}
var H=browserLayoutManager_getBrowserHeight();
var _9=document.getElementById(_7);
var _a=_9.offsetTop;
var _b=H-_a-30;
return _b;
}
function browserLayoutManager_getMaxWidth(){
var _c;
if(arguments[0]!=undefined){
_c=arguments[0];
}else{
_c=browserLayoutManager_FlashContainers[0];
}
var W=browserLayoutManager_getBrowserWidth();
var _e=document.getElementById(_c);
var _f=_e.offsetLeft;
var _10=browserLayoutManager_convertPxToInt(_e.style.width);
_10=parseInt(_10)+_f;
var _11;
if(browserLayoutManager_horizontalExpandDirection=="left"){
_11=_10;
}else{
_11=W-_f-30;
}
return _11;
}
function browserLayoutManager_getBrowserWidth(){
var _12=0;
if(typeof (window.innerWidth)=="number"){
_12=window.innerWidth;
}else{
if(document.documentElement&&(document.documentElement.clientWidth||document.documentElement.clientHeight)){
_12=document.documentElement.clientWidth;
}else{
if(document.body&&(document.body.clientWidth||document.body.clientHeight)){
_12=document.body.clientWidth;
}
}
}
var _13=browserLayoutManager_convertPxToInt(String(_12));
return _13;
}
function browserLayoutManager_getBrowserHeight(){
var _14=0;
var _15="";
if(typeof (window.innerWidth)=="number"){
_14=window.innerHeight;
_15="browserLayoutManager_getBrowserHeight NON IE MODE";
}else{
if(document.documentElement&&(document.documentElement.clientWidth||document.documentElement.clientHeight)){
_14=document.documentElement.clientHeight;
_15="browserLayoutManager_getBrowserHeight IE6+";
}else{
if(document.body&&(document.body.clientWidth||document.body.clientHeight)){
_15="browserLayoutManager_getBrowserHeight IE 4 compatible";
_14=document.body.clientHeight;
}
}
}
return _14;
}
function browserLayoutManager_getBrowserDim(){
var w,h,wr,hr;
w=browserLayoutManager_getBrowserWidth();
h=browserLayoutManager_getBrowserHeight();
wr=browserLayoutManager_getMaxWidth();
hr=browserLayoutManager_getMaxHeight();
var _17="avail:"+w+","+h+" max:"+wr+","+hr;
_17+=" cont:"+browserLayoutManager_getObject("smartsearchcontainer").style.width;
_17+=","+browserLayoutManager_getObject("smartsearchcontainer").style.height;
return new browserLayoutManager_DimObject(w,h,wr,hr);
}
function browserLayoutManager_ResizeDefaultID(w,h){
browserLayoutManager_ResizeID(browserLayoutManager_FlashContainers[0],w,h);
browserLayoutManager_ResizeID(browserLayoutManager_FlashObjects[0],w,h);
}
function browserLayoutManager_ResizeID(_1a,w,h){
var _1d=browserLayoutManager_getObject(_1a);
w=parseInt(w);
h=parseInt(h);
var _1e=0;
var _1f;
if(document.all&&!document.getElementById){
_1f=_1d.offsetLeft+browserLayoutManager_convertPxToInt(_1d.style.pixelWidth);
var _20=(parseInt(w)+_1e);
var _21=parseInt(h);
if(!isNaN(_20)){
_20=_20+"px";
if(_1d.style.pixelWidth!=_20){
_1d.style.pixelWidth=_20;
}
}else{
}
if(!isNaN(_21)){
_21=_21+"px";
if(_1d.style.pixelHeight!=_21){
_1d.style.pixelHeight=_21;
}
}else{
}
}else{
_1f=_1d.offsetLeft+browserLayoutManager_convertPxToInt(_1d.style.width);
_1d.style.width=(parseInt(w)+_1e)+"px";
_1d.style.height=parseInt(h)+"px";
var _22=_1d.childNodes[0];
var _23=(parseInt(w)+_1e);
var _24=parseInt(h);
if(!isNaN(_23)){
_23=_23+"px";
if(_1d.style.width!=_23){
_1d.style.width=_23;
}
}else{
}
if(!isNaN(_24)){
_24=_24+"px";
if(_1d.style.height!=_24){
_1d.style.height=_24;
}
}else{
}
}
}
function browserLayoutManager_Resize(){
if(browserLayoutManager_onResizeIntervalTimeout!=null){
window.clearInterval(browserLayoutManager_onResizeIntervalTimeout);
}
browserLayoutManager_onResizeIntervalTimeout=window.setTimeout("browserLayoutManager_DoResize()",browserLayoutManager_onResizeIntervalTime);
}
function browserLayoutManager_DoResize(){
var n;
var w=browserLayoutManager_getBrowserWidth();
var h=browserLayoutManager_getBrowserHeight();
var wr=browserLayoutManager_getMaxWidth();
var hr=browserLayoutManager_getMaxHeight();
for(n=0;n<browserLayoutManager_FlashObjects.length;n++){
var _2a=browserLayoutManager_getObject(browserLayoutManager_FlashObjects[n]);
if(_2a!=null){
try{
_2a.onBrowserResize(w,h,wr,hr);
}
catch(err){
}
}
}
}
function browserLayoutManager_GetDimension(){
return;
}
function Flash_logIt(){
}
function browserLayoutManager_alert(){
if(!browserLayoutManager_isDebugging){
return;
}
var _2b=browserLayoutManager_debugPanel;
if(_2b==null||_2b==undefined){
_2b=browserLayoutManager_getObject("debugpanel");
if(_2b==null||_2b==undefined){
if(document.forms.blmDebugForm["debugpanel"]!=null){
_2b=document.forms.blmDebugForm["debugpanel"];
}else{
if(browserLayoutManager_getObject("debugpanel")){
_2b=browserLayoutManager_getObject("debugpanel");
}
}
}
}
if(_2b!=null){
_2b.value+=(browserLayoutManager_loggingMsgCount++)+"> "+arguments[0]+"\n";
}else{
alert("debugger not found");
}
}
function browserLayoutManager_addListener(a,b,c,d){
if(a.addEventListener){
a.addEventListener(b,c,d);
return true;
}else{
if(a.attachEvent){
var e=a.attachEvent("on"+b,c);
return e;
}else{
}
}
}
function browserLayoutManager_getObject(_31){
var _32;
if(navigator.appName.indexOf("Microsoft")!=-1){
_32=window[_31];
}else{
_32=document[_31];
}
if(_32==null){
_32=document.getElementById(_31);
}
return _32;
}
function browserLayoutManager_getIsDebugging(){
return browserLayoutManager_isDebugging;
}
function browserLayoutManager_convertPxToInt(_33){
if(_33.indexOf("px")>0){
return parseInt(_33.slice(0,_33.length-2));
}else{
return parseInt(_33);
}
}
function browserLayoutManager_onFocus(){
browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])["onBrowserFocus"]();
}
function browserLayoutManager_onBlur(){
browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])["onBrowserBlur"]();
}
function resizeSmartSearch(w,h){
var _36=document.getElementById("smartsearchcontainer");
alert("rss:"+_36);
_36.style.width=(parseInt(w)+20)+"px";
_36.style.height=(parseInt(h)+50)+"px";
}
function connectiontest(){
var _37=browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0]);
_37.onBrowserResize(600,600,600,600);
}

