import flash.external.*;
import com.eea.styling.skins.RoundRectBorder;
import com.eea.utilities.logging.Logger;
import com.eea.projects.aliss.application.AlissApplication;

import com.eea.layout.BrowserLayoutManager;

import com.eea.projects.aliss.smartsearch.AlissClient;
import com.eea.projects.aliss.views.SmartSearchView;

import com.eea.projects.aliss.views.RelatedItemList;



var application:AlissApplication;

var blm:BrowserLayoutManager;
var ssClient:AlissClient;
var ssView:SmartSearchView;
var resultDisplay_mc:RelatedItemList;

//----------------------------------------------------------------------

function onApplicationReady():Void
{
//	blm=new BrowserLayoutManager("smartsearchcontainer");
	blm=new BrowserLayoutManager();
	ssView=attachMovie("SmartSearchViewClip","ssView_mc",1,{_x:0,_y:0});	
	ssClient=new AlissClient();
	
	ssView.setController(ssClient);

	blm.addEventListener("onResize",ssView);
	blm.addEventListener("onBrowserResize",ssView);
	blm.addEventListener("onStageResize",ssView);
	blm.addEventListener("onBrowserBlur",ssView);
	blm.addEventListener("onBrowserFocus",ssView);
	
	ssView.addEventListener("onSetStageSize",blm);
	ssView.addEventListener("onCallGoogle",ssClient);
	
	ssClient.addEventListener("smartSearch_GetTopPagesForTermsResult",ssView.getRelatedItemResultView());
	
	ssView.getRelatedItemResultView().addEventListener("relatedItemSelection",ssView);
	
	ssClient.addEventListener("smartSearch_GetTopPagesForTermsResult",ssView);
	//trace("ssView="+ssView);
	//for(var s:String in ssView){trace("  "+s+"="+ssView[s]);}
	//AUTH DEBUG
	//Stage.addListener(blm);
}

//----------------------------------------------------------------------
function main():Void
{
	//replace true w the below to turn logging OFF in published versions
	//System.capabilities.playerType=="External";
	//Stage.align="RT";
	
	

	
	
	
	
	fscommand("allowscale", false);
	fscommand("showmenu", false);
	Stage.align="TL";
	Stage.scaleMode = "noScale";

	Logger.ENABLED = true;
	Logger.PREFIX = "Flash";
	Logger.LOGGING_MODE = MODE_JAVASCRIPT;
	Logger.EXTERNAL_JS_FUNCTION_NAME="browserLayoutManager_alert";
	
	System.security.allowDomain("*");	
	System.security.allowInsecureDomain("*");	
	
	application = new AlissApplication();
	trace("app="+application);
	application.addEventListener("onApplicationReady", this);
	application.init();	
}

//----------------------------------------------------------------------


main();
//onApplicationReady();

//ExternalInterface.call("browserLayoutManager_alert", "STARTUP");
stop();
