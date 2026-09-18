
import joblib
import re


MODEL_PATH = "models/scam_pipeline.joblib"

# Load the trained ML model
model = joblib.load(MODEL_PATH)


def analyze_job(text):

    # Convert input to string
    text = str(text).strip()

    # Original ML prediction (Genuine / Likely Scam)
    ml_prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    text_lower = text.lower()

    risk_score = 0
    reasons = []

    # --------------------------------------------------
    # Helper function to add warning points
    # --------------------------------------------------

    def add_warning(points, message):
        nonlocal risk_score

        risk_score += points

        explanation = f"{message} (+{points} points)"

        if explanation not in reasons:
            reasons.append(explanation)

    # --------------------------------------------------
    # 1. PAYMENT AND FINANCIAL FRAUD WARNING
    # --------------------------------------------------

    payment_pattern = (
        r"registration fee|processing fee|pay money|transfer money|"
        r"security deposit|payment required|visa charges|visa fee|"
        r"immigration fee|document processing fee|"
        r"pay.*advance|advance.*payment"
    )

    payment_exemption = (
        r"no registration fee|no processing fee|"
        r"no payment|no fees|without payment|no visa fee"
    )

    if (
        re.search(payment_pattern, text_lower)
        and not re.search(payment_exemption, text_lower)
    ):
        add_warning(
            30,
            "Job advertisement requests payment or advance fees."
        )

    # --------------------------------------------------
    # 2. GUARANTEED EMPLOYMENT WARNING
    # --------------------------------------------------

    if re.search(
        r"100% assured job|guaranteed job|assured employment|"
        r"guaranteed employment|job guaranteed|"
        r"guaranteed placement",
        text_lower
    ):
        add_warning(
            25,
            "Advertisement makes guaranteed employment claims."
        )

    # --------------------------------------------------
    # 3. OVERSEAS RECRUITMENT WARNING
    # --------------------------------------------------

    if re.search(
        r"free accommodation|free food|air tickets|family migration|"
        r"sponsor your relatives|guaranteed pr|permanent residency|"
        r"free visa",
        text_lower
    ):
        add_warning(
            15,
            "Advertisement contains broad overseas employment "
            "or migration promises."
        )

    # --------------------------------------------------
    # 4. SENSITIVE FINANCIAL INFORMATION WARNING
    # --------------------------------------------------

    if re.search(
        r"password|bank details|credit card|otp|"
        r"banking credentials|pin number|debit card details",
        text_lower
    ):
        add_warning(
            30,
            "Sensitive financial or account information is requested."
        )

    # --------------------------------------------------
    # 5. URGENCY AND PRESSURE WARNING
    # --------------------------------------------------

    if re.search(
        r"urgent|immediately|act now|limited vacancies|"
        r"join today|respond today|last chance|quick response",
        text_lower
    ):
        add_warning(
            20,
            "Advertisement uses urgency or pressure tactics."
        )

    # --------------------------------------------------
    # 6. PERSONAL DOCUMENTS WARNING
    # --------------------------------------------------

    if re.search(
        r"passport|tax details|identity documents|private documents|"
        r"aadhaar|aadhar|identity card|id proof|"
        r"personal documents|submit documents|send documents",
        text_lower
    ):
        add_warning(
            20,
            "Advertisement requests sensitive personal documents."
        )

    # --------------------------------------------------
    # 7. WHATSAPP AND TELEGRAM RECRUITMENT WARNING
    # --------------------------------------------------

    if re.search(
        r"whatsapp|telegram|contact via whatsapp|"
        r"send on whatsapp|message on telegram",
        text_lower
    ):
        add_warning(
            10,
            "Recruitment communication uses messaging applications. "
            "Independent verification is recommended."
        )

    # --------------------------------------------------
    # 8. UNCLEAR COMPANY OR JOB DETAILS WARNING
    # --------------------------------------------------

    if re.search(
        r"unclear company|unknown company|"
        r"limited company information|vague responsibilities|"
        r"unclear responsibilities|company details unavailable",
        text_lower
    ):
        add_warning(
            15,
            "Company information or job responsibilities are unclear."
        )

    # --------------------------------------------------
    # 9. UNVERIFIED COMMUNICATION WARNING
    # --------------------------------------------------

    if re.search(
        r"unverified messaging|unverified account|unknown link|"
        r"personal email address|contact only through chat",
        text_lower
    ):
        add_warning(
            15,
            "Recruiter communication cannot be easily verified."
        )

    # --------------------------------------------------
    # 10. UNREALISTIC SALARY OR INCOME WARNING
    # --------------------------------------------------

    if re.search(
        r"unusually high salary|unrealistic salary|"
        r"guaranteed income|quick promotion|"
        r"attractive salary|attractive monthly income|"
        r"earn.*per month|earn.*monthly",
        text_lower
    ):
        add_warning(
            15,
            "Advertisement contains potentially unrealistic "
            "salary or income promises."
        )

    # --------------------------------------------------
    # 11. NO INTERVIEW WARNING
    # --------------------------------------------------

    if re.search(
        r"avoids video interview|no interview|"
        r"without an interview|no verification",
        text_lower
    ):
        add_warning(
            15,
            "Recruitment process lacks normal verification steps."
        )

    # --------------------------------------------------
    # 12. LIMIT RISK SCORE TO 100
    # --------------------------------------------------

    risk_score = min(risk_score, 100)

    # --------------------------------------------------
    # 13. DETERMINE RISK LEVEL
    # --------------------------------------------------

    if risk_score <= 30:
        risk_level = "Low"

    elif risk_score <= 60:
        risk_level = "Medium"

    else:
        risk_level = "High"

    # --------------------------------------------------
    # 14. DETERMINE THREE-CLASS PREDICTION
    # --------------------------------------------------

    if risk_score >= 60:
        final_prediction = "Likely Scam"

    elif (
        ml_prediction == "Likely Scam"
        and confidence >= 75
    ):
        final_prediction = "Likely Scam"

    elif risk_score >= 30:
        final_prediction = "Suspicious"

    elif ml_prediction == "Likely Scam":
        final_prediction = "Suspicious"

    elif (
        ml_prediction == "Genuine"
        and confidence < 70
    ):
        final_prediction = "Suspicious"

    else:
        final_prediction = "Genuine"

    # --------------------------------------------------
    # 15. DETERMINE OVERALL ASSESSMENT
    # --------------------------------------------------

    if final_prediction == "Likely Scam":
        overall_assessment = (
            "High Risk - Further Verification Required"
        )

    elif final_prediction == "Suspicious":
        overall_assessment = (
            "Caution - Verify Independently"
        )

    else:
        overall_assessment = (
            "No Specific Warning Signals Detected"
        )

    # --------------------------------------------------
    # 16. COMBINE ML PREDICTION AND RULE SCORE
    # --------------------------------------------------

    if risk_score >= 60:
        final_decision = "High Risk"

    elif (
        ml_prediction == "Likely Scam"
        and confidence >= 75
    ):
        final_decision = "High Risk - ML Warning"

    elif (
        final_prediction == "Suspicious"
        or risk_score >= 30
    ):
        final_decision = (
            "Medium Risk - Verify Independently"
        )

    else:
        final_decision = (
            "Low Risk - No Specific Warning Signals"
        )

    # --------------------------------------------------
    # 17. LOW ML CONFIDENCE NOTE
    # --------------------------------------------------

    confidence_note = ""

    if confidence < 70:
        confidence_note = (
            "ML confidence is below 70%. "
            "Independent verification is recommended."
        )

    # --------------------------------------------------
    # 18. NO WARNING MESSAGE
    # --------------------------------------------------

    if not reasons:
        reasons.append(
            "No specific warning signals detected."
        )

    # --------------------------------------------------
    # 19. RETURN ANALYSIS RESULT
    # --------------------------------------------------

    return {
        "prediction": final_prediction,
        "ml_prediction": ml_prediction,
        "confidence": round(float(confidence), 2),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "overall_assessment": overall_assessment,
        "final_decision": final_decision,
        "confidence_note": confidence_note,
        "reasons": reasons
    }