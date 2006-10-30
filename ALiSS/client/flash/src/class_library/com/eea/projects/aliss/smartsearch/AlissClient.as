	
/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissClient is the local interface to the EEA Aliss webservice
*/
	
import com.mattism.http.xmlrpc.Connection;
import com.mattism.http.xmlrpc.ConnectionCancellableImpl;
import com.mattism.http.xmlrpc.util.XMLRPCDataTypes;

import mx.utils.Delegate;
import mx.events.UIEventDispatcher;

import com.eea.projects.aliss.application.AlissApplication;
import com.eea.projects.aliss.events.AlissEvents;
import com.eea.projects.aliss.datatypes.TopPagesResults;
import com.eea.utilities.logging.Logger;

class com.eea.projects.aliss.smartsearch.AlissClient 
extends Object{
		

	
	//Placeholder for mixin functions from UIEventDispatcher
	public var addEventListener;
	//Placeholder for mixin functions from UIEventDispatcher
	public var removeEventListener;
	//Placeholder for mixin functions from UIEventDispatcher
	public var dispatchEvent;
	
	private var _VERSION					:String = "1.0.0";
	private var _PRODUCT					:String = "AlissClient";
	
	//Static var that defines the webservice method for getTermSuggestions
	static var GET_TERM_SUGGESTIONS			:String="getTermSuggestions";
	
	//Static var that defines the webservice method for getTopPagesForTerms
	static var GET_TOP_PAGES				:String="getTopPagesForTerms";
	
	//Static var that defines the webservice method for getTermsInText
	static var GET_TERMS_IN_TEXT			:String="getTermsInText";
	
	//URL of the webservice
	static var SERVICE_URL					:String = "http://webservices.eea.europa.eu/alissBIG/agentBIG/";
	
	//Prefix to a google query
	static var GOOGLE_PREFIX_URL			:String="http://google.eea.europa.eu/search?q=";
	
	//Suffix to a google query
	static var GOOGLE_SUFFIX_URL			:String="&client=default_frontend&site=default_collection&ie=ISO-8859-1&oe=UTF-8&output=xml_no_dtd&proxystylesheet=default_frontend";
	
	//Pagesize to be returned
	static var RESULT_PAGESIZE				:Number=10;
	
	//Counts number of webservice calls in a session
	static var CALL_COUNTER					:Number=0;
	
	//How long we wait before firing an onTimeout event
	static var TIMEOUT_DURATION				:Number=1000;

	//Object (hashmap) of pending calls
	public var pendingCalls:Object;
	
	//linear array of terms returned
	public var terms_array:Array;
	
	//Instance that contains structured results from GET_TOP_PAGES
	public var relatedPagesResults:TopPagesResults;
	
	//Private counter for latest call ID
	private var callID:Number=0;
	
	//ID for current timeout interval
	private var timeoutIntervalID:Number;
	
	//AlissClient state
	private var state:Number=0;
	
	
	//Static var defining state: STATE_TERMS
	private static var STATE_TERMS:Number=1;
	
	//Static var defining state: STATE_RELATED
	private static var STATE_RELATED:Number=2;
		
	//Static var defining state: STATE_TERMSINTEXT
	private static var STATE_TERMSINTEXT:Number=3;	
	
	//Static var defining state: STATE_READY	
	private static var STATE_READY:Number=0;
	
	//Static var defining state: STATE_ERROR
	private static var STATE_ERROR:Number=-1;
	//------------------------------------------------------------------------------
	/**
	@description	Constructor for the AlissClient
	*/	
	function AlissClient()
	{
		init();
	}
	//------------------------------------------------------------------------------
	/**
	 * @description	Inits the client, loads configuration information from XML document defined in AlissApplication.getConfig("service_url")
	 * @return	Void	 */
	function init():Void
	{
		UIEventDispatcher.initialize(this);
		Logger.logIt("TEST SERVICE URL:"+AlissApplication.getConfig("service_url"));
		if(AlissApplication.getConfig("service_url")!=undefined)
		{
			SERVICE_URL			= String( AlissApplication.getConfig("service_url") );
			GOOGLE_PREFIX_URL	= String( AlissApplication.getConfig("search_prefix_url") );
			GOOGLE_SUFFIX_URL	= String( AlissApplication.getConfig("search_suffix_url") );
			RESULT_PAGESIZE		= Number(AlissApplication.getConfig("result_pages_size") );
			Logger.logIt("LOADING SERVICE INFO FROM XML CONFIG");
			Logger.logIt("	SERVICE_URL:"+SERVICE_URL);
		}else{
			Logger.logIt("NO SERVICE INFO FROM XML CONFIG, USING DEFAULT");
			Logger.logIt("	SERVICE_URL:"+SERVICE_URL);
		}
		
		state=STATE_READY;
		pendingCalls={};
	}
	//------------------------------------------------------------------------------
	
	
	/*------------------------------------------------------------------------------
	* XMLRPC METHODS
	*------------------------------------------------------------------------------*/
	/**
	 * @description Calls getTermsInText() from the Webservice. 
	 * @return Connection
	 */
	function callGetTermsInText(event:Object):Connection
	{
			Logger.logIt("callGetTermsInText "+arguments);
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_BUSY});
		

		var rpc:Connection = new ConnectionCancellableImpl(SERVICE_URL);
		rpc.addParam(event.data);  //Text to find terms in 
		var searchDepth=10;

		rpc.addParam(10, XMLRPCDataTypes.INT);  //Max depth to search the text for terms
		rpc.onLoad = Delegate.create(this,onGetTermsInTextResult);
		
		rpc.call(GET_TERMS_IN_TEXT);
		
		if(pendingCalls.callGetTermsInText!=undefined){
			pendingCalls.callGetTermsInText.cancel();
			delete pendingCalls.callGetTermsInText;
		}
		pendingCalls.callGetTermsInText=rpc;
		
		startTimeoutInterval();
		state=STATE_TERMSINTEXT;
		
		return rpc;
	}
		
	/**
	 * @description Event fired on succesfull response from the getTermsInText() method of the service.Broadcasts results in the form of
	 * {
	 * 		type:"smartSearch_GetTermsInTextResult",
	 * 		data:{
	 * 			marked_text:HtmlText,
	 * 			linkedterms:Array,
	 * 			foundterms:Array
	 * 		}
	 * }
	 * @return Void
	 */
	function onGetTermsInTextResult(event:Object ):Void 
	{
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TERMS_IN_TEXT_RESULT,
			data:event});
		state=STATE_READY;
	}
		
		
		
	/**
	 * @description	Calls the getTermSuggestions() method of the webservice
	 * @param	event	An event object with the property "data" which defines the text to search on. {data:"my search string"} 
	 * @return Connection object
	 */
	function callGetTermSuggestions(event:Object):Connection{
	
		Logger.logIt("callGetTermSuggestions "+arguments);
		
		
		var rpc:Connection = new ConnectionCancellableImpl(SERVICE_URL);
		rpc.addParam(event.data+"*");  //Search terms with wildcard
		rpc.addParam(true);  			//get extended
		rpc.onLoad = Delegate.create(this,onGetTermSuggestionsResult);
		rpc.call(GET_TERM_SUGGESTIONS);
		
		if(pendingCalls.callGetTermSuggestions!=undefined){
			pendingCalls.callGetTermSuggestions.cancel();
			delete pendingCalls.callGetTermSuggestions;
		}
		pendingCalls.callGetTermSuggestions=rpc;
		
		startTimeoutInterval();
		state=STATE_TERMS;
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_BUSY});
		return rpc;
	}
	//------------------------------------------------------------------------------
	/**
	 * @description	Fired on a result from getTermSuggestions(). Broadcasts an event of type AlissEvents.EVENT_SERVICE_GET_TERMS_RESULT
	 * @see com.eea.projects.aliss.events.AlissEvents
	 * @return	Void
	 */
	function onGetTermSuggestionsResult( ):Void {
		clearTimeoutInterval();
		Logger.logIt("+-- GOT TERMS RESULT --+");
		var suggestions:Array=arguments[0];
		
		if(suggestions.length==0)
		{
			dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TERMS_RESULT,
			data:[],isEmptyResult:true});
			return;
		}	
		
		terms_array=[];		
		var len:Number=suggestions.length;
		if(len==0){Logger.logIt("TERM RESULTS EMPTY!");}
		for(var nn:Number=0;nn<len;nn++)
		{	
			terms_array.push(suggestions[nn]);
		}
		
		
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TERMS_RESULT,
			data:terms_array,isEmptyResult:false});
		state=STATE_READY;
	}	
	//------------------------------------------------------------------------------
	/**
	 * @description	Calls the getTopPagesForTerms() method of the webservice. 
	 * @param	event	An event object with the property "data" which defines the text to search on. e.g. {data:"my search string"}.The method appends an asterix "*" to the end of the search string.
	 * @return	Connection
	 */
	function callGetTopPagesForTerms(event:Object):Connection
	{		
		Logger.logIt("GET RELATED FOR:::::"+event.data+newline);
		
		var rpc:Connection = new ConnectionCancellableImpl(SERVICE_URL);
		rpc.addParam(String(event.data));  //Search terms with wildcard
		rpc.addParam(RESULT_PAGESIZE, XMLRPCDataTypes.INT);
		//rpc.addParam(getTimer(),XMLRPCDataTypes.INT);
		rpc.onLoad = Delegate.create(this,onGetTopPagesForTermsResult);
		rpc.call(GET_TOP_PAGES);
		
		if(pendingCalls.callGetTopPagesForTerms!=undefined){
			pendingCalls.callGetTopPagesForTerms.cancel();
			delete pendingCalls.callGetTopPagesForTerms;
		}
		pendingCalls.callGetTopPagesForTerms=rpc;
		
		startTimeoutInterval();
		state=STATE_RELATED;
		
		return rpc;
	}
	
	/**
	 * @description	Fired on a result from getTopPagesForTermsResult(). Broadcasts an event of type AlissEvents.EVENT_SERVICE_GET_TOP_PAGES_RESULT.
	 * @see com.eea.projects.aliss.events.AlissEvents
	 * @return	Void
	 */
	function onGetTopPagesForTermsResult():Void
	{
		Logger.logIt("+-- GOT onGetTopPagesForTermsResult --+");
		clearTimeoutInterval();
		relatedPagesResults=new TopPagesResults(arguments[0]);
		Logger.logIt("+-- DISPATCH EVENT --+");
		dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TOP_PAGES_RESULT,target:this,data:relatedPagesResults});
		state=STATE_READY;
	}
	//------------------------------------------------------------------------------	
	/**
	 * @description Calls the Google webservice defined by GOOGLE_PREFIX_URL and GOOGLE_SUFFIX_URL with the query defined in e.data
	 * @param	e	A standard event object with a "data" property that defines the terms to search for: e.g. {data:"my google query string"}
	 * @return	Void
	 */
	public function onCallGoogle(e:Object):Void
	{
		callGoogle(e.data);
	}
	
	/**
	 * @description Opens the google search results for the terms defined in str
	 * @param	str	The google search string
	 * @return	Void
	 */
	public function callGoogle(str:String):Void
	{
		getURL(GOOGLE_PREFIX_URL+escape(str)+GOOGLE_SUFFIX_URL)		
	}
	/**
	 * @description	Begins a timeout interval after an XMLRPC call is made
	 * @return	Void
	 */
	private function startTimeoutInterval():Void
	{
		clearTimeoutInterval();
		timeoutIntervalID=setInterval(this,"onTimeout",TIMEOUT_DURATION);
	}
	/**
	 * @description	Clears and removes the timeout interval
	 * @return	Void
	 */
	private function clearTimeoutInterval():Void
	{
		clearInterval(timeoutIntervalID);
		timeoutIntervalID=undefined;
	}
	/**
	 * @description	An event fired when an XML-RPC call takes longer than TIMEOUT_DURATION
	 * @return	Void
	 */
	public function onTimeout():Void
	{
		if(timeoutIntervalID==undefined){return;}
		Logger.logIt("SSCLIENT HAS TIMED OUT:"+state);
		clearTimeoutInterval(timeoutIntervalID);
		
		if(state==STATE_TERMS){
			dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TERMS_TIMEOUT,target:this});
		}else if(state==STATE_RELATED){
			dispatchEvent({type:AlissEvents.EVENT_SERVICE_GET_TOP_PAGES_TIMEOUT,target:this});
		}
		
		state=STATE_READY;
	}
	public function toString():String{return "{AlissClient "+_VERSION+"}";}
}