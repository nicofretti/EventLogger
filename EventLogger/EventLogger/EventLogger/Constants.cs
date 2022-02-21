
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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
    public const String API_KEY = "H1ZEFWV9A7";
    public static String[] BANNED_PROCESS = {"TextInputHost", "ApplicationFrameHost", "SystemSettings"};
    public int MAX_CONT_EVENTS = 4098;
    public int SECONDS_API_INVOKE = 60;
    public bool LOG_PROCESS_ON_DOUBLE_CLICK = true; // to log process on double click otherwise only on api call
    public bool LOG_MOUSE_EVENTS = true;
    public bool LOG_KEYBOARD_EVENTS = true;
    

    private class SettingsRequest
    {
        public int SECONDS_API_INVOKE;
        public bool LOG_PROCESS_ON_DOUBLE_CLICK;
        public bool LOG_MOUSE_EVENTS;
        public bool LOG_KEYBOARD_EVENTS;
    }

    public Constants()
    {
        
    }

    public void UpdateConfig(string? json)
    {
        // convert json to object
        if (json == null) return;
        SettingsRequest config = JsonConvert.DeserializeObject<SettingsRequest>(json);
        if (config == null) return;
        this.SECONDS_API_INVOKE = config.SECONDS_API_INVOKE;
        this.LOG_PROCESS_ON_DOUBLE_CLICK = config.LOG_PROCESS_ON_DOUBLE_CLICK;
        this.LOG_MOUSE_EVENTS = config.LOG_MOUSE_EVENTS;
        this.LOG_KEYBOARD_EVENTS = config.LOG_KEYBOARD_EVENTS;
        
    }

}