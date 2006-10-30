/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	CellRendererWithClickEvent allows subclasses to intercept mouse events on individual cells while maintaining the flow of events to the List class. 
*/

 import mx.core.UIComponent;
 import com.eea.cellrenderer.ICellRenderer;
 
class com.eea.cellrenderer.CellRendererWithClickEvent
extends UIComponent
implements ICellRenderer{
	
	//	Invisible movieclip that intercepts mouse events
	var mouseEvent_mc:MovieClip;
	
	//	Reference to List owner mixed in by List Control
	var listOwner;
	
	//	Placeholder for property mixed in by listOwner
	var owner;
	
	//	Placeholder for function mixed in by listOwner
	var getCellIndex:Function;
	
	//	Placeholder for function mixed in by listOwner
	var getDataLabel:Function;
	
	
	/**
	*	@description Constructor for the cell renderer
	*	@return A new CellRendererWithClickEvent instance
	*/
	function CellRendererWithClickEvent(){
		super();
	}
	//----------------------------------------------------------------
	/**
	*	@description method that creates child objects
	*	@return Void
	*/
	function createChildren(){
		super.createChildren();
		
		mouseEvent_mc=createEmptyMovieClip("mouseEvent_mc",getNextHighestDepth());
		mouseEvent_mc.swapDepths(1);
		
		var x1:Number=0;
		var x2:Number=10;
		var y1:Number=0;
		var y2:Number=10;
		mouseEvent_mc.beginFill(0xFFFFFF,0);
		mouseEvent_mc.lineStyle(0,0xFFFFFF,0);
		mouseEvent_mc.moveTo(x1,y1);
		mouseEvent_mc.lineTo(x2,y1);
		mouseEvent_mc.lineTo(x2,y2);
		mouseEvent_mc.lineTo(x1,y2);
		mouseEvent_mc.lineTo(x1,y1);
		mouseEvent_mc.endFill();
	}
	//----------------------------------------------------------------
	/**
	*	@description Method that handles layout on size
	*	@return Void
	*/
	function size():Void
	{
		super.size();
		
		mouseEvent_mc._width=_width;
		mouseEvent_mc._height=_height;
	}
	//----------------------------------------------------------------
	/**
	*	@description method that returns preferred height
	*	@return Void
	*/
	function getPreferredHeight():Number
	{
		return listOwner.rowHeight;
	}
	//----------------------------------------------------------------
	/**
	*	@description method that returns preferred width
	*	@return Void
	*/
	function getPreferredWidth():Number
	{
		return listOwner.width;
	}
	//----------------------------------------------------------------
	/**
	*	@description method that is called by listOwner to set the values the cell should display.
	*	As this class is "top level" it does not directly render any data. It only supplies advanced mouse events.
	*	@return Void
	*/
	function setValue(str:String, item:Object, sel:Boolean)
	{
		
	}
	//----------------------------------------------------------------
	/**
	*	@description Method that dispatches events on onRelease
	*	@return Void
	*/
	function onRelease():Void{
		var i:Number=getCellIndex().itemIndex;
		//listOwner.onRowRelease(i);
		listOwner.selectRow(i-listOwner.__vPosition,true,true);
		listOwner.dispatchEvent({type:"click",target:listOwner});
		//listOwner.selectedIndex=i;
	}
	//----------------------------------------------------------------
	/**
	*	@description Method that dispatches events on onRollOver
	*	@return Void
	*/
	function onRollOver():Void{
		listOwner.onRowRollOver(owner.rowIndex);
	}
	//----------------------------------------------------------------
	/**
	*	@description Method that dispatches events on onRollOut
	*	@return Void
	*/
	function onRollOut():Void{
		listOwner.onRowRollOut(owner.rowIndex);
	}
	//----------------------------------------------------------------
}