/**
* @author	Matt Shaw <xmlrpc@mattism.com>
* @url		http://sf.net/projects/xmlrpcflash
* 			http://www.osflash.org/doku.php?id=xmlrpcflash			
*/

import com.mattism.http.xmlrpc.util.XMLRPCUtils;
import com.mattism.http.xmlrpc.util.XMLRPCDataTypes;
import com.mattism.http.xmlrpc.MethodCall;

class com.mattism.http.xmlrpc.MethodCallImpl
extends XML 
implements MethodCall
{
	
	private var _VERSION:String = "1.0";
	private var _PRODUCT:String = "MethodCallImpl";
	private var _TRACE_LEVEL:Number = 3;	
	private var _parameters:Array;
	private var _name:String;
	
	public function MethodCallImpl(){
		this.removeParams();

		this.debug("MethodCallImpl instance created. (v" + _VERSION + ")");
	}
	
	
	public function setName( name:String ):Void {
		this._name=name;
	}
	
	public function addParam(param_value:Object,param_type:String):Void {
		this.debug("MethodCallImpl.addParam("+arguments+")");
		this._parameters.push({type:param_type,value:param_value});
	}
	
	public function removeParams( Void ):Void {
		this._parameters=new Array();
	}

	public function getXml( Void ):XML {
		this.debug("getXml()");
		var ParentNode:XMLNode = new XMLNode();
		var ChildNode:XMLNode = new XMLNode();
		
		// Create the <methodCall>...</methodCall> root node
		ParentNode = this.createElement("methodCall");
		this.appendChild(ParentNode);
		
		// Create the <methodName>...</methodName> node
		ChildNode = this.createElement("methodName");
		ChildNode.appendChild(this.createTextNode(this._name));
		ParentNode.appendChild(ChildNode);
		
		// Create the <params>...</params> node
		ChildNode = this.createElement("params");
		ParentNode.appendChild(ChildNode);
		ParentNode = ChildNode;
		
		// build nodes that hold all the params
		this.debug("Render(): Creating the params node.");
		
		var i:Number;		
		for (i=0; i<this._parameters.length; i++) {
			this.debug("PARAM: " + [this._parameters[i].type,this._parameters[i].value]);
			ChildNode = this.createElement("param");
			ChildNode.appendChild( this.createParamsNode(this._parameters[i]) );
			ParentNode.appendChild(ChildNode);
		}
		this.debug("Render(): Resulting XML document:");
		this.debug("Render(): "+this.toString());
		
		
		var x:XML = new XML();
		x.xmlDecl = '<?xml version="1.0"?>';
		x.contentType = "text/xml";
		x.parseXML( this.toString() );
		return x;
	}
	
		
	private function createParamsNode( parameter:Object ):XMLNode {
		this.debug("CreateParameterNode()");
		var Node:XMLNode = this.createElement("value");
		var TypeNode:XMLNode;

		if (!parameter.value && parameter){
			parameter = {value:parameter};
		}
				
		if ( typeof parameter == "object") {

			
			// Default to 
			if (!parameter.type){
				var v:Object = parameter.value;
				if ( v instanceof Array )
					parameter.type=XMLRPCDataTypes.ARRAY;
				else if ( v instanceof Object )
					parameter.type=XMLRPCDataTypes.STRUCT;
				else
					parameter.type=XMLRPCDataTypes.STRING;
			}

			// Handle Explicit Simple Objects
			if ( XMLRPCUtils.isSimpleType(parameter.type) ) {
			    //cdata is really a string type with a cdata wrapper, so don't really make a 'cdata' tag
			    parameter = this.fixCDATAParameter(parameter);
			    
				this.debug("CreateParameterNode(): Creating object '"+parameter.value+"' as type "+parameter.type);
				TypeNode = this.createElement(parameter.type);
				TypeNode.appendChild( this.createTextNode(parameter.value) );
				Node.appendChild(TypeNode);
				return Node;
			}
			// Handle Array Objects
			if (parameter.type == XMLRPCDataTypes.ARRAY) {
				var DataNode:XMLNode;
				this.debug("CreateParameterNode(): >> Begin Array");
				TypeNode = this.createElement("array");
				DataNode = this.createElement("data");
				//for (var i:String in parameter.value) {
				//	DataNode.appendChild(this.createParamsNode(parameter.value[i]));
				//}
				var i; //:Number
				for (i=0; i<parameter.value.length; i++) {
					DataNode.appendChild( XMLNode(this.createParamsNode( parameter.value[i] )) );
				}
				TypeNode.appendChild(DataNode);
				this.debug("CreateParameterNode(): << End Array");
				Node.appendChild(TypeNode);
				return Node;
			}
			// Handle Struct Objects
			if (parameter.type == XMLRPCDataTypes.STRUCT) {
				this.debug("CreateParameterNode(): >> Begin struct");
				TypeNode = this.createElement("struct");
				for (var i:String in parameter.value) {
					var MemberNode:XMLNode = this.createElement("member");

					// add name node
					MemberNode.appendChild(this.createElement("name"));
					MemberNode.lastChild.appendChild(this.createTextNode(i));

					// add value node
					MemberNode.appendChild(this.createElement("value"));
					MemberNode.lastChild.appendChild(this.createTextNode(parameter.value[i]));
					
					TypeNode.appendChild(MemberNode);
				}
				this.debug("CreateParameterNode(): << End struct");
				Node.appendChild(TypeNode);
				return Node;
			}
		}
	}
	
	
    /*///////////////////////////////////////////////////////
	fixCDATAParameter()
	?:      Turns a cdata parameter into a string parameter with 
	        CDATA wrapper
	IN:	    Possible CDATA parameter
	OUT:	Same parameter, CDATA'ed is necessary
 	///////////////////////////////////////////////////////*/
    private function fixCDATAParameter(parameter:Object):Object{
        if (parameter.type==XMLRPCDataTypes.CDATA){
            parameter.type=XMLRPCDataTypes.STRING;
            parameter.value='<![CDATA['+parameter.value+']]>';  
        }
        return parameter;
    }
    
    
	public function cleanUp():Void {
		this.removeParams();
		this.parseXML(null);
	}

	private function debug(a:Object):Void {
		//trace(a);
	}
}