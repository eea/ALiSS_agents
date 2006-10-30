import mx.core.View;

/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissApplication is the core logic controller 
				for the SmartSearch application.
*/

class com.eea.controls.BusyGradient
extends View{
	
	static var symbolName:String = "BusyGradient";
    static var symbolOwner = com.eea.controls.BusyGradient;
    var className:String = "BusyGradient";

	public var gradient1_rgb:Number=0xFF0000;
	public var gradient2_rgb:Number=0x0000FF;
	public var padding:Number;
	private var p1_mc:MovieClip;
	private var bg_mc:MovieClip;
	
	function BusyGradient()
	{
		super();
		setStyle("styleName",className);
		trace("FOOPADD:"+getStyle("padding"));
		padding=Number(getPriorityValue("padding", 0));
	}
	
		
	function init():Void
	{
		super.init();
	}
	
	function draw():Void
	{
		super.draw();
	}
	
	function size():Void
	{
		super.size();
		//p1_mc._width=bg_mc._width=width;
		_width=Math.floor(width*2);
		trace("DRAW TEST: w="+width+" p1_mc._width=bg_mc._width="+p1_mc._width);
	}
	
	function createChildren():Void
	{
		var styleColor1:Number=Number(getPriorityValue("color1", gradient1_rgb) );
		var styleColor2:Number=Number(getPriorityValue("color2", gradient2_rgb) );
	
	
		var c1a:Color=new Color(p1_mc.p1_mc);
		var c1b:Color=new Color(p1_mc.p2_mc);
		var c2:Color=new Color(bg_mc);
		
		
		
		c1a.setRGB(styleColor1);c1b.setRGB(styleColor1);
		c2.setRGB(styleColor2);
		
		
		_height=Number(getPriorityValue("busyHeight",_height));
		

	}
	
	
	/*
	*	@description	looks for a value for prop in the local CSS map, if not found, return the defaultValue
	*	@param prop	The name of the property to check. ex: "fontFamily"
	*	@param defaultValue	The default value that is returned if there is no custom value.
	*	@see com.eea.styling.css.ComponentCSS 
	*	@return	Void
	*/	
	public function getPriorityValue(prop:String, defaultValue:Object):Object
	{
		var styleVal=getStyle(prop);	
		if(styleVal!=undefined && styleVal!=null){return styleVal;}else{return defaultValue;}
	}

}