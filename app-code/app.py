from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os
import socket
import psutil
from datetime import timedelta

app = Flask(__name__)


def get_pod_name():
    return os.environ.get('HOSTNAME', socket.gethostname())

def get_git_sha():
   
    sha = os.environ.get('GIT_SHA')
    if sha:
        return sha[:7]

   
    try:
        with open('git_sha.txt') as f:
            return f.read().strip()[:7]
    except:
        return "local-dev"
def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return str(timedelta(seconds=int(uptime_seconds))).split('.')[0]
    except:
        return "unknown"

def get_version():
    try:
        with open("version.txt") as f:
            return f.read().strip()
    except:
        return "v1.0.0"

@app.route('/')
def home():
   
    transactions = [
        {"type": "Debit", "amount": "$120", "desc": "Grocery Store", "time": "10:32 AM"},
        {"type": "Credit", "amount": "$500", "desc": "Salary Deposit", "time": "09:00 AM"},
        {"type": "Debit", "amount": "$60", "desc": "Uber Ride", "time": "Yesterday"},
        {"type": "Debit", "amount": "$45", "desc": "Netflix", "time": "Yesterday"},
        {"type": "Credit", "amount": "$50", "desc": "Refund", "time": "Yesterday"}
    ]

    services = [
        {"name": "Payment Gateway", "status": "Running", "latency": "23ms"},
        {"name": "Database Cluster", "status": "Running", "latency": "8ms"},
        {"name": "Auth Service", "status": "Running", "latency": "15ms"},
        {"name": "Redis Cache", "status": "Running", "latency": "2ms"},
        {"name": "Notification Service", "status": "Degraded", "error": "High latency"}
    ]

    logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": "Payment processed successfully"},
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": "User authentication completed"},
        {"time": (datetime.now() - timedelta(minutes=5)).strftime("%H:%M:%S"), "level": "WARNING", "message": "High memory usage detected"},
        {"time": (datetime.now() - timedelta(minutes=10)).strftime("%H:%M:%S"), "level": "INFO", "message": "Database backup completed"},
        {"time": (datetime.now() - timedelta(minutes=15)).strftime("%H:%M:%S"), "level": "ERROR", "message": "Notification service timeout"}
    ]

    return render_template(
        "index.html",
        version=get_version(),
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        balance=5230,
        transactions=transactions,
        services=services,
        logs=logs,
        namespace=os.environ.get('NAMESPACE', 'default'),
        git_sha=get_git_sha(),
        uptime=get_uptime(),
        pod_name=get_pod_name(),
        image_tag=os.environ.get('IMAGE_TAG', get_version()),
        git_repo=os.environ.get('GIT_REPO', 'https://github.com/Misha010199/bank-monitoring-dashboard'),
        trigger_name=os.environ.get('TRIGGER_NAME', 'bank-dashboard-trigger'),
        build_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        datetime=datetime
    )

@app.route('/api')
def api():
    return jsonify({
        "version": get_version(),
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pod": get_pod_name(),
        "services": {
            "payment": "running",
            "database": "running", 
            "auth": "running"
        }
    })

@app.route('/api/logs')
def api_logs():
   
    logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": "Auto-refreshed log entry"},
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "DEBUG", "message": "Health check passed"}
    ]
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)