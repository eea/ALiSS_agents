class com.eea.projects.aliss.events.AlissEvents
extends Object{
		
	/**
	 * @author			Tor Kristensen	tor.kristensen@tietoenator.com
	 * @version		1.2
	 * @description	AlissEvents is a class with static properties that define the Events used in the Aliss application and related components
	 */

	// Event fired when the Application is Initilaising	
	static var EVENT_APP_INITING							:String="onApplicationInit";
	
	// Event fired when the Application is Loading the external XML config file	
	static var EVENT_APP_LOAD_XML							:String="onApplicationLoadXML";
	// Event fired when the Application is Loading External CSS		
	static var EVENT_APP_LOAD_CSS							:String="onApplicationLoadCSS";
	
	// Event fired when the Application is Ready	
	static var EVENT_APP_READY								:String="onApplicationReady";
	
	// Event fired when the Application is Halted by an Error	
	static var EVENT_APP_ERROR								:String="onApplicationError";
	
	
	// Event fired when the User has clicked on a Definition
	static var EVENT_DEFINTION_SELECTION					:String="definitionSelection";
	
	// Event fired when the User has selected a RelatedItem
	static var EVENT_RELATEDITEM_SELECTION					:String="relatedItemSelection";	
	
	
	// Event fired when the User selects a Term, and the application is configured to navigate to the associated URL insted of displaying extended information
	static var EVENT_SEEALLRESULTS_SELECTION				:String="seeAllResultsSelection";
	
	// Event fired when the the search text has changed
	static var EVENT_SEARCHTERM_CHANGE						:String="searchTermChange";
	
	
	// Event fired when the Application is beginning a new RPC getTermSuggestions() call	
	static var EVENT_SERVICE_GET_TERMS						:String="callGetTermSuggestions";
	
	// Event fired when the Application has recieved a RPC getTermSuggestions() result	
	static var EVENT_SERVICE_GET_TERMS_RESULT				:String="smartSearch_GetTermSuggestionsResult";
	
	// Event fired when the Application has timed out on a RPC getTermSuggestions() call
	static var EVENT_SERVICE_GET_TERMS_TIMEOUT				:String="smartSearch_GetTermSuggestionsResult_Timeout";
	
	
	// Event fired when the Application is beginning a new RPC getTopPagesForTerms() call	
	static var EVENT_SERVICE_GET_TOP_PAGES					:String="callGetTopPagesForTerms";
	
	// Event fired when the Application has recieved a RPC getTopPagesForTerms() result	
	static var EVENT_SERVICE_GET_TOP_PAGES_RESULT			:String="smartSearch_GetTopPagesForTermsResult";		
	
	// Event fired when the Application has timed out on a RPC getTopPagesForTerms() call
	static var EVENT_SERVICE_GET_TOP_PAGES_TIMEOUT			:String="smartSearch_GetTopPagesForTermsResult_Timeout";
	
	// Event fired when the Application is beginning a new RPC getTermsInText() call	
	static var EVENT_SERVICE_GET_TERMS_IN_TEXT				:String="callGetTermsInText";
	
	// Event fired when the Application has recieved a RPC getTermsInText() result	
	static var EVENT_SERVICE_GET_TERMS_IN_TEXT_RESULT		:String="smartSearch_GetTermsInTextResult";		
	
	// Event fired when the Application has timed out on a RPC getTermsInText() call
	static var EVENT_SERVICE_GET_TERMS_IN_TEXT_TIMEOUT		:String="smartSearch_GetTermsInTextResult_Timeout";
	
	
	// Event fired when the Application is busy
	static var EVENT_SERVICE_BUSY							:String="smartSearch_Busy";

	

	// Event fired when the Application has recieved a new Stage size from the browser	
	static var EVENT_BROWSERLAYOUTMANAGER_SET_STAGE_SIZE	:String="onSetStageSize";
					
	function AlissEvents(){}
}