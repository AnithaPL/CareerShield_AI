# System Design - DFD and Flowchart

These diagrams describe the current implementation in `app.py`, the analyzer modules, and `history_db.py`.

## Data Flow Diagram

```mermaid
flowchart LR
    User[User / browser]

    subgraph System[CareerShield Flask application]
        Routes[Flask routes and Jinja templates]
        Job[Job analyzer<br/>joblib model + rule checks]
        Privacy[Resume privacy analyzer<br/>regex findings + score]
        Email[Recruiter email verifier<br/>format + domain category]
        Website[Website verifier<br/>URL parsing + HTTPS scheme]
        Users[(users table)]
        History[(analysis_history table)]
        ResetConfig[Server environment<br/>CAREERSHIELD_RESET_KEY]
    end

    User -->|credentials and analysis input| Routes
    Routes -->|HTML, results, history| User
    Routes -->|register, lookup, password hash update| Users
    Users -->|user id, username, password hash| Routes
    Routes -->|job text| Job
    Job -->|prediction, confidence, risk score, reasons| Routes
    Routes -->|resume text| Privacy
    Privacy -->|privacy score and findings| Routes
    Routes -->|recruiter email| Email
    Email -->|format validity and email type| Routes
    Routes -->|website URL| Website
    Website -->|format validity, scheme, domain| Routes
    Routes -->|insert result / request history| History
    History -->|user-specific records| Routes
    ResetConfig -->|shared reset-key value at startup| Routes
```

The application does not send password-reset email, perform DNS/domain ownership checks, or fetch websites. The website verifier parses the URL and checks its scheme only. Flask session data is kept in a signed browser cookie; passwords are stored as Werkzeug password hashes. The reset key is read from the server environment and is not stored in SQLite.

## Flowcharts

### Account and Session Flow

```mermaid
flowchart TD
    Start([Request arrives]) --> Route{Account route?}
    Route -->|Register| Register[Read username and passwords]
    Register --> RegValid{Username at least 3 characters;<br/>password at least 8 and confirmation matches?}
    RegValid -->|No| RegError[Render registration error]
    RegValid -->|Yes| SaveUser[Hash password and insert user]
    SaveUser --> LoginPage[Redirect to login]

    Route -->|Login| Login[Read username and password]
    Login --> Lookup[Load user and verify password hash]
    Lookup --> LoginValid{Credentials valid?}
    LoginValid -->|No| LoginError[Render login error]
    LoginValid -->|Yes| SetSession[Clear and set user_id and username in session]
    SetSession --> Protected[Continue to requested protected route]

    Route -->|Reset password| ResetKey{CAREERSHIELD_RESET_KEY configured<br/>and submitted key matches?}
    ResetKey -->|No| ResetError[Render reset error]
    ResetKey -->|Yes| ResetValid{Username exists;<br/>new password valid and confirmed?}
    ResetValid -->|No| ResetError
    ResetValid -->|Yes| UpdateHash[Hash new password and update user row]
    UpdateHash --> ResetDone[Show success and link to login]

    Route -->|Logout| ClearSession[Clear session]
    ClearSession --> LoginPage
```

### Protected Analysis Flow

```mermaid
flowchart TD
    Request([Protected route request]) --> Session{user_id in session?}
    Session -->|No| Redirect[Redirect to login]
    Session -->|Yes| Dispatch{Requested route}

    Dispatch -->|GET analysis page| Form[Render module form]
    Dispatch -->|POST analysis| HasInput{Required input is non-empty?}
    HasInput -->|No| Form
    HasInput -->|Yes| AnalysisType{Analysis type}
    AnalysisType -->|Job text| Job[analyze_job: model prediction + rule checks]
    AnalysisType -->|Resume text| Privacy[analyze_resume: sensitive-data patterns]
    AnalysisType -->|Recruiter email| Email[verify_email: syntax + domain category]
    AnalysisType -->|Website URL| Website[verify_website: URL + HTTPS scheme]
    Dispatch -->|GET history| Query[Load this user's records, filter, and paginate]

    Job --> Save[Save analysis type, input, and result]
    Privacy --> Save
    Email --> Save
    Website --> Save
    Save --> Result[Render result in the matching template]
    Query --> HistoryPage[Render history page]
```

Analysis results are saved only after a non-empty analysis submission. Loading a form or viewing history does not create an analysis record.
