/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash			
*/

import com.mattism.http.xmlrpc.Parser;
import com.mattism.http.xmlrpc.util.XMLRPCUtils;
import com.mattism.http.xmlrpc.util.XMLRPCDataTypes;

class com.mattism.http.xmlrpc.ParserImpl
implements Parser {
    
	// Metadata
    private var _VERSION:String = "1.0.0";
	private var _PRODUCT:String = "ParserImpl";

	// Constants
	private var ELEMENT_NODE:Number = 1;
	private var TEXT_NODE:Number = 3;
	
	private var METHOD_RESPONSE_NODE:String = "methodResponse";
	private var PARAMS_NODE:String = "params";
	private var PARAM_NODE:String = "param";
	private var VALUE_NODE:String = "value";
	private var FAULT_NODE:String = "fault";
	private var ARRAY_NODE:String = "array";
	
	private var DATA_NODE:String = "data";
	private var STRUCT_NODE:String = "struct";
	private var MEMBER_NODE:String = "member";
	
	public function parse( xml:XML ):Object {
		//trace(xml.toString());
		if ( xml.toString().toLowerCase().indexOf('<html') >= 0 ){
			trace("WARNING: XML-RPC Response looks like an html page.");
			return xml.toString();
		}
		
		xml.ignoreWhite = true;
		return this._parse( xml.firstChild );
	}
	
	private function _parse( node:XMLNode ):Object {		
		var data:Object;
		
		if (node.nodeType == TEXT_NODE) {
			return node.nodeValue;
		}
		else if (node.nodeType == ELEMENT_NODE) {
			if (
				node.nodeName == METHOD_RESPONSE_NODE || 
				node.nodeName == PARAMS_NODE		  ||				
				node.nodeName == VALUE_NODE 		  || 
				node.nodeName == PARAM_NODE 		  ||
				node.nodeName == FAULT_NODE 		  ||
				node.nodeName == ARRAY_NODE
				) {
				
				this.debug("_parse(): >> " + node.nodeName);
				return this._parse( node.firstChild );
			}
			else if (node.nodeName == DATA_NODE) {
				this.debug("_parse(): >> Begin Array");
				data = new Array();
				for (var i:Number=0; i<node.childNodes.length; i++) {
					data.push( this._parse(node.childNodes[i]) );
					this.debug("_parse(): adding data to array: "+data[data.length-1]);
				}
				this.debug("_parse(): << End Array");
				return data;
			}
			else if (node.nodeName == STRUCT_NODE) {
				this.debug("_parse(): >> Begin Struct");
				data = new Object();
				for (var i:Number=0; i<node.childNodes.length;i++) {
					var temp:Object = this._parse(node.childNodes[i]);
					data[temp.name]=temp.value;
					this.debug("_parse(): Struct  item "+temp.name + ":" + temp.value);
				}
				this.debug("_parse(): << End Stuct");
				return data;
			}
			else if (node.nodeName == MEMBER_NODE) {
				/* 
				* The member tag is *special*. The returned
				* value is *always* a hash (or in Flash-speak,
				* it is always an Object).
				*/
				var temp1:Object;
				var temp2:Object;
				data = new Object();
				temp1 = this._parse(node.firstChild);
				temp2 = this._parse(node.lastChild);
				data.name = temp1;
				data.value = temp2;

				return data;
			}
			else if (node.nodeName == "name") {
				return this._parse(node.firstChild);
			}
			else if ( XMLRPCUtils.isSimpleType(node.nodeName) ) {
				return this.createSimpleType( node.nodeName, node.firstChild.nodeValue );
			}			
		}
		
		this.debug("Received an invalid Response.");
		return false;
	}
	
	private function createSimpleType( type:String, value:String ):Object {
		switch (type){
			case XMLRPCDataTypes.i4:	
			case XMLRPCDataTypes.INT:	
			case XMLRPCDataTypes.DOUBLE:						
				return new Number( value );
				break;
				
			case XMLRPCDataTypes.STRING:
				return new String( value );
				break;
			
			case XMLRPCDataTypes.DATETIME:
				return this.getDateFromIso8601( value );
				break;
				
			case XMLRPCDataTypes.BASE64:
				return value;
				break;
				
			case XMLRPCDataTypes.CDATA:
				return value;
				break;

			case XMLRPCDataTypes.BOOLEAN:
				if (value=="1" || value.toLowerCase()=="true"){
					return new Boolean(true);
				}
				else if (value=="0" || value.toLowerCase()=="false"){
					return new Boolean(false);
				}
				break;
				
		}
		
		return value;
	}
	
	private function getDateFromIso8601( iso:String ):Date {
	 	// yyyy-MM-dd'T'HH:mm:ss
		var tmp:Array = iso.split("T");
		var date_str:String = tmp[0];
		var time_str:String = tmp[1];
		var date_parts:Array = date_str.split("-");
		var time_parts:Array = time_str.split(":");		
		
		return new Date(date_parts[0],date_parts[1]-1,date_parts[2],time_parts[0],time_parts[1],time_parts[2]);
	}
										
	private function debug(a:String):Void {
		//trace(this._PRODUCT + " -> " + a);
	}

}