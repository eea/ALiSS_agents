	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissApplication is the core logic controller 
				for the SmartSearch application.
*/
	
import com.eea.projects.aliss.events.AlissEvents;
import com.eea.projects.aliss.application.AlissApplication;
import mx.core.UIComponent;

class com.eea.projects.aliss.views.DefinitionView 
extends UIComponent {
		
	/*
	@author			Tor Kristensen	tor.kristensen@tietoenator.com
	@version		1.2
	@description	AlissApplication is the core logic controller 
					for the SmartSearch application.
	*/
	
	static var symbolName:String = "DefinitionView";
    static var symbolOwner = com.eea.projects.aliss.views.DefinitionView ;
    var className:String = "DefinitionView";

	public var definition_txt:TextField;
	public var term_txt:TextField;
	
	private var __term:String;
	private var __definition:String;
	
	public var quoteStart_mc:MovieClip;
	public var quoteEnd_mc:MovieClip;
	public var bg_mc:MovieClip;
	
	function DefinitionView(){
		super();
	}
	
	
	function init():Void
	{
		super.init();
	}
	
	function createChildren():Void
	{
		
		definition_txt.multiline=true;
		definition_txt.html=true;
		definition_txt.autoSize="left";
		quoteStart_mc._visible=quoteEnd_mc._visible=false;
		//definition_txt.border=true;
		size();
	}
	function draw():Void
	{
		super.draw();
		//if(!_visible){return;}
		
		if(definition!=undefined){
			var def_str:String=cleanHtml(__definition);
			var len_max:Number=Number(AlissApplication.getConfig("definition_max_length"));
			var len:Number=Math.min(len_max,def_str.length);
			def_str=def_str.slice(0,len);
			if(len==len_max){def_str+="...";}
			definition_txt.htmlText=def_str;	
		}
		
		//trace("__term:"+__term);
		if(__term!=undefined){
			var displayTerm:String=__term.charAt(0).toUpperCase()+term.slice(1,term.length);
			term_txt.text=displayTerm;	
		}
		
		var tf:TextFormat=definition_txt.getTextFormat();
		var h:Number=tf.getTextExtent(definition,width-60).height;

		
		//drawRect(this,0xCCCCCC,0,0,width,height);
		
		//trace("DEF TEXT DIM"+definition_txt.textWidth+","+definition_txt.textHeight+" :: "+definition_txt._width+","+definition_txt._height);
	}
	//------------------------------------------------------------------------------
	function size():Void
	{
		super.size();

		
		this.clear();
		
		var totH:Number=definition_txt.textHeight;
		definition_txt._width=width-60;
		term_txt._width=width-10;
		
		definition_txt.textHeight=height;
		var tf:TextFormat=definition_txt.getTextFormat();
		var h:Number=tf.getTextExtent(definition,width-60).height;
		
		quoteEnd_mc._y=definition_txt._y+definition_txt._height-quoteEnd_mc._height;//(h+definition_txt._y)-(quoteEnd_mc._height*2)+5;
		quoteEnd_mc._x=width-quoteEnd_mc._width-5;
		
		//invalidate();
	
	}
	
	public function get height():Number
	{
		return definition_txt.getTextFormat().getTextExtent(definition,definition_txt._width).height+definition_txt._y+25;
	}
	
	
	
	//------------------------------------------------------------------------------
	// GETTER/SETTER
	//------------------------------------------------------------------------------
	public function get definition():String
	{
		return __definition;
	}
	public function set definition(s:String):Void
	{
		if(s==undefined || s=="undefined"){
			s=String(AlissApplication.getConfig("no_definition_txt"));
		}
		__definition=s;
		invalidate();
	}

	public function get term():String
	{
		return __term;
	}
	public function set term(s:String):Void
	{
		__term=s;
		invalidate();
	}
	
	//------------------------------------------------------------------------------
	// EVENTS
	//------------------------------------------------------------------------------
	function callGetTopPagesForTerms(e:Object):Void
	{
		term=e.data;
	}
	function click():Void
	{
		dispatchEvent({type:"click",target:this});
	}	
	function focus():Void
	{
		
	}	
	function blur():Void
	{
		
	}
	//------------------------------------------------------------------------------
	function onRollOver():Void
	{
		focus();
	}
	//------------------------------------------------------------------------------
	function onRollOut():Void
	{
		blur();
	}
	//------------------------------------------------------------------------------
	function onRelease():Void
	{
		click();
	}
	//------------------------------------------------------------------------------
	function onReleaseOutside():Void
	{
		blur();
	}
	//------------------------------------------------------------------------------
	
	private function cleanHtml(str:String):String {
	 	var val_str = str;
	 	var tmp_str = "";
	 	while(val_str.indexOf(">") != -1) {
	 		tmp_str = val_str.slice(0, val_str.indexOf("<"));
	 		val_str = tmp_str + val_str.slice(val_str.indexOf(">")+1);
	 	}
	 	return val_str;
	 }
	//------------------------------------------------------------------------------
	//UTIL
	//------------------------------------------------------------------------------	
	 function drawRect(mc, fillColor, x, y, w, h) {
		 
		mc.clear();
		mc.beginFill(fillColor,100);
		mc.moveTo(x, y);
		mc.lineTo(x+w, y);
		mc.lineTo(x+w, y+h);
		mc.lineTo(x, y+h);
		mc.lineTo(x, y);
		mc.endFill();
	}
	//------------------------------------------------------------------------------
}