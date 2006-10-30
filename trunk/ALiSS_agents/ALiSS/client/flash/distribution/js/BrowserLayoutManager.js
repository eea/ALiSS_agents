var browserLayoutManager_loggingMsgCount=0;
var browserLayoutManager_isDebugging=false;

//left or right, depending on which way you want to measure available space
var browserLayoutManager_horizontalExpandDirection="left"; 

var  browserLayoutManager_FlashContainers=new Array();
var  browserLayoutManager_FlashObjects=new Array();

var browserLayoutManager_onResizeIntervalTimeout;
var browserLayoutManager_onResizeIntervalTime=100;

var browserLayoutManager_debugPanel;
//--------------------------------------------------------------------------------
function browserLayoutManager_registerFlashContainerForLayout(obj)
{
	browserLayoutManager_FlashContainers.push(obj);
}
function browserLayoutManager_registerFlashObjectForLayout(obj)
{
	browserLayoutManager_FlashObjects.push(obj);
	browserLayoutManager_Resize();
}
//--------------------------------------------------------------------------------
function browserLayoutManager_GetControllableDivs()
{
	return browserLayoutManager_FlashContainers;
}
function browserLayoutManager_GetControllableSwfs()
{
	return browserLayoutManager_FlashObjects;
}
//--------------------------------------------------------------------------------
function browserLayoutManager_DimObject(w,h,wmax,hmax){
	this.width=w;
	this.height=h;
	this.widthMax=wmax;
	this.heightMax=hmax;
	}
//--------------------------------------------------------------------------------
function browserLayoutManager_getMaxHeight()
{
	var obj_id;
	
	if(arguments[0]!=undefined){
		obj_id=arguments[0];
	}else{
		obj_id=browserLayoutManager_FlashContainers[0];
	}

	var H=browserLayoutManager_getBrowserHeight();
	

	var flashTarget = document.getElementById(obj_id);  
	var topY=flashTarget.offsetTop ;

	var result=H-topY-30;

	return result;
}
//--------------------------------------------------------------------------------
function browserLayoutManager_getMaxWidth()
{
	var obj_id;
	
	if(arguments[0]!=undefined){
		obj_id=arguments[0];
	}else{
		obj_id=browserLayoutManager_FlashContainers[0];
	}
	
	var W=browserLayoutManager_getBrowserWidth();

	var flashTarget = document.getElementById(obj_id);  
	var leftX=flashTarget.offsetLeft ;
	var rightX=browserLayoutManager_convertPxToInt(flashTarget.style.width);

	rightX=parseInt(rightX)+leftX;
	
	var result;
	if(browserLayoutManager_horizontalExpandDirection=="left"){
		result=rightX;
	}else{
		result=W-leftX-30;
	}


	return result;
}
//--------------------------------------------------------------------------------
function browserLayoutManager_getBrowserWidth()
{
	// browserLayoutManager_alert("GBW");
	var myWidth = 0;
	if( typeof( window.innerWidth ) == 'number' ) {
		//Non-IE
		myWidth = window.innerWidth;
	} else if( document.documentElement &&
	( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
		//IE 6+ in 'standards compliant mode'
		myWidth = document.documentElement.clientWidth;
	} else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
		//IE 4 compatible
		myWidth = document.body.clientWidth;
	}
	
	var result=browserLayoutManager_convertPxToInt(String(myWidth));

	
	
	
	return result;
}
//--------------------------------------------------------------------------------
function browserLayoutManager_getBrowserHeight()
{
	var myHeight = 0;
	var alert_str="";
	if( typeof( window.innerWidth ) == 'number' ) {
		//Non-IE
		myHeight = window.innerHeight;
		alert_str="browserLayoutManager_getBrowserHeight NON IE MODE";
	} else if( document.documentElement &&
	( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
		//IE 6+ in 'standards compliant mode'
		myHeight = document.documentElement.clientHeight;
		alert_str="browserLayoutManager_getBrowserHeight IE6+";
	} else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
		//IE 4 compatible
		alert_str="browserLayoutManager_getBrowserHeight IE 4 compatible";
		myHeight = document.body.clientHeight;
	}
// browserLayoutManager_alert(alert_str);
	return myHeight;
}
//--------------------------------------------------------------------------------
function browserLayoutManager_getBrowserDim()
{
	var w,h,wr,hr;
	w=browserLayoutManager_getBrowserWidth();
	h=browserLayoutManager_getBrowserHeight();
	wr=browserLayoutManager_getMaxWidth();
	hr=browserLayoutManager_getMaxHeight();
	
	var status_str="avail:"+w+","+h+" max:"+wr+","+hr;
	status_str+=" cont:"+browserLayoutManager_getObject("smartsearchcontainer").style.width
	status_str+=","+browserLayoutManager_getObject("smartsearchcontainer").style.height;
	// browserLayoutManager_alert(status_str);
	
	
//	document.forms.blmDebugForm['debugpanel']['browserDim'].value="avail:"+w+","+h+" max:"+wr+","+hr;
	return new browserLayoutManager_DimObject(w,h,wr,hr);
}
//--------------------------------------------------------------------------------

function browserLayoutManager_ResizeDefaultID(w,h)
{
	browserLayoutManager_ResizeID(browserLayoutManager_FlashContainers[0],w,h);
	browserLayoutManager_ResizeID(browserLayoutManager_FlashObjects[0],w,h);
}
//--------------------------------------------------------------------------------
function browserLayoutManager_ResizeID(obj_id,w,h)
{

	var flashTarget = browserLayoutManager_getObject(obj_id);
	w=parseInt(w);
	h=parseInt(h);
	
	var wbuf=0;
	var origRightX;
	
	
	if(document.all && !document.getElementById) {
	 	// browserLayoutManager_alert("SET MODE 1");
		origRightX = flashTarget.offsetLeft+browserLayoutManager_convertPxToInt(flashTarget.style.pixelWidth);
		
		var finalW=(parseInt(w)+wbuf) ;
		var finalH=parseInt(h) ;
		
		if(!isNaN(finalW)){		
			finalW=finalW+ "px";
			if(flashTarget.style.pixelWidth!=finalW){
				flashTarget.style.pixelWidth = finalW; 
			}
		}else{
			// browserLayoutManager_alert("ERR IS NAN");
		}
		
		if(!isNaN(finalH)){
			finalH=finalH+ "px"; 
			if(flashTarget.style.pixelHeight != finalH){
				flashTarget.style.pixelHeight = finalH; 
			}
 		}else{
			// browserLayoutManager_alert("ERR IS NAN");
		}
 	

	}else{
		//// browserLayoutManager_alert("SET MODE 2");
		
		origRightX = flashTarget.offsetLeft+browserLayoutManager_convertPxToInt(flashTarget.style.width);

		flashTarget.style.width = (parseInt(w)+wbuf) + "px"; 
		flashTarget.style.height = parseInt(h) + "px"; 

		var flashTargetO = flashTarget.childNodes[0]; 		
		var finalW=(parseInt(w)+wbuf) ;
		var finalH=parseInt(h) ;
		
		if(!isNaN(finalW)){	
			finalW=finalW+ "px";					
			//// browserLayoutManager_alert("SET MODE 2 - COMPARE "+flashTarget.style.width+" vs "+finalW);
			if(flashTarget.style.width !=finalW){
				flashTarget.style.width = finalW; 
				// browserLayoutManager_alert("SET MODE 2 - WIDTH = "+finalW);
			}

		}else{
			// browserLayoutManager_alert("ERR IS NAN");
		}
		
		if(!isNaN(finalH)){
			finalH=finalH+ "px";
			//// browserLayoutManager_alert("SET MODE 2 - COMPARE "+flashTarget.style.height+" vs "+finalH);
			if(flashTarget.style.height !=finalH){
				flashTarget.style.height = finalH; 
				// browserLayoutManager_alert("SET MODE 2 - HEIGHT = "+finalH);
			}
 		}else{
			// browserLayoutManager_alert("ERR IS NAN");
		}
 		
	}
	//// browserLayoutManager_alert("ID JS SET '"+obj_id+"' TO "+w+","+h+" TARG:"+flashTarget);
	//// browserLayoutManager_alert("	CALC RIGHT EDGE:"+origRightX);	
//	browserLayoutManager_getObject("flashReq").value=flashTarget.style.width+","+flashTarget.style.height;			

}
//--------------------------------------------------------------------------------
function browserLayoutManager_Resize()
{

	if(browserLayoutManager_onResizeIntervalTimeout!=null){
		window.clearInterval(browserLayoutManager_onResizeIntervalTimeout);
	}
	browserLayoutManager_onResizeIntervalTimeout=
		window.setTimeout('browserLayoutManager_DoResize()',browserLayoutManager_onResizeIntervalTime);
		
	
}
//--------------------------------------------------------------------------------
function browserLayoutManager_DoResize()
{	
	// browserLayoutManager_alert("-----------------------browserLayoutManager_DoResize------------------------");
	//alert("browserLayoutManager_DoResize");
	var n;

		var w=browserLayoutManager_getBrowserWidth();
		var h=browserLayoutManager_getBrowserHeight();
		var wr=browserLayoutManager_getMaxWidth();
		var hr=browserLayoutManager_getMaxHeight();
		for(n=0;n<browserLayoutManager_FlashObjects.length;n++)
					{
						var flashTarget = browserLayoutManager_getObject(browserLayoutManager_FlashObjects[n]);
						if(flashTarget!=null){
							try{
								// browserLayoutManager_alert("send onBrowserResize "+flashTarget);
								// browserLayoutManager_alert("send onBrowserResize vars:"+w+","+h+","+wr+","+hr);

								flashTarget.onBrowserResize(w,h,wr,hr);
							}catch(err){
									// browserLayoutManager_alert("ERR onBrowserResize FAILED FOR:"+browserLayoutManager_FlashObjects[n]+" "+flashTarget);
									// browserLayoutManager_alert(err);
							}
							
						}
					}
		
		
		
		
	

}
function browserLayoutManager_GetDimension(){
	return 
}
//--------------------------------------------------------------------------------
function Flash_logIt(){
	// browserLayoutManager_alert(arguments[0]);
}

function  browserLayoutManager_alert(){
	

	
	if(!browserLayoutManager_isDebugging){
		return;
	}
	
	var dbug=browserLayoutManager_debugPanel;
	if(dbug==null || dbug==undefined){
		dbug=browserLayoutManager_getObject("debugpanel");
	
		if(dbug==null || dbug==undefined){
			if(document.forms.blmDebugForm['debugpanel']!=null){
				dbug=document.forms.blmDebugForm['debugpanel'];	
			}else if(browserLayoutManager_getObject("debugpanel")){
				dbug=browserLayoutManager_getObject("debugpanel");
			}
		}
	}
		
		
	
	if(dbug!=null){
		dbug.value+=(browserLayoutManager_loggingMsgCount++)+"> "+arguments[0]+"\n"; 		
	}else{
		alert("debugger not found");
	}

	//
}
//--------------------------------------------------------------------------------
function browserLayoutManager_addListener(a,b,c,d)
{
	//alert("browserLayoutManager_addListener:"+a+","+b+","+c+","+d);
	if(a.addEventListener)
	{

		// browserLayoutManager_alert(" browserLayoutManager_addListener TYPE 1");
		a.addEventListener(b,c,d);
		return true;
	}
	else if(a.attachEvent)
	{	

		// browserLayoutManager_alert(" browserLayoutManager_addListener TYPE 2");

		var e=a.attachEvent("on"+b,c);

		return e;
	}
	else
	{	

		// browserLayoutManager_alert("Handler could not be attached");
	}
}
//--------------------------------------------------------------------------------
function browserLayoutManager_getObject(movieName)
{
	var result;
	if (navigator.appName.indexOf("Microsoft") != -1) {
        result = window[movieName]
    }
    else {    
        result = document[movieName]
    }
	
    if(result==null){result=document.getElementById(movieName); }
    return result;

}
//--------------------------------------------------------------------------------
function browserLayoutManager_getIsDebugging()
{
	return browserLayoutManager_isDebugging;
}
//--------------------------------------------------------------------------------

function browserLayoutManager_convertPxToInt(px_str)
{
	if(px_str.indexOf("px")>0){
		return parseInt(px_str.slice(0,px_str.length-2));
	}else{
		return parseInt(px_str);
	}
}
//--------------------------------------------------------------------------------
function browserLayoutManager_onFocus(){
// browserLayoutManager_alert("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
	// browserLayoutManager_alert("FOCUS EVENT");
	browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])['onBrowserFocus']();
	// browserLayoutManager_alert("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
}
function browserLayoutManager_onBlur(){
// browserLayoutManager_alert("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
	// browserLayoutManager_alert("BLUR EVENT");
	//alert("BLUR OBJ:"+browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])+" FUNC "+browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])['onBrowserBlur']);
browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0])['onBrowserBlur']();
// browserLayoutManager_alert("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
}
//--------------------------------------------------------------------------------
function resizeSmartSearch(w,h){  
	//used by test app
	var flashTarget = document.getElementById("smartsearchcontainer");  
	alert("rss:"+flashTarget);
	flashTarget.style.width = (parseInt(w)+20) + "px"; 
	flashTarget.style.height = (parseInt(h)+50) + "px"; 
	// browserLayoutManager_alert("resizeSmartSearch: "+w+","+h);
} 
//--------------------------------------------------------------------------------
function connectiontest(){
		var flashTarget = browserLayoutManager_getObject(browserLayoutManager_FlashObjects[0]);
				// browserLayoutManager_alert("send onBrowserResize "+flashTarget);
				
				flashTarget.onBrowserResize(600,600,600,600);
}