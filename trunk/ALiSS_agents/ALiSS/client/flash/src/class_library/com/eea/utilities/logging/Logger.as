import flash.external.*;

class com.EEA.utilities.logging.Logger 
extends Object{
	
	static var ENABLED:Boolean=true;
	static var LOGGING_LEVEL:Number=1;
	static var LOG_COUNT:Number=0;
	static var RECURSION_MAX:Number=10;
	static var LOGMODE:Number=0;
	static var MODE_FLASH:Number=0;
	static var MODE_JAVASCRIPT:Number=1;
	
	static var LOW:Number=0;
	static var MEDIUM:Number=1;
	static var HIGH:Number=2;
	static var PREFIX:String="Logger"
	
	static var EXTERNAL_JS_FUNCTION_NAME:String="Flash_logIt";
	
	//-----------------------------------------------------------------------------------------
	static function setLoggingLevel(n:Number):Void
	{
		LOGGING_LEVEL=n;
	}
	//-----------------------------------------------------------------------------------------
	/**
	 * @description Static function that handles logging messages to the Output window or to a Javascript function.
	 */
	static function logIt(str:String,priority:Number):Void
	{
		if(!ENABLED){return;}
		
		LOG_COUNT++;
		//trace("LOG EVT:"+arguments+" "+LOGGING_LEVEL);
		if(priority==undefined)
		{
			priority=HIGH;
		}
		if(priority>=LOGGING_LEVEL){
			
			var logStr:String=PREFIX+" #"+LOG_COUNT+" level:"+priority+"> "+str;
			
			if(LOGMODE==MODE_FLASH){
				trace(logStr);
			}else{
				ExternalInterface.call(EXTERNAL_JS_FUNCTION_NAME, logStr);
			}
			ExternalInterface.call(EXTERNAL_JS_FUNCTION_NAME, logStr);
			
		}
		
	}
	//-----------------------------------------------------------------------------------------
	/**
	 * @description Static function that recurses through an object and returns a string of the name/value tuples.
	 */
	static function printObj():String
	{
		
		var n:Number=1;
		var o:Object=arguments[0];
		var str:String="";
		var indent="	";
		var indentCap="+->";
		var indent_str:String="";
		
		if(arguments.length==2){n=arguments[1];}
		
		for(var i:Number=0;i<n;i++){
			indent_str+=indent;
		}
		indent_str+=indentCap;
		for(var s:String in o){
			str+=newline+indent_str+' name="'+s+'" : "'+o[s]+'"';					
			if(o[s] instanceof XML){
				str+=o[s].toString();				
			}else if(n<RECURSION_MAX){				
				str+=Logger.printObj(o[s],n+1);
			}
		}
		return str;
	}
}
