/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	ComponentCSS allows importing of CSS at runtime, and applying the loaded styles to global CSS classes.
*/
import mx.core.UIComponent;
import mx.styles.CSSStyleDeclaration;
import TextField.StyleSheet;
import mx.utils.Delegate;

class com.eea.styling.css.ComponentCSS 
extends UIComponent{
	//URL of the CSS file to load
	public var url:String;
	//Reference to the CSS StyleSheet instance
	public var css:StyleSheet;
	//-------------------------------------------------------
	/**
	 * @description	Constructor for a ComponentCSS instance
	 * @param css_url	The url of the CSS file to load	 */
	function ComponentCSS(css_url:String){
		super();
		
		if(css_url!=undefined){
			url=css_url;

		}
	}
	function init():Void{super.init();}
	function createChildren():Void{super.createChildren();}
	function draw():Void{super.draw();}
	//-------------------------------------------------------
	/**
	 * @description The load() method initiates loading the external file. 
	 * @param css_url If supplied, overrides the URL passed to the constructor.	 */
	function load(css_url:String):Void
	{
		if(css_url!=undefined){
			url=css_url;
		}
		css=new StyleSheet();	
		css.onLoad=Delegate.create(this, processCSS);
		css.load(url);
	}
	//-------------------------------------------------------
	/**
	 * @description Serializes the CSS file, and loads them into the _global.styles object. The ComponentCSS instance emits a "complete" event after parsing.
	 * @param	success	Boolean, true if file loaded successfully. 	 */
	private function processCSS(success:Boolean):Void
	{
		var arrStyles:Array;
		var styleProp:String;
		var gStyleDec:Object;
		var styleAttributes:Object;
		
		if(success){
			
			
			arrStyles = css.getStyleNames();
			var len:Number=arrStyles.length;
			
			for(var n:Number=0;n<len;n++){
				
				styleProp=arrStyles[n];

				// Get the components global style.
				gStyleDec =  _global.styles[styleProp];

				// Get the style object containing the style attributes.
				styleAttributes = css.getStyle(styleProp);
				
				
				// If there is no stylesheet, make one.
				if( gStyleDec == undefined){
					
					 gStyleDec = new CSSStyleDeclaration();
					 _global.styles[styleProp]=gStyleDec;
				}
				
	
				// Loop through and apply the attributes to the gloabl style for the given component.
				for(var z:String in styleAttributes)
				{
					if(styleAttributes[z].substr(0,2)=="0x"){
						styleAttributes[z]=Number(styleAttributes[z]);
					}
					
					 var tesT=_global.styles[styleProp].setStyle(z, styleAttributes[z]);
					 gStyleDec.setStyle(z, styleAttributes[z]);
					 //trace(" set: "+styleProp+"."+z+"="+styleAttributes[z]);
					 
				}
			}
			dispatchEvent({type:"complete"});
			
		}else{
			trace("The style sheet failed to laod!");
			dispatchEvent({type:"error"});
		}
			
	}
	//-------------------------------------------------------
	//-------------------------------------------------------
	//-------------------------------------------------------
}