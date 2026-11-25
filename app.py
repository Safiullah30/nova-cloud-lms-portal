import os
from flask import Flask, request, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "k3s-dev")
CAMPUS_NAME = os.getenv("CAMPUS_NAME", "DESC Shankar, Mardan — nova cloud")

COURSES = [
    {"id": 1, "code": "CS-401", "title": "Hybrid Cloud & K3s Architecture", "instructor": "Safiullah", "status": "In Progress"},
    {"id": 2, "code": "CS-405", "title": "GitHub Actions & Container CI/CD", "instructor": "Shabeer", "status": "Completed"},
    {"id": 3, "code": "CS-410", "title": "Platform Design & Release Planning", "instructor": "Hafsa", "status": "Enrolled"},
]

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Student LMS Portal</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 820px; margin: 30px auto; padding: 0 16px; background: #f5f7fb; color: #1f2937; }
    .card { background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; background: #e0e7ff; color: #1d4ed8; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { text-align: left; padding: 10px; border-bottom: 1px solid #e5e7eb; }
    input, select, button { padding: 8px 12px; border-radius: 6px; border: 1px solid #cbd5e1; margin-right: 8px; }
    button { background: #2563eb; color: #fff; border: none; cursor: pointer; }
    button:hover { background: #1d4ed8; }
    .btn-sm { padding: 5px 10px; font-size: 12px; background: #0f766e; }
    .btn-sm:hover { background: #115e59; }
    .meta { font-size: 13px; color: #4b5563; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Student LMS Portal</h2>
    <p class="meta"><strong>Institution:</strong> {{ campus }} &nbsp;|&nbsp; <span class="badge">ENV: {{ env }}</span></p>
  </div>

  <div class="card">
    <h3>My Courses</h3>
    <table>
      <thead>
        <tr>
          <th>Code</th>
          <th>Course Title</th>
          <th>Instructor</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {% for c in courses %}
        <tr>
          <td><strong>{{ c.code }}</strong></td>
          <td>{{ c.title }}</td>
          <td>{{ c.instructor }}</td>
          <td><span class="badge">{{ c.status }}</span></td>
          <td>
            <form method="post" action="{{ url_for('toggle_status', course_id=c.id) }}" style="display:inline;">
              <button type="submit" class="btn-sm">Next Status</button>
            </form>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h3>Add New Course</h3>
    <form method="post" action="{{ url_for('add_course') }}">
      <input type="text" name="code" placeholder="Code (e.g. CS-420)" required>
      <input type="text" name="title" placeholder="Course Name" required>
      <input type="text" name="instructor" placeholder="Instructor" required>
      <button type="submit">Add Course</button>
    </form>
  </div>
</body>
</html>
"""

STATUS_FLOW = ["Enrolled", "In Progress", "Completed"]

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "lms-portal", "env": APP_ENV}), 200

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, courses=COURSES, env=APP_ENV, campus=CAMPUS_NAME)

@app.route("/add", methods=["POST"])
def add_course():
    next_id = max([c["id"] for c in COURSES], default=0) + 1
    COURSES.append({
        "id": next_id,
        "code": request.form["code"].strip().upper(),
        "title": request.form["title"].strip(),
        "instructor": request.form["instructor"].strip(),
        "status": "Enrolled"
    })
    return redirect(url_for("index"))

@app.route("/toggle/<int:course_id>", methods=["POST"])
def toggle_status(course_id):
    for c in COURSES:
        if c["id"] == course_id:
            idx = STATUS_FLOW.index(c["status"]) if c["status"] in STATUS_FLOW else -1
            c["status"] = STATUS_FLOW[(idx + 1) % len(STATUS_FLOW)]
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
