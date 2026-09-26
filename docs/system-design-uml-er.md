# System Design - UML and ER Diagram

This design reflects the current function-based Flask application. The UML view models source modules as components because the project does not define application classes for these services.

## UML Component View

```mermaid
classDiagram
    direction LR

    class FlaskRoutes {
        <<module>>
        +register()
        +login()
        +reset_password()
        +logout()
        +home()
        +analyze()
        +privacy()
        +email_verification()
        +website_verification()
        +history()
    }

    class JobAnalyzer {
        <<module>>
        +analyze_job(text)
    }

    class ScamPipeline {
        <<artifact>>
        +predict(text)
        +predict_proba(text)
    }

    class PrivacyAnalyzer {
        <<module>>
        +analyze_resume(text)
    }

    class EmailVerifier {
        <<module>>
        +verify_email(email)
    }

    class WebsiteVerifier {
        <<module>>
        +verify_website(url)
    }

    class HistoryDatabaseAPI {
        <<module>>
        +create_table()
        +create_user(username, password_hash)
        +get_user(username)
        +update_user_password(username, password_hash)
        +save_analysis(user_id, type, input, result)
        +get_history(user_id)
    }

    class SQLiteDatabase {
        <<database>>
        users
        analysis_history
    }

    class SignedSession {
        <<session>>
        user_id
        username
    }

    class ResetKey {
        <<environment>>
        CAREERSHIELD_RESET_KEY
    }

    FlaskRoutes ..> JobAnalyzer : calls analyze_job
    FlaskRoutes ..> PrivacyAnalyzer : calls analyze_resume
    FlaskRoutes ..> EmailVerifier : calls verify_email
    FlaskRoutes ..> WebsiteVerifier : calls verify_website
    FlaskRoutes ..> HistoryDatabaseAPI : auth and history operations
    JobAnalyzer ..> ScamPipeline : predicts with loaded model
    HistoryDatabaseAPI --> SQLiteDatabase : reads and writes
    FlaskRoutes ..> SignedSession : checks and updates session
    FlaskRoutes ..> ResetKey : validates local password reset
```

`ScamPipeline` is loaded from `models/scam_pipeline.joblib`; it is a TF-IDF and Logistic Regression pipeline. The analyzer modules are Python functions, not separately instantiated service classes.

## Entity-Relationship Diagram

```mermaid
erDiagram
    USERS o|--o{ ANALYSIS_HISTORY : associates

    USERS {
        INTEGER id PK "autoincrement"
        TEXT username UK "not null"
        TEXT password_hash "not null; Werkzeug hash"
        TIMESTAMP created_at "default current timestamp"
    }

    ANALYSIS_HISTORY {
        INTEGER id PK "autoincrement"
        INTEGER user_id FK "nullable; references users.id"
        TEXT analysis_type "not null"
        TEXT input_text "not null"
        TEXT result "not null; stringified result dictionary"
        TIMESTAMP created_at "default current timestamp"
    }
```

A user may have zero or many history records; a history record may have no associated user because `user_id` is nullable. The schema declares the foreign key, although SQLite foreign-key enforcement is not enabled explicitly by the current connection code. User accounts do not store an email address, and password-reset keys/tokens are not persisted in the database.
