using System.Diagnostics;

namespace EventLogger;
// class that handles the logging of events
public class Logger
{
    private String _line;
    private int _strokes = 0; // used to determine when invoke a server-side api
    private DateTime _previousClick = DateTime.Now; // used to determine double-left-click
    private String _processes = ""; // used to determine if a process is running
    public Logger()
    {
        _line = "";
    }

    public void MouseLog(String key)
    {
        if (key=="[ML]")
        {
            if (DateTime.Now.Subtract(_previousClick).TotalMilliseconds <= 500)
            {
                key = "[DML]";
                this.ProcessLog(Process.GetProcesses());
                
            }
            _previousClick = DateTime.Now;
        }
        _line += key;
    }

    public void KeyLog(String key)
    {
        _line += key;
        _strokes++;
    }

    private void ProcessLog(Process[] processes)
    {
        String newProcesses = "{"+
            String.Join(",",processes
            .Where(p => p.MainWindowTitle.Length > 0)
            .Select(p => p.ProcessName)
            .Distinct()
            .OrderBy(p=>p))+"}";
        if (_processes!=newProcesses)
        {
            //Console.WriteLine(newProcesses);
            // do something
        }
        _processes = newProcesses;
    }
    
    
}