/**
*	@author			Tor Kristensen	tor.kristensen@tietoenator.com
*	@version		1.2
*	@description	BrowserLayoutManager is the Actionscript parallel of the Javascript BrowserLayoutManager.js
*					It communicates and coordinates with the Javascript to allow the flash movie to dynamically change the size of its' host DIV, and resize from browser genereated events.
*	
*/

import flash.external.*;
import com.eea.utilities.logging.Logger;
import mx.events.UIEventDispatcher;

class com.eea.layout.BrowserLayoutManager extends Object
{
	
	//Placeholders for mixin functions from UIEventDispatcher
	public var addEventListener;
	//Placeholders for mixin functions from UIEventDispatcher
	public var removeEventListener;
	//Placeholders for mixin functions from UIEventDispatcher
	public var dispatchEvent;
	
	//The ID of the browser DOM object to control
	public var browserElementIDToControl:String;
	
	//Default ID of the browser DOM object to control
	public var defaultBrowserElementIDToControl:String="flashBLMClient";	
	
	//default height for stage	
	public var defaultLayoutHeight:Number=400;
	//default width for stage
	public var defaultLayoutWidth:Number=400;
	
	//stores current browser width
	public var browserWidth:Number;
	//stores current browser height
	public var browserHeight:Number;
	//stores current free width (browserWidth - left)
	public var browserAvailableWidth:Number;
	//stores current free width (browserHeight - top)
	public var browserAvailableHeight:Number;
	//stores width the flash has _requested_ from the browser
	public var browserRequestedWidth:Number;
	//stores height the flash has _requested_ from the browser
	public var browserRequestedHeight:Number;
	
	//Static var that holds the name of an Event type
	static var EVENT_STAGE_RESIZE:String="onStageResize";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_RESIZE:String="onBrowserLayoutManagerResize";
	
	//Static var that holds the name of an Event type
	static var EVENT_BROWSER_RESIZE:String="onBrowserResize";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_GET_MAXHEIGHT:String="browserLayoutManager_getMaxHeight";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_GET_MAXWIDTH:String="browserLayoutManager_getMaxWidth";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_GET_BROWSER_DIM:String="browserLayoutManager_getBrowserDim";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_GET_CONTROLLABLE_DIVS:String="browserLayoutManager_GetControllableDivs";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_ALERT:String="browserLayoutManager_alert";
	
	//Static var that holds the name of an Event type
	static var EVENT_BLM_IS_DEBUGGING:String="browserLayoutManager_getIsDebugging";
	
	//---------------------------------------------------------------
	/**
	*	@description	Constructor for the BrowserLayoutManager instance
	*	@param browserElementIDToControl_str	The ID of the Browser DOM object to control
	*	@return	A new BrowserLayoutManager instance
	*/
	function BrowserLayoutManager(browserElementIDToControl_str:String)
	{
		
		//Stage.align = "LT";
		Stage.scaleMode = "noScale";
		Stage.addListener(this);		
		
		UIEventDispatcher.initialize(this);
		ExternalInterface.addCallback("onBrowserBlur", this, onBrowserBlur);
		ExternalInterface.addCallback("onBrowserFocus", this, onBrowserFocus);
		ExternalInterface.addCallback("onBrowserResize", this, onBrowserResize);
		ExternalInterface.addCallback("onBLMResize", this, onBLMResize);
		ExternalInterface.addCallback("setBrowserLayoutManagerID", this, onSetBrowserLayoutManagerID);
		
		if(browserElementIDToControl_str!=undefined)
		{
			onSetBrowserLayoutManagerID(browserElementIDToControl_str);
		}
		
		var dim:Object=getBrowserDim();
		browserWidth=dim.width;
		browserHeight=dim.height;
		browserAvailableWidth=dim.widthMax;
		browserAvailableHeight=dim.heightMax;
		
		Logger.logIt("BLM INITS TO:"+browserWidth+","+browserHeight+", max:"+browserAvailableWidth+","+browserAvailableHeight)
	}
	//---------------------------------------------------------------
	/**
	*	@description	Event that is fired when the browser sets a new DOM ID to control
	*	@param id the DOM ID to control
	*	@return	Void
	*/
	function onSetBrowserLayoutManagerID(id:String):Void
	{
		if(id!=undefined)
		{
			browserElementIDToControl=id;
		}else{
			browserElementIDToControl=defaultBrowserElementIDToControl;
		}
	}
	//---------------------------------------------------------------
	/**
	*	@description	Fired on browser resize, broadcasts an "onStageResize" event
	*	@return	Void
	*/
	function onResize():Void
	{
		Stage.align="TL";
		dispatchEvent({type:EVENT_STAGE_RESIZE,width:Stage.width,height:Stage.height});
	}
	//---------------------------------------------------------------
	/**
	*	@description	Fired by the Javascript BrowserLayoutManager after a browser onResize event
	*	@return	Void
	*/
	function onBLMResize():Void
	{
		dispatchEvent({type:EVENT_BLM_RESIZE,width:Stage.width,height:Stage.height});
	}
	
	
	function onBrowserBlur():Void{
		dispatchEvent({type:"onBrowserBlur"});
	}
	
	function onBrowserFocus():Void{
		dispatchEvent({type:"onBrowserFocus"});
	}
	
	//---------------------------------------------------------------
	/**
	*	@description	onBrowserResize is called by the Javascript BrowserLayoutManager
	*	@param w	The width of the browser window
	*	@param h	The height of the browser window
	*	@param w_max	The maximum width of the browser window	
	*	@param h_max	The maximum height of the browser window	
	*	@return	Void
	*/
	function onBrowserResize(w:Number,h:Number,w_max:Number,h_max:Number):Void
	{
		
			Logger.logIt("FLASH GOT onBrowserResize "+arguments);
		browserWidth=w;
		browserHeight=h;
		browserAvailableWidth=w_max;
		browserAvailableHeight=h_max;
		
		if(w==browserRequestedWidth && h==browserRequestedHeight){
			Logger.logIt("BROWSER SET SIZE OK");
			return;
		}
		
		dispatchEvent({type:EVENT_BROWSER_RESIZE,data:
		{browserWidth:w,
		browserHeight:browserHeight,
		browserAvailableWidth:browserAvailableWidth,
		browserAvailableHeight:browserAvailableHeight}
		});
	}	
	//---------------------------------------------------------------
	/**
	*	@description	onSetStageSize is called by objects that wish to set a new Stage size
	*	@param e	An event object, with the properties width and height, ex: {width:400,height:800}
	*	@return	Void
	*/
	function onSetStageSize(e:Object):Void
	{
		setStageSize(e.width,e.height);
	}
	//---------------------------------------------------------------
	/**
	*	@description	setStageSize is called by onSetStageSize
	*	@param w	The new Stage width
	*	@param h	The new Stage height
	*	@return	Void
	*/
	function setStageSize(w:Number,h:Number):Void
	{
		if(w==undefined || h==undefined){
			Logger.logIt("AS BLM setStageSize ERROR"+" w:"+w+" h:"+h+" for:"+browserElementIDToControl);
			return;
		}else{
			Logger.logIt("AS BLM setStageSize"+" w:"+w+" h:"+h+" for:"+browserElementIDToControl);
		}
		browserRequestedWidth=w;
		browserRequestedHeight=h;
		
		if(browserElementIDToControl!=undefined)
		{
			Logger.logIt("setStageSize C1"+" w:"+w+" h:"+h);
			ExternalInterface.call(
				"browserLayoutManager_ResizeID",
				browserElementIDToControl,
				w,
				h
			);			
		}else{
			Logger.logIt("setStageSize C2"+" w:"+w+" h:"+h);
			ExternalInterface.call(
				"browserLayoutManager_ResizeDefaultID", 
				w,
				h				
			);	
		}
		
	}
	//---------------------------------------------------------------
	/**
	*	@description	Returns the document height minus the flash controls' y position
	*	@return	Number
	*/
	public function getAvailableHeight():Number
	{
		/*
		* Returns the document height minus the flash controls' y position
		* */
		var h:Number=Number(ExternalInterface.call(EVENT_BLM_GET_MAXHEIGHT));		
		if(isNaN(h)){h=defaultLayoutHeight;Logger.logIt("AS BLM ERR:NO REPLY FROM JS ON "+EVENT_BLM_GET_MAXHEIGHT);}		
		return h;
	}
	//---------------------------------------------------------------
	/**
	*	@description	Returns the document width minus the flash controls' x position
	*	@return	Number
	*/
	public function getAvailableWidth():Number
	{
		/*
		* Returns the document width minus the flash controls' x position
		* */
		var w:Number=Number(ExternalInterface.call(EVENT_BLM_GET_MAXWIDTH));		
		if(isNaN(w)){w=defaultLayoutWidth;}		
		return w;
	}
	//---------------------------------------------------------------
	/**
	*	@description	Returns an object width width and height properties that reflect the current browser size
	*	@return	Object
	*/
	public function getBrowserDim():Object
	{
		/*
		* Returns the document dimension as an object of the form {width:Number,height:Number}
		* */
		var dim:Object=Object(ExternalInterface.call(EVENT_BLM_GET_BROWSER_DIM));				
		if(dim.width==undefined){dim={width:defaultLayoutWidth,height:defaultLayoutHeight};}
		return dim;
	}
	//---------------------------------------------------------------
	/**
	*	@description	returns a list of browser objects that are registered fpr control by the BrowserLayoutManager
	*	@return	Array
	*/
	public function getControllableObjects():Array
	{
		return Array(ExternalInterface.call(EVENT_BLM_GET_CONTROLLABLE_DIVS));
	}
	//---------------------------------------------------------------
	/**
	*	@description	Calls the javascript function browserLayoutManager_alert() to alert or trace the str passed
	*	@param str	The message
	*	@return	Void
	*/
	public function doAlert(str:String):Void
	{
		trace("				alert-blm:"+str);
		ExternalInterface.call(EVENT_BLM_ALERT, str);
	}
	//---------------------------------------------------------------
	/**
	*	@description	Returns a boolean defining whether debugging is on
	*	@return	Boolean
	*/
	public function get isDebugging():Boolean{
		var result:Boolean=Boolean(ExternalInterface.call(EVENT_BLM_IS_DEBUGGING));
		if(result==undefined){result=false;}
		return 
	}
}