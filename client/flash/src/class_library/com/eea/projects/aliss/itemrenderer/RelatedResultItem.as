/**
 * @author		Tor Kristensen	tor.kristensen@tietoenator.com
 * @version		1.2
 * @description	RelatedResultItem is the display CellRenderer for... RelatedResult items */
	
import mx.core.UIComponent;
import com.eea.cellrenderer.ICellRenderer;
import com.eea.cellrenderer.CellRendererWithClickEvent;
import com.eea.projects.aliss.application.AlissApplication;
import mx.controls.Loader;

class com.eea.projects.aliss.itemrenderer.RelatedResultItem 
extends CellRendererWithClickEvent
implements ICellRenderer{
	
	static var symbolName:String = "RelatedResultItem";
    static var symbolOwner:Object = RelatedResultItem;
    var className:String = "RelatedResultItem";
	
	//CELLRENDERER API - Vars mixedin from Listowner
	var listOwner : MovieClip; 
	//CELLRENDERER API - Vars mixedin from Listowner
	var getCellIndex:Function;
	//CELLRENDERER API - Vars mixedin from Listowner
	var getDataLabel:Function;
	
	//The data index of the cell
	public var index:Number=0;
	
	//The visual index of the cell
	public var layoutIndex:Number=0;
	
	//The type/category of the item
	public var itemType:String;
	
	//Pointer to the DataProvider
	public var dataProvider:Array;
	
	//Pointer to List owner
	public var owner:Object;
	
	//TextField for the Snippet
	public var snippet_txt:TextField;
	
	//TextField for the Title
	public var title_txt:TextField;
	
	//TextField for the URL
	public var url_txt:TextField;
	
	//TextField for the trailing "..." after long items
	public var dots_txt:TextField;
	
	//The rollover hilight
	public var hilight_mc:MovieClip;
	
	//The icon movieclip for the item
	public var icon_mc:Loader;
	//The URL for the icon graphic
	public var icon_url:String;
	//reference for the fill color movieclip
	public var fill_mc:MovieClip;
	//Dim object with width/height for the size of the URL TextField
	private var url_dim:Object;
	//The RGB value for bold <b/> text in snippet and title
	private var em_rgb:String;
	private var norm_rgb:String;

	//------------------------------------------------------------------------------
	/**
	 * @description The Constructor for RelatedResultItem	 */
	function RelatedResultItem()
	{
		
	}
	//------------------------------------------------------------------------------
	/**
	 * @description Method to create child objects	 */
	function createChildren(){
		super.createChildren();
		/*size();
		invalidate();
		*/
		var temp_rgb=this.getStyle("emphasisColor");
		if(temp_rgb==undefined){
			em_rgb="#FF0000";
		}else{
			em_rgb=temp_rgb;
		}
		
		var temp_norm_rgb=this.getStyle("textColor");
		if(temp_norm_rgb==undefined){
			norm_rgb="#000000";
		}else{
			norm_rgb=temp_norm_rgb;
		}
		
		


		icon_mc=Loader( createClassObject(Loader, "icon_mc", getNextHighestDepth()) ); 
		icon_mc.autoLoad = true;
		icon_mc.scaleContent=false;
		icon_mc.addEventListener("complete",this);
		icon_mc.setSize(50,50);
		
		snippet_txt=this.createLabel("snippet_txt", getNextHighestDepth(), " ");	
	
		snippet_txt.html=true;
		snippet_txt.multiline=true;
		snippet_txt.wordWrap=true;
		//snippet_txt.setStyle("styleName","");
		snippet_txt._x=50;
		
		var styleObj:TextField.StyleSheet = new TextField.StyleSheet();

		styleObj.setStyle("styleName","FOO");
		styleObj.setStyle(".TEST",
		{fontFamily:"Verdana",fontWeight:"bold",color:'#FF0000',
			fontSize:'10px'}
		);
		
		
		//snippet_txt.setStyle("styleName","FOO");
		//snippet_txt.setStyle(".TEST",{fontFamily:"Verdana",fontWeight:"bold",color:'#FF0000',
		//	fontSize:'10px'});
		//snippet_txt.styleSheet=styleObj;
		title_txt=this.createLabel("title_txt", getNextHighestDepth(), " ");	
		title_txt.multiline=true;
		title_txt.html=true;
		title_txt.autoSize=false;
		title_txt.setSize(150,20);
			//title_txt.styleSheet =styleObj;
	
		
//title_txt.setStyle("styleName", "RelatedResultItem");
/*
		
		title_txt.setStyle("styleName", "RelatedItemPreview_Info");
		title_txt.setStyle("main", {fontFamily: 'Arial', 
   fontSize: 12,
   color: 0xFF0000});
		title_txt.setStyle(".main.b"s,{color:0xFF0000});
		title_txt.setStyle("b",{color:0xFF0000});
		title_txt.setStyle("bold",{color:0xFFFF00});
		
		
		snippet_txt.setStyle(".b",{color:0xFF0000});*/
		//url_txt.autoSize="left";
		//snippet_txt.border=title_txt.border=true;
	}
	//------------------------------------------------------------------------------
	/**
	 * @description Handles layout for the cell after it has been resized	 */
	function size():Void
	{
		super.size();
		
		fill_mc._width=_width;
		fill_mc._height=_height;
		
		title_txt.move(5,5);	
		title_txt.setSize(
			listOwner.width-30,
			title_txt.height
			);

		snippet_txt._y=title_txt._y+title_txt._height;
		snippet_txt.setSize(
			listOwner.width-70,
			Math.min(35,snippet_txt.getTextFormat().getTextExtent(snippet_txt.text,snippet_txt._width).textFieldHeight+8 )
			);
		
		url_dim=url_txt.getTextFormat().getTextExtent(url_txt.text,listOwner.width-70-url_txt._x);
		
		url_txt._y=snippet_txt._y+snippet_txt._height-3;		
		var showDots:Boolean=url_txt._width > listOwner.width-url_txt._x-25;
		dots_txt._visible=showDots;		
		if(showDots){
			url_txt.autoSize=false;
			url_txt._width=listOwner.width-url_txt._x-45;
			dots_txt._x= url_txt._x+url_txt._width-3;	
		}else{
			url_txt.autoSize="left";
		}

		dots_txt._y=url_txt._y;
		
		icon_mc._x=Math.floor(25-(icon_mc._width/2));
		icon_mc._y=title_txt._y+title_txt._height+5; //Math.floor((owner.rowHeight/2)-(icon_mc._height/2)-12);
	}
	//------------------------------------------------------------------------------

	//------------------------------------------------------------------------------
	/**
	 * @description onRelease handler, loads item URL into browser window
	 * @return Void	 */
	function onRelease():Void
	{
		
		getURL(listOwner.dataProvider[getCellIndex().itemIndex].url,"somewindow"+getTimer());
		dispatchEvent({type:"click",target:this, index:getCellIndex().itemIndex});
	}
	//------------------------------------------------------------------------------
	/**
	 * @description	Loads an icon into the item display, if icon_str is null the method looks up the default icon from the group/category definition 
	 * @param	icon_str	the linkageID or URL of the image to load as an icon.	 */
	function loadIcon(icon_str:String):Void
	{		
		
		
		var url_str:String=AlissApplication.getImageUrlForItemType(icon_str);
		if(url_str=="")
		{
			trace("NO URL FOR:"+icon_str);
			icon_mc._visible=false;
		}
		
		if(icon_url!=url_str){
			icon_url=url_str;
			icon_mc.load(url_str);
		//	trace("icon_str->"+url_str+" in "+icon_mc);
		}
	}
	
	//------------------------------------------------------------------------------
	// CELLRENDERER API
	//------------------------------------------------------------------------------
	/**
	 * @description	Return the preferred height of the control, CellRenderer API standard
	 */
	 function getPreferredHeight():Number
	{
		return _height;
	}
	/**
	 * @description	Return the preferred width of the control, CellRenderer API standard
	 */
	function getPreferredWidth():Number
	{
		return _width;
	}
	
	/**
	 * @description	Sets the values for the cell to display, CellRenderer API standard
	 * @paran str	String
	 * @param item	Data object
	 * @param sel isSelected Boolean
	 * 
	 */
	function setValue(str:String, item:Object, sel:Boolean)
	{
		_visible=item!=undefined;
		
		var fOpen:String='<FONT COLOR="'+norm_rgb+'">';
		var fClose:String='</FONT>';
		
		var tStr:String=fOpen+convertTagToClass(item.title,"b",'FONT COLOR="'+em_rgb+'"','FONT')+fClose;
		title_txt.htmlText="<b>"+tStr+"</b>";	
		
		var snip:String=fOpen+convertTagToClass(item.snippet,"b",'FONT COLOR="'+em_rgb+'"','FONT')+fClose;
		snippet_txt.htmlText=snip;

		//trace("SNIP:"+item.snippet);
		url_txt.text=item.url;	
		loadIcon(item.itemType);
		invalidate();
	}
	/**
	 * @description starts the timing interval for preview image display	 */
	private function startinterval():Void
	{
		listOwner['controller'].startPreviewInterval(getCellIndex().itemIndex,this.owner.rowIndex);
	}
	/*public function onMouseMove():Void
	{
		if(intervalID!=undefined){
			startinterval();
		}
	}*/
	
	/**
	 * @description onRollover starts the preview image interval, and passes the event to its' superclass
	 * @see #startinterval	 */
	public function onRollOver():Void
	{
		super.onRollOver();			
		doLater(this,"startinterval");
	}
	/**
	 * @description onRollOut fires a message to kill any preview image
	 * @see #startinterval
	 */
	public function onRollOut():Void
	{
		super.onRollOut();			
		listOwner['controller'].hidePreview();
	}
	

	/**
	 * @description Called when the icon has loaded	 */
	public function complete():Void
	{
		icon_mc._visible=true;
		size();
	}
	/**
	 * @description Searches a given HTML string, and replaces tags of type tag with new open closing tags, this allows converting "<b></b>" into "<span class="foo"></span>"
	 * @param	str	The html string to search
	 * @param	tag The tag to search for
	 * @param	openTag	The new opening tag to insert
	 * @param	closeTag	The new closing tag to insert
	 * @return String
	 */
	private function convertTagToClass(str:String,tag:String,opentag:String,closetag:String):String
	{
		return searchAndReplace(searchAndReplace(str,"</"+tag+">",'</'+closetag+'>'),"<"+tag+">",'<'+opentag+'>');
		
	}
	/**
	 * @description Does search and replace on a string
	 * @return String
	 * @param	holder	The string to search and replace within
	 * @param	searchFor	The target for replacement
	 * @param	replacement	The string to repalce the searchFor string with.	 */
	private function searchAndReplace(holder:String, searchfor:String, replacement:String):String {
		var temparray:Array = holder.split(searchfor);
		holder = temparray.join(replacement);
		return (holder);
	}
}