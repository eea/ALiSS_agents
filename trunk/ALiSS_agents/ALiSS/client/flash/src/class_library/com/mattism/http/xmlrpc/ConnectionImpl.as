/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash			
*/

import mx.utils.Delegate;

import com.mattism.http.xmlrpc.Connection;
import com.mattism.http.xmlrpc.MethodCall;
import com.mattism.http.xmlrpc.MethodCallImpl;
import com.mattism.http.xmlrpc.MethodFault;
import com.mattism.http.xmlrpc.MethodFaultImpl;
import com.mattism.http.xmlrpc.Parser;
import com.mattism.http.xmlrpc.ParserImpl;

class com.mattism.http.xmlrpc.ConnectionImpl 
implements Connection {

	// Metadata
	private var _VERSION:String = "1.0.0";
	private var _PRODUCT:String = "ConnectionImpl";
	
	private var ERROR_NO_URL:String =  "No URL was specified for XMLRPCall.";
	
	private var _url:String;
	private var _method:MethodCall;
	private var _rpc_response:Object;
	private var _parser:Parser;
	private var _response:XML;
	
	public function ConnectionImpl( url:String ) {
		//prepare method response handler
		//this.ignoreWhite = true;
		
		//init method
		this._method = new MethodCallImpl();
		
		//init parser
		this._parser = new ParserImpl();

		if (url){
			this.setUrl( url );
		}
		
	}
	
	public function call( method:String ):Void { this._call( method ); }

	private function _call( method:String ):Void {
		if ( !this.getUrl() ){
			trace(ERROR_NO_URL);
			throw Error(ERROR_NO_URL);
		}
		else {		
			this.debug( "Call -> " + method+"() -> " + this.getUrl());
			
			this._response = new XML();
			this._response.ignoreWhite = true;
			this._response.onLoad = Delegate.create( this, this._onLoad );
			
			this._method.setName( method );
			
			var x:XML = this._method.getXml();
			/*
			trace("66666666666666666666666666666");
			trace(x.toString());
			trace("66666666666666666666666666666");
			*/
			x.sendAndLoad( this.getUrl(), this._response );
		}
	}

	private function _onLoad( success:Boolean ):Void {
		if ( success ) {
			var a:Object = this.parseResponse();
			
			// Tiny Hack to pas to onFault
			if (a.faultCode){
				var mf:MethodFault = new MethodFaultImpl( a );
				this.onFault( mf );
			}
			else {
				this.onLoad( a );
			}
			
		} else {
			this._onFail();
		}
	}
	
	private function _onFail():Void {
		this.debug( "onFailed()");
		this.onFail();
	}
	
	private function parseResponse():Object { return this._parser.parse( this._response );}
		
	//public function __resolve( method:String ):Void { this._call( method ); }

	public function getUrl( Void ):String { return this._url; }	

	public function setUrl( a:String ):Void { this._url = a; }
	
	public function addParam( o:Object, type:String ):Void { this._method.addParam( o,type ); }
	
	public function removeParams():Void { this._method.removeParams(); }
	
	public function toString():String { return '<xmlrpc.ConnectionImpl Object>'; }
	
	private function debug( a:String ):Void { /*trace( this._PRODUCT + " -> " + a )*/ }
	
	public function onLoad( result:Object ):Void {}
	
	public function onFail( error:Object ):Void {}
	
	public function onFault( fault:MethodFault ):Void {
		trace("XMLRPC Fault (" + fault.getFaultCode() + "):\n" + fault.getFaultString());
	}	

}