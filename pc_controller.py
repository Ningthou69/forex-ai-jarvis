import subprocess
import os
import platform
import psutil
from config import ALLOW_PC_CONTROL, COMMAND_TIMEOUT

class PCController:
    """Controls PC operations safely"""
    
    def __init__(self):
        self.system = platform.system()
        self.allowed = ALLOW_PC_CONTROL
        self.command_timeout = COMMAND_TIMEOUT
        
        # Safe commands whitelist
        self.safe_commands = [
            "open", "start", "launch",
            "shutdown", "restart", "sleep",
            "get_system_info", "list_processes",
            "kill_process", "open_app"
        ]
    
    def execute_command(self, command_type, params=None):
        """Execute PC control commands safely"""
        if not self.allowed:
            return {"error": "PC control is disabled"}
        
        if command_type not in self.safe_commands:
            return {"error": f"Command '{command_type}' not allowed"}
        
        try:
            if command_type == "open":
                return self._open_file(params.get("path"))
            
            elif command_type == "start" or command_type == "launch":
                return self._launch_app(params.get("app"))
            
            elif command_type == "open_app":
                return self._launch_app(params.get("app_name"))
            
            elif command_type == "get_system_info":
                return self._get_system_info()
            
            elif command_type == "list_processes":
                return self._list_processes()
            
            elif command_type == "kill_process":
                return self._kill_process(params.get("pid"))
            
            elif command_type == "shutdown":
                return self._shutdown()
            
            elif command_type == "restart":
                return self._restart()
            
            elif command_type == "sleep":
                return self._sleep()
            
            else:
                return {"error": "Unknown command"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def _open_file(self, file_path):
        """Open a file with default application"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            if self.system == "Windows":
                os.startfile(file_path)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["open", file_path], timeout=self.command_timeout)
            else:  # Linux
                subprocess.run(["xdg-open", file_path], timeout=self.command_timeout)
            
            return {"status": "success", "message": f"Opened {file_path}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _launch_app(self, app_name):
        """Launch an application"""
        try:
            if self.system == "Windows":
                subprocess.Popen(app_name)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["open", "-a", app_name], timeout=self.command_timeout)
            else:  # Linux
                subprocess.Popen([app_name])
            
            return {"status": "success", "message": f"Launched {app_name}"}
        except Exception as e:
            return {"error": f"Could not launch {app_name}: {str(e)}"}
    
    def _get_system_info(self):
        """Get system information"""
        try:
            info = {
                "system": self.system,
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "boot_time": psutil.boot_time(),
            }
            return {"status": "success", "data": info}
        except Exception as e:
            return {"error": str(e)}
    
    def _list_processes(self, limit=10):
        """List running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    processes.append(proc.info)
                except:
                    pass
            
            # Sort by CPU usage
            processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)[:limit]
            
            return {"status": "success", "processes": processes}
        except Exception as e:
            return {"error": str(e)}
    
    def _kill_process(self, pid):
        """Kill a process by PID"""
        try:
            if pid in [os.getpid()]:  # Don't allow killing self
                return {"error": "Cannot kill current process"}
            
            proc = psutil.Process(pid)
            proc.terminate()
            
            return {"status": "success", "message": f"Terminated process {pid}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _shutdown(self):
        """Shutdown the PC"""
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "60"], timeout=self.command_timeout)
            else:
                subprocess.run(["shutdown", "-h", "+1"], timeout=self.command_timeout)
            
            return {"status": "success", "message": "PC will shutdown in 60 seconds"}
        except Exception as e:
            return {"error": str(e)}
    
    def _restart(self):
        """Restart the PC"""
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "60"], timeout=self.command_timeout)
            else:
                subprocess.run(["shutdown", "-r", "+1"], timeout=self.command_timeout)
            
            return {"status": "success", "message": "PC will restart in 60 seconds"}
        except Exception as e:
            return {"error": str(e)}
    
    def _sleep(self):
        """Put PC to sleep"""
        try:
            if self.system == "Windows":
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], timeout=self.command_timeout)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["pmset", "sleepnow"], timeout=self.command_timeout)
            else:  # Linux
                subprocess.run(["systemctl", "suspend"], timeout=self.command_timeout)
            
            return {"status": "success", "message": "PC is going to sleep"}
        except Exception as e:
            return {"error": str(e)}