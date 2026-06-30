from flask import Flask, render_template, request, send_file, jsonify
from services.jira_client import JiraClient
from services.calculations import process_project
from services.exporter import create_excel_files
from services.zipper import create_zip
from services.worker import run_job, get_job
from services.dashboard import build_dashboard

app = Flask(__name__)
client = JiraClient()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return jsonify(client.get_projects())

@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    projects = data.get("projects", [])

    job_id = run_job(process_export, projects)

    return jsonify({"job_id": job_id})

@app.route("/status/<job_id>")
def status(job_id):
    return jsonify(get_job(job_id))

@app.route("/download/<job_id>")
def download(job_id):
    job = get_job(job_id)
    if not job or job.get("status") != "done":
        return "Not ready", 400

    return send_file(job["result"], as_attachment=True)

# ----------------------------
# DASHBOARD API
# ----------------------------
@app.route("/api/dashboard", methods=["POST"])
def dashboard_api():
    data = request.get_json()
    projects = data.get("projects", [])

    result = build_dashboard(client, projects)

    return jsonify(result)

# ----------------------------
# PIPELINE
# ----------------------------
def process_export(job_id, projects):

    files = []
    total = len(projects)

    for i, p in enumerate(projects):

        issues = client.download_project(p)

        durations, transitions = process_project(p, issues)

        files += create_excel_files(p, durations, transitions)

        progress = int(((i + 1) / total) * 100)

        from services.worker import update_progress
        update_progress(job_id, progress)

    zip_path = create_zip(files)

    from services.worker import update_progress
    update_progress(job_id, 100)

    return zip_path

if __name__ == "__main__":
    app.run(debug=True, port=5000)
