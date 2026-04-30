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


def get_real_build_time():
    try:
        with open('build_time.txt') as f:
            return f.read().strip()
    except:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S PKT")


def get_build_info():
    try:
        with open('build_info.txt') as f:
            return f.read().strip()
    except:
        return "Build info not available"



def get_build_details():
    details = {}
    try:
        with open('build_details.txt') as f:
            for line in f:
                if ': ' in line:
                    key, value = line.strip().split(': ', 1)
                    details[key] = value
    except:
      
        details = {
            'BUILD_ID': os.environ.get('BUILD_ID', 'N/A'),
            'TRIGGER_NAME': os.environ.get('TRIGGER_NAME', 'bank-trigger'),
            'BUILD_STATUS': 'SUCCESS',
            'BRANCH_NAME': 'main',
            'REPO_NAME': 'bank-monitoring-dashboard',
            'COMMIT_SHA': get_git_sha(),
            'SHORT_SHA': get_git_sha(),
            'PROJECT_ID': os.environ.get('PROJECT_ID', 'bank-dashboard-project-493816'),
            'LOCATION': 'asia-south1'
        }
    return details


@app.route('/')
def home():
    real_build_time = get_real_build_time()
    real_git_sha = get_git_sha()
    real_build_info = get_build_info()
    build_details = get_build_details()   
    
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
        {"name": "Notification Service", "status": "Running", "latency": "45ms"}
    ]

    logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": f"✅ Git commit: {real_git_sha} - Deployed via Cloud Build"},
        {"time": real_build_time.split()[1] if ' ' in real_build_time else datetime.now().strftime("%H:%M:%S"), "level": "SUCCESS", "message": f"🚀 Cloud Build triggered deployment at {real_build_time}"},
        {"time": (datetime.now() - timedelta(minutes=2)).strftime("%H:%M:%S"), "level": "INFO", "message": "📦 Image pushed to Artifact Registry"},
        {"time": (datetime.now() - timedelta(minutes=3)).strftime("%H:%M:%S"), "level": "INFO", "message": "🔄 GKE rolling update initiated"},
        {"time": (datetime.now() - timedelta(minutes=5)).strftime("%H:%M:%S"), "level": "INFO", "message": "✅ Deployment successful - 2 pods running"},
    ]

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    alerts = [
        {"level": "SUCCESS", "message": f"✅ Latest Git commit {real_git_sha} deployed successfully"},
        {"level": "INFO", "message": f"⏱️  Last Cloud Build: {real_build_time}"},
        {"level": "INFO", "message": f"🆔 Build ID: {build_details.get('BUILD_ID', 'N/A')[:20]}..."},
        {"level": "INFO", "message": "🟢 GKE cluster health: All nodes ready"},
    ]

    return render_template(
        "index.html",
        version=get_version(),
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S PKT"),
        balance=8247,
        transactions=transactions,
        services=services,
        logs=logs,
        namespace=os.environ.get('NAMESPACE', 'production'),
        git_sha=real_git_sha,
        uptime=get_uptime(),
        pod_name=get_pod_name(),
        image_tag=os.environ.get('IMAGE_TAG', f"build-{real_git_sha}"),
        git_repo=os.environ.get('GIT_REPO', 'https://github.com/Misha010199/bank-monitoring-dashboard'),
        trigger_name=os.environ.get('TRIGGER_NAME', 'bank-dashboard-trigger'),
        build_time=real_build_time,
        datetime=datetime,
        cpu=cpu,
        memory=memory,
        alerts=alerts,
        build_info=real_build_info,
        build_details=build_details,  
    )


@app.route('/api')
def api():
    build_details = get_build_details()
    return jsonify({
        "version": get_version(),
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pod": get_pod_name(),
        "last_build_time": get_real_build_time(),
        "git_commit": get_git_sha(),
        "build_id": build_details.get('BUILD_ID', 'N/A'),
        "trigger_name": build_details.get('TRIGGER_NAME', 'N/A'),
        "services": {
            "payment": "running",
            "database": "running",
            "auth": "running"
        }
    })


@app.route('/api/logs')
def api_logs():
    build_details = get_build_details()
    logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": f"Git commit: {get_git_sha()} - Active"},
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": f"Build ID: {build_details.get('BUILD_ID', 'N/A')[:20]}..."},
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": f"Trigger: {build_details.get('TRIGGER_NAME', 'N/A')}"},
        {"time": datetime.now().strftime("%H:%M:%S"), "level": "DEBUG", "message": "Health check passed"}
    ]
    return jsonify({"logs": logs})


@app.route('/api/deployment-info')
def deployment_info():
    build_details = get_build_details()
    return jsonify({
        "git_commit": get_git_sha(),
        "build_time": get_real_build_time(),
        "build_info": get_build_info(),
        "pod_name": get_pod_name(),
        "uptime": get_uptime(),
        "build_id": build_details.get('BUILD_ID', 'N/A'),
        "trigger_name": build_details.get('TRIGGER_NAME', 'N/A'),
        "branch": build_details.get('BRANCH_NAME', 'main'),
        "repo": build_details.get('REPO_NAME', 'bank-monitoring-dashboard'),
        "timestamp": datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)