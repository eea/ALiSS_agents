	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissApplication is the core logic controller 
				for the SmartSearch application.
*/
	
import mx.core.View;
import com.eea.projects.aliss.application.AlissApplication;
import flash.filters.DropShadowFilter;
import mx.controls.Loader;
import mx.controls.Button;
import TextField.StyleSheet;
import mx.utils.Delegate;
	

class com.eea.projects.aliss.views.RelatedItemPreview
extends mx.core.View{
	
	/*
	@author			Tor Kristensen	tor.kristensen@tietoenator.com
	@version		1.2
	@description	AlissApplication is the core logic controller 
					for the SmartSearch application.
	*/
	
	private var _VERSION						:String = "1.0.2";
	private var _PRODUCT						:String = "RelatedItemPreview";
	
	static var symbolName:String = "RelatedItemPreview";
    static var symbolOwner:Object = RelatedItemPreview;
    var className:String = "RelatedItemPreview";
    

	private var __data:Object;
	private var requestedImageURL:String;
	public var img_ldr:Loader;
	public var pct_txt:TextField;
	public var border_mc:MovieClip;
	private var __hasPreviewImage:Boolean=false;
	//---------------------------------------------
	function RelatedItemPreview(){
		super();
	}
	//---------------------------------------------
	function init():Void
	{
		super.init();
	}
	//---------------------------------------------
	function createChildren():Void
	{
		super.createChildren();
		

		
		//IMAGE LOADER
		var img_ldr_cfg:Object={};
		img_ldr=Loader(this.createChild(Loader, "img_ldr",img_ldr_cfg));
		img_ldr.autoLoad = true;
		img_ldr.scaleContent=true;
		
		//img_ldr.setSize(100,200);
		img_ldr.setStyle("styleName","RelatedItemPreview_PreviewImage");

		
		//PROGRESS
		var cfg:Object={autoSize:"center",wordWrap:false,multiLine:false,html:true,border:false};
		pct_txt=this.createLabel("pct_txt", getNextHighestDepth(), " ");
		for(var prop:String in cfg){pct_txt[prop]=cfg[prop];}
		pct_txt.setStyle("styleName","RelatedItemPreview_Progress");
		
		//DROPSHADOW
		var filter:DropShadowFilter = makeStyledDropShadow(
											0, 
											0, 
											0x000000, 
											.30, 
											8, 
											8, 
											2, 
											3, 
											false, 
											false, 
											false);

		filters=[filter];
		doLater(this,"createListeners");
	}
	function createListeners(){
		img_ldr.addEventListener("complete",Delegate.create(this,onPreviewComplete));
		img_ldr.addEventListener("progress",Delegate.create(this,onPreviewProgress));
		img_ldr.addEventListener("error",Delegate.create(this,onPreviewError));

	}
	//---------------------------------------------
	function onPreviewComplete(e:Object)
	{
	
		
		trace("onPreviewComplete "+newline+"	"+requestedImageURL+newline+"	"+img_ldr['checkThis']+newline+"	"+img_ldr.__contentPath);
			trace("	disp - complete");
			
			dispatchEvent({type:'onPreviewComplete',target:this});
			
		if(img_ldr['checkThis']!=requestedImageURL){trace("OOOOK!");return;}
		
		img_ldr._visible=pct_txt._visible=false;
		img_ldr.contentHolder._visible=true;
		
		
		img_ldr.invalidate();
		
		invalidate();
		
		doLater(this,"showPreviewImage");
		
		
	}
	//---------------------------------------------
	private function showPreviewImage():Void
	{
		img_ldr._visible=true;
	}
	//---------------------------------------------
	function onPreviewProgress(e:Object)
	{
		pct_txt.htmlText="<p>"+Math.floor(e.target.percentLoaded)+"%</p>";	
	}
	//---------------------------------------------
	function onPreviewError(e:Object)
	{
		pct_txt._visible=false;
	}
	//---------------------------------------------
	
	//---------------------------------------------
	function draw():Void
	{
		super.draw();

		
		//_visible=__data!=undefined;
	}
	//---------------------------------------------
	function setSize(w:Number,h:Number):Void{
		//if(w<(title_txt._width+title_txt._x)){w=_width;}
		//if(h<(snippet_txt._y+snippet_txt._height)){h=_height;}
		super.setSize(w,h);
	}
	//---------------------------------------------
	function size():Void
	{
		super.size();
		var offsetX:Number;
		var offsetY:Number=0;
		var offsetBorder:Number=Number(this.getStyle("borderOffset"));
		var paddedWidth:Number=width-(offsetBorder*2);
		var paddedHeight:Number=height-(offsetBorder*2);
		
		
		
		

		
		if(__hasPreviewImage){
			img_ldr.move(offsetBorder,offsetBorder);
			img_ldr.setSize(paddedWidth,paddedHeight);
			pct_txt.width=paddedWidth
			pct_txt.height=pct_txt.getTextFormat().getTextExtent("99%",pct_txt._width).textFieldHeight;
			pct_txt.move(
				int((width/2)-(pct_txt._width/2)),
				int(img_ldr._y+(img_ldr.height/2))
				);
			offsetY=img_ldr._height+img_ldr._y+5;
			
		}else{
			img_ldr.move(offsetBorder,offsetY);
			img_ldr.setSize(paddedWidth,1);
			offsetY=offsetBorder;
		}
		
		
		
/*
		border_mc.setSize(width,
		go_btn._y+go_btn.height+Math.max(5,offsetBorder));
		border_mc.invalidate();*/
		//_parent.positionPreview();
		//doLater(_parent,"positionPreview");
	}
	//---------------------------------------------
	function click(){
		getURL(__data.url);
	}
	//---------------------------------------------
	function hide(){
		_visible=false;
	}
	//---------------------------------------------
	//function onRelease(){super.onRelease();click();}
	//function onRollOut(){super.onRollOut();hide();}
	//function onDragOutside(){hide();}	
	//function onReleaseOutside(){super.onReleaseOutside();hide();}
	//---------------------------------------------
	public function get data():Object
	{
		return __data;
	}
	public function set data(d:Object):Void
	{
		_visible=false;
		__data=d;
		//snippet_txt.htmlText=__data.snippet;
		//title_txt.htmlText=__data.title;
		
		hasPreviewImage=(__data.preview_img!=undefined )&& (__data.preview_img!="undefined");
		//trace("HASPREVIEW-->"+(__data.preview_img!=undefined )+" "+(__data.preview_img!="undefined"));
		img_ldr._visible=hasPreviewImage;
		
		if(hasPreviewImage)
		{
			requestedImageURL=__data.preview_img;
			img_ldr.load(__data.preview_img);
			img_ldr['checkThis']=requestedImageURL;
			pct_txt._visible=true;
			pct_txt.text="Loading preview...";
		}
		//trace("LOAD PREVIEW:"+__data.preview_img);

		invalidate();
	}
	//---------------------------------------------
	//---------------------------------------------
	public function get hasPreviewImage():Boolean
	{
		return __hasPreviewImage;
	}
	public function set hasPreviewImage(b:Boolean):Void
	{
		__hasPreviewImage=b;		
		invalidate();
	}
	//---------------------------------------------
	public function makeStyledDropShadow(
			distance:Number,
			angle:Number,
			color:Number,
			alpha:Number,
			blurX:Number,
			blurY:Number,
			strength:Number,
			quality:Number,
			inner:Boolean,
			knockout:Boolean,
			hideObject:Boolean):DropShadowFilter
	{
			
			return new DropShadowFilter(
				Number(getPriorityValue("dropShadowDistance",distance)),
				Number(getPriorityValue("dropShadowAngle",angle)),
				Number(getPriorityValue("dropShadowColor",color)),
				Number(getPriorityValue("dropShadowAlpha",alpha)),
				Number(getPriorityValue("dropShadowBlurX",blurX)),
				Number(getPriorityValue("dropShadowBlurY",blurY)),
				Number(getPriorityValue("dropShadowStrength",strength)),
				Number(getPriorityValue("dropShadowQuality",quality)),
				(getPriorityValue("dropShadowInner",inner))=="true",
				(getPriorityValue("dropShadowKnockout",knockout)=="true"),
				(getPriorityValue("dropShadowHideObject",hideObject))=="true"
			);
			
	}
	//---------------------------------------------
	public function getPriorityValue(prop:String, defaultValue:Object):Object
	{
		var styleVal=getStyle(prop);
		if(styleVal!=undefined && styleVal!=null){return styleVal;}else{return defaultValue;}
	}
	//---------------------------------------------
}
