interface com.eea.cellrenderer.ICellRenderer{
	
	function getPreferredHeight():Number;
	function getPreferredWidth():Number;
	function setValue(str:String, item:Object, sel:Boolean);

}