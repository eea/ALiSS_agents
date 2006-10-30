/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	MultiLineCell is a class for rendering list items with more than one line of text. Implements CellRenderer API.
*/
import mx.controls.Loader

class com.eea.projects.aliss.cellrenderer.ImageLeftMultiLineTextCell 
extends com.eea.cellrenderer.MultiLineCell{

	
	//CELLRENDERER API -  the reference we receive to the list	
	var listOwner : MovieClip; 
	
	//Loader control for listitem icon
	public var imgLoader:Loader;
	
	//URL to the image
	private var img_url:String;
    
    //------------------------------------------------------------------------------
	/**
	*@description	Constructor for MultiLineCell
	*/
	public function MultiLineCell()
    {
		super();
    }
	//------------------------------------------------------------------------------
	
	//------------------------------------------------------------------------------
	/**
	*@description	method that creates child objects
	*/
	function createChildren(Void) : Void
	{
		super.createChildren();
		
		imgLoader = Loader( createClassObject(Loader, "imgLoader", 2) ); 

		
		imgLoader.setSize(16, listOwner.rowHeight);
		imgLoader.scaleContent=true;
/*		
		imgLoader.addEventListener("click", this);
		imgLoader.addEventListener("complete", this);
		imgLoader.setStyle("backgroundColor", 0xEEEEEE);
*/
		
		multiLineLabel.move(imgLoader.width+10);

		invalidate();
	}
	//------------------------------------------------------------------------------
	public function setValue(suggestedValue:String, item:Object, selected:Boolean):Void
    {
		super.setValue(suggestedValue,item,selected);
		_visible=item!=undefined;

		if(img_url!=item.preview_img){
			img_url=item.preview_img;
			imgLoader.load(item.preview_img);
		}
		
		
    }
	//------------------------------------------------------------------------------
}