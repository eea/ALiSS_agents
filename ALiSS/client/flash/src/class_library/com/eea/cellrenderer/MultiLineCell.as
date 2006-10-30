/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	CellRendererWithClickEvent allows subclasses to intercept mouse events on individual cells while maintaining the flow of events to the List class. 
*/

import mx.core.UIComponent;
import com.eea.cellrenderer.CellRendererWithClickEvent;
class com.eea.cellrenderer.MultiLineCell 
extends CellRendererWithClickEvent
{
    private var multiLineLabel; // The label to be used for text.
    private var owner; 			// The row that contains this cell.
    private var listOwner; 		// The List, data grid or tree containing this cell.

    // Cell height offset from the row height total and preferred cell width.
    private static var PREFERRED_HEIGHT_OFFSET = 4; 
    private static var PREFERRED_WIDTH = 100;
	
    // Starting depth.
    private var startDepth:Number = 1;

    // Constructor. Should be empty.
    public function MultiLineCell()
    {
    }

    /* UIObject expects you to fill in createChildren by instantiating all the movie clip assets you might need upon initialization. In this case we are creating one label*/
    public function createChildren():Void
    {
        // The createLabel method is a useful method of UIObject and a handy
        // way to make labels in components.
        var c = multiLineLabel = this.createLabel("multiLineLabel", startDepth);
        // Links the style of the label to the style of the grid
        c.styleName = listOwner;
        c.selectable = false;
        c.tabEnabled = false;
        c.background = false;
        c.border = false;
        c.multiline = true;
        c.wordWrap = true;
		c.html=true;
    }

    public function size():Void
    {
/* 
* By extending UIComponent which imports UIObject, you get setSize automatically, however, 
* UIComponent expects you to implement size(). 
* Assume __width and __height are set for you now. 
* You're going to expand the cell to fit the whole rowHeight. 
* The rowHeight itself is a property of the list type component that we are rendering a cell in. 
* Since we want the rowHeight to fit two lines, when creating the list type component using this 
* cellRenderer class, make sure its rowHeight property is set large enough that two lines of text 
* can render within it.
* __width and __height are the underlying variables of the getter/setters .width and .height.*/

        var c = multiLineLabel;
        c.setSize(__width, __height);
    }

    // Provides the preferred height of the cell. Inherited method.
    public function getPreferredHeight():Number
    {
/* The cell is given a property, "owner", that references the row. 
* It's always preferred that the cell take up most of the row's height. 
* In this case we will keep the cell slightly smaller.*/
		return owner.__height - PREFERRED_HEIGHT_OFFSET;
		var tf:TextFormat=multiLineLabel.getTextFormat();
		var h:Number=tf.getTextExtent(multiLineLabel.text, owner.__width).height+20;
		trace("XXX tl:"+multiLineLabel.text.length+" -> h:"+h);
		return h;
        
    }

    // Called by the owner to set the value in the cell. Inherited method.
    public function setValue(suggestedValue:String, item:Object, selected:Boolean):Void
    {
/* If item is undefined, nothing should be rendered in the cell, so set the label as invisible. 
* Note: For scrolling List type components like a scrolling datagrid, 
* the cells are intended to be empty as they scroll just out of sight, 
* and then the cell is reused again and set to a new value producing an animated effect of scrolling. 
* For this reason, you cannot rely on any one cell always having data to show or the same value.*/
        if (item!=undefined){
            multiLineLabel.text._visible = false;
        }
        multiLineLabel.htmlText = suggestedValue;
    }
    // function getPreferredWidth :: only for menus and DataGrid headers
    // function getCellIndex :: not used in this cell renderer
    // function getDataLabel :: not used in this cell renderer
}

