
import hmac
import os
from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from analyzer import analyze_job
from privacy_analyzer import analyze_resume
from email_verifier import verify_email
from website_verifier import verify_website

from history_db import (
    create_table,
    create_user,
    get_history,
    get_user,
    save_analysis,
    update_user_password,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "CAREERSHIELD_SECRET_KEY",
    "career-shield-development-key"
)
app.config["PASSWORD_RESET_KEY"] = os.environ.get("CAREERSHIELD_RESET_KEY")

create_table()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(username) < 3:
            error = "Username must contain at least 3 characters."
        elif len(password) < 8:
            error = "Password must contain at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif create_user(username, generate_password_hash(password)) is None:
            error = "That username is already registered."
        else:
            return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = get_user(username)

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Invalid username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(request.args.get("next") or url_for("home"))

    return render_template("login.html", error=error)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    error = None
    success = None
    reset_key = app.config["PASSWORD_RESET_KEY"]

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        submitted_key = request.form.get("reset_key", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not reset_key:
            error = "Password reset is not enabled on this server."
        elif not hmac.compare_digest(submitted_key, reset_key):
            error = "Invalid reset key."
        elif len(username) < 3:
            error = "Enter a valid username."
        elif len(password) < 8:
            error = "Password must contain at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif not update_user_password(username, generate_password_hash(password)):
            error = "No account was found for that username."
        else:
            success = "Password updated. You can now log in."

    return render_template(
        "reset_password.html",
        enabled=bool(reset_key),
        error=error,
        success=success
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    result = None

    if request.method == "POST":
        job_text = request.form.get("job_text", "").strip()

        if job_text:
            result = analyze_job(job_text)

            save_analysis(
                session["user_id"],
                "Job Scam Detection",
                job_text,
                result
            )

    return render_template("index.html", result=result)


@app.route("/privacy", methods=["GET", "POST"])
@login_required
def privacy():
    result = None

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()

        if resume_text:
            result = analyze_resume(resume_text)

            save_analysis(
                session["user_id"],
                "Resume Privacy Analysis",
                resume_text,
                result
            )

    return render_template("privacy.html", result=result)


@app.route("/email", methods=["GET", "POST"])
@login_required
def email_verification():
    result = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()

        if email:
            result = verify_email(email)

            save_analysis(
                session["user_id"],
                "Recruiter Email Verification",
                email,
                result
            )

    return render_template("email.html", result=result)


@app.route("/history")
@login_required
def history():

    all_records = get_history(session["user_id"])
    records = all_records

    job_count = sum(record[1] == "Job Scam Detection" for record in all_records)
    privacy_count = sum(record[1] == "Resume Privacy Analysis" for record in all_records)
    verification_count = sum(
        record[1] in (
            "Recruiter Email Verification",
            "Company Website Verification"
        )
        for record in all_records
    )

    filter_key = request.args.get("filter", "all")
    filter_types = {
        "jobs": "Job Scam Detection",
        "privacy": "Resume Privacy Analysis",
        "verification": (
            "Recruiter Email Verification",
            "Company Website Verification"
        )
    }

    if filter_key in filter_types:
        selected_type = filter_types[filter_key]
        if isinstance(selected_type, tuple):
            records = [record for record in records if record[1] in selected_type]
        else:
            records = [record for record in records if record[1] == selected_type]
    else:
        filter_key = "all"

    per_page = 10
    filtered_records = len(records)
    total_pages = max((filtered_records + per_page - 1) // per_page, 1)
    page = request.args.get("page", 1, type=int)
    page = min(max(page, 1), total_pages)

    start_index = (page - 1) * per_page
    page_records = records[start_index:start_index + per_page]

    formatted_records = []

    import ast

    for record in page_records:

        record_id = record[0]
        analysis_type = record[1]
        input_text = record[2]
        result_text = record[3]
        created_at = record[4]

        try:
            result = ast.literal_eval(result_text)
        except (ValueError, SyntaxError):
            result = {}

        formatted_records.append({
            "id": record_id,
            "type": analysis_type,
            "input_text": input_text,
            "result": result,
            "date": created_at
        })

    return render_template(
        "history.html",
        records=formatted_records,
        page=page,
        total_pages=total_pages,
        total_records=filtered_records,
        total_all_records=len(all_records),
        job_count=job_count,
        privacy_count=privacy_count,
        verification_count=verification_count,
        per_page=per_page,
        filter_key=filter_key
    )


@app.route("/website", methods=["GET", "POST"])
@login_required
def website_verification():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if url:
            result = verify_website(url)

            save_analysis(
                session["user_id"],
                "Company Website Verification",
                url,
                result
            )

    return render_template("website.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)