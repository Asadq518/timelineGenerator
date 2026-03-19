import os
import html
from datetime import datetime


def safe(value):
    if value is None:
        return ""
    return html.escape(str(value))


def format_bytes(size):
    """
    Convert bytes to human-readable format.
    """
    try:
        size = float(size)
    except (ValueError, TypeError):
        return safe(size)

    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def pretty_label(key):
    return safe(str(key).replace("_", " ").title())


def pretty_value(key, value):
    """
    Format selected fields nicely for human reading.
    """
    if value is None or value == "":
        return "N/A"

    key_lower = str(key).lower()

    if "size" in key_lower and "bytes" in key_lower:
        return format_bytes(value)

    return safe(value)


def get_summary_value(summary, *possible_keys, default="N/A"):
    for key in possible_keys:
        if key in summary:
            return summary.get(key, default)
    return default


def build_key_value_table(data):
    rows = ""
    for key, value in data.items():
        rows += f"""
        <tr>
            <th>{pretty_label(key)}</th>
            <td>{pretty_value(key, value)}</td>
        </tr>
        """
    return rows


def get_score_class(score):
    try:
        score = float(score)
    except (ValueError, TypeError):
        return "score-low"

    if score >= 8:
        return "score-high"
    if score >= 6:
        return "score-medium"
    return "score-low"


def suspicious_rows(suspicious_items, limit=20):
    rows = ""

    for item in suspicious_items[:limit]:
        score = item.get("suspicion_score", "")
        score_class = get_score_class(score)

        rows += f"""
        <tr>
            <td class="path-cell">{safe(item.get("item", ""))}</td>
            <td>{safe(item.get("source", ""))}</td>
            <td>{safe(item.get("event_count", ""))}</td>
            <td>{safe(item.get("confidence", ""))}</td>
            <td><span class="score-badge {score_class}">{safe(score)}</span></td>
            <td>{safe(item.get("reasons", ""))}</td>
        </tr>
        """
    return rows


def chart_block(output_dir, filename, title, description=""):
    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        return ""

    return f"""
    <div class="chart-card">
        <div class="chart-head">
            <h3>{safe(title)}</h3>
            <p>{safe(description)}</p>
        </div>
        <img src="{safe(filename)}" alt="{safe(title)}">
    </div>
    """


def build_stat_card(title, value, subtitle=""):
    return f"""
    <div class="stat-card">
        <div class="stat-title">{safe(title)}</div>
        <div class="stat-value">{safe(value)}</div>
        <div class="stat-subtitle">{safe(subtitle)}</div>
    </div>
    """


def build_highlights(summary, suspicious_items, source_metadata):
    total_events = get_summary_value(summary, "total_events", "total_timeline_events", default="N/A")
    total_items = get_summary_value(summary, "total_items", "total_correlated_items", default="N/A")
    peak_date = get_summary_value(summary, "peak_activity_date", default="N/A")
    peak_count = get_summary_value(summary, "peak_activity_count", default="N/A")

    suspicious_count = len(suspicious_items)
    source_mode = source_metadata.get("source_mode", "Unknown")
    source_path = source_metadata.get("source_path", "Unknown")

    cards = ""
    cards += build_stat_card("Analysis Mode", source_mode, source_path)
    cards += build_stat_card("Timeline Events", total_events, "Total filtered events")
    cards += build_stat_card("Correlated Items", total_items, "Grouped timeline artefacts")
    cards += build_stat_card("Suspicious Items", suspicious_count, "Flagged for review")
    cards += build_stat_card("Peak Activity Date", peak_date, f"Peak count: {peak_count}")

    return cards


def generate_html_report(
    investigator,
    case_id,
    source_metadata,
    summary,
    suspicious_items,
    output_dir
):
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    source_info_rows = build_key_value_table(source_metadata)
    timeline_summary_rows = build_key_value_table(summary)
    suspicious_table = suspicious_rows(suspicious_items)
    highlight_cards = build_highlights(summary, suspicious_items, source_metadata)

    charts_html = ""
    charts_html += chart_block(
        output_dir,
        "daily_activity_timeline.png",
        "Daily Timeline Activity",
        "Shows activity spikes across the investigation period."
    )
    charts_html += chart_block(
        output_dir,
        "suspicious_score_chart.png",
        "Top Suspicious Items by Score",
        "Highlights the highest-priority artefacts flagged by the detector."
    )
    charts_html += chart_block(
        output_dir,
        "event_type_distribution.png",
        "Event Type Distribution",
        "Compares created, modified, and accessed events."
    )

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Investigation Report - {safe(case_id)}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --panel: #ffffff;
            --panel-soft: #f8fafc;
            --text: #0f172a;
            --muted: #64748b;
            --line: #e2e8f0;
            --accent: #2563eb;
            --accent-soft: #dbeafe;
            --danger: #dc2626;
            --warning: #d97706;
            --success: #16a34a;
            --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            --radius: 16px;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
            color: var(--text);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }}

        .hero {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            border-radius: 24px;
            padding: 32px;
            box-shadow: var(--shadow);
            margin-bottom: 24px;
        }}

        .hero h1 {{
            margin: 0 0 10px 0;
            font-size: 32px;
            line-height: 1.2;
        }}

        .hero p {{
            margin: 6px 0;
            color: #cbd5e1;
            font-size: 15px;
        }}

        .hero-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin-top: 24px;
        }}

        .hero-chip {{
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 14px;
            padding: 14px 16px;
        }}

        .hero-chip-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #93c5fd;
            margin-bottom: 6px;
        }}

        .hero-chip-value {{
            font-size: 15px;
            color: #f8fafc;
            word-break: break-word;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .stat-card {{
            background: var(--panel);
            border-radius: var(--radius);
            padding: 20px;
            box-shadow: var(--shadow);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }}

        .stat-title {{
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .stat-value {{
            font-size: 28px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
            word-break: break-word;
        }}

        .stat-subtitle {{
            font-size: 13px;
            color: var(--muted);
            word-break: break-word;
        }}

        .section {{
            background: var(--panel);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: var(--shadow);
            margin-bottom: 24px;
        }}

        .section h2 {{
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 22px;
        }}

        .section p.section-note {{
            margin-top: 0;
            color: var(--muted);
            font-size: 14px;
        }}

        .two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            border-radius: 12px;
        }}

        th, td {{
            border: 1px solid var(--line);
            padding: 12px 14px;
            text-align: left;
            vertical-align: top;
            font-size: 14px;
        }}

        th {{
            background: var(--panel-soft);
            font-weight: 600;
        }}

        td {{
            background: #fff;
        }}

        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 20px;
        }}

        .chart-card {{
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
        }}

        .chart-head h3 {{
            margin: 0 0 6px 0;
            font-size: 18px;
            color: var(--text);
        }}

        .chart-head p {{
            margin: 0 0 14px 0;
            font-size: 13px;
            color: var(--muted);
        }}

        .chart-card img {{
            width: 100%;
            height: auto;
            border-radius: 12px;
            border: 1px solid var(--line);
            background: white;
        }}

        .score-badge {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
        }}

        .score-high {{
            background: #fee2e2;
            color: var(--danger);
        }}

        .score-medium {{
            background: #fef3c7;
            color: var(--warning);
        }}

        .score-low {{
            background: #dcfce7;
            color: var(--success);
        }}

        .path-cell {{
            max-width: 360px;
            word-break: break-word;
            font-family: Consolas, monospace;
            font-size: 12px;
        }}

        .footer-note {{
            text-align: center;
            color: var(--muted);
            font-size: 13px;
            padding: 8px 0 24px 0;
        }}

        @media (max-width: 960px) {{
            .two-col {{
                grid-template-columns: 1fr;
            }}

            .hero h1 {{
                font-size: 26px;
            }}

            .stat-value {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">

        <div class="hero">
            <h1>Automated Digital Evidence Timeline Generator</h1>
            <p>Investigation report generated from filtered timeline evidence and suspicious artefact analysis.</p>

            <div class="hero-grid">
                <div class="hero-chip">
                    <div class="hero-chip-label">Case ID</div>
                    <div class="hero-chip-value">{safe(case_id)}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">Investigator</div>
                    <div class="hero-chip-value">{safe(investigator)}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">Generated</div>
                    <div class="hero-chip-value">{safe(report_time)}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">Source Mode</div>
                    <div class="hero-chip-value">{safe(source_metadata.get("source_mode", "Unknown"))}</div>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            {highlight_cards}
        </div>

        <div class="section">
            <h2>Investigation Overview</h2>
            <p class="section-note">
                This report summarises acquisition source details, timeline findings, generated visualisations,
                and the highest-priority suspicious artefacts identified by the analysis pipeline.
            </p>
        </div>

        <div class="two-col">
            <div class="section">
                <h2>Source Information</h2>
                <p class="section-note">Human-readable metadata about the analysed source or mounted evidence.</p>
                <table>
                    {source_info_rows}
                </table>
            </div>

            <div class="section">
                <h2>Timeline Summary</h2>
                <p class="section-note">Key statistics derived from the filtered and correlated timeline.</p>
                <table>
                    {timeline_summary_rows}
                </table>
            </div>
        </div>

        <div class="section">
            <h2>Visualisations</h2>
            <p class="section-note">Charts generated directly from timeline and suspicious-activity outputs.</p>
            <div class="chart-grid">
                {charts_html if charts_html else "<p>No charts available.</p>"}
            </div>
        </div>

        <div class="section">
            <h2>Suspicious Items</h2>
            <p class="section-note">Top 20 suspicious items ranked by heuristic suspicion score.</p>
            <table>
                <tr>
                    <th>Item</th>
                    <th>Source</th>
                    <th>Event Count</th>
                    <th>Confidence</th>
                    <th>Score</th>
                    <th>Reasons</th>
                </tr>
                {suspicious_table if suspicious_table else '<tr><td colspan="6">No suspicious items detected.</td></tr>'}
            </table>
        </div>

        <div class="footer-note">
            Generated by the Automated Digital Evidence Timeline Generator
        </div>
    </div>
</body>
</html>
"""

    report_path = os.path.join(output_dir, "investigation_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML investigation report saved to: {report_path}")