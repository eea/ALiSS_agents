	
/**
@author			Tor Kristensen	tor.kristensen@tietoenator.com
@version		1.2
@description	AlissApplication is the core logic controller 
				for the SmartSearch application.
*/
	
import flash.external.*;

import mx.core.UIComponent;
import mx.utils.Delegate;

import com.eea.utilities.logging.Logger;
import com.eea.projects.aliss.events.AlissEvents;
import com.eea.styling.css.ComponentCSS;

import com.tec.xml.SimpleXmlSerializer;

class com.eea.projects.aliss.application.AlissApplication 
extends UIComponent{
	
	//	Private var for application state
	private var __state							:Number=-1;
	//	Private var for previous application state
	private var __oldState						:Number=-1;
	
	//	The URL of the Xml configuration file
	public var xml_url							:String="flash_config_xml";
	// The URL of the external CSS file
	public var css_url							:String;
	
	//	Stores the serialized configuration from xml_url @see #xml_url
	static var configuration					:Object;
	
	//	Instance of the XML Serializer
	private var parser_sxs						:SimpleXmlSerializer;
	//	Instance of the CSS parser
	private var component_ccss					:ComponentCSS;
	
	//	Static reference to the application (singleton)
	static var application						:AlissApplication;
	
	//	Static var for Startup application state
	static var STATE_STARTUP					:Number=-1;
	//	Static var for Initing application state
	static var STATE_INITING					:Number=0;
	//	Static var for Loading Xml application state
	static var STATE_LOAD_XML					:Number=1;
	//	Static var for Loading CSS application state
	static var STATE_LOAD_CSS					:Number=2;
	//	Static var for Ready application state
	static var STATE_READY						:Number=3;
	//	Static var for Errored application state
	static var STATE_ERROR						:Number=-999;
	
	//	Private var for the initial clock time at app start
	private var startTime:Number;
	//	Private var for the final clock time at the end of the init cycle
	private var endTime:Number;
	
	/**
	* 
	*	@description 
	*		loads xml config file, loads external CSS, handles top level application state
	* 		access avialable to other objects via
	* 		getConfiguration();
	* 		or by static prop access
	* 		com.eea.projects.aliss.application.AlissApplication.configuration[propName]
	* 
	* 		loads CSS info into the _global.styles tree for components
	* 
	* 		broadcasts errors and success events
	*	@return a new AlissApllication instance
	* 
	* */
	//------------------------------------------------------------------------------
	function AlissApplication()
	{
		super();
		Logger.logIt("new AlissApplication");
		Logger.logIt("CMS SUPPLIED XML URL: '"+_root.variable1+"'");
		if(application==undefined){
			application=this;
			
		}
		if(_root.variable1!=undefined)
		{
			xml_url=_root.variable1;	
			
		}else{
			Logger.logIt("CMS SUPPLIED XML URL IS UNDEFINED");
			Logger.logIt("		DEFAULTING TO:'"+xml_url+"'");
		}
		
		Logger.logIt("LOAD XML:"+xml_url);
	}
	//------------------------------------------------------------------------------
	/**
	*	@description starts the init process
	*/
	function init():Void
	{
		super.init();
		Logger.logIt("init");		
		startTime=getTimer();
		state=STATE_INITING;
		
	}
	//------------------------------------------------------------------------------
	/**
	*	@description draw method
	*/
	function draw():Void
	{		
		super.draw();
		Logger.logIt("draw");
		
	}
	//------------------------------------------------------------------------------
	function createChildren():Void{super.createChildren();invalidate();}
	//------------------------------------------------------------------------------
	
	
	
	
	//------------------------------------------------------------------------------
	/**
	*	@description configXmlLoad() starts the process of loading the external XML
	*				 uses success/fail listeners	
	*/	
	public function configXmlLoad():Void
	{
		Logger.logIt("LOAD CONFIG:"+xml_url);
		configuration={};
		parser_sxs=new SimpleXmlSerializer();
		parser_sxs.addEventListener("xml_load", Delegate.create(this, configXmlResult));
		parser_sxs.addEventListener("xml_error", Delegate.create(this, handleError));
		parser_sxs.load( urlRepair(xml_url) );
	}
	/**
	*	@description configXmlResult() starts the process of loading the external XML
	*				 uses success/fail listeners	
	*	@param e	A standard Event object
	*/	
	public function configXmlResult(e:Object):Void
	{
		var data:Object=e.data.hashmap;
		
			for(var s:String in data)
			{
				if(s=="group"){
					configuration[s]=new Array();
					for(var ss:String in data[s])
					{
						configuration[s].push(data[s][ss]);
					}
					_global.FOO=configuration[s];
				}else{
					configuration[s]=data[s];
				}
				/*
				var logstr:String="";
		
				Logger.logIt("	configuration."+s+"='"+data[s]+"'"+typeof(configuration[s]));
				for(var ss:String in data[s])
				{
					Logger.logIt("	configuration."+s+"."+ss+"='"+data[s][ss]+"'");
					for(var sss:String in data[s][ss])
					{
						Logger.logIt("	configuration."+s+"."+ss+"."+sss+"='"+data[s][ss][sss]+"'");
					}	
				}	
			*/
			
			}	

		
		state=STATE_LOAD_CSS;
	}
	//------------------------------------------------------------------------------
	/**
	*	@description cssLoad() starts the process of loading the external CSS
	*				 uses success/fail listeners	
	*/	
	public function cssLoad():Void
	{
		
		component_ccss=new ComponentCSS();
		
		if(configuration.css_path!=undefined){
			css_url=urlRepair(AlissApplication.configuration.css_path);		
			
		}else{
			Logger.logIt("LOAD DEFAULT CSS PATH");
			css_url="css/flash_client.css";
		}

		component_ccss.addEventListener("complete", Delegate.create(this, cssResult));
		component_ccss.addEventListener("error", Delegate.create(this, handleError));
		
		Logger.logIt("LOAD CSS:"+css_url);
		component_ccss.load(css_url);
	}
	/**
	*	@description cssResult() calledback on CSS success
	*/	
public function cssResult():Void
	{
		Logger.logIt("CSS LOADED");
		state=STATE_READY;
	}
	//------------------------------------------------------------------------------
	/**
	*	@description called after the application UI is built
	*/
	public function applicationUiLoad():Void
	{
		endTime=getTimer();
		Logger.logIt("---- APPLICATION IS CONFIGURED AND READY : STARTUP TOOK "+(endTime-startTime)+" msecs-----");
		
		dispatchEvent({type:AlissEvents.EVENT_APP_READY});
	}
	//------------------------------------------------------------------------------
	/**
	*	@description handleError() handles error events, broadcasts them
	*/
	public function handleError():Void
	{
		Logger.logIt("---- APPLICATION ERRORED. BUMMER. ---- ");
		Logger.logIt(Logger.printObj(arguments[0]));
		dispatchEvent({type:AlissEvents.EVENT_APP_ERROR});
	}
	
	//------------------------------------------------------------------------------
	/**
	*	@description handleState() executes actions based on previous and current states
	*/
	private function handleState():Void
	{
		Logger.logIt("handleState "+__oldState+" -> "+__state);
		switch(true)
		{
			case (__oldState==STATE_STARTUP && __state==STATE_INITING):
				_root.status_txt.text="Loading XML..."+xml_url;
				Logger.logIt("Loading XML..."+xml_url);
				state=STATE_LOAD_XML;
				break;
				
			case (__oldState==STATE_INITING && __state==STATE_LOAD_XML):
				configXmlLoad();
				break;
				
			case (__oldState==STATE_LOAD_XML && __state==STATE_LOAD_CSS):
				_root.status_txt.text="Loading CSS...";
				Logger.logIt("Loading CSS...");
				cssLoad();
				break;
				
			case (__oldState==STATE_LOAD_CSS && __state==STATE_READY):
				applicationUiLoad();
				_root.status_txt.text="Ready...";
				//_root.status_txt.removeMovieClip();
				break;
				
				
			case (__state==STATE_ERROR):
			_root.status_txt.text="ERROR LOADING CONFIG OR CSS DATA";
				Logger.logIt("ERROR LOADING CONFIG OR CSS DATA");
				_root.status_txt.text="Config Error...";
				handleError();
				break;
				
			default:
				Logger.logIt("STATE: OLD:"+__oldState+" NEW:"+__state+" IS UNHANDLED");
				break;
		}
		
		
	}
	//------------------------------------------------------------------------------
	/**
	*	@description fixes urs in external documents by stripping prepending a "." to urls that begin with "/"
	*	@param url_str	The URL to repar
	*	@return A new URL string
	*/
	static function urlRepair(url_str:String):String
	{
		if(url_str.substr(0,1)=="/"){url_str="."+url_str;}
		return url_str;
	}
	//------------------------------------------------------------------------------
	/*
	*	@description returns a value from the configuraion object when given a string key 
	*	@usage <pre>AlissApplication.application.getConfig("service_url");</pre>
	*	@param id	The id (key) of the value to return
	*	@return The untyped value loaded from the external xml file
	*/
	static function getConfig(id:String):Object{
		return configuration[id];
	}
	//------------------------------------------------------------------------------
	static function getImageUrlForItemType(type_str:String):String
	/**
	*	@description returns a URL for the image that should be displayed for a group of type type_str
	*	@param type_str	The group type to find the icon URL for
	*	@return The untyped value loaded from the external xml file
	*/	
	{
		var types:Array=configuration.group;
		var len:Number=types.length;
		var o:Object;
		//trace("configuration.groups="+configuration.group+" "+configuration.group.length);
		for(var n:Number=0;n<len;n++){
			o=types[n];
			//trace("AA.tests "+o.name+" vs "+type_str);
			if(o.name==type_str){
				return o.standardicon;
			}
		}
		return "";
	}
	
	
	//------------------------------------------------------------------------------
	public function set state(n:Number):Void
	{
		if(n==__state){return;}
		__oldState=__state;
		__state=n;
		handleState();
	}
	//------------------------------------------------------------------------------
	public function get state():Number
	{
		return __state;
	}
	//---------------------------------------------------------------
	//------------------------------------------------------------------------------
}