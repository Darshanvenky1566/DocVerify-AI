# DocVerify AI — Product Definition

## Project Details

- Author: Darshan Venkatesh
- Module: MIT 5.2 – Senior IT Project
- Professor: Dr. Ali Alhosseini
- Institution: Mediadesign Hochschule
- Semester: Winter Semester 2026/27
- Project format: Individual project
- Document status: Phase 1 draft

## 1. Motivation and Problem Statement

### 1.1 Context

University admissions teams review documents such as degree
certificates, academic transcripts, and language certificates.
Reviewers must check that the required documents are present,
information is consistent, and admission requirements are met.

This project uses university admissions as its initial use case.
The prototype will process synthetic documents and use clearly
labelled demonstration admission rules.

### 1.2 Problem

Manual document verification requires reviewers to read files,
extract information, compare documents, and consult admission rules.

This creates several challenges:

- Time and cost: repetitive checks consume staff time and can
  delay application processing.
- Human error: reviewers may overlook missing fields, expired
  certificates, or inconsistent names and dates.
- Inconsistent decisions: different reviewers may interpret or
  apply the same requirements differently.
- Limited traceability: findings may lack a clear record of the
  rules and evidence used.
- Applicant uncertainty: applicants may not understand which
  documents or corrections are needed.
- Suspicious information: unusual dates or inconsistent content
  may require investigation beyond routine checks.

These are problem assumptions to investigate during the project.
No measured time savings or accuracy improvements are claimed
at this stage.

### 1.3 Why AI Is Suitable

Optical Character Recognition (OCR) can extract text from scanned
documents. Direct PDF text extraction can process digital PDFs.

A Large Language Model (LLM) can help classify documents, extract
structured fields, and explain findings.

Retrieval-Augmented Generation (RAG) can retrieve relevant admission
rules and reference material so that findings cite their sources.

Deterministic checks will handle explicit comparisons, such as
required fields, dates, and minimum scores. AI will support tasks
that require interpreting document text.

### 1.4 Limitations and Human Oversight

OCR can misread text, and LLMs can produce incorrect or unsupported
answers. Retrieved rules may also be incomplete or outdated.

The system must identify missing evidence and uncertain findings.
A human reviewer must inspect the evidence and make the final
decision.

The prototype can flag possible authenticity concerns. It cannot
prove that a document is genuine or replace confirmation from
the issuing institution.

Only synthetic or anonymized documents will be used. Real personal
documents will not be uploaded to external AI services.

## 2. Product Vision

For university admissions teams and applicants who need a clear
and consistent document-checking process, DocVerify AI is a
web-based document verification support platform that extracts
document information, checks it against defined requirements,
and presents explainable findings with source citations.

Unlike a manual workflow using separate files and checklists,
DocVerify AI brings document submission, rule-based checks,
AI-assisted analysis, and human review into one traceable workflow.

The product supports reviewers while keeping final decisions
under human control.

## 3. Personas

These personas are fictional design assumptions, not findings from
user interviews. They will guide development and later usability testing.

### P1 — Aisha Rao: Applicant

- Background: International graduate applying for a master's programme.
- Technical skills: Comfortable with websites and uploading files;
  unfamiliar with document verification processes.
- Goals:
  - Submit all required documents in one application.
  - Know whether files were uploaded successfully.
  - Track progress and understand requests for corrections.
- Frustrations:
  - Unclear document requirements and upload errors.
  - Repeated requests for the same information.
  - Status messages that do not explain what action is needed.
- Needs:
  - Clear upload instructions and useful validation messages.
  - An application checklist and visible document status.
  - Specific requests for additional or replacement documents.

### P2 — Lena Fischer: Admissions Reviewer

- Background: Admissions officer assessing postgraduate applications.
- Technical skills: Confident with office software and admissions
  portals; no programming or AI expertise.
- Goals:
  - Identify missing, inconsistent, or non-compliant information.
  - Compare findings with original documents and relevant rules.
  - Make justified decisions with a clear audit trail.
- Frustrations:
  - Repetitive manual comparisons across multiple files.
  - AI conclusions without evidence or source references.
  - Difficulty correcting extraction errors.
- Needs:
  - Original documents displayed beside extracted fields and reports.
  - Clear explanations, cited rules, and highlighted problem fields.
  - Controls to correct data and accept or override recommendations.

### P3 — Omar Becker: Platform Administrator

- Background: IT administrator supporting the admissions platform.
- Technical skills: Experienced with account management, access
  permissions, configuration, and operational monitoring.
- Goals:
  - Maintain appropriate access for applicants and staff.
  - Keep document types, verification rules, and sources current.
  - Trace which configuration produced a verification result.
- Frustrations:
  - Outdated rules producing inconsistent findings.
  - Unrecorded configuration changes.
  - Limited visibility into processing failures.
- Needs:
  - User and role management.
  - Versioned rules, knowledge-base sources, and prompts.
  - Audit logs and basic operational analytics.

## 4. Usage Scenarios

All documents, identities, institutions, and admission rules used
in these scenarios are synthetic demonstration data.

### SC1 — Applicant Submits an Application

Persona: P1 — Aisha Rao

Context: Aisha needs to submit a degree certificate, academic
transcript, and language certificate for a demonstration programme.

Main flow:

1. Aisha registers and signs in as an applicant.
2. She creates an application and views its required-document checklist.
3. She selects a document type and uploads each PDF, JPG, or PNG file.
4. The system checks file type, size, and readability.
5. Accepted files are linked to her application and queued for processing.
6. Aisha sees upload confirmation and the processing status.
7. When a reviewer requests a clearer transcript, she uploads a
   replacement linked to that request.

Alternative flow: An unreadable file is rejected with an explanation.
Aisha can upload a clearer copy without losing the other documents.

Expected outcome: Aisha can submit and track her application and
understand any action required from her.

### SC2 — Reviewer Investigates a Flagged Application

Persona: P2 — Lena Fischer

Context: An application is marked Needs Review because the extracted
surname differs between two documents.

Main flow:

1. Lena signs in and opens the application in the review dashboard.
2. She views the original documents beside extracted fields.
3. The report highlights the surname mismatch and cites the relevant
   demonstration consistency rule.
4. Lena checks the original image and identifies an OCR error.
5. She corrects the extracted surname; the original value is retained
   in the correction history.
6. The system reruns affected checks and preserves the earlier report.
7. Lena asks the assistant whether the language requirement is met.
8. The assistant answers using the extracted score and cites the
   applicable knowledge-base rule.
9. Lena records her final decision with a justification.

Alternative flow: If the source document remains unclear, Lena
requests a replacement and leaves the application awaiting action.

Expected outcome: A human decision is recorded with supporting
evidence, correction history, and applicable rule references.

### SC3 — Administrator Updates a Verification Rule

Persona: P3 — Omar Becker

Context: A demonstration programme changes its minimum language
score requirement for new applications.

Main flow:

1. Omar signs in as an administrator.
2. He opens the programme's verification rules.
3. He adds a new rule version with its effective date and source.
4. He uploads the corresponding knowledge-base document.
5. The system validates and indexes the updated source.
6. Omar activates the new configuration after successful indexing.
7. New verification runs use the applicable active rule version.
8. Existing reports retain references to the versions originally used.
9. Omar checks the audit log for the recorded configuration change.

Alternative flow: If indexing fails, the new configuration remains
inactive, the previous version stays active, and an error is shown.

Expected outcome: Rules can be updated without losing the history
needed to explain earlier verification results.

## 5. User Stories and Acceptance Criteria

These stories describe planned functionality. They are not claims
that the features have already been implemented.

### US01 — Register and Sign In

As an applicant, I want to register and sign in securely,
so that I can manage my own applications.

Acceptance criteria:

- Registration requires a valid email address and a password of
  at least 12 characters.
- Duplicate email registration is rejected.
- Passwords are stored as secure hashes, never as plain text.
- Valid credentials allow access; invalid credentials show a
  generic error without revealing whether an account exists.
- Signing out prevents further access through that session.

### US02 — Enforce Roles and Ownership

As an administrator, I want access restricted by role and ownership,
so that users can access only permitted information and actions.

Acceptance criteria:

- Public registration creates applicant accounts only.
- Only an administrator can assign reviewer or administrator roles.
- Applicants cannot read or modify another applicant's application,
  including through direct API requests.
- Applicants cannot access reviewer or administrator actions.
- Unauthenticated requests to protected resources are denied.

### US03 — Create an Application and Upload Documents

As an applicant, I want to upload related documents into one
application, so that they can be assessed together.

Acceptance criteria:

- An application shows its required-document checklist.
- Applicants can select a document type, upload one or more files,
  and add optional notes.
- PDF, JPG, and PNG files up to 10 MiB per file are supported.
- Unsupported, oversized, corrupt, or unreadable files are rejected
  with an actionable message.
- Validation checks file content as well as the filename extension.
- Accepted documents receive unique identifiers and are linked
  to the application and its owner.

### US04 — Track Progress and Respond to Requests

As an applicant, I want to see processing status and reviewer
requests, so that I know whether I need to take action.

Acceptance criteria:

- Each document shows whether it is queued, processing, processed,
  or failed.
- Processing failures show a useful message and do not appear
  as successful verification.
- Reviewer requests identify the document and required action.
- A replacement upload is linked to the request and preserves
  the earlier document's history.
- The application distinguishes an AI recommendation from
  the reviewer's final decision.

### US05 — Extract and Classify Document Information

As a reviewer, I want document text and structured fields extracted,
so that I can inspect information without repeatedly transcribing it.

Acceptance criteria:

- Digital PDFs use direct text extraction where possible;
  scanned documents use OCR.
- The detected document type is compared with the selected type,
  and disagreements are flagged.
- Extracted fields are stored as JSON linked to the document.
- Fields include name, issuing institution, relevant dates,
  document number, and scores or grades where applicable.
- Missing or unreadable values are marked unknown rather than invented.
- Extracted information remains accessible only to authorized users.

### US06 — Verify Against Rules and Reference Sources

As a reviewer, I want documents checked against applicable rules,
so that I can identify issues consistently.

Acceptance criteria:

- Checks cover required documents and fields, date validity,
  consistency across documents, and programme requirements.
- Relevant knowledge-base passages are retrieved for verification.
- Each rule-dependent finding identifies the rule and source version.
- Missing evidence or conflicting sources produce Needs Review.
- Possible manipulation indicators are described as concerns
  requiring investigation, not proof of fraud.
- Document text is treated as evidence, not as instructions
  that can override system rules.

### US07 — View an Explainable Verification Report

As a reviewer, I want a report with evidence and explanations,
so that I can assess the recommendation.

Acceptance criteria:

- The report shows an AI recommendation of Verified,
  Needs Review, or Rejected, labelled as provisional.
- Passed, failed, and undetermined checks are listed separately.
- Findings include explanations, source references, and links
  to affected fields or document sections.
- The report includes a confidence score with its definition
  and a notice that it is not proof of authenticity.
- The report records the processing time, model identifier,
  prompt version, and knowledge-base versions used.
- A processing error cannot produce a Verified recommendation.

### US08 — Correct Data and Make a Human Decision

As a reviewer, I want to correct extraction errors and accept
or override recommendations, so that the final decision is justified.

Acceptance criteria:

- The original document, extracted fields, and report can be
  viewed together.
- Corrections preserve the original value, corrected value,
  reviewer identity, timestamp, and reason.
- Corrections trigger a new run of affected checks.
- Earlier reports remain available in the application history.
- Accepting or overriding a recommendation requires justification.
- Final decisions record the reviewer and timestamp.

Optional enhancement — F13 (Should):

- Reviewers can filter applications awaiting review and applications
  with failed document processing.
- Clearing a filter restores the full authorized application list.
- Filters never reveal applications the reviewer cannot access.

### US09 — Ask Questions with Source Citations

As a reviewer, I want to ask questions about an application,
so that I can clarify findings using relevant evidence.

Acceptance criteria:

- Answers use only the authorized application's data and
  retrieved knowledge-base sources.
- Rule-based answers cite the supporting source passages.
- Insufficient evidence produces an explicit unknown or
  insufficient-information response.
- The assistant cannot access another application's documents
  or make a final review decision.
- Questions and answers are logged with the model and prompt version.

### US10 — Manage Document Types and Verification Rules

As an administrator, I want to manage document types and rules,
so that verification reflects the intended programme requirements.

Acceptance criteria:

- Administrators can create and update document types and rules.
- Rules include an identifier, version, effective date,
  source reference, and active status.
- Invalid rule configurations cannot be activated.
- Previous rule versions remain identifiable in historical reports.
- Changes record the administrator, timestamp, and change details.

### US11 — Maintain the Knowledge Base and Prompts

As an administrator, I want versioned sources and prompts,
so that AI behaviour is reproducible and maintainable.

Acceptance criteria:

- Knowledge-base documents have source identifiers and versions.
- Sources are split into chunks, embedded, and indexed for retrieval.
- Failed indexing is visible and does not activate an incomplete update.
- Classification, extraction, verification, report, and chat prompts
  are maintained as versioned templates.
- Every AI run records its prompt and source versions.
- Prompt templates require unknown values when evidence is missing.

### US12 — Inspect Audit Logs and Analytics

As an administrator, I want audit records and operational metrics,
so that I can investigate changes and monitor the platform.

Acceptance criteria:

- Audit events record the actor, action, target, and timestamp.
- Events cover role changes, rule updates, processing runs,
  reviewer corrections, and final decisions.
- Ordinary users cannot modify audit records.
- Analytics show verification counts, processing times,
  failure counts, and reviewer override rate.
- Accuracy is reported only against labelled evaluation data,
  with the dataset and metric definition identified.
- Passwords, API keys, and session tokens are excluded from logs.

### US13 — Export a Report as PDF

As a reviewer, I want to export a verification report,
so that I can share a readable assessment through approved channels.

Acceptance criteria:

- Only an authorized reviewer can export an application report.
- The export includes findings, citations, report version,
  and any recorded human decision.
- Provisional AI recommendations remain clearly labelled.
- Exporting does not change the application or decision.

### US14 — Verify Digital Signatures or QR References

As a reviewer, I want supported signatures or QR references checked,
so that additional authenticity evidence can be considered.

Acceptance criteria:

- Supported checks identify the verification method and outcome.
- Unsupported or unavailable checks are marked not checked.
- A QR code alone is never treated as proof of authenticity.
- External reference checks use an approved trust policy.

## 6. Prioritized Feature List

### 6.1 Prioritization Method

Features use the MoSCoW method:

- Must: required for the assessed core prototype.
- Should: valuable improvements after the core workflow works.
- Could: optional enhancements if time permits.
- Won't: explicitly excluded from this project release.

Priority describes implementation scope, not completion status.
All features below are currently planned.

### 6.2 Features and User Story Mapping

| ID | Feature | Priority | Related stories | Reason |
| --- | --- | --- | --- | --- |
| F01 | Registration, sign-in, and sign-out | Must | US01 | Provides authenticated access. |
| F02 | Role permissions and application ownership | Must | US02 | Protects documents and privileged actions. |
| F03 | Application checklist and validated document upload | Must | US03 | Enables submission of related documents. |
| F04 | Status tracking and replacement requests | Must | US04 | Keeps applicants informed and supports corrections. |
| F05 | PDF text extraction, OCR, classification, and structured fields | Must | US05 | Supplies document data for verification. |
| F06 | Rule checks and RAG-based verification | Must | US06 | Checks completeness, validity, consistency, and compliance with evidence. |
| F07 | Explainable report with provisional result, confidence, citations, and highlighted fields | Must | US07 | Makes recommendations inspectable. |
| F08 | Review dashboard, corrections, and justified final decisions | Must | US08 | Keeps decisions under human control. |
| F09 | Application assistant with grounded answers and citations | Must | US09 | Supports reviewer questions required by the brief. |
| F10 | Document-type and verification-rule administration | Must | US10 | Maintains verification configuration. |
| F11 | Versioned knowledge base and prompt management | Must | US11 | Supports traceable and reproducible AI runs. |
| F12 | Audit logs and basic operational analytics | Must | US12 | Supports accountability and monitoring. |
| F13 | Dashboard filters for failed processing and pending reviews | Should | US04, US08, US12 | Helps users locate work efficiently. |
| F14 | PDF report export | Could | US13 | Adds a portable report format. |
| F15 | Digital-signature and QR-reference verification | Won't | US14 | Requires additional trust infrastructure beyond the release scope. |

### 6.3 Scope Boundaries

The initial use case is university admissions, using synthetic
degree certificates, transcripts, and language certificates.

The release will demonstrate all Must features for this defined
use case. It will not claim support for every document type or
every institution.

Should and Could features will be attempted only after the Must
features meet their acceptance criteria.

US14 is retained as a future backlog item. Its acceptance criteria
describe a possible future implementation, not a release commitment.

The following are also outside this release:

- Legally binding certification of document authenticity.
- Autonomous final admission decisions.
- Live connections to banks, government systems, or issuing institutions.
- Processing real personal documents.
- Production operation for a real admissions department.

### 6.4 Implementation Order and Dependencies

1. Establish authentication, roles, and ownership controls.
2. Implement applications, validated uploads, and status tracking.
3. Build the review dashboard and administrative configuration.
4. Integrate extraction, classification, and structured data storage.
5. Prepare versioned rules, knowledge-base sources, and prompts.
6. Integrate RAG verification, reports, and the reviewer assistant.
7. Complete corrections, re-verification, and human decisions.
8. Validate audit records, analytics, and the complete workflow.

Audit logging and access controls will be developed alongside
the features they protect rather than postponed until the end.

### 6.5 Scenario Traceability

| Scenario | Personas | Related stories |
| --- | --- | --- |
| SC1 — Submit an application | P1 | US01, US02, US03, US04 |
| SC2 — Investigate a flagged application | P2 | US02, US05, US06, US07, US08, US09 |
| SC3 — Update a verification rule | P3 | US02, US10, US11, US12 |

## 7. Quality Requirements and Evaluation Targets

These are proposed targets to be tested in later phases,
not measured results.

| Area | Requirement or target | Planned verification |
| --- | --- | --- |
| Security | Deny unauthorized role and ownership access. | Automated API authorization tests. |
| Explainability | Every rule-dependent finding identifies its supporting source, or explicitly states that evidence is missing. | Review reports against labelled examples. |
| Traceability | Each AI run records its model, prompt version, source versions, and timestamp. | Inspect stored run records and audit events. |
| Performance | Target a report within 60 seconds for a synthetic application of up to three documents, each no more than five pages, on the documented test environment. | Record end-to-end timings, failures, hardware, model, and network conditions. |
| Usability | Applicants and reviewers can complete the main scenario tasks without developer intervention. | Task-based usability sessions with consent and recorded feedback. |
| Accessibility | Main flows support keyboard navigation, labelled inputs, and status information that does not rely on colour alone. | Keyboard and accessibility checks. |
| Reproducibility | The complete system starts using one Docker Compose command. | Clean-environment setup test. |
| Maintainability | Services are modular and required build, lint, unit, and integration checks pass in GitHub Actions. | Inspect the pipeline result on main. |

AI evaluation will use a labelled synthetic dataset to measure
field extraction accuracy, document classification accuracy,
verification precision, recall and F1, retrieval quality,
answer faithfulness, processing time, and cost.

At least two prompt versions will be compared. Numerical results
and the final configuration will be reported only after testing.

## 8. Assignment Reference

This product definition follows the project brief:

Dr. Ali Alhosseini, MIT 5.2 – Senior IT Project:
DocVerify AI — AI-Powered Document Verification System,
dated 18 October 2026.

Relevant sections:

- Phase 1 tasks: page 6.
- Functional and non-functional requirements: pages 2–5.
- Expected deliverables: pages 9–10.
- Technical and submission requirements: page 12.