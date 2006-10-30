	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissApplication is the core logic controller 
				for the SmartSearch application.
*/
	
import mx.core.UIObject;

import com.eea.projects.aliss.itemrenderer.RelatedResultItem;
import com.eea.projects.aliss.views.DefinitionView;
import com.eea.projects.aliss.events.AlissEvents;

class com.eea.projects.aliss.views.RelatedItemList
extends UIObject{
		
	/*
	@author			Tor Kristensen	tor.kristensen@tietoenator.com
	@version		1.2
	@description	AlissApplication is the core logic controller 
					for the SmartSearch application.
	*/
	
	public var controller:Object;
	
	//styles
	public var bg_color:Number=0xE6F2E1;
	public var bg_border_width:Number=0;
	public var bg_border_color:Number=0x000000;
	public var alternateRowColors:Array=[0xC0CEAD,0xEAF0E4];
	
	public var rowHeight:Number=35*2;
	
	public var displayWidth:Number=310;
	public var displayHeight:Number=500;
	
	//data provider
	public var data:Object;
	public var showNResultsPerCategory:Number=5;

	//mc references
	public var bg_mc:MovieClip;
	public var content_mask_mc:MovieClip;
	public var content_host_mc:MovieClip;
	
	public var display_mc:MovieClip;
	public var displayItemClass:String="RelatedResultItem";
	public var definitionItemClass:String="DefinitionClip";
	public var displayChildren:Array;
	public var definitionView_mc:DefinitionView;

	private var layoutY:Number;
	private var z:Number=1;
	
	static var ERROR_NO_INFORMATION_ON_TOPIC:String="There is no available information on this topic.";

	//------------------------------------------------------------------------------
	function RelatedItemList()
	{
		super();
	}
	//------------------------------------------------------------------------------
	function setController(o:Object):Void	
	{
		controller=o;
		trace("setController"+arguments);		
		
	}
	//------------------------------------------------------------------------------
	function createChildren():Void
	{
		displayChildren=[];
		bg_mc=createEmptyMovieClip("bg_mc",1);
		display_mc=createEmptyMovieClip("display_mc",2);
		display_mc._x=display_mc._y=5;
	}
	//------------------------------------------------------------------------------
	public function setSize(w:Number,h:Number):Void
	{
		
	}
	//------------------------------------------------------------------------------
	public function click(e:Object):Void
	{
		trace("CLICK");
		//this._visible=false;
		dispatchEvent({type:AlissEvents.EVENT_RELATEDITEM_SELECTION});
	}
	//------------------------------------------------------------------------------
	function smartSearch_GetTopPagesForTermsResult(event:Object):Void
	{
		
		trace("%%%%%%%%%%%%%%%%%%%%%%%%");
		trace(toString()+"GOT smartSearch_GetTopPagesForTermsResult");
		
		data=event.data;
		invalidate();
	}
	function draw():Void
	{
	
		var isDisplayable:Boolean=false;
		for(var section:String in data.results)
		{
			
			if(data.results[section].length>0)
			{
				isDisplayable=true;
				break;
			}
		}
		
		if(!isDisplayable && (data.definition==undefined ||data.definition.length==0))
		{
			trace("RESULT HAS NO DISPLAYABLE INFORMATION");
			return;
		}
		
		layoutY=0;
		z=1;
		for(var n:Number=0;n<displayChildren.length;n++)
		{			
			displayChildren[n].removeMovieClip();		
		}
		
		displayChildren=[];
		
		
		trace("DEFINITION="+data.definition);
		if(data.definition!=undefined && data.definition!="undefined" && data.definition!=null)
		{
			definitionView_mc=makeDefinitionItem(data.definition,displayChildren.length+1);
			definitionView_mc.addEventListener("click",this);
			displayChildren.push( definitionView_mc );	
		}else{
			if(!isDisplayable){
				definitionView_mc=makeDefinitionItem(ERROR_NO_INFORMATION_ON_TOPIC,displayChildren.length+1);
				definitionView_mc.addEventListener("click",this);
				displayChildren.push( definitionView_mc );					
			}
			
		}
		
		
		for(var section:String in data.results)
		{
			
			for(var n:Number=0;n<Math.min(showNResultsPerCategory,data.results[section].length);n++)
			{			
				var mc:MovieClip=createDisplayItem(data.results[section],n,displayChildren.length+1,section);
				mc.addEventListener("click",this);
				displayChildren.push( mc );
			}
		}
		doLater(this,"drawBgFills");
		
			
		this._visible=true;
	}
	//------------------------------------------------------------------------------
	function drawBgFills():Void
	{
		/*
		draw bg rects
		*/
		bg_mc.clear();
		for(var n:Number=0;n<displayChildren.length;n++){
			/*
			trace(n+" "+(n%alternateRowColors.length)+"> RGB:"+alternateRowColors[n%alternateRowColors.length]);
			trace("         0,"+displayChildren[n]._y+","+displayWidth+","+displayChildren[n]._height);
			trace("          test:"+displayChildren[n].height);
			trace(" 		title:"+displayChildren[n].title_txt.text+newline);
			*/
			var h:Number;
			
			if(n<displayChildren.length){
				h=displayChildren[n+1]._y-(displayChildren[n]._y+displayChildren[n]._height);
			}else{
				h=displayChildren[n]._height;
			}
			
			drawRect(
				bg_mc,
				alternateRowColors[n%2],
				bg_border_width,
				bg_border_color,
				0,
				Math.floor(displayChildren[n]._y),
				displayWidth,
				h
			);
		}
		
		
	}
	function makeDefinitionItem(definition_str:String,layoutIndex:Number):DefinitionView
	{
		var cfg:Object={
			owner:this,
			definition:definition_str,
			term:controller.currentRelatedTopicsTerm_str,
			layoutIndex:layoutIndex,
			_y:layoutY
		}
		
		var mc:DefinitionView=DefinitionView(
			display_mc.attachMovie(definitionItemClass,
			"defin"+displayChildren.length+"_mc",
			z++,
			cfg) 
		);
		
		//trace("MAKE AT:"+(displayChildren.length*rowHeight));
		mc.size(displayWidth,rowHeight);
		
		layoutY+=mc.height;
		
		return mc;
		
	}
	//------------------------------------------------------------------------------
	function createDisplayItem(dp:Array,index:Number,layoutIndex:Number, section_str:String):MovieClip
	{
		var cfg:Object={
			owner:this,
			itemType:section_str,
			dataProvider:dp,
			index:index,
			layoutIndex:layoutIndex,
			_y:layoutY 
		}
		
		var mc:RelatedResultItem=RelatedResultItem(
		
			display_mc.attachMovie(displayItemClass,
				"item"+displayChildren.length+"_mc",
				z++,
				cfg)
				
			);
		
		layoutY+=rowHeight;
		
		trace("MAKE AT:"+(displayChildren.length*rowHeight)+" NEW Y:"+layoutY);
		
		mc.size(displayWidth,rowHeight);
		
		return mc;
	}
	//------------------------------------------------------------------------------
	 function drawRect(mc, fillColor, lineWidth, lineColor, x, y, w, h) {
		 
		
		mc.beginFill(fillColor,100);
		mc.lineStyle(lineWidth,lineColor,100)
		mc.moveTo(x, y);
		mc.lineTo(x+w, y);
		mc.lineTo(x+w, y+h);
		mc.lineTo(x, y+h);
		mc.lineTo(x, y);
		mc.endFill();
	}
	//------------------------------------------------------------------------------
	function toString():String
	{
		return "{RelatedItemList}";
	}
	public function get numChildren():Number{return displayChildren.length;}
}


