
async function analyzePerformance() {

    // Get input values
    const fifoHits = Number(document.getElementById("fifoHits").value);
    const fifoFaults = Number(document.getElementById("fifoFaults").value);

    const lruHits = Number(document.getElementById("lruHits").value);
    const lruFaults = Number(document.getElementById("lruFaults").value);

    const optimalHits = Number(document.getElementById("optimalHits").value);
    const optimalFaults = Number(document.getElementById("optimalFaults").value);

    const output = document.getElementById("output");

    // Validate input
    const values = [
        fifoHits, fifoFaults,
        lruHits, lruFaults,
        optimalHits, optimalFaults
    ];

    if (values.some(value => !Number.isInteger(value) || value < 0)) {
        output.textContent = "Please enter valid non-negative numbers.";
        return;
    }

    // Check total page references
    const totals = [
        fifoHits + fifoFaults,
        lruHits + lruFaults,
        optimalHits + optimalFaults
    ];

    if (totals[0] === 0 || !totals.every(total => total === totals[0])) {
        output.textContent =
            "The total page references must be equal and greater than zero for all algorithms.";
        return;
    }

    // Prepare results for Flask
    const results = {
        FIFO: {
            page_hits: fifoHits,
            page_faults: fifoFaults
        },
        LRU: {
            page_hits: lruHits,
            page_faults: lruFaults
        },
        Optimal: {
            page_hits: optimalHits,
            page_faults: optimalFaults
        }
    };

    output.textContent = "Analyzing performance...";

    try {

        // Send results to Flask backend
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ results })
        });

        const data = await response.json();

        // Handle backend errors
        if (!response.ok || !data.success) {
            output.textContent =
                data.message || data.error || "Performance analysis failed.";
            return;
        }

        // Handle best algorithm whether string or array
        const bestAlgorithm = Array.isArray(data.best_algorithm)
            ? data.best_algorithm.join(", ")
            : data.best_algorithm;

        // Display complete analysis
        output.innerHTML = `
            <h2>Performance Analysis Results</h2>

            <p>
                <strong>Total Page References:</strong>
                ${data.total_references}
            </p>

            <h3>Algorithm Comparison</h3>

            <table style="width:100%; border-collapse:collapse; text-align:center;">
                <tr>
                    <th style="padding:8px; border:1px solid #ccc;">Algorithm</th>
                    <th style="padding:8px; border:1px solid #ccc;">Hits</th>
                    <th style="padding:8px; border:1px solid #ccc;">Faults</th>
                    <th style="padding:8px; border:1px solid #ccc;">Hit Rate</th>
                    <th style="padding:8px; border:1px solid #ccc;">Fault Rate</th>
                </tr>

                ${data.comparison.map(item => `
                    <tr>
                        <td style="padding:8px; border:1px solid #ccc;">
                            ${item.algorithm}
                        </td>
                        <td style="padding:8px; border:1px solid #ccc;">
                            ${item.page_hits}
                        </td>
                        <td style="padding:8px; border:1px solid #ccc;">
                            ${item.page_faults}
                        </td>
                        <td style="padding:8px; border:1px solid #ccc;">
                            ${item.page_hit_rate}%
                        </td>
                        <td style="padding:8px; border:1px solid #ccc;">
                            ${item.page_fault_rate}%
                        </td>
                    </tr>
                `).join("")}
            </table>

            <h3>Best Performing Algorithm</h3>

            <p>
                <strong>${bestAlgorithm}</strong>
            </p>

            <h3>Performance Explanation</h3>

            <p>${data.explanation}</p>

            <h3>Recommendation</h3>

            <p>${data.recommendation}</p>
        `;

    } catch (error) {

        console.error("Performance Analysis Error:", error);

        output.textContent =
            "Unable to connect to the backend. Please check the Flask server.";
    }
}
