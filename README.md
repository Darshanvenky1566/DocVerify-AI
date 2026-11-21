# DocVerify AI

AI-Powered Document Verification System

## Project Information

- Student: Darshan Venkatesh
- Module: MIT 5.2 – Senior IT Project
- Institution: Mediadesign Hochschule
- Professor: Dr. Ali Alhosseini
- Semester: Winter Semester 2026/27
- Project format: Individual project

## Overview

DocVerify AI is a planned web platform that helps applicants submit
documents and supports reviewers in checking completeness, validity,
consistency, and compliance with defined requirements.

The system will use OCR, a large language model, and
Retrieval-Augmented Generation (RAG) to produce explainable findings
with references to verification rules.

A human reviewer makes the final decision. AI findings do not prove
document authenticity.

## Current Status

Phase 1 product definition is documented. Phase 2 core features are implemented, including authentication, role-based access, document upload, application submission, and the reviewer dashboard. All four Docker services start together, and CI passes on the feature branch. Submission documentation and integration into main are in progress.

## Documentation
- [Phase 2 implementation sprint](docs/sprints/phase-2.md)
- [Phase 1 – Product Definition](docs/phase-1/product-definition.md)
- Sprint documentation: docs/sprints/

## Data Protection

Only synthetic or anonymized test documents will be used.
API keys and secrets must never be committed to this repository.

## Project Management

- [GitHub Repository](https://github.com/Darshanvenky1566/DocVerify-AI)
- [Product Backlog](https://github.com/users/Darshanvenky1566/projects/1/views/2)

The backlog contains user stories with acceptance criteria and
MoSCoW priorities. Implementation has not started, so the stories
remain in Todo.

US01–US12 are Must priorities. US13 is optional (Could).
US14 is excluded from this release (Won't).

Future changes will use feature branches and pull requests.
Pull-request review and approval must follow the assignment requirements.


## Phase 2 setup

Install Docker Desktop and Git. Start Docker Desktop before running these commands.

```bash
git clone https://github.com/Darshanvenky1566/DocVerify-AI.git
cd DocVerify-AI
cp .env.example .env
```

Edit `.env` and replace `replace_with_your_own_password` with a password of your choice.

Start all four services and build the application images.

```bash
docker compose up -d --build
```

Open the reviewer dashboard at http://127.0.0.1:8080/.

Open Swagger UI at http://127.0.0.1:8004/docs.

PostgreSQL stores application data and uploaded files. Qdrant runs on port 6333 for the vector database infrastructure. The backend creates its database tables automatically at startup.

## Create accounts for a fresh installation

In Swagger, use `POST /auth/register` to create an applicant account. New accounts receive the applicant role.

To create a reviewer, register `reviewer-test@example.com` with a password of your choice, then run this command from the project folder.

```bash
docker compose exec db psql -U docverify -d docverify -c "UPDATE users SET role = 'reviewer' WHERE email = 'reviewer-test@example.com';"
```

Sign in to the reviewer dashboard using that email and the password you registered.

For an administrator account, register `admin-test@example.com`, then run the following command.

```bash
docker compose exec db psql -U docverify -d docverify -c "UPDATE users SET role = 'admin' WHERE email = 'admin-test@example.com';"
```

Use the administrator account with the administration endpoints in Swagger.

## Demonstration

1. Register and sign in as an applicant using Swagger.
2. Copy the returned access token into Swagger's Authorize dialog.
3. Create an application, upload a supported test document, and submit the application.
4. Sign in to the reviewer dashboard as a reviewer.
5. Open the submitted application's document list and download a document.
6. Approve or reject the application with a reason.
7. Sign in as the applicant again and list applications to see the updated status.

Use synthetic or anonymized documents for testing.

## Automated checks

GitHub Actions runs Python linting, six API tests, Compose validation, and backend/frontend image builds on every push and pull request.

To run linting and tests locally with Python 3.11, first create a virtual environment if needed.

```bash
python3.11 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-dev.txt
backend/.venv/bin/python -m ruff check backend/app backend/tests
PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q
```

## Stop the services

```bash
docker compose down
```

Named Docker volumes retain the database and vector database data between restarts.