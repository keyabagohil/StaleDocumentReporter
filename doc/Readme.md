# State_Doc_Detector

## Overview

**State_Doc_Detector** is an AI-powered tool that analyzes and reports on the staleness of documents within a codebase, with smart suggestions to improve documentation quality scores. Designed for developers and documentation teams, it identifies outdated or incomplete documentation and helps prioritize areas for improvement.

## Key Features

- **Automated Stale Document Detection:** Scans documentation files to detect age, last update, and quality metrics, flagging those that are likely outdated or insufficient.
- **AI-Based Suggestions:** Provides actionable AI-driven recommendations to enhance the quality and relevancy of your docs, helping teams systematically improve their documentation score.
- **Comprehensive Report Generation:** Outputs summaries and detailed reports showing each document’s status along with suggestions for targeted updates.
- **Extensible Pipeline:** Built on Python and Jupyter Notebook, allowing easy extension and integration with existing workflows.

## Project Structure
State_Doc_Detector/
├── StaleDocDetector/
│ ├── init.py
│ ├── detector.py # Main detection logic for staleness
│ ├── ai_suggester.py # AI-powered suggestion/score module
│ └── doc/
│ ├── example_report.md
│ └── ... # Output documents, generated reports, or documentation
├── notebooks/
│ ├── demo.ipynb # Jupyter notebook demonstration
│ └── ... # Experimentation, usage examples
├── README.md
├── requirements.txt # Dependencies (Python, Jupyter, AI libs, etc.)
└── ...


- The `StaleDocDetector/doc` folder contains generated reports and documentation files as outputs from the analysis.
- The `detector.py` and `ai_suggester.py` modules contain the core logic and improvement algorithms.
- Example notebooks are provided for running and testing the tool in an interactive way.

## How It Works

1. **Analyze:** The tool scans the target documentation directory for Markdown and text-based documents.
2. **Detect:** It checks each doc’s last modification date, content completeness, and structural markers for signs of staleness.
3. **Score:** Documents are assigned a staleness score based on update frequency, coverage, and detected issues.
4. **Suggest:** For each stale or low-scoring document, the AI suggests specific revisions (e.g., add sections, update references, clarify points).
5. **Report:** Generates clear, actionable reports to guide the documentation team.

## Getting Started

**1. Clone the repository**
git clone https://github.com/keya714/State_Doc_Detector.git
cd State_Doc_Detector

text

**2. Install dependencies**
pip install -r requirements.txt

text

**3. Run analysis**
To run a basic scan and see suggestions for your documentation directory, use:
python -m StaleDocDetector.detector --path ./docs/

text
Or open and run the provided Jupyter notebook in the `notebooks/` directory for step-by-step guidance.

## Example Output

A sample report is available in [StaleDocDetector/doc/example_report.md](StaleDocDetector/doc/example_report.md) showing the staleness score of each document along with tailored improvement tips.

## How to Contribute

- **Issues and Suggestions:** Please open an issue for bug reports, ideas, or questions.
- **Pull Requests:** Contributions are welcome! Fork the repo, create a feature branch, and submit a pull request.
- **New AI Suggestion Modules:** If you have ideas for smarter document evaluation metrics, feel free to contribute new modules.

## License

This project is licensed under the MIT License.

---

For further details or in-depth documentation, check the `doc` folder for generated reports and refer to the demonstration notebooks for hands-on examples

