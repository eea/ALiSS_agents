import mx.skins.RectBorder;
import mx.core.ext.UIObjectExtensions;

class RedGreenBlueSkin extends RectBorder
{
    static var symbolName:String = "RedGreenBlueSkin";
    static var symbolOwner:Object = RedGreenBlueSkin;
    
    function size():Void
    {
        var c:Number; // color
        var borderStyle:String = getStyle("borderStyle");

        switch (borderStyle) {
            case "falseup":
            case "falserollover":
            case "falsedisabled":
                c = 0xFF0000;
                break;
            case "falsedown":
                c = 0x77FF77;                
                break;
            case "trueup":
            case "truedown":
            case "truerollover":
            case "truedisabled":
                c = 0xFF7777;
                break;
        }

        clear();
        var thickness = _parent.emphasized ? 2 : 0;
        lineStyle(thickness, 0, 100);
        beginFill(c, 100);
        drawRect(0, 0, __width, __height);
        endFill();
    }
    
    // Required for skins.
    static function classConstruct():Boolean
    {
        UIObjectExtensions.Extensions();
        _global.skinRegistry["ButtonSkin"] = true;
        return true;
    }
    static var classConstructed:Boolean = classConstruct();
    static var UIObjectExtensionsDependency = UIObjectExtensions;
}

