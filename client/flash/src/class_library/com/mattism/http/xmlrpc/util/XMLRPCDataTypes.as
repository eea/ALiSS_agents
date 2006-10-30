/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash			
*/

class com.mattism.http.xmlrpc.util.XMLRPCDataTypes {

    static var STRING:String   = "string";
    static var CDATA:String    = "cdata";
    static var i4:String       = "i4";
    static var INT:String      = "int";
    static var BOOLEAN:String  = "boolean";
    static var DOUBLE:String   = "double";
    static var DATETIME:String = "dateTime.iso8601";
    static var BASE64:String   = "base64";
    static var STRUCT:String   = "struct";
    static var ARRAY:String    = "array";
    
}

/*
<i4> or <int>		java.lang.Integer	Number
<boolean>			java.lang.Boolean	Boolean
<string>			java.lang.String	String
<double>			java.lang.Double	Number
<dateTime.iso8601>	java.util.Date		Date
<struct>			java.util.Hashtable	Object
<array>				java.util.Vector	Array
<base64>			byte[ ]				Base64
*/