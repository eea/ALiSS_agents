/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash
* 			
* @description	This is the expected interface for a Connection class
* 				implementation used for XMLRPC. Any class that wants to behave
* 				as an XMLRPC Connection needs to implement this interface.
*/

import com.mattism.http.xmlrpc.MethodFault;

interface com.mattism.http.xmlrpc.Connection {

	/**
	* Sets the URL of the remote XMLRPC service
	*
	* @description  This URL will be the path to your remote XMLRPC
	* .				service that you have setup. Refer to your specific XMLRPC
	* 				server implementation for more info.
	*
	* @usage	<code>myConn.setUrl("http://mysite.com/xmlrpcProxy");</code>
	* @param	A URL (String)
	*/
	public function setUrl( s:String ):Void;
	
	/**
	* Gets the URL of the remote XMLRPC service
	*
	* @description  Returns the URL set by the user. Returns undefined if no URL
	* 				has been specified.
	*
	* @usage	<code>var url:String = myConn.getUrl();</code>
	* @param	None..
	*/
	public function getUrl( Void ):String;
	
	/**
	* Calls a remote method at the URL specified via {@link #setUrl}
	*
	* @description  Calls a remote method at the URL specified via {@link #setUrl}
	*
	* @usage	<code>myConn.call("getMenu");</code>
	* @param	A remote method name (String).
	*/
	public function call( method:String ):Void;
	
	
	/**
	* Invoked when a remote call is has successfully ended.
	*
	* @description  This event handler should be overriden by the end-coder. This
	* 				event is only fired if everything goes well. Otherwise, {@link #onFault}
	* 				or {@link onFail} are fired accordingly.
	*
	* @usage	<code>
	* 				var myOnLoad = function(result:Object){ 
	*									trace( result );
	*								}
	* 				myConn.onLoad = myOnLoad
	* 			</code>
	* @param	The object returned by the remote method.
	*/
	public function onLoad( result:Object ):Void;
	
	
	/**
	* Invoked when a the remote server encounters a fault while trying to process your request
	*
	* @description  This event handler should be overriden by the end-coder. The event 
	* 				handler is passed a {@link MethodFault} object as the first argument.  This
	* 				event is only fired when a the remote server encounters a 
	* 				fault while trying to process your request.  This event is not fired
	* 				when there is a problem connecting to the server. For that, see {@link #onFail}.
	*
	* @usage	<code>
	* 				var myOnFault = function(mf:MethodFault){ 
	*									trace("XMLRPC Fault (" + fault.getFaultCode() + "):\n" + fault.getFaultString());
	*								}
	* 				myConn.onFault = myOnFault
	* 			</code>
	* @param	The object returned by the remote method.
	*/
	public function onFault( fault:MethodFault):Void;
	
	/** 
	* Invoked when there is a problem connecting to the server.
	*
	* @description  This event handler should be overriden by the end-coder. The event 
	* 				handler is passed an error object which contains pretty much no information.  
	* 				All that can be said is that there was an error trying to reach the XMLRPC
	* 				server. This event is not fired
	* 				when there is a server fault. For that, see {@link #onFault}.
	*
	* @usage	<code>
	* 				var myOnFault = function(mf:MethodFault){ 
	*									trace("XMLRPC Fault (" + fault.getFaultCode() + "):\n" + fault.getFaultString());
	*								}
	* 				myConn.onFault = myOnFault
	* 			</code>
	* @param	The object returned by the remote method.
	*/
	public function onFail( error:Object ):Void;
	
	public function addParam( o:Object, type:String ):Void;
	
}