# Automated Digital Evidence Timeline Generator

A Python-based digital forensic tool designed to automatically generate chronological timelines from Windows-based systems. The tool assists investigators by collecting file metadata, identifying event types, filtering events, correlating activity, detecting suspicious behaviour, and generating structured outputs and visual charts to support forensic investigations.

This tool was developed as part of an MSc dissertation project in **Digital Forensics and Cyber Investigation** at **Teesside University**.

---

## Features

- Live system analysis
- Mounted evidence drive analysis
- Automated timeline generation
- Event type identification
- Event-type based filtering
- Event correlation
- Structured raw and correlated timeline export
- Suspicious activity detection with score-based indicators and reasons
- Timeline visualisation charts
- Structured CSV and JSON outputs
- Case-based investigation folders
- Command-line forensic investigation interface

---

## System Workflow

1. The investigator launches the tool.
2. The investigator enters the **Investigator Name** and **Case ID**.
3. The investigator selects the investigation mode:
   - Live PC Analysis
   - Mounted Evidence Drive Analysis
4. If mounted mode is selected, the investigator provides the mounted drive path.
5. The tool collects file metadata and extracts timestamp-based events.
6. The investigator selects an event-type filter option.
7. Events are sorted into a chronological raw timeline.
8. Related events are correlated into a structured timeline with grouped timestamps, event types, and event counts.
9. Suspicious activity is analysed using timeline indicators, path-based keywords, and score-based reasoning.
10. The tool generates reports and visual charts in the case folder.

---

## Requirements

Python 3.9 or higher

Required Python library:

```bash
pip install matplotlib
````

---

## Running the Tool

Run the main program using:

```bash
python main.py
```

Example program interface:

```text
======================================================================
        Automated Digital Evidence Timeline Generator
======================================================================

Investigator Name: Asad
Case ID: CASE001

Select Analysis Mode
1. Live PC Analysis
2. Mounted Evidence Drive Analysis
```

If mounted analysis is selected, enter the mounted drive path:

```text
Enter mounted drive path (example I:\)
```

The program will then ask whether events should be filtered before export:

```text
Filter by event type before export?
1. All events
2. File Created only
3. File Modified only
4. File Accessed only
5. Created + Modified
6. Created + Modified + Accessed
```

---

## Output Files

Results are automatically stored in a case folder:

```text
cases/
└── CASE001/
```

Generated files include:

```text
timeline_raw.csv
timeline_raw.json
timeline_correlated.csv
timeline_correlated.json
suspicious_activity.csv
suspicious_activity.json
investigation_summary.json
activity_chart.png
source_chart.png
```

### Output Description

| File                       | Description                                                                      |
| -------------------------- | -------------------------------------------------------------------------------- |
| timeline_raw.csv           | Raw chronological list of extracted events                                       |
| timeline_raw.json          | Structured raw timeline data                                                     |
| timeline_correlated.csv    | Correlated timeline showing grouped file activity, event types, and event counts |
| timeline_correlated.json   | Structured correlated timeline data                                              |
| suspicious_activity.csv    | Suspicious items with scores and explanatory reasons                             |
| suspicious_activity.json   | Structured suspicious activity data                                              |
| investigation_summary.json | Summary of investigation findings                                                |
| activity_chart.png         | Activity distribution chart                                                      |
| source_chart.png           | Event source distribution chart                                                  |

---

## Forensic Workflow Example

1. Acquire a forensic image from the target system.
2. Mount the image using **FTK Image Mounter** or another forensic mounting tool.
3. Run the timeline generator.
4. Enter the case details.
5. Select the mounted evidence analysis mode.
6. Provide the mounted drive path.
7. Select an event-type filter if required.
8. Review the generated reports and visualisations.

---

## Repository Structure

```text
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
│   ├── investigation_summary.py
│   └── event_filter.py
│
├── visualization/
│   └── timeline_visualizer.py
│
└── cases/
```

---

## Academic Context

This tool was developed as part of a postgraduate research project titled:

**"An Automated Digital Evidence Timeline Generation System for Windows-Based Forensic Investigations"**

**Author:** Muhammad Asad<br>
**Supervisor:** Harry Stewart<br>
**Programme:** MSc Digital Forensics and Cyber Investigation<br>
**Institution:** Teesside University

---

## Disclaimer

This tool is intended for educational and research purposes only. Investigators should ensure that forensic analysis is conducted in accordance with legal, ethical, and organisational guidelines.

---

## Author

**Muhammad Asad**

MSc Digital Forensics and Cyber Investigation
Teesside University
