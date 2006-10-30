/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash			
*/

interface com.mattism.http.xmlrpc.MethodCall
{
	
	public function setName( name:String ):Void;
	
	public function addParam( arg:Object, type:String ):Void;
	
	public function removeParams( Void ):Void;

	public function getXml( Void ):XML;

}