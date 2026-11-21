# Phase 2 implementation sprint

Author — Darshan Venkatesh  
Project — DocVerify AI  
Implementation and verification recorded on 18–21 November 2026

## Sprint goal

Implement the document submission and human review workflow, containerize the services, and automate linting, testing, and image builds.

## Delivered functionality

- User registration, login, and logout.
- Applicant, reviewer, and administrator access checks.
- Application creation and submission.
- Document upload, storage, and applicant document listing.
- Reviewer queue for submitted applications.
- Reviewer document listing and downloads.
- Approval and rejection with a reason.
- Reviewer dashboard with sign-in, document downloads, decisions, and sign-out.
- Automatic database table creation during backend startup.

## Containers

Docker Compose starts four services.

| Service | Purpose | Local access |
| --- | --- | --- |
| frontend | Reviewer dashboard and API proxy | http://127.0.0.1:8080 |
| backend | FastAPI application and Swagger | http://127.0.0.1:8004/docs |
| db | PostgreSQL application and document storage | Local port 5432 |
| qdrant | Vector database infrastructure | http://127.0.0.1:6333 |

PostgreSQL and Qdrant use named volumes.

## Verification evidence

| Check | Observed result |
| --- | --- |
| Applicant login | 200 |
| Supported PNG upload | 201 |
| Unsupported document type | 415 |
| Another applicant accessing an owned application's documents | 404 |
| Application submission with an uploaded document | 200 and submitted status |
| Reviewer queue | Submitted application displayed |
| Reviewer document listing | 200 |
| Reviewer document download | PNG downloaded and opened |
| Approval through Swagger | Application status changed to approved |
| Rejection through the dashboard | Application status changed to rejected |
| Sign out and sign in after rejection | Application remained absent from the queue |
| Fresh database startup | Five tables created from an empty database |
| Python linting | All checks passed |
| Automated API tests | Six passed, with one dependency deprecation warning |
| GitHub Actions on feature branch | Passed for commit 7489258 |

The six automated tests cover health, the Swagger redirect, and unauthenticated access to protected routes. Authenticated workflows were checked manually.

## Development workflow

Implementation used the feature branch feat/phase-2-core and descriptive commits.

The CI workflow runs on pushes and pull requests. It performs Python linting, automated API tests, Compose validation, and backend and frontend Docker image builds.

The main branch protection was configured to require pull requests, the checks CI job, and an up-to-date branch before merging. Required external approvals were disabled for this individual project.

## Review and remaining hand-in work

- Link the implementation pull request to the relevant backlog issues and GitHub Project.
- Verify the documented setup from a fresh checkout.
- Review and merge the implementation through a pull request.
- Confirm successful CI on main.
- Update the GitHub Project to reflect verified delivery.
- Submit the repository link and Phase 2 documentation through Teams.

## Retrospective

Small changes followed by verification helped identify indentation and authorization problems early.

A downloaded PNG initially received an incorrect extension through Swagger. Direct API downloads and downloads through the reviewer dashboard opened successfully.

Future work includes the OCR, language model, and retrieval workflow planned for later phases.