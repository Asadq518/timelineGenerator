# Automated Digital Evidence Timeline Generation System

## Project Overview

This project presents the design and implementation of an **Automated Digital Evidence Timeline Generation System** for Windows-based digital forensic investigations.

Digital forensic investigations often involve analysing large volumes of system data to reconstruct events and identify suspicious activity. Manually building system timelines can be time-consuming and complex. This system automates the process of collecting digital events, generating structured timelines, detecting suspicious behaviour, and producing visual reports.

The tool assists investigators by simplifying evidence analysis and improving the efficiency of forensic investigations.

---

# Features

✔ Automated timeline generation from Windows artefacts
✔ Supports **live system analysis**
✔ Supports **mounted forensic evidence drives (E01 images)**
✔ Suspicious activity detection
✔ Timeline export to **JSON and CSV formats**
✔ Visual charts of system activity
✔ Investigation summary report generation

---

# Technologies Used

* Python
* pytsk3 (filesystem analysis)
* matplotlib (visualization)
* JSON / CSV for structured data
* Digital forensic concepts (timeline analysis)

---

# Project Structure

```
timeline-generator
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules
│   ├── timeline_parser.py
│   ├── suspicious_detector.py
│   └── report_generator.py
│
├── output
│   ├── timeline.json
│   ├── timeline.csv
│   ├── suspicious_activity.json
│   ├── investigation_summary.json
│   ├── activity_chart.png
│   └── source_chart.png
│
└── screenshots
```

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/timeline-generator.git
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Usage

Run the main program:

```
python main.py
```

The system will allow the investigator to:

1. Analyse a **live Windows system**
2. Analyse a **mounted forensic drive**

After execution, the program generates structured forensic outputs including timelines and investigation summaries.

---

# Output Files

The system generates the following files:

| File                       | Description                          |
| -------------------------- | ------------------------------------ |
| timeline.json              | Structured timeline of system events |
| timeline.csv               | Timeline in spreadsheet format       |
| suspicious_activity.json   | Detected suspicious behaviour        |
| investigation_summary.json | Summary of forensic findings         |
| activity_chart.png         | Visualization of system activity     |
| source_chart.png           | Visualization of event sources       |

---

# Educational Purpose

This project was developed as part of an **MSc Digital Forensics and Cyber Investigation** program.

The objective is to demonstrate how automation can assist forensic investigators in analysing large volumes of digital evidence efficiently.

---

# Author

**Asad Rajput**
MSc Digital Forensics and Cyber Investigation
Teesside University

---

# License

This project is developed for **academic research purposes**.

---
