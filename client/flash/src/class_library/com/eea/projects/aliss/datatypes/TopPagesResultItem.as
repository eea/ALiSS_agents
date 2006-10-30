/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AS2 Datatype for results _items_ returned by the Aliss getTopPagesForTerms service
*/
class com.eea.projects.aliss.datatypes.TopPagesResultItem
extends Object{
	
	//	The URL of the result item
	public var url:String;
	//	The text snippet
	public var snippet:String;
	//	The title of the item
	public var title:String;
	//	The "type" (category) of the item
	public var itemType:String;
	//	The URL of the preview image
	public var previewImg:String;
	
	/**
	*	@description Constructor for the TopPagesResultItem data type
	*	@param o	the RPC-returned object to use as a data source
	*	@return A new TopPagesResultItem instance
	*/
	function TopPagesResultItem(o:Object)
	{
		this.url=o.url;
		this.snippet=o.snippet;
		this.title=o.title;
		this.itemType=o.itemType;
		this.previewImg=o.previewImg;
		trace(this);
	}
	
	/**
	*	@description Getter that returns the snippet as "label", allowing easy use with V2 Components
	*/
	public function get label():String
	{
		return snippet;
	}
	public function toString():String
	{
		var str:String="{RRItem ";
		str+=newline+"title:"+title;
		str+=newline+" snippet:"+snippet;
		str+=newline+" itemType:"+itemType;
		str+=newline+" previewImg:"+previewImg;
		str+=newline+" url:"+url;	
		str+=newline+"}";
		return str;
	}
		
	
}