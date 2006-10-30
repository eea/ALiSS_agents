/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	CellRendererWithLableAndClickEvents inherits extended mouse events from CellRendererWithClickEvent, and adds Label display functionality.
@see com.eea.cellrenderer.CellRendererWithClickEvent
*/
 import com.eea.cellrenderer.CellRendererWithClickEvent;
 import com.eea.cellrenderer.ICellRenderer;
  
class com.eea.cellrenderer.CellRendererWithLableAndClickEvents 
extends CellRendererWithClickEvent implements ICellRenderer{
	var label_tf:TextField;
	
	function CellRendererWithClickEvent(){
		super()
	}
	
	/**
	*	@description method that creates child objects
	*	@return Void
	*/
	function createChildren():Void
	{
		super.createChildren();
		
		label_tf=createLabel("label_tf",getNextHighestDepth(),"");
		size();
		invalidate();	
	}
	
	/**
	*	@description Method that handles layout on size
	*	@return Void
	*/
	function size(){
		super.size();
		label_tf._height=listOwner.rowHeight-1;
		label_tf._width=listOwner.width;
	}
	
	/**
	*	@description method that is called by listOwner to set the values the cell should display.
	*	@return Void
	*/
	function setValue(str:String, item:Object, sel:Boolean)
	{
		label_tf.text=str;
	}
	
/**
* @description This func is stolen from UIObject to mmake Label creation easier
* @return TextField
*/
	function createLabel(name:String, depth:Number, text):TextField
	{
		createTextField(name, depth, 0, 0, 0, 0);
		var o:TextField = this[name];
		o._color = UIObject.textColorList;
		o._visible = false;

		o.__text = text;
		if (tfList == undefined)
			tfList = new Object();
		tfList[name] = o;
		o.invalidateStyle();
		invalidate();		// force redraw call
		o.styleName = this;	// labels always inherit styles of parent unless set otherwise
		return o;
	}
}