namespace EventLogger;

// This class is used to read the configuration for the EventLogger
public static class Constants
{
    public const int WH_KEYBOARD_LL = 13;
    public const int WH_MOUSE_LL = 14;
    public const int WM_KEYDOWN = 0x0100;
    public const int WM_KEYUP = 0x0101;
    public const int WM_LBUTTONDOWN = 0x0201;
    public const int WM_RBUTTONDOWN = 0x0204;
    public const int LINE_LENGHT = 10;
    public const int API_INVOKE = 10;
    public const int MAX_LOG_LENGTH = 2048;
    public const bool LOG_PROCESS_ON_DOUBLE_CLICK = true;
    public const String PATH = @"C:\Users\nicof\Desktop\PROJECTS\logger\log.txt";
    
}