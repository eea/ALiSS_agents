import com.mattism.http.xmlrpc.ConnectionImpl;
import com.mattism.http.xmlrpc.Connection;
import com.mattism.http.xmlrpc.MethodFault;
import com.mattism.http.xmlrpc.MethodFaultImpl;
class com.mattism.http.xmlrpc.ConnectionCancellableImpl 
extends ConnectionImpl
implements Connection {
	public var id:Number;
	public static var idcounter:Number=0;
	public var isCancelled:Boolean=false;
	//------------------------------------------------------
	public function ConnectionCancellableImpl(url:String )
	{
		super(url);
		super._onLoad=this._onLoad;
		id=idcounter++;
	}
	//------------------------------------------------------
	public function cancel():Void
	{
		isCancelled=true;
		trace(" CANCELLED: {ConnectionCancellableImpl "+id+"}");
	}
	//------------------------------------------------------
	private function _onLoad( success:Boolean ):Void {
		trace(" PARSE : {ConnectionCancellableImpl "+id+"}");		
		if ( success  ) {
			if(!isCancelled){
				var a:Object = this.parseResponse();
				
				// Tiny Hack to pas to onFault
				if (a.faultCode){
					var mf:MethodFault = new MethodFaultImpl( a );
					this.onFault( mf );
				}
				else {
					this.onLoad( a );
				}
			}else{
				trace(" PARSE ABORTED: {ConnectionCancellableImpl "+id+"}");		
			}
			
		} else {
			this._onFail();
		}
	}
	//------------------------------------------------------
}
