import psutil
import logging
from datetime import datetime

# Set up logging to a file
logging.basicConfig(filename='system_health.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Thresholds
CPU_THRESHOLD = 10  # 80%
MEMORY_THRESHOLD = 10  # 80%
DISK_THRESHOLD = 10  # 90%
PROCESS_THRESHOLD = 100  # Number of processes

def check_cpu_usage():
    """Check CPU usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        alert_message = f"High CPU usage detected: {cpu_usage}%"
        log_alert(alert_message)

def check_memory_usage():
    """Check memory usage."""
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        alert_message = f"High memory usage detected: {memory_usage}%"
        log_alert(alert_message)

def check_disk_usage():
    """Check disk usage for all mounted partitions."""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            if usage.percent > DISK_THRESHOLD:
                alert_message = f"High disk usage detected on {partition.mountpoint}: {usage.percent}%"
                log_alert(alert_message)
        except PermissionError:
            # Skips partitions where we don't have access
            continue

def check_running_processes():
    """Check the number of running processes."""
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        alert_message = f"High number of running processes detected: {process_count} processes"
        log_alert(alert_message)

def log_alert(message):
    """Log the alert message to both console and log file."""
    print(message)
    logging.warning(message)


