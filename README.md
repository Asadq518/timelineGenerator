# Automated Digital Evidence Timeline Generator

A Python-based digital forensic tool designed to automatically generate chronological timelines from Windows-based systems. The system assists investigators by collecting file metadata, correlating events, detecting suspicious activity, and producing visual charts to support forensic investigations.

This tool was developed as part of an MSc dissertation project in **Digital Forensics and Cyber Investigation** at **Teesside University**.

---

## Features

- Live system analysis
- Mounted evidence drive analysis
- Automated timeline generation
- Event correlation
- Suspicious activity detection
- Timeline visualisation charts
- Structured outputs (CSV and JSON)
- Case-based investigation folders
- Command-line forensic investigation interface

---

## System Workflow

1. Investigator launches the tool.
2. Investigator enters **Investigator Name** and **Case ID**.
3. Select investigation mode:
   - Live system analysis
   - Mounted evidence drive analysis
4. If mounted mode is selected, provide the mounted evidence drive path.
5. The system scans files and extracts metadata timestamps.
6. Events are sorted into a chronological timeline.
7. Correlated events are analysed for suspicious activity.
8. The tool generates reports and visual charts.

---

## Requirements

Python 3.9 or higher

Required Python libraries:

```

matplotlib
tqdm

```

Install dependencies using:

```

pip install matplotlib tqdm

```

---

## Running the Tool

Run the main program:

```

python main.py

```

Example program interface:

```

=======================================================
Automated Digital Evidence Timeline Generator
Digital Forensics Investigation Tool
====================================

Investigator Name: Asad
Case ID: CASE001

Select Analysis Mode

1. Live PC Analysis
2. Mounted Evidence Drive Analysis

```

If mounted analysis is selected, enter the mounted drive path:

```

Enter mounted drive path (example I:)

```

---

## Output Files

Results are automatically stored in a case folder:

```

cases/
CASE001/

```

Generated files include:

```

timeline.csv
timeline.json
suspicious_activity.csv
suspicious_activity.json
investigation_summary.json
activity_chart.png
source_chart.png

```

### Output Description

| File | Description |
|-----|-------------|
| timeline.csv | Chronological list of system events |
| timeline.json | Structured timeline data |
| suspicious_activity.csv | Detected suspicious events |
| suspicious_activity.json | Structured suspicious activity data |
| investigation_summary.json | Investigation overview |
| activity_chart.png | Timeline activity distribution |
| source_chart.png | Event source distribution |

---

## Forensic Workflow Example

1. Acquire forensic image from target system.
2. Mount the image using **FTK Image Mounter**.
3. Run the timeline generator.
4. Provide the mounted drive path.
5. Review generated reports and visualisations.

---

## Repository Structure

```

project/
│
├── main.py
├── modes/
│   ├── live_mode.py
│   └── mounted_mode.py
│
├── core/
│   ├── timeline.py
│   ├── correlator.py
│   ├── suspicious_detector.py
│   └── investigation_summary.py
│
├── visualization/
│   └── timeline_visualizer.py
│
└── cases/

```

---

## Academic Context

This tool was developed as part of a postgraduate research project titled:

**"An Automated Digital Evidence Timeline Generation System for Windows Based Forensic Investigations"**

Supervisor:  
Harry Stewart  
Teesside University

---

## Disclaimer

This tool is intended for educational and research purposes only. Investigators should ensure that forensic analysis is conducted in accordance with legal and ethical guidelines.

---

## Author

Muhammad Asad 
MSc Digital Forensics and Cyber Investigation  
Teesside University




