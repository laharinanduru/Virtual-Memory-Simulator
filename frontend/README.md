# Virtual Memory Simulator — Frontend

Static HTML, CSS, and JavaScript frontend for the Flask Virtual Memory Simulator.

## Files
- `index.html` — dashboard structure
- `style.css` — responsive styling
- `script.js` — API requests, simulation history, metrics, comparison, and bot UI

## Run
1. Start the backend from the repository root:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   python backend/app.py
   ```
2. Open `frontend/index.html` in a browser, or use the VS Code Live Server extension.
3. The frontend expects Flask at `http://127.0.0.1:5000`.

## API routes used
- `GET /api/health`
- `POST /api/simulate` with `{ "pages": [1,2,3,1], "frames": 3, "algorithm": "FIFO" }`
- `POST /api/tutor` — placeholder integration point; requires the tutor bot developer's endpoint.
- `POST /api/analyze` — placeholder integration point; requires the analysis bot developer's endpoint.

The bot cards are UI placeholders until the corresponding backend routes are implemented. No database is required.
