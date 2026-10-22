# Virtual Memory Simulator for Efficient RAM Management

## Project Overview
The Virtual Memory Simulator is a web-based educational tool that demonstrates how operating systems manage memory using page replacement algorithms. It simulates page requests, visualizes RAM frame allocation, and compares algorithm performance.

## Objectives
- Understand virtual memory and page replacement.
- Visualize memory frame allocation step by step.
- Compare FIFO, LRU, and Optimal page replacement algorithms.
- Analyze page hits, page faults, and page fault rates.
- Provide interactive learning and performance analysis through two bots.

## Features
- **Interactive Simulation:** Enter a page-reference sequence and number of RAM frames.
- **Page Replacement Algorithms:** Simulate FIFO, LRU, and Optimal.
- **Memory Visualization:** View frame states after each page request.
- **Performance Metrics:** Display page hits, page faults, and page fault rates.
- **Virtual Memory Tutor Bot:** Explains virtual memory concepts and algorithms.
- **Performance Analysis Bot:** Compares results and explains which algorithm performs best for a given input.

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Visualization:** JavaScript charts (planned)
- **Version Control:** Git and GitHub

## Project Structure
```text
virtual-memory-simulator/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py
│   ├── algorithms.py
│   └── bots.py
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Team Members
1. **Lahari** — Backend Developer
2. **Pujitha** — Frontend Developer
3. **Bindu** — Algorithm Developer
4. **Jowshnavi** — Virtual Memory Tutor Bot Developer and Integration Support
5. **Bhanu** — Performance Analysis Bot Developer and Integration Lead

## How It Works
1. Enter a page-reference sequence and the number of available RAM frames.
2. Select an algorithm or compare all three algorithms.
3. Run the simulation and inspect the frame states.
4. Compare performance metrics.
5. Use the tutor and analysis bots to understand the concepts and results.

## Database and Hardware
This project does not require a database or additional hardware. Simulations are processed directly by the application.

## Project Status
Development in progress.
