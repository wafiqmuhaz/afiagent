"""
Code Server Management Module for Afiagent

This module provides functionality to manage Code Server instances
for the Afiagent multi-agent system.
"""

import subprocess
import time
import requests
import os
import psutil
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CodeServerManager:
    """Manages Code Server instances for code generation and execution."""
    
    def __init__(self, 
                 port: int = 8329,
                 workspace_dir: str = "/home/wafiqmuhaz/afiagent_workspace",
                #  workspace_dir: str = os.path.expanduser("~/afiagent_workspace"),
                 password: str = "4f9c26af9e42b1b8"):
        self.port = port
        self.workspace_dir = workspace_dir
        self.password = password
        self.process = None
        
    def is_running(self) -> bool:
        """Check if Code Server is currently running."""
        try:
            # Check if port is listening
            for conn in psutil.net_connections():
                if conn.laddr.port == self.port and conn.status == 'LISTEN':
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking if Code Server is running: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get detailed status of Code Server."""
        status = {
            "running": self.is_running(),
            "port": self.port,
            "workspace_dir": self.workspace_dir,
            "url": f"http://localhost:{self.port}",
            "process_id": None
        }
        
        if status["running"]:
            # Try to find the process ID
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'code-server' in proc.info['name'] or \
                       any('code-server' in cmd for cmd in proc.info['cmdline'] if cmd):
                        status["process_id"] = proc.info['pid']
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        return status
    
    def ensure_workspace_exists(self):
        """Ensure the workspace directory exists."""
        os.makedirs(self.workspace_dir, exist_ok=True)
        logger.info(f"Workspace directory ensured: {self.workspace_dir}")
    
    # def start(self) -> bool:
    #     """Start Code Server if not already running."""
    #     if self.is_running():
    #         logger.info("Code Server is already running")
    #         return True
        
    #     try:
    #         self.ensure_workspace_exists()
            
    #         # Start Code Server
    #         cmd = [
    #             # "code-server",
    #             "/usr/bin/code-server",  # full path dari which
    #             "--bind-addr", f"0.0.0.0:{self.port}",
    #             "--auth", "password",
    #             "--password", self.password,
    #             "--disable-workspace-trust",
    #             self.workspace_dir
    #         ]
            
    #         logger.info(f"Starting Code Server with command: {' '.join(cmd)}")
    #         self.process = subprocess.Popen(
    #             cmd,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             cwd=self.workspace_dir
    #         )
            
    #         # Wait for server to start
    #         max_attempts = 30
    #         for attempt in range(max_attempts):
    #             if self.is_running():
    #                 logger.info(f"Code Server started successfully on port {self.port}")
    #                 return True
    #             time.sleep(1)
            
    #         logger.error("Code Server failed to start within timeout")
    #         return False
            
    #     except Exception as e:
    #         logger.error(f"Error starting Code Server: {e}")
    #         return False
    def start(self) -> bool:
        if self.is_running():
            logger.info("Code Server is already running")
            return True

        try:
            self.ensure_workspace_exists()

            cmd = [
                "/usr/bin/code-server",  # or just "code-server" if in PATH
                "--bind-addr", f"0.0.0.0:{self.port}",
                "--auth", "password",
                "--disable-workspace-trust",
                self.workspace_dir
            ]

            env = os.environ.copy()
            env["PASSWORD"] = self.password

            logger.info(f"Starting Code Server with command: {' '.join(cmd)}")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.workspace_dir,
                env=env,
            )

            for attempt in range(30):
                if self.is_running():
                    logger.info(f"Code Server started successfully on port {self.port}")
                    return True
                time.sleep(1)

            logger.error("Code Server failed to start within timeout")
            return False

        except Exception as e:
            logger.error(f"Error starting Code Server: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop Code Server if running."""
        try:
            if not self.is_running():
                logger.info("Code Server is not running")
                return True
            
            # Find and terminate Code Server processes
            terminated = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'code-server' in proc.info['name'] or \
                       any('code-server' in cmd for cmd in proc.info['cmdline'] if cmd):
                        proc.terminate()
                        terminated = True
                        logger.info(f"Terminated Code Server process {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if terminated:
                # Wait for processes to terminate
                time.sleep(3)
                
                # Force kill if still running
                if self.is_running():
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if 'code-server' in proc.info['name'] or \
                               any('code-server' in cmd for cmd in proc.info['cmdline'] if cmd):
                                proc.kill()
                                logger.info(f"Force killed Code Server process {proc.info['pid']}")
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
            
            return not self.is_running()
            
        except Exception as e:
            logger.error(f"Error stopping Code Server: {e}")
            return False
    
    def restart(self) -> bool:
        """Restart Code Server."""
        logger.info("Restarting Code Server")
        if self.stop():
            time.sleep(2)
            return self.start()
        return False
    
    def get_workspace_files(self) -> list:
        """Get list of files in the workspace."""
        try:
            files = []
            for root, dirs, filenames in os.walk(self.workspace_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, self.workspace_dir)
                    files.append(rel_path)
            return files
        except Exception as e:
            logger.error(f"Error getting workspace files: {e}")
            return []
    
    def write_file(self, filename: str, content: str) -> bool:
        """Write content to a file in the workspace."""
        try:
            file_path = os.path.join(self.workspace_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"File written: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error writing file {filename}: {e}")
            return False
    
    def read_file(self, filename: str) -> Optional[str]:
        """Read content from a file in the workspace."""
        try:
            file_path = os.path.join(self.workspace_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            return None
    
    def cleanup_workspace(self) -> bool:
        """Clean up the workspace directory."""
        try:
            import shutil
            if os.path.exists(self.workspace_dir):
                shutil.rmtree(self.workspace_dir)
            self.ensure_workspace_exists()
            logger.info("Workspace cleaned up")
            return True
        except Exception as e:
            logger.error(f"Error cleaning up workspace: {e}")
            return False


# Global instance
code_server_manager = CodeServerManager()


def detect_code_request(user_message: str) -> bool:
    """Detect if user message is requesting code-related task."""
    code_keywords = [
        'code', 'script', 'program', 'function', 'class', 'algorithm',
        'python', 'javascript', 'java', 'c++', 'html', 'css',
        'write', 'create', 'build', 'develop', 'implement',
        'game', 'app', 'application', 'website', 'api'
    ]
    
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in code_keywords)


def ensure_code_server_running() -> bool:
    """Ensure Code Server is running, start if necessary."""
    if not code_server_manager.is_running():
        logger.info("Code Server not running, starting...")
        return code_server_manager.start()
    return True


def get_code_server_status() -> Dict[str, Any]:
    """Get current Code Server status."""
    return code_server_manager.get_status()


def collect_generated_code() -> Dict[str, str]:
    """Collect all generated code files from workspace."""
    files = {}
    workspace_files = code_server_manager.get_workspace_files()
    
    for filename in workspace_files:
        content = code_server_manager.read_file(filename)
        if content is not None:
            files[filename] = content
    
    return files


def package_code_for_delivery(files: Dict[str, str]) -> Dict[str, Any]:
    """Package code files for delivery to user."""
    return {
        "files": files,
        "file_count": len(files),
        "workspace_url": f"http://localhost:{code_server_manager.port}",
        "timestamp": time.time()
    }

