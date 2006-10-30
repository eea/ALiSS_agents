/**
 * @author			Tor Kristensen	tor.kristensen@tietoenator.com
 * @version		1.2
 * @description	AS2 Datatype for the result Object returned by the Aliss getTopPagesForTerms service
 * @see com.eea.projects.aliss.datatypes.TopPagesResultItem
 *  */

class com.eea.projects.aliss.datatypes.TopPagesResults
extends Object{
	
	public var results:Object;
	public var definition:String;
	/**
	 * @see com.eea.projects.aliss.datatypes.TopPagesResultItem
	 * @description results_array allows Array access to the results while maintianing grouping and ordering.	 */
	public var results_array:Array;
	
	/**
	*	@description Constructor for the TopPagesResults data type
	*	@param resultObject	the RPC-returned object to use as a data source. The constructor serializes the result object returned by the RPC call, but also creates a property called results_array that allows Array access to the results while maintianing grouping and ordering.
	*	@return A new TopPagesResults instance
	*/
	function TopPagesResults(resultObject:Array)
	{
		
		results={};
		results_array=new Array();
		
		var groupName:String;
		for(var n:Number=0;n<resultObject.length;n++)
			{
				trace("resultObject["+n+"]---------"+resultObject[n].GroupName+"------- has:"+resultObject[n].Pages.length);
				groupName=resultObject[n].GroupName;
				if(definition==undefined 
				&& resultObject[n].ElementDefinition!=undefined
				&& resultObject[n].ElementDefinition.length>5)
				{
					definition=resultObject[n].ElementDefinition;
				}
				
				if(resultObject[n].Pages.length>0)
				{
					for(var nn:Number=0;nn<resultObject[n].Pages.length;nn++)
					{
						resultObject[n].Pages[nn].itemType=groupName;
					}
					results[resultObject[n].GroupName]=resultObject[n].Pages;
					results_array=results_array.concat(resultObject[n].Pages);
				}
					
			}
			results_array.reverse();
	}
	/**
	*	@description a toString for an item
	*	@return String
	*/
	function itemToString(item:Object):String
	{
		var str:String='[ResultItem - "'+item.title+'"'+newline+'   url:'+item.url+newline+'Definition:'+definition+newline+' ]';
		return str;
	}
	
	
}