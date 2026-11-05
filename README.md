# Virtual Memory Simulator for Efficient RAM Management

An interactive web application that simulates virtual memory management and compares page replacement algorithms to help users understand how operating systems manage memory efficiently.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives](#2-project-objectives)
3. [Features](#3-features)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Project Structure](#6-project-structure)
7. [Team Responsibilities](#7-team-responsibilities)
8. [Prerequisites](#8-prerequisites)
9. [Installation and Setup](#9-installation-and-setup)
10. [Running the Application](#10-running-the-application)
11. [Development Guidelines](#11-development-guidelines)
12. [GitHub Workflow](#12-github-workflow)
13. [Branch Naming Convention](#13-branch-naming-convention)
14. [Commit Message Convention](#14-commit-message-convention)
15. [Pull Request Guidelines](#15-pull-request-guidelines)
16. [API Guidelines](#16-api-guidelines)
17. [Testing Guidelines](#17-testing-guidelines)
18. [Integration Guidelines](#18-integration-guidelines)
19. [Contribution Checklist](#19-contribution-checklist)
20. [Expected Outcome](#20-expected-outcome)

---

## 1. Project Overview

The Virtual Memory Simulator for Efficient RAM Management is a web-based simulation platform designed to demonstrate how operating systems manage memory using page replacement algorithms.

Users can enter a page-reference sequence and specify the number of available memory frames. The application simulates how different algorithms manage pages in memory, identifies page hits and page faults, and compares the performance of the algorithms.

The application also incorporates two rule-based bots:

- **Virtual Memory Tutor:** Explains virtual memory concepts, page hits, page faults, and page replacement algorithms.
- **Performance Analysis Bot:** Analyzes simulation results, compares algorithm performance, and identifies which algorithm produces the fewest page faults for the given input.

The project combines operating systems concepts, algorithm implementation, backend development, frontend visualization, and interactive educational features in one application.

## 2. Project Objectives

- Understand the working of virtual memory and page replacement.
- Simulate different page replacement algorithms.
- Visualize memory allocation and page replacement step by step.
- Calculate and compare page hits, page faults, and page-fault rates.
- Provide an interactive learning experience through rule-based bots.
- Demonstrate collaboration using Git, GitHub branches, pull requests, and code reviews.

## 3. Features

### 3.1 Page Replacement Simulation

The application supports three page replacement algorithms.

**FIFO — First-In, First-Out**
- Replaces the page that entered memory first.
- Maintains the order in which pages are loaded.

**LRU — Least Recently Used**
- Replaces the page that has not been used for the longest time.
- Uses recent page-reference history to determine replacement.

**Optimal Page Replacement**
- Replaces the page whose next use is farthest in the future.
- Serves as a theoretical benchmark for minimizing page faults when the complete reference sequence is known.

### 3.2 Memory Visualization

- Display the contents of memory frames after each page reference.
- Show whether each reference results in a page hit or a page fault.
- Indicate when a page is loaded or replaced.
- Allow users to follow the simulation step by step.

### 3.3 Performance Metrics

Display the following metrics for each algorithm:

- Total page references.
- Total page hits.
- Total page faults.
- Page-hit rate.
- Page-fault rate.
- Comparative algorithm performance.

The page-fault rate is calculated as:

`Page-Fault Rate = (Total Page Faults / Total Page References) × 100`

The page-hit rate is calculated as:

`Page-Hit Rate = (Total Page Hits / Total Page References) × 100`

### 3.4 Algorithm Comparison

- Compare the page-fault counts of FIFO, LRU, and Optimal.
- Display the results using charts or other suitable visualizations.
- Identify the algorithm with the fewest page faults for the selected input.
- Explain that results depend on the page-reference sequence and frame count.

### 3.5 Virtual Memory Tutor Bot

The tutor provides educational explanations about:
- Virtual memory.
- Memory frames and page references.
- Page hits and page faults.
- FIFO, LRU, and Optimal algorithms.
- The steps performed during a simulation.

### 3.6 Performance Analysis Bot

The analysis bot:
- Reads the simulation results.
- Compares page hits and page faults.
- Identifies the algorithm with the lowest page-fault count.
- Explains the performance differences in simple language.
- Provides recommendations based on the current simulation results.

**Note:** Both bots will use rule-based logic. No paid AI API or external AI service is required for the planned implementation.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Cross-origin requests | Flask-CORS |
| Page replacement algorithms | Python |
| Data exchange | JSON over HTTP |
| Version control | Git |
| Repository hosting | GitHub |
| Development environment | VS Code |
| Automated testing | Python testing tools |

**Database:** Not required for the current project scope.

**Additional hardware:** Not required.

## 5. System Architecture

The application follows a frontend-backend architecture.

```text
                 USER
                   |
                   v
       FRONTEND: HTML, CSS, JS
                   |
                   | HTTP Requests
                   v
           FLASK BACKEND API
                   |
          +--------+---------+
          |                  |
          v                  v
   PAGE REPLACEMENT       BOT LOGIC
     ALGORITHMS               |
          |             +-----+------+
          |             |            |
          v             v            v
     FIFO, LRU,      VIRTUAL      PERFORMANCE
      OPTIMAL        MEMORY         ANALYSIS
                      TUTOR           BOT
          |             |            |
          +-------------+------------+
                        |
                        v
                 JSON RESPONSES
                        |
                        v
             FRONTEND VISUALIZATION
                        |
                        v
                 RESULTS TO USER
```

### Application Flow

1. The user enters a page-reference sequence and memory-frame count.
2. The frontend validates the basic input and sends a request to the Flask backend.
3. The backend validates the request and invokes the appropriate algorithms.
4. The algorithm module generates memory-frame states and performance metrics.
5. The bot module generates explanations or performance analysis when requested.
6. The backend returns structured JSON responses.
7. The frontend displays simulation steps, results, charts, and bot responses.

## 6. Project Structure

The following is the planned project structure. Files can be added as development progresses.

```text
virtual memory simulator/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── algorithms.py
│   └── bots.py
│
├── tests/
│   ├── test_algorithms.py
│   └── test_bots.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### 6.1 Frontend — `frontend/`

**`index.html`**
- Defines the application structure.
- Contains input fields, simulation controls, results sections, and bot interfaces.

**`style.css`**
- Defines the visual design, layout, colors, and responsive styling.
- Styles memory frames, metrics, charts, and bot interfaces.

**`script.js`**
- Handles user interactions.
- Sends requests to the backend API.
- Displays simulation results and errors.
- Updates memory visualizations and charts.
- Connects the bot interfaces to their corresponding backend functionality.

### 6.2 Backend — `backend/`

**`app.py`**
- Initializes the Flask application.
- Defines API endpoints.
- Validates incoming requests.
- Calls the algorithm and bot modules.
- Returns JSON responses.

**`algorithms.py`**
- Implements FIFO, LRU, and Optimal page replacement.
- Generates step-by-step memory-frame states.
- Calculates page hits, page faults, and performance rates.

**`bots.py`**
- Implements the Virtual Memory Tutor.
- Implements the Performance Analysis Bot.
- Produces explanations based on the concepts and simulation results.

### 6.3 Tests — `tests/`

**`test_algorithms.py`**
- Tests page replacement algorithms.
- Verifies frame states, page hits, page faults, and edge cases.

**`test_bots.py`**
- Tests bot responses.
- Verifies that explanations and performance summaries use the supplied data correctly.

### 6.4 Root Files

**`requirements.txt`**

Lists the Python dependencies required to run the backend.

**`.gitignore`**

Excludes generated files, virtual environments, secrets, and other files that should not be tracked by Git.

**`README.md`**

Contains the project documentation, setup instructions, team roles, development rules, and GitHub workflow.

## 7. Team Responsibilities

Each team member is responsible for their assigned module, testing their changes, and coordinating with the other members when integration is required.

### 7.1 Lahari — Backend Developer

**Primary responsibility:** Backend development using Python and Flask.

Tasks:
- Develop the Flask application and API endpoints.
- Implement request validation and error handling.
- Define consistent API request and response formats.
- Connect the backend to the algorithm and bot modules.
- Return structured JSON responses to the frontend.
- Debug backend issues and support integration.

### 7.2 Pujitha — Frontend Developer

**Primary responsibility:** Frontend development using HTML, CSS, and JavaScript.

Tasks:
- Develop the application dashboard.
- Create inputs for page-reference sequences and frame counts.
- Implement memory-frame visualization.
- Display page hits, page faults, and page-fault rates.
- Build algorithm comparison charts.
- Create the interfaces for both bots.
- Ensure the application is responsive and user-friendly.

### 7.3 Bindu — Algorithm Developer

**Primary responsibility:** Page replacement algorithm implementation.

Tasks:
- Implement FIFO, LRU, and Optimal algorithms.
- Generate step-by-step memory-frame states.
- Track page hits and page faults.
- Calculate page-hit and page-fault rates.
- Test the algorithms using different page sequences and frame counts.
- Coordinate the output format with the backend developer.

### 7.4 Jowshnavi — Virtual Memory Tutor Bot

**Primary responsibility:** Development of the Virtual Memory Tutor.

Tasks:
- Create a rule-based tutor for virtual memory concepts.
- Explain page hits, page faults, and memory frames.
- Explain FIFO, LRU, and Optimal algorithms.
- Generate beginner-friendly educational responses.
- Coordinate with Bhanu on frontend-backend integration.
- Help test bot communication and response display.

### 7.5 Bhanu — Performance Analysis Bot and Integration

**Primary responsibility:** Development of the Performance Analysis Bot and collaboration on integration.

Tasks:
- Create a rule-based performance analysis bot.
- Compare algorithm results using page-fault counts and other metrics.
- Identify which algorithm performs best for the current input.
- Generate clear explanations of the comparison.
- Collaborate with Jowshnavi to connect the frontend with the Flask backend.
- Help test API requests, responses, and bot interactions.
- Support integration debugging and coordinate testing with the team.

### Shared Responsibilities

All team members must:
- Understand the overall project and its architecture.
- Test their assigned functionality before submitting changes.
- Follow the agreed GitHub workflow.
- Review project documentation when interfaces or file structures change.
- Communicate before modifying shared contracts or another member's module.
- Be prepared to explain the complete project during demonstrations and viva.

## 8. Prerequisites

Install the following software before starting development:

- **Python 3.10 or later**
- **Git**
- **VS Code** or another code editor
- **A modern web browser**
- **A GitHub account** with access to the project repository

Check your installations:

```bash
python --version
git --version
```

If your system uses the `python3` command instead, use it in place of `python` where appropriate.

## 9. Installation and Setup

### Step 1: Clone the Repository

Clone the repository using the URL shared by the project owner.

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd "virtual memory simulator"
```

Replace `<repository-url>` with the actual GitHub clone URL.

### Step 2: Switch to the Development Branch

The team uses `dev` as the shared integration branch.

```bash
git checkout dev
git pull origin dev
```

### Step 3: Create a Feature Branch

Before implementing your assigned feature, create a separate branch.

Example:

```bash
git checkout -b feature/your-feature-name
```

Refer to the [Branch Naming Convention](#13-branch-naming-convention) for examples.

### Step 4: Create a Python Virtual Environment

From the project root:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 5: Install Dependencies

Ensure `requirements.txt` contains the required packages:

```text
Flask
Flask-Cors
```

Install them:

```bash
python -m pip install -r requirements.txt
```

If additional dependencies are introduced, update `requirements.txt` and inform the team.

## 10. Running the Application

### Start the Backend

From the project root, run:

```bash
python backend/app.py
```

The backend should start at the address configured in the Flask application, typically:

`http://127.0.0.1:5000`

The exact startup command and address depend on how the Flask application is configured.

### Start the Frontend

Open `frontend/index.html` in a browser or serve the frontend through a local development server.

Ensure the API URL in `script.js` matches the running Flask backend.

### Verify the Application

Check that:
- The frontend loads correctly.
- User inputs are accepted and validated.
- Simulation requests reach the backend.
- Algorithm results are returned correctly.
- Page hits, page faults, and rates are displayed.
- Both bots return appropriate responses.
- Invalid inputs and API errors are handled gracefully.

## 11. Development Guidelines

### 11.1 Code Organization

- Keep code in the designated project folders.
- Avoid putting all functionality into a single file.
- Keep algorithm logic separate from API routing.
- Keep bot logic separate from the frontend presentation.
- Use reusable functions for repeated operations.

### 11.2 Naming Conventions

**Python**
- Use `snake_case` for variables and functions.
- Use `PascalCase` for classes.
- Use meaningful function names such as `simulate_fifo()` and `calculate_page_fault_rate()`.

**JavaScript**
- Use `camelCase` for variables and functions.
- Use meaningful names such as `runSimulation()` and `displayResults()`.

**Files and folders**
- Use descriptive names.
- Follow the existing naming style of the project.
- Avoid spaces in new source-code filenames.

### 11.3 Input Validation

Validate:
- That the page-reference sequence is provided.
- That page references use the agreed data type.
- That the frame count is a positive integer.
- That the selected algorithms are supported.
- That incoming requests follow the agreed API format.

The backend must validate requests even if the frontend already performs validation.

### 11.4 Error Handling

- Return clear error messages for invalid inputs.
- Avoid exposing internal stack traces to users.
- Handle backend errors without breaking the entire frontend.
- Do not silently ignore failed API requests.

### 11.5 Code Quality

- Write readable and maintainable code.
- Avoid unnecessary duplication.
- Remove debugging statements before submitting changes.
- Add comments where the logic is not self-explanatory.
- Do not commit generated files or environment-specific configuration.

### 11.6 Coordination

Before changing a shared interface:
- Inform the relevant team members.
- Agree on the new input or output format.
- Update the documentation when necessary.
- Test all dependent modules after the change.

## 12. GitHub Workflow

The project uses a branch-based workflow to keep development organized and prevent unfinished code from affecting the stable version.

### Branch Structure

| Branch | Purpose |
|---|---|
| `main` | Stable, tested version of the project |
| `dev` | Shared integration branch |
| Feature branches | Individual features and assigned tasks |

### Step 1: Get the Latest Changes

Before starting work:

```bash
git checkout dev
git pull origin dev
```

### Step 2: Create Your Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Each member should work on their own feature branch instead of directly modifying `dev` or `main`.

### Step 3: Make and Review Changes

After implementing your feature:

```bash
git status
git diff
```

Review your changes and make sure you are not committing unrelated files.

### Step 4: Stage and Commit

```bash
git add .
git commit -m "feat: add your feature"
```

Use a descriptive commit message following the convention in Section 14.

If unrelated changes are present, stage only the relevant files rather than using `git add .`.

### Step 5: Push Your Feature Branch

```bash
git push -u origin feature/your-feature-name
```

Replace the example branch name with your actual branch name.

### Step 6: Create a Pull Request

Open the repository on GitHub and create a pull request with:

- **Base branch:** `dev`
- **Compare branch:** Your feature branch

Include a clear title, a summary of the changes, and any testing details.

### Step 7: Review and Merge

- Review the changes and test the feature where possible.
- Resolve review comments.
- Merge the approved pull request into `dev`.
- Delete the feature branch after merging if it is no longer needed.

### Step 8: Integrate and Test

After features are merged into `dev`:
- Pull the latest `dev` branch.
- Run the application.
- Test the integrated features.
- Resolve integration conflicts or bugs through appropriate branches and pull requests.

### Step 9: Merge into Main

When the application is ready and the team has verified the integrated version, create a pull request from `dev` into `main`.

Merge only after the team has completed the necessary checks.

### Important Rules

- Do not push directly to `main`.
- Do not push directly to `dev` for ordinary feature development.
- Do not commit directly to another member's feature branch without coordination.
- Always pull the latest `dev` before starting new work.
- Use pull requests to review and integrate changes.
- Create one pull request per logical feature or task, not one pull request for every commit.
- A pull request may contain multiple related commits.

## 13. Branch Naming Convention

Use lowercase names with hyphens to describe the work.

Recommended examples:

| Developer / Feature | Example branch |
|---|---|
| Lahari — Flask API | `feature/flask-api` |
| Pujitha — Dashboard | `feature/memory-dashboard` |
| Bindu — Page replacement algorithms | `feature/page-replacement` |
| Jowshnavi — Tutor bot | `feature/virtual-memory-tutor` |
| Bhanu — Performance analysis bot | `feature/performance-analysis-bot` |

Other useful prefixes:

- `feature/` — New functionality
- `fix/` — Bug fixes
- `test/` — Test additions or improvements
- `docs/` — Documentation changes
- `refactor/` — Code restructuring

If you need to fix a bug in an existing feature, create an appropriately named branch rather than working directly on `dev`.

## 14. Commit Message Convention

Use clear, consistent commit messages.

### Format

`type: short description`

### Common Types

| Type | Purpose |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `test` | Test-related changes |
| `refactor` | Code restructuring |
| `style` | Formatting or styling changes |
| `chore` | Maintenance tasks |

### Examples

```text
feat: implement FIFO page replacement
feat: add memory frame visualization
feat: create virtual memory tutor
feat: implement performance analysis bot
fix: correct LRU page fault calculation
fix: handle invalid frame count
test: add page replacement test cases
docs: update project setup instructions
refactor: simplify API response handling
style: improve dashboard layout
```

Commit messages should describe the actual change. Avoid vague messages such as `update`, `changes`, `final code`, or `new code`.

## 15. Pull Request Guidelines

Every pull request should represent a clear, reviewable change.

### Pull Request Title

Use a concise title that describes the feature or fix.

Examples:
- `feat: Add FIFO page replacement`
- `feat: Implement memory dashboard`
- `feat: Add virtual memory tutor`
- `fix: Handle invalid simulation inputs`
- `docs: Update GitHub workflow`

### Pull Request Description

Include:
1. **Purpose:** What problem does the change solve?
2. **Changes:** What files or functionality were added or modified?
3. **Testing:** What did you test?
4. **Integration notes:** Does another module depend on this change?

### Before Opening a Pull Request

- Make sure the code runs locally.
- Test the relevant functionality.
- Review your changes.
- Remove debugging statements and unrelated modifications.
- Update documentation if necessary.
- Confirm that the target branch is `dev`.

### Review Rules

- Review code for correctness and readability.
- Check whether the change follows the agreed architecture.
- Verify that API contracts remain compatible.
- Request fixes for issues before merging.
- Test the integrated feature after merging when applicable.

## 16. API Guidelines

The frontend and backend must agree on API routes, request fields, response fields, and error formats before integration.

### Suggested Simulation Endpoint

`POST /api/simulate`

This endpoint is intended to accept a page-reference sequence, memory-frame count, and selected algorithms.

Example request:

```json
{
  "pages": [1, 2, 3, 1, 4, 2],
  "frames": 3,
  "algorithms": ["FIFO", "LRU", "Optimal"]
}
```

Example response structure:

```json
{
  "success": true,
  "results": {
    "FIFO": {
      "page_hits": 1,
      "page_faults": 5,
      "page_fault_rate": 83.33,
      "steps": []
    },
    "LRU": {
      "page_hits": 1,
      "page_faults": 5,
      "page_fault_rate": 83.33,
      "steps": []
    },
    "Optimal": {
      "page_hits": 2,
      "page_faults": 4,
      "page_fault_rate": 66.67,
      "steps": []
    }
  }
}
```

**Important:** This JSON is an illustrative response schema, not a verified output for the example input. The final field names and response format must be agreed upon by Lahari, Bindu, Pujitha, Bhanu, and Jowshnavi before implementation.

### API Design Rules

- Use consistent field names.
- Return valid JSON.
- Validate incoming requests in the backend.
- Use appropriate HTTP status codes.
- Return useful error messages.
- Keep the frontend independent of internal algorithm implementation details.
- Document any changes to request or response formats.

### Suggested Bot Endpoints

The following routes can be considered during implementation:

- `POST /api/tutor` — Returns a Virtual Memory Tutor response.
- `POST /api/analyze` — Returns a performance comparison and explanation.

These endpoints are proposed routes and should be finalized by the team before implementation.

## 17. Testing Guidelines

Testing is required before submitting changes for review.

### 17.1 Algorithm Testing

Verify:
- Correct memory-frame states.
- Correct page-hit and page-fault counts.
- Correct page-fault and page-hit rates.
- Behavior when a page is already present in memory.
- Behavior when memory frames are initially empty.
- Behavior with one frame and multiple frames.
- Behavior with repeated page references.
- Behavior with different reference sequences.

Test FIFO, LRU, and Optimal independently.

### 17.2 Backend Testing

Verify:
- API endpoints accept valid requests.
- Invalid input is rejected appropriately.
- JSON responses follow the agreed schema.
- Algorithm and bot modules are called correctly.
- Errors are returned in a predictable format.

### 17.3 Frontend Testing

Verify:
- Input fields work correctly.
- Invalid input is handled clearly.
- API requests reach the backend.
- Results are displayed accurately.
- Charts and memory visualizations update correctly.
- Both bot interfaces display responses.
- Loading and error states are handled properly.

### 17.4 Bot Testing

Verify:
- The tutor explains the intended concepts.
- The analysis bot uses the supplied simulation results.
- The selected best-performing algorithm matches the returned page-fault counts.
- Ties are handled correctly.
- Responses remain understandable and do not claim results unsupported by the input data.

### 17.5 Integration Testing

After modules are connected, test the complete user flow:

1. Enter the page-reference sequence.
2. Select the number of memory frames.
3. Run the simulation.
4. Review the memory-frame steps.
5. Compare algorithm results.
6. Ask the Virtual Memory Tutor a question.
7. Request a performance analysis.
8. Verify error handling.

## 18. Integration Guidelines

Bhanu and Jowshnavi will jointly handle frontend-backend integration, coordinating with Lahari, Pujitha, and Bindu.

### Integration Responsibilities

- Connect frontend requests to the Flask API endpoints.
- Ensure request and response formats match the agreed API contract.
- Connect the simulation dashboard to the backend.
- Connect both bot interfaces to their backend functionality.
- Verify that returned results display correctly.
- Identify and resolve frontend-backend communication issues.
- Test the complete application after integration.

### Integration Workflow

1. Lahari defines and implements the backend API.
2. Bindu provides tested algorithms and their expected output format.
3. Pujitha develops the frontend and its visualization components.
4. Jowshnavi and Bhanu coordinate the connections between the frontend, backend, and bots.
5. All team members test the combined application.
6. Fixes are submitted through feature branches and pull requests targeting `dev`.

The team should agree on API contracts early so frontend and backend development can proceed independently without incompatible assumptions.

## 19. Contribution Checklist

Before submitting a pull request, confirm the following:

- [ ] I am working on the correct feature branch.
- [ ] I have pulled the latest relevant changes from `dev`.
- [ ] I have implemented only the intended changes.
- [ ] My code follows the project's naming and organization guidelines.
- [ ] I have tested my assigned functionality.
- [ ] I have handled relevant invalid inputs and errors.
- [ ] I have checked for unintended changes or debugging statements.
- [ ] I have updated documentation when necessary.
- [ ] My commit messages are descriptive.
- [ ] My pull request targets `dev`.
- [ ] I have explained the changes and testing in the pull request.
- [ ] I have coordinated with teammates if a shared API or module changed.

## 20. Expected Outcome

The final application will provide an interactive platform for understanding virtual memory management through page replacement simulation, step-by-step memory visualization, performance comparison, and rule-based educational bots.

The project aims to combine operating systems concepts with practical full-stack development while encouraging modular implementation, testing, documentation, and collaborative software development.

---

**Project documentation note:** This README describes the planned project and agreed development workflow. Update it when the actual file structure, endpoints, dependencies, or implementation details change.
