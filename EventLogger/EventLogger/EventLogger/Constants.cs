using System.Data;

namespace EventLogger;

// This class is used to read the configuration for the EventLogger
public class Constants
{
    public const int WH_KEYBOARD_LL = 13;
    public const int WH_MOUSE_LL = 14;
    public const int WM_KEYDOWN = 0x0100;
    public const int WM_KEYUP = 0x0101;
    public const int WM_LBUTTONDOWN = 0x0201;
    public const int WM_RBUTTONDOWN = 0x0204;
    public const String PATH = @"C:\Users\nicof\Desktop\PROJECTS\logger\log.txt";
    public const String API_URL = "http://localhost:8000/api/logger";
    public const String API_KEY = "1234";
    public const int COUNT_EVENTS_BEFORE_LOG_ON_FILE = 4096;
    public int SECONDS_API_INVOKE = 30;
    public bool LOG_PROCESS_ON_DOUBLE_CLICK = true; // to log process on double click otherwise only on api call
    public bool LOG_MOUSE_EVENTS = true;
    public bool LOG_KEYBOARD_EVENTS = true;

    public Constants()
    {
        
    }

    UpdateConfig(String json)
    {
        
    }

}