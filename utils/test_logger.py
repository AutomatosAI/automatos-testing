import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class WorkflowTestLogger:
    """Enhanced workflow testing logger that provides structured JSON logging for test journeys"""
    
    def __init__(self, journey_name: str, log_file: Optional[str] = None):
        self.journey_name = journey_name
        self.start_time = datetime.now()
        
        # Set up log file
        if log_file:
            self.log_file = log_file
        else:
            timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
            self.log_file = f'logs/{journey_name}_{timestamp}.log'
        
        # Ensure log directory exists
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize journey
        self.log_journey_start()
    
    def log_journey_start(self):
        """Log the start of a journey"""
        print(f'🚀 JOURNEY STARTED: {self.journey_name}')
        print(f'📁 Log file: {self.log_file}')
        print(f'⏰ Start time: {self.start_time}')
    
    def log_step(self, step_id: str, step_name: str, status: str = 'in_progress', 
                 response: Any = None, metadata: Optional[Dict[str, Any]] = None):
        """Log a journey step with structured data"""
        
        # Determine emoji based on status
        if status == 'completed':
            emoji = '✅'
        elif status == 'failed':
            emoji = '❌'
        elif status == 'warning':
            emoji = '⚠️'
        else:
            emoji = '🔄'
        
        message = f'{emoji} STEP {status.upper()}: [{step_id}] {step_name}'
        print(message)
        
        # Also log to file
        with open(self.log_file, 'a') as f:
            f.write(f'{datetime.now().isoformat()} | {message}\n')
    
    def log_api_call(self, method: str, endpoint: str, status_code: int, 
                     response_time_ms: float, response_data: Any = None,
                     request_data: Any = None):
        """Log API call details"""
        
        status_emoji = '✅' if status_code < 400 else '❌'
        message = f'{status_emoji} API {method} {endpoint} - HTTP {status_code} ({response_time_ms:.1f}ms)'
        print(message)
        
        # Log to file
        with open(self.log_file, 'a') as f:
            f.write(f'{datetime.now().isoformat()} | {message}\n')
    
    def log_validation(self, validation_name: str, expected: Any, actual: Any, passed: bool):
        """Log validation results"""
        
        emoji = '✅' if passed else '❌'
        status = 'PASSED' if passed else 'FAILED'
        message = f'{emoji} VALIDATION {status}: {validation_name}'
        print(message)
        
        if not passed:
            print(f'  Expected: {expected}')
            print(f'  Actual: {actual}')
    
    def log_journey_end(self, status: str = 'completed', summary: Optional[Dict[str, Any]] = None):
        """Log the end of a journey"""
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        emoji = '🎉' if status == 'completed' else '💥'
        print(f'{emoji} JOURNEY {status.upper()}: {self.journey_name}')
        print(f'⏱️ Duration: {duration:.2f} seconds')
        
        if summary:
            print('📊 Summary:')
            for key, value in summary.items():
                print(f'  {key}: {value}')
    
    def log_error(self, error_message: str, exception: Optional[Exception] = None):
        """Log error with details"""
        print(f'💥 ERROR: {error_message}')
        if exception:
            print(f'Exception details: {exception}')
