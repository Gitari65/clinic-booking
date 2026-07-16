# 🏥 Clinic Booking API

## Overview
This project is a FastAPI backend for medical appointment scheduling.
It supports:
- booking appointments
- cancelling appointments
- rescheduling appointments
- checking doctor availability
- listing active patient appointments

## Tech Stack
- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- python-dotenv

## Setup
1. Create and activate a Python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate  # Windows
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Create a `.env` file in the repository root with:
   ```ini
   DATABASE_URL=sqlite:///./clinic.db
   ```
4. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Appointments
- `POST /appointments/`
  - Request body: `AppointmentCreate`
  - Fields: `doctor_id`, `patient_id`, `slot_time`
  - Books a new appointment slot
- `PATCH /appointments/{appointment_id}/cancel`
  - Request body: `AppointmentCancel`
  - Cancels an appointment
- `PATCH /appointments/{appointment_id}/reschedule`
  - Request body: `AppointmentReschedule`
  - Reschedules an appointment to a new slot
- `GET /appointments/patients/{patient_id}`
  - Returns active appointments for a patient

### Doctors
- `GET /doctors/{doctor_id}/availability?query_date=YYYY-MM-DD`
  - Returns available slots for the given doctor on that date

## Models

### Doctor
- `id`
- `full_name`
- `email`
- `work_start`
- `work_end`

### Appointment
- `id`
- `doctor_id`
- `patient_id`
- `slot_time`
- `cancelled`
- `cancel_reason`

## Tests
Run the appointment tests with:
```bash
python -m pytest tests/test_appointment.py -q
```

## Notes
- The app uses SQLite by default.
- Database tables are created automatically at startup.
- Booking logic prevents past bookings, double-booking, and out-of-hours appointments.

## Submission
- GitHub repository: [Add your repository link here]
- Deployed application: [Add your deployment link here]

## Deployment & CI/CD
- Deployment branch: `main`
- Deployment provider: Render
- Public app URL: https://clinic-booking-e9yu.onrender.com/
- Deployment trigger: merges into `main` trigger the deployment workflow
- CI/CD pipeline summary: GitHub Actions runs the test suite on pull requests and deploys the app after a merge into `main`
- CI/CD branch note: this branch is prepared for a pull request review and deployment workflow validation.

### Deployment Steps
1. Create a free Render account and connect your GitHub repository.
2. Create a new Web Service and select this repository.
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Render will build and deploy the app automatically.
5. After the first successful deployment, copy the public Render URL and update the README.

### CI/CD Pipeline Behavior
- Runs the full test suite on every pull request to `main`.
- Deploys automatically when a pull request is merged into `main`.
- Uses GitHub Actions to install dependencies, run pytest, and trigger a Render deploy hook.

### GitHub Secrets
Add this secret in GitHub repository settings:
- `RENDER_DEPLOY_HOOK_URL`: the deploy hook URL from your Render service

### Render Deploy Hook
In Render, open your service and copy the Deploy Hook URL. Then add it as the GitHub secret above.

## Design Decisions
- Used FastAPI for a lightweight, developer-friendly REST API.
- Kept database interaction simple with SQLAlchemy ORM and SQLite for easy local setup.
- Separated business logic into `app/crud.py`, request validation into `app/schemas.py`, and routing into `app/routers`.
- Implemented appointment validation to prevent booking outside doctor hours, duplicate bookings, and past times.

## CI/CD Note
- I set up a basic CI/CD workflow to automatically run tests whenever code is pushed. I used GitHub Actions to run pytest and make sure everything is working before changes are accepted.

This helps catch errors early and keeps the code stable. Even though the project is small, adding CI/CD makes it more reliable and closer to real-world development practices.

## Section 4 Reflection
1. What did you use AI for?

I used AI to help me think through the API design, test edge cases, improve my README content, and check my overall structure while building the project.

2. Example where AI improved your work

One strong example was when I asked AI: “What edge cases should I test for an appointment booking system?” It suggested cases like double-booking, past-time booking, and invalid doctor hours, which helped me build stronger tests.

3. Example where AI was wrong or incomplete

One AI suggestion gave me a test setup that did not reset the database properly. I caught this because the tests started behaving inconsistently, so I fixed the setup using better pytest fixtures and a more reliable test structure.

4. Two decisions without AI

I chose the project structure myself and wrote the appointment conflict logic on my own. I trusted my own judgment because I understood the business rules clearly and wanted to keep the implementation simple, practical, and easy to follow.
