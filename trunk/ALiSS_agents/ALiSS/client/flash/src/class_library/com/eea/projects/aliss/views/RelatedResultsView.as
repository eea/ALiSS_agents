	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	RelatedResultsView is the display View for the RelatedResults returned by the Webservice
*/
	
import mx.core.View;
import mx.controls.List;
import mx.controls.Button;
import com.eea.projects.aliss.views.DefinitionView;
import com.eea.projects.aliss.events.AlissEvents;
import com.eea.projects.aliss.application.AlissApplication;
import com.eea.utilities.logging.Logger;
import com.eea.projects.aliss.views.RelatedItemPreview;

class com.eea.projects.aliss.views.RelatedResultsView
extends View {
	
	static var symbolName:String = "RelatedResultsView";
    static var symbolOwner = com.eea.projects.aliss.views.RelatedResultsView;
    var className:String = "RelatedResultsView";
	
	//Boolean flag, true if 1st draw event has passed
	private var isInitialDrawComplete=false;
	//Number ID of the current preview Img
	private var curPreviewNum:Number;
	
	//List Control that displays the RelatedResults
	public var relatedResults_ls:List;
	
	//Definition Control, displays.... Definitions
	public var definition_dv:DefinitionView;
	
	//RelatedItemPreview handles loading external preview images
	public var relatedItemPreview_rip:RelatedItemPreview;
	
	//Number with default Height for the preview image
	public var previewDefaultHeight:Number;
	
	//Button control for "see more"
	public var seeMore1_btn:Button;
	
	//Button control for "see more"
	public var seeMore2_btn:Button;
	
	//Pointer to the Controller for this View
	public var controller:Object;
	
	//Object with x,y properties for the Mouse
	private var mouseLoc:Object;
	
	//Private Boolean, true if the Preview is _visible
	private var __isPreviewVisible:Boolean;
	
	//private internal ID for interval callbacks
	private var intervalID:Number;
	
	//private iunternal used for flagging preview visibility
	private var isPreviewDesired:Boolean=false;

	//------------------------------------------------------------------------------
	/*
	*	@description	Constructor for the RelatedResultsView
	*	@return	RelatedResultsView
	*/
	function RelatedResultsView(){
		super();
	}
	/*
	*	@description	init(9 function
	*	@return	Void
	*/	
	function init():Void
	{
	super.init();
		
	}
	//------------------------------------------------------------------------------	
	/*
	*	@description	Creates child objects
	*	@return	Void
	*/
	function createChildren():Void{
		
			
		var pdh=(getStyle("previewDefaultHeight"));
		if(pdh!=undefined){previewDefaultHeight=Number(pdh);}else{previewDefaultHeight=250;}
		Logger.logIt("CSS previewDefaultHeight="+pdh);
		Logger.logIt("previewDefaultHeight="+previewDefaultHeight);
		
		_visible=false;
		super.createChildren();
		
		definition_dv=DefinitionView(
			this.createChild(
				com.eea.projects.aliss.views.DefinitionView,
				"definition_dv"			
				)
			);
			
		seeMore1_btn=Button(
				this.createChild(
				mx.controls.Button, 
				"seeMore1_btn",
				{label:AlissApplication.getConfig("see_more_def_txt")}
				)
			);
		
		relatedResults_ls=List(
			this.createChild(
				mx.controls.List, 
				"relatedResults_ls",
				{controller:this,vScrollPolicy:"auto"}				
				)
			);
			
		seeMore2_btn=Button(
				this.createChild(
				mx.controls.Button, 
				"seeMore2_btn",
				{label:AlissApplication.getConfig("see_more_def_txt")}
				)
			);
			

		
		var color1:Number=this.getStyle("rowColor1");
		var color2:Number=this.getStyle("rowColor2");
		var arc:Array=cssArrayToNumberArray(getStyle("alternatingRowColors"));
		
		if(arc.length>1){
			relatedResults_ls.setStyle("alternatingRowColors",arc);
		}else if(color1 && color2){
			relatedResults_ls.setStyle("alternatingRowColors",[color1,color2]);
		}else if(color1){
			relatedResults_ls.setStyle("backgroundColor",color1);
		}else if(color2){
			relatedResults_ls.setStyle("backgroundColor",color2);
		}
		
		var selCol:Number=this.getStyle("selectionColor");
		if(selCol){
			relatedResults_ls.setStyle("selectionColor ",selCol);		
			
		}
		var rolCol:Number=this.getStyle("rollOverColor");
		if(rolCol){
			relatedResults_ls.setStyle("rollOverColor ",0xF5821F);					
		}
		relatedResults_ls.setStyle("cellRenderer","RelatedResultItemClip");
		
		
		var rH:Number=Number(this.getStyle("rowHeight"));
		//trace("&&&*"+rH);
		if(rH){
			relatedResults_ls.rowHeight=rH;		
		}else{
			relatedResults_ls.rowHeight=70;		
		}
		
		
			
		relatedResults_ls.move(10,definition_dv._height);
		
	
		
		
		relatedItemPreview_rip=RelatedItemPreview(this.createChild(
				RelatedItemPreview, 
				"relatedItemPreview_rip",
				{_visible:false}	
				));
		
		relatedItemPreview_rip.move(20,20);
		setupListeners();
//		size();
		
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	sets the size of the View
	*	@param w	The new Width
	*	@param h	The new Height
	*	@return	Void
	*/
	function setSize(w:Number,h:Number):Void{
			super.setSize(w,h);
			
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Size event called after invalidate()
	*	@return	Void
	*/
	function size():Void
	{
		super.size();
		
		definition_dv.setSize(width,200);
		var occupiedH:Number=Math.floor(
			definition_dv._height+
			(seeMore1_btn.height*2)+10
			);

		var scrollheight:Number=Math.floor(height-occupiedH)-(seeMore2_btn.height);
		var maxListHeight:Number=(relatedResults_ls.dataProvider.length+.1)*relatedResults_ls.rowHeight;
		var isRelatedListNeeded:Boolean=relatedResults_ls.dataProvider.length>0;
		
		var w:Number=Math.floor(width-20);
		var h:Number=Math.floor( Math.min( maxListHeight,scrollheight ) );
		
		relatedResults_ls.setSize(0,0);
		if(isRelatedListNeeded){
			relatedResults_ls.setSize(w,h);
		}
		
		seeMore1_btn.setSize(150,seeMore1_btn.height);
		seeMore2_btn.setSize(150,seeMore2_btn.height);
			
		
		
		if(!isInitialDrawComplete){isInitialDrawComplete=true;_visible=true;}
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Layout method that handles positioning ans sizing of the UI for this control
	*	@return	Void
	*/
	function doLayout():Void
	{
		/*
		Logger.logIt("----------RelatedRV DoLayout S----------");
		Logger.logIt("	w:"+_width+" h:"+_height);
		*/
		var pad:Number=5;
		var padX:Number=10;
		var posY:Number=0;
		
		//relatedItemPreview_rip.move(int(width*.1),0);
		
		var isRelatedListNeeded:Boolean=relatedResults_ls.dataProvider.length>0;
		seeMore2_btn.enabled=relatedResults_ls.enabled=
		seeMore2_btn._visible=relatedResults_ls._visible=isRelatedListNeeded;
		
		definition_dv.move(0,0);
		posY+=definition_dv._height+pad+pad;
		
		
		seeMore1_btn.move(width-seeMore1_btn.width-padX,posY);
		posY+=seeMore1_btn.height+pad;
		
		if(isRelatedListNeeded)
		{
			relatedResults_ls.move(10,posY);
		
			posY+=relatedResults_ls.height+pad;			
			
			
			seeMore2_btn.move(width-seeMore2_btn.width-padX, height-seeMore2_btn.height-10);
			posY+=seeMore2_btn.height+pad;
			posY=height;
		}else{
			seeMore2_btn.move(0,0);
			relatedResults_ls.move(0,0);
			border_mc.setSize(width,posY+seeMore1_btn.height+10);
		}
	/*
		var b:Object=relatedResults_ls.getBounds(_root);
		Logger.logIt("	RelatedRV.relatedResults_ls.bounds="+b.yMin+" ,"+b.yMax);
		b=seeMore2_btn.getBounds(_root);
		Logger.logIt("	RelatedRV.seeMore2_btn.bounds="+b.yMin+" ,"+b.yMax);
		b=getBounds(_root);
		Logger.logIt("	RelatedRV.bounds="+b.yMin+" ,"+b.yMax);
		Logger.logIt("----------RelatedRV DoLayout E----------");
		*/
	}
	//------------------------------------------------------------------------------

	/*
	*	@description	Creates listeners for events
	*	@return	Void
	*/
	private function setupListeners():Void
	{
		relatedResults_ls.addEventListener("changeHACK",this);
		relatedResults_ls.addEventListener("scroll",this);
		
		definition_dv.addEventListener("click",this);
		
		seeMore1_btn.addEventListener("click",this);
		seeMore2_btn.addEventListener("click",this);
		relatedItemPreview_rip.addEventListener("onComponentResize",this);
		relatedItemPreview_rip.addEventListener("onPreviewComplete",this);
		
		Logger.logIt("LISTEN;"+controller+" "+definition_dv);
		controller.addEventListener(AlissEvents.EVENT_SERVICE_GET_TOP_PAGES,definition_dv);
	}
	/*
	*	@description	Method that listens for the smartSearch_GetTopPagesForTermsResult Event
	*	@param e	An Event object with data.results_array and data.definition.
	*	@return	Void
	*/
	public function smartSearch_GetTopPagesForTermsResult(e:Object):Void
	{
		relatedResults_ls.dataProvider=e.data.results_array;		
		
		definition_dv.definition=e.data.definition;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	startPreviewInterval
	*	@param n	The index of the item to preview
	*	@param rowNum	The row index of the item (independant of scrollIndex, allows finding the y of the row).
	*	@return	Void
	*/
	public function startPreviewInterval(n:Number,rowNum:Number):Void
	{
		//trace(">startPreviewInterval");
		hidePreview();
		clearInterval(intervalID);
		
		mouseLoc={x:_xmouse,y:_ymouse,rowNum:rowNum,n:n};
		
		var duration:Number=Number(AlissApplication.getConfig("preview_show_delay"));
		intervalID=setInterval(
			this,'showPreview',
			duration
			);
		
		
		//trace("RRV startPreviewInterval "+arguments+" in "+duration+" msec"); 
		
	
		
		this['onMouseMove']=internalMouseMove;
			Mouse.addListener(this);
	}
	
	/*
	*	@description	Displays the preview control
	*	@return	Void
	*/
	public function showPreview():Void{
		//trace(">showPreview");
		clearInterval(intervalID);
		relatedItemPreview_rip._visible=false;

		
		curPreviewNum=mouseLoc.n;
		var data:Object=relatedResults_ls.dataProvider[curPreviewNum];
		
		if( (data.preview_img==undefined ) || (data.preview_img=="undefined"))
		{
			hidePreview();
			return;
		}
		data['n']=mouseLoc.n;
		relatedItemPreview_rip.setSize(relatedResults_ls.width-18-20,previewDefaultHeight);
		relatedItemPreview_rip.data=data;
		
		isPreviewDesired=true;
		
		//doLater(this,"positionPreview");
		positionPreview();
	}
	
	function onPreviewComplete(e:Object):Void
	{
		//trace(">RRV complete");
		//trace("	"+relatedItemPreview_rip.data['n']+" "+mouseLoc.n);
		
		if(isPreviewDesired && e.target==relatedItemPreview_rip && relatedItemPreview_rip.data.n==mouseLoc.n)
		{
			//relatedItemPreview_rip._visible=true;
			isPreviewDesired=false;
			doLater(this,"showStub");
		}
	}
	function showStub(){relatedItemPreview_rip._visible=true;}
	//------------------------------------------------------------------------------
	/*
	*	@description	Hides the preview control
	*	@return	Void
	*/
	public function hidePreview():Void{
		isPreviewDesired=false;
		clearInterval(intervalID);
	
		curPreviewNum=-1;
		Mouse.removeListener(this);	
		relatedItemPreview_rip.move(0,0);
		//relatedItemPreview_rip.data={};
		relatedItemPreview_rip._visible=false;
		delete onMouseMove;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Called onMouseMove, if mouse has moved >50px calls hidePreview()
	*	@return	Void
	*/
	public function internalMouseMove():Void
	{
		//if(!isPreviewVisible){return;}
	
		var xdist:Number=mouseLoc.x-_xmouse;
		var ydist:Number=mouseLoc.y-_ymouse;
		var dist:Number=Math.round(Math.sqrt((xdist*xdist) + (ydist*ydist)));
		//trace("DIST:"+dist);
		if(dist>70)
		{
			//trace("MOUSE TOO FAR "+dist+" "+xdist+" "+ydist);
			hidePreview();
			return;
		}
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Places the preview control correctly, handles whether the preview pops up or down
	*	@return	Void
	*/
	public function positionPreview():Void{
		//trace("positionPreview() previewDefaultHeight:"+previewDefaultHeight);
		//if(isPreviewVisible){
			
			var newY:Number;
			var newX:Number=relatedResults_ls.x+1+10;
			
			var ripH:Number=previewDefaultHeight;
			var hi_n:Number=mouseLoc.rowNum;
			var buff:Number=relatedResults_ls.rowHeight;
			var ym:Number=relatedResults_ls._y+(relatedResults_ls.rowHeight*hi_n);
			
			var f:Object=relatedItemPreview_rip.filters[0];

			var isPopAbove:Boolean=ripH+ym+y >= height-relatedResults_ls.rowHeight;
			
			//Logger.logIt("RIP_> H:"+(ripH+ym+y)+" Y:"+_y+" LIM:"+height+" STAGE:"+Stage.height+" isPopAbove="+isPopAbove);
			
			if(isPopAbove){
				ym+=4;
				relatedItemPreview_rip.setStyle("borderStyle","roundedTop");
				f.angle=-90;
				newY=ym-ripH+2;
				if(newY-relatedItemPreview_rip.height<0){
					//Logger.logIt("AM TOO TALL!");
					
					
					var adjustedH:Number=Math.min(previewDefaultHeight,ym);
					relatedItemPreview_rip.setSize(
						relatedItemPreview_rip.width,
						adjustedH
						);
						//Logger.logIt("	***>SIZE RIP TO:"+relatedItemPreview_rip.width+", "+adjustedH);
					newY=ym-adjustedH;
				}
			}else{
				f.angle=90;
				relatedItemPreview_rip.setStyle("borderStyle","roundedBottom");
				newY=ym+buff;
			}
			relatedItemPreview_rip.filters=[f];
			//Logger.logIt("	***>POS RIP AT:"+newX+", "+newY);
			
			relatedItemPreview_rip.move(newX,newY);
			
		//}
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Depreciated
	*	@depreciated
	*	@return	Void
	*/
	public function changeHACK(e:Object):Void	
	{	
		dispatchEvent(
			{
				type:AlissEvents.EVENT_RELATEDITEM_SELECTION,
				index:e.target.selectedIndex,
				item:e.target.selectedItem
			}
		);
	}	
	//------------------------------------------------------------------------------
	/*
	*	@description	Scroll event handler
	*	@param e	Standard event object
	*	@return	void
	*/
	public function scroll(e:Object):Void
	{	
		if( 
			(e.target==relatedResults_ls)){
				hidePreview();
		}
	
	}
	/*
	*	@description	Click event handler
	*	@param e	Standard event object
	*	@return	void
	*/
	public function click(e:Object):Void
	{	
		if( 
			(e.target==seeMore2_btn)||
			(e.target==seeMore1_btn)||
			(e.target==definition_dv)
		){
				e.type=AlissEvents.EVENT_SEEALLRESULTS_SELECTION;
				dispatchEvent(e);
		}else{
			hidePreview();
		}
	
	}
	/*
	*	@description	onComponentResize event handler
	*	@param e	Standard event object
	*	@return	Void
	*/
	public function onComponentResize(e:Object):Void
	{
		hidePreview();
	}
	//------------------------------------------------------------------------------
	
	
	
	
	//------------------------------------------------------------------------------
	//UTIL
	//------------------------------------------------------------------------------	
	/*
	*	@description	Draws a rect
	*	@param mc	The MovieClip to draw in
	*	@param a	The alpha of the fill
	*	@param fillColor	The colro to fill the rect
	*	@param x	X value of the upper-left color
	*	@param y	Y value of the upper-left color
	*	@param w	Width of the rect
	*	@param h	Height of the rect			
	*	@return	Void
	*/
	 function drawRect(mc, a,fillColor, x, y, w, h) {
		 
		mc.clear();
		mc.beginFill(fillColor,a);
		mc.moveTo(x, y);
		mc.lineTo(x+w, y);
		mc.lineTo(x+w, y+h);
		mc.lineTo(x, y+h);
		mc.lineTo(x, y);
		mc.endFill();
	}
	//------------------------------------------------------------------------------
	/*
	*	@description	Splits a CSS string into an Array
	*	@param str	The string to split
	*	@return	Array
	*/
    private function cssArrayToArray(str:String):Array
    {
    	return str.substr(1,str.length-2).split(",");
    }
	//------------------------------------------------------------------------------
	/*
	*	@description	Converts a CSS string array into numerical values
	*	@param str	The string to convert
	*	@return	Array
	*/
    private function cssArrayToNumberArray(str:String):Array
    {
    	var res:Array=cssArrayToArray(str);
    	for(var n:Number=0;n<res.length;n++){
    		res[n]=Number(res[n]);
    	}
    	return res;
    }
    //------------------------------------------------------------------------------
	/*
	*	@description	getter for isPreviewVisible
	*	@return	Boolean
	*/
    public function get isPreviewVisible():Boolean{return relatedItemPreview_rip._visible;}
    
	/*
	*	@description	Returns height the control required for layout
	*	@return	Number
	*/
    public function getLayoutHeight():Number
    {
    	return 200 + (relatedResults_ls.dataProvider.length*relatedResults_ls.rowHeight);
    }
    
    
    
}