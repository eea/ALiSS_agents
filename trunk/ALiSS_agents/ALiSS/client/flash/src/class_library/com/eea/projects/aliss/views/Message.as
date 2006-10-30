	
/*
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	Message is a View that displays a notification in the Application
*/
	
import mx.core.View;
import com.eea.projects.aliss.application.AlissApplication;

import mx.controls.Button;
import mx.utils.Delegate;

class com.eea.projects.aliss.views.Message
extends mx.core.View{
	
	
	static var symbolName:String = "Message";
    static var symbolOwner:Object = com.eea.projects.aliss.views.Message;
    var className:String = "Message";
    
    public var ok_btn:Button;
    public var message_txt:TextField;
    
    private var __text:String="";
    private var __buttonLabel:String="OK";
    
    
    
	function Message(){
		super();
		
	}
	function init():Void
	{
		super.init();
	}
	function createChildren():Void
	{
		super.createChildren();
		_global.MSG=this;
		
		var cfg:Object={type:"dynamic",
			autoSize:"center",wordWrap:true,multiLine:true,html:true,
			border:false};
		message_txt=this.createLabel("message_txt", getNextHighestDepth(), " ");
		for(var prop:String in cfg){message_txt[prop]=cfg[prop];}
		message_txt.type="dynamic";
		
		ok_btn=Button(
				this.createChild(
					Button, "ok_btn", 
					{controller:this,_y:30,_visible:true,label:__buttonLabel}
					)
			);
		ok_btn.addEventListener("click",this);
		
		
	}
	public function click():Void
	{
		dispatchEvent({type:"click"});
	}
	function size():Void
	{
		super.size();
		
	}
	
	function doLayout():Void
	{
		var offset=Number(getStyle("borderOffset"));
		super.doLayout();
		var offsetWidth:Number=width-offset-offset;
		message_txt.text=__text;
		message_txt.move(offset,offset);
		var h:Number=message_txt.getTextFormat().getTextExtent(__text,offsetWidth).textFieldHeight;
		if(h>height){setSize(width,h);return;}
		message_txt.setSize(offsetWidth,h);
		
		ok_btn.move(offset,height-ok_btn.height-offset);
		ok_btn.setSize(offsetWidth,ok_btn.height);
	}	
	
	public function get text():String
	{
		return __text;
	}
	
	public function set text(str:String):Void
	{
		message_txt.text=__text=str;	
		invalidate();
	}
	
	public function get buttonLabel():String
	{
		return ok_btn.label;
	}
	
	public function set buttonLabel(str:String):Void
	{
		ok_btn.label=__buttonLabel=str;	
		invalidate();
	}
	//---------------------------------------------
}