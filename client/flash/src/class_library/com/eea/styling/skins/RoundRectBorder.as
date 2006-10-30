/**
 * @author krisutor
 */
 import mx.styles.CSSStyleDeclaration;
 import mx.core.ext.UIObjectExtensions;
 import mx.skins.RectBorder;
 
class com.eea.styling.skins.RoundRectBorder 
extends  mx.skins.RectBorder{
	
	
 	static var symbolName:String = "RectBorder";
    static var symbolOwner:Object = RoundRectBorder;
    var className:String = "RoundRectBorder";
	
	private static var STYLE_ROUNDED:String="rounded";
	private static var STYLE_ROUNDED_T:String="roundedTop";
	private static var STYLE_ROUNDED_L:String="roundedLeft";
	private static var STYLE_ROUNDED_R:String="roundedRight";
	private static var STYLE_ROUNDED_B:String="roundedBottom";
	private static var STYLE_NONE:String="none";
	private static var STYLE_SOLID:String="solid";
	private static var STYLE_INSET:String="inset";
	private static var STYLE_OUTSET:String="outset";
	private static var STYLE_DEFAULT:String="default";
	private static var STYLE_ALERT:String="alert";
	private static var STYLE_MENUBORDER:String="menuBorder";
	private static var STYLE_FALSEDOWN:String="falsedown";
	private static var STYLE_FALSEOVER:String="falseover";
	private static var STYLE_FALSEUP:String="falseover";
	private static var STYLE_TRUEUP:String="trueup";
	private static var STYLE_TRUEDOWN:String="truedown";
	private static var STYLE_TRUEROLLOVER:String="truerollover";
	
	private static var STYLE_GRADIENT_LINEAR:String="linear";
	private static var STYLE_GRADIENT_RADIAL:String="radial";	
	
	private static var TYPE_OBJECT:String="object";
	private static var TYPE_BOX:String="box";

	private var radiusStyleName:String="borderRadius";
	private var gradientTypeStyleName:String="borderGradientType";
	private var gradientColorStyleName:String="borderGradientColor";
	private var gradientColorRatioStyleName:String="borderGradientColorRatio";
	private var gradientAngleStyleName:String="borderGradientAngle";
	private var gradientAlphaStyleName:String="borderGradientAlpha";

	private var gradientStrokeColor:String="borderStrokeColor";
	private var gradientStrokeThickness:String="borderStrokeThickness";
	private var gradientStrokeAlpha:String="borderStrokeAlpha";
	private var gradientStrokeStyle:String="borderStrokeStyle";
	
	private var offsetStyleName:String="borderOffset";
	

/**
* @private
* list of color style properties that affect this component
*/
	private var colorList:Object = { highlightColor: 0, borderColor: 0, buttonColor: 0, shadowColor: 0 };

/**
@private
* constructor
*/
	function RectBorder()
	{
	}

/**
* @private
* init variables.  Components should implement this method and call super.init() at minimum
*/
	function init(Void):Void
	{
		super.init();
	}

/**
* @private
* return the thickness of the border edges
* @return Object	top, bottom, left, right thickness in pixels
*/
	function getBorderMetrics(Void):Object
	{
		if (offset == undefined)
		{
			var b:String = getStyle(borderStyleName);
			offset = 0;
			if (b == STYLE_SOLID)
				offset = 1;
			else if (b == STYLE_INSET || b == STYLE_OUTSET)
				offset = 2;
		}
		if (getStyle(borderStyleName) == STYLE_MENUBORDER )
 		{
 			__borderMetrics = { left: 1, top: 1, right: 2, bottom:1 };
 			return __borderMetrics;
 		}

		return super.getBorderMetrics();
	}

/**
* @private
* draw the border, either 3d or 2d or nothing at all
*/
	function drawBorder(Void):Void
	{
		////trace(newline+"=====================================");
		var z:CSSStyleDeclaration = _global.styles[className];
		if (z == undefined)
			z = _global.styles.RectBorder;
		var b:String = getStyle(borderStyleName);
		var c:Number = getStyle(borderColorName);
		if (c == undefined) c = z[borderColorName];
		var d:Number = getStyle(backgroundColorName);
		if (d == undefined) d = z[backgroundColorName];
		if (b != "none")
		{
			var f:Number = getStyle(shadowColorName);
			if (f == undefined) f = z[shadowColorName];
			var g:Number = getStyle(highlightColorName);
			if (g == undefined) g = z[highlightColorName];
			var h:Number = getStyle(buttonColorName);
			if (h == undefined) h = z[buttonColorName];
		}
		offset = 0;

		clear();

		_color = undefined;
		////trace("HACK>"+borderStyleName+">"+className+">"+b);
		if(b.substr(0,7)==STYLE_ROUNDED){	
			
			clear();
			
			var radius:Number=getStyle(radiusStyleName);
			if(!radius){radius=6;}
		
			var gC=getStyle("backgroundColor");
			var gC_array=getStyle(gradientColorStyleName);
			if(gC_array!=undefined)
			{
				gC_array=cssArrayToArray(gC_array);
			}
			var gCr=getStyle(gradientColorRatioStyleName);
			if(gCr!=undefined)
			{
				gCr=cssArrayToArray(gCr);
			}
			
			var gType:String=getStyle(gradientTypeStyleName);
			
			var gAngle=Number( getStyle("styleName").getStyle("borderGradientAngle") );
			//getStyle(gradientAngleStyleName));
			////trace("GANGLE:"+gAngle);
			////trace("ANGLE OF:"+getStyle("styleName")+" "+getStyle(gradientAlphaStyleName)+" "+className)
			////trace("TEST:"+(getStyle("styleName").getStyle("borderGradientAngle")));
			
		//for(var s:String in this){//trace("		"+s+" "+this[s]);}
			var gAlpha=Number(getStyle(gradientAlphaStyleName));
			var colors;
			if(gC_array.length>1){colors=gC_array;}else{colors=gC;}
			
			var ratios;
			if(gCr.length>1){ratios=gCr;}else{ratios=undefined;}
			
			var isGradient:Boolean=(gCr.length>1 && gC_array.length>1);
			////trace("	"+b+" ***> "+isGradient);
			
			

			
			if(b==STYLE_ROUNDED && !isGradient){
				offset=radius/2;
				////trace("DERAIL");
				drawRoundRect(0,0,width,height,radius,colors,100,0);
				return;
				
			}else if(b==STYLE_ROUNDED_B){
				var cornerRadii:Object={br:radius,bl:radius,tl:0,tr:0};
				offset=radius/2;
				
			}else if(b==STYLE_ROUNDED_L){
				var cornerRadii:Object={br:0,bl:radius,tl:radius,tr:0};
				offset=radius/2;
				
			}else if(b==STYLE_ROUNDED_R){
				var cornerRadii:Object={br:radius,bl:0,tl:0,tr:radius};			
							
			}else if(b==STYLE_ROUNDED_T){
				var cornerRadii:Object={br:0,bl:0,tl:radius,tr:radius};			
					
			}else{
				var cornerRadii:Object={br:0,bl:0,tl:0,tr:0};		
			}
			
			var css_offset:Number=getStyle(offsetStyleName);
			if(css_offset){
				offset=css_offset;
			}else{
				offset=radius/2;	
			}
			
			////trace("isGradient:"+isGradient);
			
			if(isGradient){
				//set defaults if params are missing
				if(!gType){gType=STYLE_GRADIENT_LINEAR;}
				if(isNaN(gAngle) || gAngle==undefined){gAngle=90;}
				if(!gAlpha){gAlpha=100;}
				//trace("----------------");
				//trace("Draw Complex:"+0+", "+0+", "+width+", "+height+", "+cornerRadii+", ["+colors+"], "+
				//gAlpha+", gAngle:"+gAngle+", "+gType+",["+ratios+"]");
				//trace("SHUOLD USE A:"+getStyle("styleName").getStyle("borderGradientAngle")+" real:"+gAngle);
				
				drawRoundRect(0,0,width,height,cornerRadii,colors,gAlpha,gAngle,gType,ratios);
				//trace("----------------");
			}else{
				//trace("----------------");
				//trace("Draw Simple");
				drawRoundRect(0,0,width,height,cornerRadii,gC,100);
				//trace("----------------");
			}
				return;
		}
		if (b == "none")
		{
		}
		
		else if (b == STYLE_INSET || b == STYLE_DEFAULT || b == STYLE_ALERT|| b == STYLE_FALSEDOWN)
		{
			_color = colorList;
			offset = 2;
			draw3dBorder(h, f, g, c);

		}
		else if (b == STYLE_OUTSET || b == STYLE_FALSEUP|| b == STYLE_FALSEOVER)
		{
			_color = colorList;
			offset = 2;
			draw3dBorder(c, h, f, g);

		}
		else if (b == STYLE_TRUEROLLOVER || b == STYLE_TRUEDOWN)
		{
			_color = colorList;
			offset = 2;
			draw3dBorder(h, f, g, c);

		}
		else //if ((b == "solid") || (b == undefined))
		{
			var w:Number = width;
			var h:Number = height;
			offset = 1;
			beginFill(c);
			drawRect(0,0,w,h);
			drawRect(1,1,w-1,h-1);
			endFill();
			_color = borderColorName;
		}

		var o:Number = offset;

		beginFill(d);
		drawRect(o,o,width-o,height-o);
		endFill();
	//trace("= = = = = = = = = = = = "+newline);
	}

/**
* @private
* draw a 3d border
*/
	function draw3dBorder(c1:Number, c2:Number, c3:Number, c4:Number):Void
	{
		var w:Number = width;
		var h:Number = height;

		beginFill(c1);
		drawRect(0,0,w,h);
		drawRect(0,0,w-1,h-1);
		endFill();
		beginFill(c2);
		drawRect(0,0,w,h-1);
		drawRect(1,1,w,h-1);
		endFill();
		beginFill(c3);
		drawRect(1,1,w-1,h-1);
		drawRect(1,1,w-2,h-2);
		endFill();
		beginFill(c4);
		drawRect(1,1,w-1,h-2);
		drawRect(2,2,w-1,h-2);
		endFill();
	}
	static function classConstruct():Boolean
	{
		UIObjectExtensions.Extensions();
		_global.styles.rectBorderClass = RoundRectBorder;
		_global.skinRegistry["RectBorder"] = true;
		return true;
	}
	static var classConstructed:Boolean = classConstruct();
	static var UIObjectExtensionsDependency = UIObjectExtensions;










    
	// drawRoundRect
	// x - x position of  fill
	// y - y position of  fill
	// w - width of  fill
	// h  - height of  fill
	// r - corner radius of fill :: number or object {br:#,bl:#,tl:#,tr:#}
	// c - hex color of fill :: number or array [0x######,0x######]
	// alpha - alpha value of fill :: number or array [0x######,0x######]
	// rot - rotation of fill :: number or matrix object  {matrixType:"box",x:#,y:#,w:#,h:#,r:(#*(Math.PI/180))}
	// gradient - type of gradient "linear" or "radial"
	// ratios - (optional :: default  [0,255]) - specifies the distribution of colors :: array [#,#];
	function drawRoundRect(x,y,w,h,r,c,alpha,rot,gradient,ratios)
	{
		//trace("DRAW BORDER:"+arguments);
		
					//gradientStrokeColor,gradientStrokeThickness,gradientStrokeAlpha,gradientStrokeStyle
				var lineColor:Number=Number( getStyle( gradientStrokeColor ) );
				var lineThickness:Number=Number( getStyle( gradientStrokeThickness ) );
				var lineAlpha:Number=Number( getStyle( gradientStrokeAlpha ) );
				var lineStyle:String=getStyle( gradientStrokeStyle );
				
				if(lineColor!=undefined && lineThickness!=undefined){
					if(!isNaN(lineColor)){lineColor=0x000000;}
					if(!isNaN(lineThickness)){lineThickness=0;}
					if(!isNaN(lineStyle)){lineStyle="round";}
					this.lineStyle(lineThickness,lineColor,lineAlpha,true,"none",lineStyle);
				}
			
			
		
		
			if (typeof r == TYPE_OBJECT) {
				var rbr = r.br //bottom right corner
				var rbl = r.bl //bottom left corner
				var rtl = r.tl //top left corner
				var rtr = r.tr //top right corner
			}
			else
			{
				var rbr =  rbl = rtl = rtr = r;
			}
			
			
				
			// if color is an object then allow for complex fills
			if(typeof c == TYPE_OBJECT)
			{
				if (typeof alpha != TYPE_OBJECT)
					var alphas = [alpha,alpha];
				else
					var alphas = alpha;

				if (ratios == undefined)
					var ratios = [ 0, 0xff ];

				var sh = h *.7
				if (typeof rot != TYPE_OBJECT){

					var radians:Number=rot * (Math.PI / 180);
					var matrix = {matrixType:TYPE_BOX, x:0, y:0, w:w, h:h, r:radians };

				}else{
					var matrix = rot;
				}
				
				
				
				
				if (gradient == STYLE_GRADIENT_RADIAL)
					this.beginGradientFill( STYLE_GRADIENT_RADIAL, c, alphas, ratios, matrix );
				else
					this.beginGradientFill( STYLE_GRADIENT_LINEAR, c, alphas, ratios, matrix,"pad" );
				
				//	//trace("MATRIX ROT:"+matrix.r);
				}
				else if (c != undefined)
				{
					this.beginFill (c, alpha);
				}

			// Math.sin and Math,tan values for optimal performance.
			// Math.rad = Math.PI/180 = 0.0174532925199433
			// r*Math.sin(45*Math.rad) =  (r*0.707106781186547);
			// r*Math.tan(22.5*Math.rad) = (r*0.414213562373095);

			//bottom right corner
			r = rbr;
			var a = r - (r*0.707106781186547); //radius - anchor pt;
			var s = r - (r*0.414213562373095); //radius - control pt;
		
			this.moveTo ( x+w,y+h-r);
			this.lineTo ( x+w,y+h-r );
			this.curveTo( x+w,y+h-s,x+w-a,y+h-a);
			this.curveTo( x+w-s,y+h,x+w-r,y+h);
			
			//bottom left corner
			r = rbl;
			var a = r - (r*0.707106781186547);
			var s = r - (r*0.414213562373095);
			this.lineTo ( x+r,y+h );
			this.curveTo( x+s,y+h,x+a,y+h-a);
			this.curveTo( x,y+h-s,x,y+h-r);

			//top left corner
			r = rtl;
			var a = r - (r*0.707106781186547);
			var s = r - (r*0.414213562373095);
			this.lineTo ( x,y+r );
			this.curveTo( x,y+s,x+a,y+a);
			this.curveTo( x+s,y,x+r,y);

			//top right
			r = rtr;
			var a = r - (r*0.707106781186547);
			var s = r - (r*0.414213562373095);
			this.lineTo ( x+w-r,y );
			this.curveTo( x+w-s,y,x+w-a,y+a);
			this.curveTo( x+w,y+s,x+w,y+r);
			this.lineTo ( x+w,y+h-r );

			if (c != undefined)
				this.endFill();
	}
	/**
	 * @description splits a CSS class into key/value (string/string) pairs
	 * @return Array	 */
    private function cssArrayToArray(str:String):Array
    {
    	return str.substr(1,str.length-2).split(",");
    }
    /**
     * @description	Converts string values into numeric values
     * @param	str	The string to operate on
     * @return Array
     *      */
    private function cssArrayToNumberArray(str:String):Array
    {
    	var res:Array=cssArrayToArray(str);
    	for(var n:Number=0;n<res.length;n++){
    		res[n]=Number(res[n]);
    	}
    	return res;
    }
}