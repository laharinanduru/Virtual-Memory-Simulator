const API_BASE = "http://127.0.0.1:5000";

const form = document.getElementById("simulationForm");
const pagesInput = document.getElementById("pagesInput");
const framesInput = document.getElementById("framesInput");
const algorithmInput = document.getElementById("algorithmInput");
const runButton = document.getElementById("runButton");
const compareButton = document.getElementById("compareButton");
const resetButton = document.getElementById("resetButton");
const formMessage = document.getElementById("formMessage");
const resultsSection = document.getElementById("results");

let latestResult = null;
let latestInput = null;
let comparisonResults = [];

// Display messages to the user
function setMessage(message, type = "") {
  formMessage.textContent = message;
  formMessage.className = `message ${type}`;
}

// Read and validate the page-reference sequence
function parsePages() {
  const raw = pagesInput.value.trim();

  if (!raw) {
    throw new Error("Enter a page-reference sequence.");
  }

  const parts = raw.split(/[\s,]+/).filter(Boolean);

  const pages = parts.map((part) => {
    if (!/^\d+$/.test(part)) {
      throw new Error(
        `"${part}" is not a valid non-negative integer page number.`
      );
    }

    const number = Number(part);

    if (!Number.isSafeInteger(number)) {
      throw new Error("Page numbers must be safe integers.");
    }

    return number;
  });

  if (!pages.length) {
    throw new Error("Enter at least one page reference.");
  }

  return pages;
}

// Read and validate simulation inputs
function readInput() {
  const pages = parsePages();
  const frames = Number(framesInput.value);

  if (!Number.isInteger(frames) || frames < 1) {
    throw new Error("RAM frames must be a positive integer.");
  }

  return { pages, frames };
}

// Send a request to the Flask backend
async function postJson(path, body) {
  let response;

  try {
    response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
  } catch {
    throw new Error(
      "Cannot connect to the backend. Start Flask with: python backend/app.py"
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.error || `Request failed with HTTP ${response.status}.`
    );
  }

  return data;
}

// Check whether the Flask API is running
async function checkApi() {
  const label = document.getElementById("apiLabel");
  const sidebarStatus = document.getElementById("connectionStatus");

  try {
    const response = await fetch(`${API_BASE}/api/health`);

    if (!response.ok) {
      throw new Error("API unavailable");
    }

    const data = await response.json();

    label.textContent = `API status: ${data.status || "connected"}`;
    sidebarStatus.textContent = "Connected to Flask";

    document.querySelectorAll(".status-dot").forEach((dot) => {
      dot.classList.add("online");
    });
  } catch {
    label.textContent = "API status: offline";
    sidebarStatus.textContent = "Start Flask on port 5000";

    document.querySelectorAll(".status-dot").forEach((dot) => {
      dot.classList.remove("online");
    });
  }
}

// Convert a rate to a percentage
function formatRate(value) {
  return `${(Number(value) * 100).toFixed(2)}%`;
}

// Display simulation results immediately without reloading the page
function renderResult(result, algorithm) {
  latestResult = result;

  document.getElementById("totalMetric").textContent =
  result.total_references;

document.getElementById("hitsMetric").textContent =
  result.page_hits;

document.getElementById("faultsMetric").textContent =
  result.page_faults;

document.getElementById("hitRateMetric").textContent =
  formatRate(result.hit_rate);

document.getElementById("faultRateMetric").textContent =
  formatRate(result.fault_rate);

  // Update the memory history table
  const table = document.getElementById("historyTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");

  thead.replaceChildren();
  tbody.replaceChildren();

  // Create table header
  const header = document.createElement("tr");

  [
    "Reference",
    ...result.history.map((step, index) => `Step ${index + 1}`)
  ].forEach((label) => {
    const th = document.createElement("th");
    th.textContent = label;
    header.appendChild(th);
  });

  thead.appendChild(header);

  // Display requested pages
  const referenceRow = document.createElement("tr");
  const referenceHead = document.createElement("td");

  referenceHead.textContent = "Page requested";
  referenceRow.appendChild(referenceHead);

  result.history.forEach((step) => {
    const td = document.createElement("td");

    td.textContent = step.page;
    td.className = step.hit ? "cell-hit" : "cell-fault";

    referenceRow.appendChild(td);
  });

  tbody.appendChild(referenceRow);

  // Display the contents of each RAM frame
  const frameCount = Number(
  result.frames_count ??
  Math.max(0, ...result.history.map(step => step.frames.length))
);

  for (let frameIndex = 0; frameIndex < frameCount; frameIndex++) {
    const row = document.createElement("tr");
    const label = document.createElement("td");

    label.textContent = `Frame ${frameIndex + 1}`;
    row.appendChild(label);

    result.history.forEach((step) => {
      const td = document.createElement("td");
      const value = step.frames[frameIndex];

      td.textContent = value === undefined ? "—" : value;

      row.appendChild(td);
    });

    tbody.appendChild(row);
  }

  // Display HIT or FAULT for each page reference
  const outcomeRow = document.createElement("tr");
  const outcomeLabel = document.createElement("td");

  outcomeLabel.textContent = "Outcome";
  outcomeRow.appendChild(outcomeLabel);

  result.history.forEach((step) => {
    const td = document.createElement("td");

    td.textContent = step.hit ? "HIT" : "FAULT";
    td.className = step.hit ? "cell-hit" : "cell-fault";

    outcomeRow.appendChild(td);
  });

  tbody.appendChild(outcomeRow);

  // Make results visible immediately
  resultsSection.classList.remove("hidden");

  // Clear the previous comparison display
  document.getElementById("comparisonChart").replaceChildren();

  document
    .getElementById("comparisonTableWrap")
    .classList.add("hidden");

  // Scroll to the updated results without refreshing the page
  requestAnimationFrame(() => {
    resultsSection.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  });
}

// Display a comparison of FIFO, LRU, and Optimal
function renderComparison(results) {
  comparisonResults = results;

  const chart = document.getElementById("comparisonChart");
  chart.replaceChildren();

  const max = Math.max(
    1,
    ...results.map(
      (item) => item.page_hits + item.page_faults
    )
  );

  // Create comparison bars
  results.forEach((item) => {
    const row = document.createElement("div");
    row.className = "bar-row";

    const label = document.createElement("span");
    label.className = "bar-label";
    label.textContent = item.algorithm;

    const track = document.createElement("div");
    track.className = "bar-track";

    const hit = document.createElement("div");
    hit.className = "bar-hit";
    hit.style.width = `${(item.page_hits / max) * 100}%`;
    hit.title = `${item.page_hits} hits`;

    const fault = document.createElement("div");
    fault.className = "bar-fault";
    fault.style.width = `${(item.page_faults / max) * 100}%`;
    fault.title = `${item.page_faults} faults`;

    track.append(hit, fault);

    const number = document.createElement("span");
    number.className = "bar-number";
    number.textContent = `${item.page_faults} F`;

    row.append(label, track, number);
    chart.appendChild(row);
  });

  // Build the comparison table
  const wrap = document.getElementById("comparisonTableWrap");
  const table = document.getElementById("comparisonTable");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");

  thead.replaceChildren();
  tbody.replaceChildren();

  const headerRow = document.createElement("tr");

  [
    "Algorithm",
    "Hits",
    "Faults",
    "Hit rate",
    "Fault rate"
  ].forEach((text) => {
    const th = document.createElement("th");
    th.textContent = text;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);

  results.forEach((item) => {
    const tr = document.createElement("tr");

    [
      item.algorithm,
      item.page_hits,
      item.page_faults,
      formatRate(item.hit_rate),
      formatRate(item.fault_rate)
    ].forEach((value) => {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });

  wrap.classList.remove("hidden");

  // Scroll to the comparison results
  requestAnimationFrame(() => {
    wrap.scrollIntoView({
      behavior: "smooth",
      block: "nearest"
    });
  });
}

// RUN SIMULATION
// This handler prevents a normal form submission and page reload.
async function handleRunSimulation(event) {
  event.preventDefault();

  try {
    const input = readInput();
    const algorithm = algorithmInput.value;

    setMessage("Running simulation…");

    runButton.disabled = true;
    runButton.setAttribute("aria-busy", "true");

    const result = await postJson("/api/simulate", {
      pages: input.pages,
      frames: input.frames,
      algorithm: algorithm
    });

    latestInput = input;
    comparisonResults = [];

    // Update the interface immediately
    renderResult(result, algorithm);

    document.getElementById("analysisResponse").textContent =
      "Simulation results are ready. Ask the Performance Analysis Bot after its endpoint has been connected.";

    setMessage("Simulation completed successfully.", "success");
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    runButton.disabled = false;
    runButton.removeAttribute("aria-busy");
  }
}

// Make sure the Run Simulation button submits the form
runButton.type = "submit";

// Register the form handler only once in this script
form.addEventListener("submit", handleRunSimulation);

// COMPARE ALL ALGORITHMS
compareButton.addEventListener("click", async () => {
  try {
    const input = readInput();

    compareButton.disabled = true;

    setMessage("Comparing FIFO, LRU, and Optimal…");

    const algorithms = ["FIFO", "LRU", "OPTIMAL"];

    const results = await Promise.all(
      algorithms.map((algorithm) =>
        postJson("/api/simulate", {
          pages: input.pages,
          frames: input.frames,
          algorithm: algorithm
        })
      )
    );

    latestInput = input;

    renderResult(results[0], "FIFO");
    renderComparison(results);

    setMessage(
      "Comparison completed. Lower page-fault counts mean fewer faults for this input.",
      "success"
    );
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    compareButton.disabled = false;
  }
});

// RESET INPUTS AND RESULTS
resetButton.addEventListener("click", () => {
  pagesInput.value = "";
  framesInput.value = "";
  algorithmInput.selectedIndex = 0;

  latestResult = null;
  latestInput = null;
  comparisonResults = [];

  resultsSection.classList.add("hidden");

  document.getElementById("comparisonChart").replaceChildren();

  document
    .getElementById("comparisonTableWrap")
    .classList.add("hidden");

  document.getElementById("historyTable").querySelector("thead").replaceChildren();
  document.getElementById("historyTable").querySelector("tbody").replaceChildren();

  document.getElementById("totalMetric").textContent = "—";
  document.getElementById("hitsMetric").textContent = "—";
  document.getElementById("faultsMetric").textContent = "—";
  document.getElementById("hitRateMetric").textContent = "—";
  document.getElementById("faultRateMetric").textContent = "—";

  setMessage("Inputs and results have been reset.");
});

// CALL THE VIRTUAL MEMORY TUTOR OR PERFORMANCE ANALYSIS BOT
async function callBot(
  endpoint,
  question,
  responseElement,
  button
) {
  if (!question.trim()) {
    responseElement.textContent = "Enter a question first.";
    return;
  }

  button.disabled = true;
  responseElement.textContent = "Connecting to bot endpoint…";

  try {
    const payload = { question };

    if (latestResult) {
      payload.results = latestResult;
    }

    if (latestInput) {
      payload.pages = latestInput.pages;
      payload.frames = latestInput.frames;
    }

    if (comparisonResults.length) {
      payload.comparison = comparisonResults;
    }

    const data = await postJson(endpoint, payload);

    responseElement.textContent =
      data.answer ||
      data.response ||
      data.message ||
      JSON.stringify(data, null, 2);
  } catch (error) {
    responseElement.textContent =
      `${error.message}\n\n` +
      "The bot endpoint may not be implemented yet. " +
      "Confirm the route and request format with the bot developer.";
  } finally {
    button.disabled = false;
  }
}

// VIRTUAL MEMORY TUTOR BUTTON
document.getElementById("tutorButton").addEventListener("click", () => {
  callBot(
    "/api/tutor",
    document.getElementById("tutorQuestion").value,
    document.getElementById("tutorResponse"),
    document.getElementById("tutorButton")
  );
});

// PERFORMANCE ANALYSIS BOT BUTTON
document.getElementById("analysisButton").addEventListener("click", () => {
  callBot(
    "/api/analyze",
    document.getElementById("analysisQuestion").value,
    document.getElementById("analysisResponse"),
    document.getElementById("analysisButton")
  );
});

// Check backend connection when the page loads
checkApi();