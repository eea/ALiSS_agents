import mx.events.UIEventDispatcher;
class com.tec.xml.SimpleXmlSerializer extends Object{
	//--------------------------------------------------------------------------------------------------
	public var url:String;
	private var data_xml:XML;
	private var root_node:XMLNode;
	//--------------------------------------------------------------------------------------------------
	public var dispatchEvent:Function;
	public var addEventListener:Function;
	public var removeEventListener:Function;
	//--------------------------------------------------------------------------------------------------
	public var data:Object;
	//--------------------------------------------------------------------------------------------------
	function SimpleXmlSerializer()
	{
		UIEventDispatcher.initialize(this);
		data={
			items:[]
			};
	}
	//--------------------------------------------------------------------------------------------------
	function load(url:String):Void{
		data_xml=new XML();
		data_xml['cb']=this;		
		data_xml.onLoad=function(success:Boolean){this.cb.onXmlLoad(success,this);}
		data_xml.ignoreWhite=true;
		data_xml.load(url);
		dispatchEvent({type:'result',data:data});
	}
	//--------------------------------------------------------------------------------------------------
	function onXmlLoad(ok:Boolean,dat:XML):Void{
		if(ok){
			parse(dat);
			delete data_xml;
			dispatchEvent({type:'xml_load',data:this.data});
		}else{
			dispatchEvent({type:'xml_error',data:dat});
		}
	}
	//--------------------------------------------------------------------------------------------------
	function parse(dat:XML):Void{
		root_node=findRootNode(dat);
		data=parseData(root_node);
	}
	//--------------------------------------------------------------------------------------------------
	function parseData(rNode:XMLNode):Object{
		
		var n:Number;

		var cnodes:Array=rNode.childNodes;
		var cnodesLen:Number=cnodes.length;
		var o:Object;
		var items:Array=[];
		var somedata:Object={};
		var hashmap:Object={};
		for(n=0;n<cnodesLen;n++){
			o=cnodes[n];
			items.push(parseItem(o,hashmap));
		}
		
		somedata.items=items;
		somedata.hashmap=hashmap;
		
		return somedata;
		
	}
	//--------------------------------------------------------------------------------------------------
	function parseItem(itemNode,scope):Object
	{
		var n:Number;
		var cnodes:Array=itemNode.childNodes;
		var cnodesLen:Number=cnodes.length;
		var o:Object;
		var o_len:Number;
		var data:Object={};
		
		var hasParamID:Boolean=itemNode.attributes.paramid!=undefined;
		var itemNameExists:Boolean;
		var itemIsComplex:Boolean=itemNode.childNodes.length>1;
		var itemName:String;
		var cScope:Object;
		
		
		if(hasParamID){
			itemName=itemNode.attributes.paramid;
		}else{
			
			if(itemNode.nodeName==undefined){
				itemName=itemNode.parentNode.nodeName;
			}else{
				itemName=itemNode.nodeName;
			}
		}
		// trace("PARSE: "+itemName+" hasParamID: "+hasParamID+" len:"+itemNode.childNodes.length);
		
		
		itemNameExists=scope[itemName]!=undefined;
		var itemHolderIsArray:Boolean=scope[itemName] instanceof Array;
		
		if(itemNameExists && !itemHolderIsArray){
			// trace(" MAKE ARRAY OUT FOR NODES OF TYPE:"+itemName+" "+(scope[itemName] instanceof Array));
			// trace("  OLD VAL:"+scope[itemName]);
			// trace("        ID TEST:"+scope[itemName].id);
			
			data[itemName]= scope[itemName]= [scope[itemName]];
			
			// trace("  NEW VAL:"+scope[itemName]+" "+(scope[itemName] instanceof Array));
			// trace("        ID TEST:"+scope[itemName][0].id);
			itemHolderIsArray=true;
		}
		
		// trace("	itemNameExists:"+itemNameExists+" itemHolderIsArray:"+itemHolderIsArray);
		// trace("	itemIsComplex:"+itemIsComplex);
		// trace(" value:"+itemNode.nodeValue);
		// trace(newline);
		
		if(itemIsComplex){
			
			// trace("++++++++++++++++++++++++");
			cScope={};			
			
			if(itemHolderIsArray){
				// trace("		HANDLE ARRAY");
				for(n=0;n<cnodesLen;n++){				
					o=cnodes[n];
					o_len=o.childNodes.length;
					parseItem( XMLNode(o), cScope);
				}
				
				var r:Object=
				scope[itemName].push(cScope);
				// trace("			add "+cScope+"to array for:"+itemName);
				data[itemName]=cScope;
				
			}else{
				
				// trace("		HANDLE OBJ");
				for(n=0;n<cnodesLen;n++){				
					o=cnodes[n];
					o_len=o.childNodes.length;
					parseItem( XMLNode(o), cScope);
				}
				

				scope[itemName]=data[itemName]=cScope;
				
			}
			// trace("++++++++++++++++++++++++");
			
			
		}else{
				// trace("		proc "+cnodesLen+" nodes");
				
			if(cnodesLen==0){
				scope[itemName]=data[itemName]=itemNode.nodeValue;				
				// trace("		set:"+itemName+"="+itemNode.nodeValue);				
				return data;
				
			}else{
				
				for(n=0;n<cnodesLen;n++){
					
					o=cnodes[n];
					o_len=o.childNodes.length;
					
					if(o_len>1){
						// trace("COMPLEX");
						
						if(!itemNameExists){
							scope[itemName]=data[itemName]=parseData( XMLNode(o), new Object());	
						}else{
							var r:Object=parseData( XMLNode(o), new Object());
							scope[itemName].push(r);
							data[itemName]=r;
						}
						
						
					}else if(o.nodeType==3){
						// trace("TEXT");
						scope[itemName]=data[itemName]=o.nodeValue;	
					}else{
						
						if(!itemNameExists){
							scope[itemName]=data[itemName]=o.firstChild.nodeValue;	
						}else{
							scope[itemName].push(o.firstChild.nodeValue);
							data[itemName]=o.firstChild.nodeValue;
						}
						
						// trace("NODE : len:"+o.childNodes.length+" name:"+itemName+'='+o.firstChild.nodeValue);
					}
					
				}
			}
			
		}
		return data;
	}
	function encapsulateItemInArray(item:Object):Array{return [item];}
	//--------------------------------------------------------------------------------------------------
	function findRootNode(dat:XML):XMLNode{return dat.firstChild;}
	//--------------------------------------------------------------------------------------------------
}