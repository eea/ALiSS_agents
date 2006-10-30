	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	SmartSearchView is the primary visual UI element for the SmartSearch UI.
				It contains the results, related items, etc.
				It is also responsible for a large amount of layout control.
*/
	
import flash.filters.DropShadowFilter;
import flash.external.*;

import com.eea.utilities.logging.Logger;

import mx.core.UIComponent ;

import mx.utils.Delegate;


import mx.controls.TextInput;
import mx.controls.Button;
import mx.controls.List;
import mx.containers.ScrollPane;

import com.eea.controls.BusyGradient;
import com.eea.projects.aliss.views.RelatedItemList;
import com.eea.projects.aliss.views.DefinitionView ;
import com.eea.projects.aliss.views.RelatedResultsView;
import com.eea.projects.aliss.views.Message;
import com.eea.projects.aliss.events.AlissEvents;
import com.eea.projects.aliss.application.AlissApplication;

class com.eea.projects.aliss.views.SmartSearchView
extends mx.core.View {

	private var _VERSION						:String = "1.0.2";
	private var _PRODUCT						:String = "SmartSearchView";
	
	private var __state							:Number=-1;
	private var __oldState						:Number=-1;
	
	//	The width set by the PREVIOUS size() call
	private var oldWidth						:Number;
	
	//	The height set by the PREVIOUS size() call
	private var oldHeight						:Number;
	
	//	Pointer to the controller
	public var controller						:Object;
	
	//	The List control to display results in 
	public var results_ls						:List;
	
	//	The TextInput for entering search terms
	public var searchterms_ti					:TextInput;
	
	//	The default width of the search interface
	public var searchInterfaceWidth				:Number=400;
	
	/*
	* @see com.eea.projects.aliss.views.RelatedResultsView
	* @description instance of the RelatedResultsView
	*/
	public var relatedResults_rrv				:RelatedResultsView;
	
	/*
	* @see com.eea.projects.aliss.views.RelatedItemList
	* @description instance of the RelatedItemList
	*/
	public var relatedItemListView_ril			:RelatedItemList;
	
	/*
	* @see com.eea.controls.BusyGradient
	* @description Control that shows when waiting for service response
	*/
	public var busy_mc							:BusyGradient;
	
	/*
	* @see com.eea.projects.aliss.views.Message
	* @description instance of the Message control
	*/	
	public var message_msg						:Message;
	
	//	default layout height
	public var defaultLayoutHeight				:Number=400;
	
	//	default layout width
	public var defaultLayoutWidth				:Number=400;
	
	//	default layout width without scrollbars
	public var defaultLayoutWidth_NoScrollBars	:Number=312;
	
	//	holds the current search term
	public var currentSearchTerm_str			:String;
	
	/*
	*	@description	holds the current term that was passed to callGetTopPagesForTerms
	*	see com.eea.projects.aliss.datatypes.TopPagesResults#callGetTopPagesForTerms
	*/
	public var currentRelatedTopicsTerm_str		:String;
	
	//	id of the current Interval
	private var intervalID						:Number;
	// is interval Active?
	private var intervalActive					:Boolean=false;
	
	public var userTimeoutDuration				:Number;
	public var userTimeoutIntervalID			:Number;
	private var userGoogledText_str				:String;
	
	// A simple Object that stores the Dim passed from the Javascript BrowserLayoutManager	
	public var browserDim								:Object;
	
	// default interval tim ein milliseconds
	static var INTERVAL_TIME					:Number=200;
	
	// Static Number for application state of : NORESULTS
	static var STATE_TERM_NORESULTS				:Number=-2;
	
	// Static Number for application state of : STARTUP
	static var STATE_STARTUP					:Number=-1;
	
	// Static Number for application state of : INITING
	static var STATE_INITING					:Number=0;
	
	// Static Number for application state of : READY
	static var STATE_READY						:Number=1;
	
	// Static Number for application state of : SHOW_TERMS	
	static var STATE_SHOW_TERMS					:Number=2;
	
	// Static Number for application state of : RELATED
	static var STATE_SHOW_RELATED				:Number=3;
	
	private var browserBlurEventID				:Number;
    private var browserFocusEventID				:Number;
    private var browserBlurFocusDelayTime		:Number=100;
    //when getting a stream of blur/focus events, we keep the last on here (blur=0,focus=1) 
    private var browserLastBlurFocusEvent		:Number=1; 
	//------------------------------------------------------------------------------
	/*
	*	@description	Constructor for the SmartSearchView control
	*	@return	A new SmartSearchView instance
	*/
	function SmartSearchView()
	{
		super();
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Simple wrapper for superclass init() method
	*	@return	Void
	*/
	function init():Void
	{
		super.init();
		this.setStyle("styleName","Application");
		userTimeoutDuration=Number(getStyle("userTimeoutDuration"));
		if(isNaN(userTimeoutDuration)){userTimeoutDuration=8000;}
		trace("userTimeoutDuration:"+userTimeoutDuration+" "+getStyle("userTimeoutDuration"));
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Simple wrapper for superclass size() method
	*	@return	Void
	*/
	function size():Void
	{
		super.size();
	}
	/*
	*	@description	Fires the measureRequiredSize() method
	*	@see #measureRequiredSize
	*	@return	Void
	*/
	function doLayout():Void
	{
		//trace("%%%% DOLAYOUT");
		measureRequiredSize();
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Based on current and previous states, decides what to draw() and what to hide.
	*	@return	Void
	*/
	function draw():Void
	{
		//trace("$$$$$$$$$$$$$$$$$$$$$$$$$$ DRAW S");
		super.draw();
		if(__state!=STATE_TERM_NORESULTS){hideMessage();}
		
		var needToLayout:Boolean=false;
		switch(true)
		{
			case (__oldState==STATE_STARTUP && __state==STATE_INITING):
				busy_mc._visible=false;
				results_ls._visible=relatedResults_rrv._visible=false;
				
				needToLayout=true;
				break;
				
			case (__oldState==STATE_INITING && __state==STATE_READY):
				busy_mc._visible=false;
				results_ls._visible=relatedResults_rrv._visible=false;
				needToLayout=true;
				break;
				
			case (__oldState==STATE_READY && __state==STATE_SHOW_TERMS):
				results_ls._visible=true;
				// busy_mc._visible=false;
				relatedResults_rrv._visible=false;
				needToLayout=true;
				//broadcastSize();
				break;
				
			case (__oldState==STATE_SHOW_TERMS && __state==STATE_SHOW_RELATED):
				busy_mc._visible=false;
				results_ls._visible=false;
				relatedResults_rrv._visible=true;
				relatedResults_rrv.relatedResults_ls.setFocus();
				//relatedResults_rrv.relatedResults_ls.selectedIndex=0;
				needToLayout=true;
				//broadcastSize();
				break;
				
			case (__oldState==STATE_SHOW_RELATED && __state==STATE_SHOW_TERMS):
				results_ls._visible=true;
				busy_mc._visible=false;
				relatedResults_rrv._visible=false;
				needToLayout=true;
				//broadcastSize();
				break;
				
			case (__state==STATE_READY):
				busy_mc._visible=false;
				results_ls._visible=relatedResults_rrv._visible=false;
				needToLayout=true;
				break;
				
			case (__state==STATE_TERM_NORESULTS):
				busy_mc._visible=false;
				results_ls._visible=relatedResults_rrv._visible=false;
				var theMessage:String=String(
					AlissApplication.getConfig("no_suggestions_txt")
				);
				var theButtonLabel:String=String(
					AlissApplication.getConfig("search_fail_button_txt")
				);
				showMessage(theMessage,theButtonLabel);
				break;
				
			default:
				//trace("STATE: OLD:"+__oldState+" NEW:"+__state+" IS UNHANDLED");
				break;
		}
		
		if(needToLayout){
			//doLater(this,"measureRequiredSize");
			Logger.logIt("DRAW CALLS measureRequiredSize");
			measureRequiredSize();
			
		}
		
		_x=0;
		
		hasBeenLayedOut = true;
		
		/*
		* @ERROR LAYOUT CALLS ARE CAUSING A DRAW-MEASURE-SIZE LOOP
		* FIND A FIX ASAP
		* */
		//trace("$$$$$$$$$$$$$$$$$$$$$$$$$$ DRAW E");
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Creates all child objects
	*	@return	Void
	*/
	function createChildren():Void
	{
		_visible=false;
		super.createChildren();
		trace("createChildren");
		
		var results_cfg:Object={_y:30,_visible:false};
		
		if(AlissApplication.getConfig("enable_suggest_icons")=="true"){
			results_cfg.cellRenderer="ImageLeftMultiLineTextCell";
		}else{
			results_cfg.cellRenderer="CellRendererWithLableAndClickEventsClip";
		}

		
		
		results_ls=List(
				this.createChild(List, "results_ls", results_cfg)
			);
		
		
		relatedResults_rrv=RelatedResultsView(
				this.createChild(
					RelatedResultsView, "relatedResults_rrv", 
					{controller:this,_y:30,_visible:false}
					)
			);
		
		busy_mc=BusyGradient(
				this.createChild(
					BusyGradient, "busy_mc", 
					{_y:searchterms_ti._y+searchterms_ti._height,_visible:true}
					)
			);
		
		createFilters();
		
		searchterms_ti.setStyle("styleName","SearchBox");
		results_ls.setStyle("styleName","List");
		searchterms_ti.setFocus();
		
		doLater(this,"setupListeners");
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Creates the DropShadowFilter and assigns it.
	*	@return	Void
	*/
	function createFilters():Void
	{
		var filter:DropShadowFilter =  makeStyledDropShadow(5, 
											45, 
											0x000000, 
											.30, 
											2, 
											2, 
											1, 
											3, 
											false, 
											false, 
											false);

		relatedResults_rrv.filters=[filter];
		results_ls.filters=[filter];
		
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Creates Listeners for child communication
	*	@return	Void
	*/
	function setupListeners():Void
	{
		trace("setupListeners");
		Stage.addListener(this);
		
		//listen to the rrv
		relatedResults_rrv.addEventListener(AlissEvents.EVENT_RELATEDITEM_SELECTION, this);
		relatedResults_rrv.addEventListener(AlissEvents.EVENT_DEFINTION_SELECTION, this);
		relatedResults_rrv.addEventListener(AlissEvents.EVENT_SEEALLRESULTS_SELECTION, this);
		
		//rrv listen to data source
		controller.addEventListener(
			AlissEvents.EVENT_SERVICE_GET_TOP_PAGES_RESULT,
			relatedResults_rrv);
		
		//listen to my controls
		searchterms_ti.addEventListener("change",this);
		searchterms_ti.addEventListener("keyUp",this);
		results_ls.addEventListener("change",this);
		results_ls.addEventListener("click",this);
		
		
		Key.addListener(this);
		Mouse.addListener(this);
		
		//configure from AlissApplication
				
		
		
		
		//runBLMTests();
		
		doLater(this,'doAfterSetup');
		state=STATE_READY;
	}
	
	/*
	*	@description	Hides this control after it is inited
	*	@return	Void
	*/
	private function doAfterSetup():Void
	{
		_visible=true;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Runs a seris of test for communication with the Javascript version of the BrowserLayoutManager
	*	@see	com.eea.layout.BrowserLayoutManager
	*	@return	Void
	*/	
	private function runBLMTests():Void
	{
		return;
		var dim:Object=ExternalInterface.call("browserLayoutManager_getBrowserDim");
		var str:String="";
		for(var s:String in dim){str+=s+"="+dim[s]+"  ";}

		var objs:Object=(ExternalInterface.call("browserLayoutManager_GetControllableObjects"));
		str="Controllable: len:"+objs.length+" ";

		for(var n:Number=0;n<objs.length;n++){str+=s+"="+objs[n]+"  ";}
		ExternalInterface.call("browserLayoutManager_alert",str);

	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Sets the controller object and assigns listeners
	*	@see	com.eea.projects.aliss.events.AlissEvents
	*	@return	Void
	*/	
	function setController(o:Object):Void	
	{
		controller=o;
		trace("setController"+arguments);
		//set up event listening here
		var events_in:Array=[
			AlissEvents.EVENT_SERVICE_GET_TERMS_RESULT,
			AlissEvents.EVENT_SERVICE_GET_TOP_PAGES_RESULT,
			AlissEvents.EVENT_SERVICE_BUSY,
			AlissEvents.EVENT_SERVICE_GET_TERMS_TIMEOUT
		];
		
		var events_out:Array=[
			AlissEvents.EVENT_SERVICE_GET_TOP_PAGES,
			AlissEvents.EVENT_SERVICE_GET_TERMS		
		];
		
		for(var n:Number=0;n<events_in.length;n++)
		{
			controller.addEventListener(events_in[n],this);	
		}
		
		for(var n:Number=0;n<events_out.length;n++)
		{
			this.addEventListener(events_out[n],controller);	
		}
		
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Called when the user has not moved mouse or pressed a key in a period longer than that defined in the CSS Application.userTimeoutDuration. If no value is defined in the CSS it defaults to 8000msecs.
	*	@return	Void
	*/	
	function onUserTimeout():Void
	{
	
		if(state!=STATE_READY){state=STATE_READY;searchterms_ti.text="";}

	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Shows the Related Item view
	*	@return	Void
	*/	
	function onRelatedItemsShow():Void
	{
		searchTipsHide();

	}
	/*
	*	@description	Hides the Related Item view
	*	@return	Void
	*/	
	function onRelatedItemsHide():Void
	{
		searchTipsShow();
		relatedResults_rrv._visible=false;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Forwards the web browser to the Concept page for a specified Term
	*	@return	Void
	*/	
	function seeAllResultsSelection(e:Object):Void
	{
		getURL(results_ls.selectedItem.concept_url);		
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Called when a RelatedItem is selected
	*	@return	Void
	*/		
	function relatedItemSelection(e:Object):Void
	{
		state=STATE_READY;
		getURL(e.item.url);
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Called when we get a result from {@link com.eea.projects.aliss.smartsearch.AlissClient#callGetTermSuggestions}
	*	@return	Void
	*/	
	function smartSearch_GetTermSuggestionsResult(e:Object):Void
	{		
		//trace("smartSearch_GetTermSuggestionsResult GOT:::::"+e.data+" "+e.data.length);
		if(e.data.length==0 || e.isEmptyResult)
		{
			//trace("DISPLAY ERR MSG");
			
			
			searchTipsHide();
			state=STATE_TERM_NORESULTS;
			
			//
		}else{
			message_msg._visible=false;
			results_ls.dataProvider=e.data;	
			
			state=STATE_SHOW_TERMS;
		}
		
		invalidate();
		
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Called when we get a result from {@link com.eea.projects.aliss.smartsearch.AlissClient#callGetTopPagesForTerms}
	*	@return	Void
	*/	
	function smartSearch_GetTopPagesForTermsResult(e:Object):Void
	{
		relatedResults_rrv.invalidate();
		state=STATE_SHOW_RELATED;
	}
	
	/*
	*	@description	Called when we get a TIMEOUT from {@link com.eea.projects.aliss.smartsearch.AlissClient#callGetTermSuggestions}
	*	@return	Void
	*/	
	function smartSearch_GetTermSuggestionsResult_Timeout(e:Object):Void
	{
				Logger.logIt("SS GOT TIMEOUT");
	}
	
	/*
	*	@description	Called when we get a TIMEOUT from {@link com.eea.projects.aliss.smartsearch.AlissClient#callGetTopPagesForTerms}
	*	@return	Void
	*/	
	function smartSearch_GetTopPagesForTermsResult_Timeout(e:Object):Void
	{
				Logger.logIt("SS GOT TIMEOUT");
				state=STATE_READY;
	}
	//------------------------------------------------------------------------------	
	/*
	*	@description	Called when the AlissClient is busy
	*	@return	Void
	*/	
	function smartSearch_Busy(e:Object):Void
	{
		results_ls.dataProvider=[{label:AlissApplication.getConfig("on_search_txt")}];
		busy_mc._visible=true;
		Logger.logIt('******* BUSY');
	}
	/*
	*	@description	Called when the AlissClient returns an empty result
	*	@return	Void
	*/	
	function smartSearch_TermNoResults(e:Object):Void
	{
		results_ls.dataProvider=[{label:AlissApplication.getConfig("no_suggestions_txt")}];
		busy_mc._visible=false;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Broadcasts an event that fires the AlissClient.callGetTermSuggestions() method
	*	@return	Void
	*/	
	function doPost():Void
	{		
		searchTipsShow();
		
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TERMS,data:searchterms_ti.text});
		dispatchEvent({type:AlissEvents.EVENT_SEARCHTERM_CHANGE,term:searchterms_ti.text});
		
		currentSearchTerm_str=results_ls.selectedItem.label;
		//controller.callGetTermSuggestions(searchterms_ti.text);
		intervalActive=false;
		clearInterval(intervalID);
	}
	/*
	*	@description	Returns a typed (RelatedResultsView) relatedResults_rrv
	*	@return	RelatedResultsView
	*/
	function getRelatedItemResultView():RelatedResultsView
	{
		return RelatedResultsView(relatedResults_rrv);
	}
	
	/*
	*	@description	Fires when a term is selected in the UI
	*	@return	RelatedResultsView
	*/	
	function onTermSelected():Void
	{
		if(AlissApplication.getConfig("enable_related_results")=="true"){
			if(results_ls.selectedItem.label!=undefined){
				dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TOP_PAGES,
					data:results_ls.selectedItem.label});
			}
		}else{
			getURL(results_ls.selectedItem.url);
		}
	}
	
	//------------------------------------------------------------------------------
	// UI SHOW/HIDE METHODS
	//------------------------------------------------------------------------------
	/*
	*	@description	Shows search tips
	*	@return	Void
	*/
	function searchTipsShow():Void
	{
		//trace("searchTipsShow");
		state=STATE_SHOW_TERMS;
		//invalidate();
		
	}
	
	/*
	*	@description	Hides search tips
	*	@return	Void
	*/
	function searchTipsHide():Void
	{
		state=STATE_SHOW_RELATED;
		//invalidate();
	}
	//------------------------------------------------------------------------------
	
	
	/**
	 * @description Rests the interval for user timeout after keypress or mousemove.
	 * @return Void	 */
	private function resetUserTimeout():Void
	{	
		clearInterval(userTimeoutIntervalID);
		userTimeoutIntervalID=setInterval(this,"onUserTimeout",userTimeoutDuration);
	}
	
	
	//------------------------------------------------------------------------------
	// UI EVENTS
	//------------------------------------------------------------------------------
	/*
	*	@description	The onMouseMove method
	*	@return	Void
	*/
	public function onMouseMove():Void
	{
		resetUserTimeout();
	}
	
	/*
	*	@description	The onKeyUp method
	*	@return	Void
	*/
	public function onKeyUp():Void
	{
		resetUserTimeout();	
		keyUp({code:Key.getCode()});
	}
	/*
	*	@description	logic called by onKeyUp
	*	@return	Void
	*/
	function keyUp(e:Object):Void
	{
		//trace("KEYUP"+(e.code==Key.ENTER) +" "+( e.code==Key.SPACE));
		
		if(AlissApplication.application.state==AlissApplication.STATE_READY){
		
			var curfocus=getFocus();
				
			if( curfocus==searchterms_ti.label && e.code==Key.ENTER && searchterms_ti.text!=userGoogledText_str){
				//CALL GOOGLE
				userGoogledText_str=searchterms_ti.text;
				dispatchEvent({type:'onCallGoogle',data:searchterms_ti.text});
				return;
			}else if(__state==STATE_SHOW_TERMS){
				
				if( curfocus!=results_ls){
					//move focus from the text input to dd
					if(e.code==Key.DOWN){
						results_ls.setFocus();
						results_ls.selectedIndex=0;
					}
					
				}else if(curfocus==results_ls){
					//focus is dd, look for enter/space event
					
					if(e.code==Key.ENTER || e.code==Key.SPACE){
						onTermSelected();				
					}
				}
			}else if(__state==STATE_SHOW_RELATED){				
				relatedResults_rrv.hidePreview();
				 if( curfocus!=relatedResults_rrv.relatedResults_ls){
					if(e.code==Key.DOWN){
						
						relatedResults_rrv.relatedResults_ls.setFocus();
						relatedResults_rrv.relatedResults_ls.selectedIndex=0;
					}
				}
			}
			
			
		}
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Event handler called by completion of loading
	*	@param	e A standard Event object
	*	@return	Void
	*/	
	function complete(e:Object):Void
	{
		//trace("GOT COMPLETE");
	}
	
	/*
	*	@description	Event handler called by change of state in a component
	*	@param	e A standard Event object
	*	@return	Void
	*/
	function change(e:Object):Void
	{
		//trace("GOT CHANGE:"+e.target);
		for(var s:String in e){trace("	change."+s+"="+e[s]);}
		//for(var s:String in e.target){trace("		change.target."+s+"="+e.target[s]);}
		switch(e.target){
			
			case searchterms_ti:
			
				if(searchterms_ti.text.length<3)
				{
					state=STATE_READY;
					return;
				}
				resetInterval();
				break;
				
			case results_ls:			
				
				currentRelatedTopicsTerm_str=results_ls.selectedItem.label;
				break;
				
			default:
				break;
		}
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Event handler called by a click in a component
	*	@param	e A standard Event object
	*	@return	Void
	*/
	function click(e:Object):Void
	{
		if(e.target==results_ls){
				onTermSelected();
		}else if(e.target=message_msg){
			dispatchEvent({type:"onCallGoogle",data:searchterm});
		}
	}
	//------------------------------------------------------------------------------		
	/*
	*	@description	Resets the interval, wait another cycle to see if the user is done typing
	*	@param	m the method name to call on interval. Default is "doPost".
	*	@return	Void
	*/
	function resetInterval(m:String):Void
	{
		if(intervalActive)
		{
			clearInterval(intervalID);
		}
		if(m==undefined){m="doPost";}
		intervalID=setInterval(this,m,INTERVAL_TIME);
		
		intervalActive=true;
	}	
	//------------------------------------------------------------------------------
	/*
	*	@description	Does the majority of UI layout for the application
	*	@return	Void
	*/
	function measureRequiredSize():Void
	{
		Logger.logIt("------------------Flash Layout Start------------------");	
		var bW=browserDim.browserAvailableWidth;
		
		var h:Number;
		var w:Number;
		
		Logger.logIt("browserDim.browserAvailableWidth="+browserDim.browserAvailableWidth);
		if(bW==undefined){bW=Stage.width;Logger.logIt("	default to Stage.width:"+Stage.width);}
		
		var bH=browserDim.browserAvailableHeight;
		if(bH==undefined || isNaN(bH) ){bH=Stage.height;}
		
		Logger.logIt("SSV ORIG BROWSER DIM:"+browserDim.browserWidth+","+browserDim.browserHeight);	
		for(var s:String in browserDim){
			Logger.logIt("		browserDim."+s+"="+browserDim[s]);
		}
		bW-=15;
		bH-=15;
		var baseH:Number=bH-40;
		var totHUsed=0;
		
		w=defaultLayoutWidth;//bW;//defaultLayoutWidth;
		
		if(relatedResults_rrv._visible)
		{
			totHUsed=relatedResults_rrv._y+relatedResults_rrv.height;
		}
		else if(results_ls._visible)
		{		
			
			totHUsed=Math.max(totHUsed,results_ls._y+results_ls.height);
			
		}else if(!results_ls._visible && !relatedResults_rrv._visible){
			
			w=searchterms_ti._x+searchterms_ti.width;
		
		}
		
		var hBounds=this.getBounds(_root);
		totHUsed=hBounds.yMax-hBounds.yMin;
		
		h=Math.max(400,Math.min(totHUsed,Math.max(22,baseH)));
		
		if(w==oldWidth || h==oldHeight){ Logger.logIt("NO NEED TO RESIZE");return;}
		
		searchInterfaceWidth=w;
		
		
			Logger.logIt("SSV BROWSER DIM:"+bW+","+bH);	
			Logger.logIt("SSV REQUIRES DIM:"+w+","+h);	
			Logger.logIt("                totHUsed:"+totHUsed+", baseH:"+baseH);	
			
		
		
			if(!isNaN(w) && !isNaN(h)){
				
				var termsH:Number=((results_ls.dataProvider.length+1)*results_ls.rowHeight);
				//trace("terms want:"+termsH);
				termsH=Math.min(Math.max(termsH,50),bH-results_ls._y);
				//trace("TARGET HEIGHT FOR FLASH:"+termsH);
				
				var dropShadowOffset:Number=Number(getPriorityValue("dropShadowDistance",5));

				var busyH:Number=Number(busy_mc.getStyle("busyHeight"));
				busy_mc.setSize(searchterms_ti.width, busyH);
				busy_mc.move(searchterms_ti.x, searchterms_ti.y+searchterms_ti.height+busy_mc.padding+1);

				results_ls.move(results_ls.x,busy_mc.y+busyH+busy_mc.padding);
				results_ls.setSize(Stage.width-dropShadowOffset,termsH);				
				results_ls.size();results_ls.draw();
		
				var rrvHeight:Number=Math.min(bH-relatedResults_rrv._y-10,
				Stage.height-relatedResults_rrv._y-searchterms_ti._height-10);
				rrvHeight=Math.max(rrvHeight,400);
		
				Logger.logIt("			SET RRV HEIGHT TO:"+rrvHeight);
		
				relatedResults_rrv.setSize(
				Stage.width-dropShadowOffset,
				rrvHeight);
				
				relatedResults_rrv.size();
				relatedResults_rrv.draw();
				//broadcastSize();
				
				doLater(this,"broadcastSize");
			}else{
				Logger.logIt("SSV NO NEED TO RESIZE DIM:"+w+","+h+" vs old:"+oldWidth+","+oldHeight);	
			}
			
			
			searchterms_ti.setSize(
				Math.min( searchInterfaceWidth, 
				Number(_global.styles.SearchBox.widthMax) ),
				searchterms_ti.height
				);	
				
				
				
			
			
			
			
			
			//_x=Stage.width-w;
			
			//_root.yline._x=Stage.width-1;
			//doLater(this,"broadcastSize");
			//broadcastSize();
		//}
	}
	//------------------------------------------------------------------------------	
	/*
	*	@description	broadcasts the required size to the Javascript BrowserLayoutManager
	*	@return	Void
	*/
	function broadcastSize():Void
	{
		var CSSDims:Object={
			min:{
				width:Number(getStyle("minimizedWidth")),
				height:Number(getStyle("minimizedHeight")),
				isHeightAuto:getStyle("minimizedHeight")=='auto'
			},
			max:{
				width:Number(getStyle("expandedWidth")),
				height:Number(getStyle("expandedHeight")),
				isHeightAuto:getStyle("expandedHeight")=='auto'
			}
			
		};
		
		
		var h:Number=CSSDims.min.height;
		var w:Number=CSSDims.min.width;
		var bounds:Object;
		
		var maxH:Number;
		if(CSSDims.max.isHeightAuto){
			maxH=getMaxLayoutHeightFromBrowser();
		}else{
			maxH=Math.min( CSSDims.max.height, getMaxLayoutHeightFromBrowser() );
		}
	
		
		Logger.logIt("	getMaxLayoutHeightFromBrowser()="+maxH);
		Logger.logIt("	__state:"+__state+" STATE_SHOW_TERMS:"+STATE_SHOW_TERMS+" STATE_SHOW_RELATED:"+STATE_SHOW_RELATED+
		" STATE_TERM_NORESULTS:"+STATE_TERM_NORESULTS);
		Logger.logIt("	starting H:"+h);
		bounds=this.getBounds(_root);		
		
		if(__state==STATE_SHOW_TERMS){
			Logger.logIt(" bsSize - STATE_SHOW_TERMS");
			bounds=this.getBounds(_root);
			
			if(CSSDims.max.width=='auto' || isNaN(Number(CSSDims.max.width))){		
				//h+=10 + results_ls._y + (( results_ls.dataProvider.length+1) * results_ls.rowHeight);
				h=CSSDims.max.height;
			}else{
				w=Number(CSSDims.max.width);
			}
			
			if(CSSDims.max.isHeightAuto ){		
				h+=10 + results_ls._y + (( results_ls.dataProvider.length+1) * results_ls.rowHeight);
				Logger.logIt(" 		HEIGHT=AUTO="+h);
			}else{
				h=Number(CSSDims.max.height);
				Logger.logIt(" 		HEIGHT=CSS="+h+" from "+CSSDims.max.height);
			}
			
		}else if(__state==STATE_SHOW_RELATED){	
			Logger.logIt(" bsSize - STATE_SHOW_RELATED");
				bounds=relatedResults_rrv.border_mc.getBounds(_root);				
				h=relatedResults_rrv.getLayoutHeight();//bounds.yMax+relatedResults_rrv._y+100;
				Logger.logIt(" RRV BOUNDS H="+h);
				
					if(CSSDims.max.width=='auto' || isNaN(Number(CSSDims.max.width))){		
						//
					}else{
						w=Number(CSSDims.max.width);
					}
					
					if(CSSDims.max.isHeightAuto){		
						h+=10 + results_ls._y + (( results_ls.dataProvider.length+1) * results_ls.rowHeight);
					}else{
						h=Number(CSSDims.max.height);
					}
				
				
				
			//
		
		}else if(__state==STATE_TERM_NORESULTS){
			Logger.logIt(" bsSize - STATE_TERM_NORESULTS");
			
			bounds=message_msg.getBounds(_root);
			
					if(CSSDims.max.width=='auto' || isNaN(Number(CSSDims.max.width))){		
						//
					}else{
						w=Number(CSSDims.max.width);
					}
					
					if( CSSDims.max.isHeightAuto ){		
						h=this.getRect(_root).yMax+10;
					}else{
						h=Number(CSSDims.max.height);
					}
			
		}else if (__state==STATE_READY){
				Logger.logIt(" bsSize - UNHANDLED");
					if(CSSDims.min.width=='auto' || isNaN(Number(CSSDims.min.width))){		
						// use default width defined at start of func
					}else{
						w=Number(CSSDims.min.width);
					}
					
					if( CSSDims.min.isHeightAuto  ){		
						// use default height defined at start of func
					}else{
						h=Number(CSSDims.min.height);
					}
		}
		
			var sbalign:String=_global.styles.SearchBox.align.toLowerCase();
			trace("SLIGN TXT:"+sbalign);
			if(sbalign==undefined){sbalign="right";}
			switch(sbalign){
				case 'left':
				//trace("LEFT");
					searchterms_ti.move(1,searchterms_ti.y);
					//trace("TXTIS@:"+searchterms_ti.x+" "+searchterms_ti._x);
					break;
				case 'right':
					searchterms_ti.move(Stage.width-searchterms_ti._width-1,searchterms_ti.y);
				
					break;
				case 'center':
					trace("CENTERCENTERCENTER");
					searchterms_ti.move(Math.floor((Stage.width/2)-(searchterms_ti.width/2)),searchterms_ti.y);
					break;
			}
		//w=bounds.xMax-bounds.xMin;
		
		Logger.logIt("APP BOUNDS: max:"+bounds.xMax+",min:"+bounds.xMin+"="+(bounds.xMax-bounds.xMin));
		Logger.logIt("APP REQUESTS SIZE: w:"+w+",h:"+Math.min(h,maxH)+" max:"+h);
	
	
		oldWidth=w=w+20;
		oldHeight=h=Math.min(h,maxH);
		dispatchEvent(
		{
			type:AlissEvents.EVENT_BROWSERLAYOUTMANAGER_SET_STAGE_SIZE,
			target:this,
			width:w,
			height:h
		});
		//Math.min(h,maxH)
	}
	
	/*
	*	@description	Returns the max available height on the HTML page
	*	@return	Number
	*/
	function getMaxLayoutHeightFromBrowser():Number
	{
		var h:Number=Number(ExternalInterface.call("browserLayoutManager_getMaxHeight"));		
		if(isNaN(h)){h=defaultLayoutHeight;}		
		return h;
	}
	/*
	*	@description	Hides the Message component if visible
	*	@return	Void
	*/
	public function hideMessage():Void
	{
		message_msg.text="";
		message_msg._visible=false;
	}
	
	/*
	*	@description	Display a Message
	*	@param	str	The text of the message
	*	@param buttonLabel	The label to display on the Message Button, default in "OK"
	*	@return	Void
	*/
	public function showMessage(str:String,buttonLabel:String):Void
	{
		Logger.logIt(" ***showMessage str:"+str+" buttonLabel:"+buttonLabel);
		//if(buttonLabel==undefined){buttonLabel="OK";}
		if(message_msg==undefined){
		message_msg=Message(
			this.createChild(
				Message, "message_msg", 
				{text:str,
					buttonLabel:buttonLabel,
					controller:this,
					_y:30,
					_visible:true}
				)
		);
		message_msg.filters=relatedResults_rrv.filters;
		message_msg.setSize(defaultLayoutWidth,200);
		message_msg.addEventListener("click",this);
		}else{
			message_msg.text=str;
			message_msg.buttonLabel=buttonLabel;
			
			message_msg._visible=true;
		}
		//trace("	>>> MESSAGE:'"+str+"' "+message_msg);
		measureRequiredSize()();
	}
	//------------------------------------------------------------------------------
	
	
	
	
	
	//------------------------------------------------------------------------------
	/*
	*	@description	invalidate()s the component
	*	@return	Void
	*/
	public function onStageResize():Void
	{
		invalidate();
		//doLater(this,"measureRequiredSize");
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	disabled the standard onResize event, The BrowserLayoutManager broadcasts "onStageResize"
	*	@see com.eea.layout.BrowserLayoutManager
	*	@return	Void
	*/
	public function onResize():Void
	{
		//doLater(this,"measureRequiredSize");
		//invalidate();
		//measureRequiredSize();
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	The replacement for onStageResize. 
						BrowserLayoutManager broadcasts "onStageResize".
	*	@see com.eea.layout.BrowserLayoutManager
	*	@return	Void
	*/
	public function onBrowserResize(e:Object):Void
	{
		//trace("*** FLASH onBrowserResize ***S");
		Logger.logIt("SSV GOT onBrowserResize wmax:"+e.data.browserAvailableWidth+"hmax:"+e.data.browserAvailableHeight);
		
		browserDim=e.data;
		/*
		for(var s:String in browserDim){
			Logger.logIt("		"+s+"="+browserDim[s]);
		}
		*/
		//doLater(this,"measureRequiredSize");
		invalidate();
		//measureRequiredSize();
		//trace("*** FLASH onBrowserResize ***E");
	}
	//------------------------------------------------------------------------------
	
    function onBrowserBlur():Void{
    	    Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        	Logger.logIt("+   BLUR EVENT   		         +");           
            Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
            
        browserLastBlurFocusEvent=0;
    	 clearInterval(browserBlurEventID);
    	  clearInterval(browserFocusEventID);
        browserBlurEventID=setInterval(this,"onBrowserBlurDo",browserBlurFocusDelayTime); 
    }
    function onBrowserBlurDo():Void{
    	Logger.logIt("+   START EXECUTE BLUR EVENT            +");
    	clearInterval(browserBlurEventID);
    	
        if(browserLastBlurFocusEvent==0){
        	Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        	Logger.logIt("+   EXECUTE BLUR EVENT            +");
            
            searchterms_ti.text="";
            state=STATE_READY; 
            setFocus(_root);
            invalidate();
            Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        }
    }
    
    function onBrowserFocus():Void{
    	
    		Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        	Logger.logIt("+   FOCUS EVENT   		         +");           
            Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
    	 browserLastBlurFocusEvent=1;
    	 clearInterval(browserBlurEventID);
    	 clearInterval(browserFocusEventID);
    	   browserFocusEventID=setInterval(this,"onBrowserFocusDo",browserBlurFocusDelayTime); 

       
        /*clearInterval(browserFocusEventID);
        browserBlurEventID=setInterval(this,"onBrowserFocusDo",browserBlurFocusDelayTime);*/
    }
    
    function onBrowserFocusDo():Void{
    	clearInterval(browserFocusEventID);
    	 dispatchEvent({type:"onBrowserFocus"}); 
    	 
    	   	Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        	Logger.logIt("+   EXECUTE FOCUS EVENT            +");           
            Logger.logIt("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
    }
    
	
	
	
	
	
	//------------------------------------------------------------------------------
	public function get searchterm(){return searchterms_ti.text;}
	//------------------------------------------------------------------------------
	public function set state(n:Number):Void
	{
		if(n==__state){return;}
		__oldState=__state;
		__state=n;
		trace("STATE: OLD:"+__oldState+" NEW:"+__state);
		invalidate();
	}
	public function get state():Number
	{
		return __state;
	}
	//------------------------------------------------------------------------------
		public function makeStyledDropShadow(
			distance:Number,
			angle:Number,
			color:Number,
			alpha:Number,
			blurX:Number,
			blurY:Number,
			strength:Number,
			quality:Number,
			inner:Boolean,
			knockout:Boolean,
			hideObject:Boolean):DropShadowFilter
	{
			
			return new DropShadowFilter(
				Number(getPriorityValue("dropShadowDistance",distance)),
				Number(getPriorityValue("dropShadowAngle",angle)),
				Number(getPriorityValue("dropShadowColor",color)),
				Number(getPriorityValue("dropShadowAlpha",alpha)),
				Number(getPriorityValue("dropShadowBlurX",blurX)),
				Number(getPriorityValue("dropShadowBlurY",blurY)),
				Number(getPriorityValue("dropShadowStrength",strength)),
				Number(getPriorityValue("dropShadowQuality",quality)),
				(getPriorityValue("dropShadowInner",inner))=="true",
				(getPriorityValue("dropShadowKnockout",knockout)=="true"),
				(getPriorityValue("dropShadowHideObject",hideObject))=="true"
			);
			
	}
	/*
	*	@description	looks for a value for prop in the local CSS map, if not found, return the defaultValue
	*	@param prop	The name of the property to check. ex: "fontFamily"
	*	@param defaultValue	The default value that is returned if there is no custom value.
	*	@see com.eea.styling.css.ComponentCSS 
	*	@return	Void
	*/	
	public function getPriorityValue(prop:String, defaultValue:Object):Object
	{
		var styleVal=getStyle(prop);	
		trace("DEF VAL:"+getStyle("styleName")+"."+prop+"="+styleVal);
		if(styleVal!=undefined && styleVal!=null){return styleVal;}else{return defaultValue;}
	}
}