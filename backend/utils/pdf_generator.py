"""
utils/pdf_generator.py

Generates a professional PDF validation report using ReportLab.
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "reports"))

# Brand colours
NAVY = HexColor("#1B2A4A")
TEAL = HexColor("#0F6E56")
AMBER = HexColor("#BA7517")
CORAL = HexColor("#993C1D")
LIGHT_GRAY = HexColor("#F1EFE8")
TEAL_LIGHT = HexColor("#E1F5EE")
AMBER_LIGHT = HexColor("#FAEEDA")
CORAL_LIGHT = HexColor("#FAECE7")
PURPLE_LIGHT = HexColor("#EEEDFE")


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", fontSize=22, textColor=white,
                                 fontName="Helvetica-Bold", spaceAfter=4, alignment=TA_CENTER),
        "subtitle": ParagraphStyle("subtitle", fontSize=11, textColor=HexColor("#9FE1CB"),
                                    fontName="Helvetica", spaceAfter=2, alignment=TA_CENTER),
        "h2": ParagraphStyle("h2", fontSize=13, textColor=NAVY, fontName="Helvetica-Bold",
                              spaceBefore=16, spaceAfter=6),
        "h3": ParagraphStyle("h3", fontSize=11, textColor=TEAL, fontName="Helvetica-Bold",
                              spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("body", fontSize=9.5, textColor=black, fontName="Helvetica",
                                leading=14, spaceAfter=6, alignment=TA_JUSTIFY),
        "bullet": ParagraphStyle("bullet", fontSize=9.5, textColor=black, fontName="Helvetica",
                                  leading=13, spaceAfter=3, leftIndent=12, bulletIndent=0),
        "label": ParagraphStyle("label", fontSize=8, textColor=HexColor("#5F5E5A"),
                                 fontName="Helvetica"),
        "score_num": ParagraphStyle("score_num", fontSize=28, textColor=NAVY,
                                     fontName="Helvetica-Bold", alignment=TA_CENTER),
        "verdict": ParagraphStyle("verdict", fontSize=11, textColor=TEAL,
                                   fontName="Helvetica-Bold", alignment=TA_CENTER),
    }


def _score_color(score: float):
    if score >= 70:
        return TEAL
    elif score >= 50:
        return AMBER
    return CORAL


def generate_pdf(job_id: str, result) -> str:
    """
    Build the full PDF report. Returns the file path.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = REPORTS_DIR / f"{job_id}.pdf"
    s = _styles()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"IdeaForge AI — {result.idea_name}",
    )

    story = []

    # ── Cover / Title block ─────────────────────────────────────────────────
    cover_data = [
        [Paragraph("IdeaForge AI", s["title"])],
        [Paragraph("Startup Idea Validation Report", s["subtitle"])],
        [Paragraph(result.idea_name, ParagraphStyle(
            "iname", fontSize=15, textColor=white, fontName="Helvetica-Bold",
            alignment=TA_CENTER, spaceBefore=8))],
    ]
    cover_table = Table(cover_data, colWidths=[16.5*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 18),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 18),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Executive Summary ────────────────────────────────────────────────────
    if result.executive_summary:
        story.append(Paragraph("Executive Summary", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(result.executive_summary, s["body"]))
        story.append(Spacer(1, 0.3*cm))

    # ── Validation Score ─────────────────────────────────────────────────────
    if result.score:
        sc = result.score
        story.append(Paragraph("Validation Score", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))

        score_color = _score_color(sc.total)
        dim_data = [
            ["Dimension", "Score", "Out of"],
            ["Market Size", f"{sc.market_size:.0f}", "20"],
            ["Competition Gap", f"{sc.competition_gap:.0f}", "20"],
            ["Technical Feasibility", f"{sc.technical_feasibility:.0f}", "20"],
            ["Idea Uniqueness", f"{sc.idea_uniqueness:.0f}", "20"],
            ["Monetisation Potential", f"{sc.monetisation_potential:.0f}", "20"],
            ["TOTAL", f"{sc.total:.0f}", "100"],
        ]
        dim_table = Table(dim_data, colWidths=[9*cm, 3.5*cm, 4*cm])
        dim_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [LIGHT_GRAY, white]),
            ("BACKGROUND", (0, -1), (-1, -1), TEAL_LIGHT),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, -1), (0, -1), TEAL),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ])
        dim_table.setStyle(dim_style)
        story.append(dim_table)
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"Verdict: {sc.verdict}", s["verdict"]))
        story.append(Spacer(1, 0.3*cm))

    # ── Market Research ──────────────────────────────────────────────────────
    if result.market_research:
        story.append(Paragraph("Market Research", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        for line in result.market_research.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith(("1.", "2.", "3.", "4.", "5.", "**", "##", "#")):
                clean = line.lstrip("0123456789.#* ").strip()
                story.append(Paragraph(clean, s["h3"]))
            else:
                story.append(Paragraph(line, s["body"]))
        story.append(Spacer(1, 0.3*cm))

    # ── Competitor Analysis ──────────────────────────────────────────────────
    if result.competitor_analysis:
        story.append(Paragraph("Competitor Analysis", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        for line in result.competitor_analysis.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith(("1.", "2.", "3.", "**", "##", "#")):
                clean = line.lstrip("0123456789.#* ").strip()
                story.append(Paragraph(clean, s["h3"]))
            else:
                story.append(Paragraph(line, s["body"]))
        story.append(Spacer(1, 0.3*cm))

    # ── Feasibility & Risk ───────────────────────────────────────────────────
    if result.feasibility:
        story.append(Paragraph("Feasibility & Risk Analysis", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        for line in result.feasibility.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith(("1.", "2.", "3.", "4.", "5.", "**", "##", "#")):
                clean = line.lstrip("0123456789.#* ").strip()
                story.append(Paragraph(clean, s["h3"]))
            else:
                story.append(Paragraph(line, s["body"]))
        story.append(Spacer(1, 0.3*cm))

    # ── SWOT ─────────────────────────────────────────────────────────────────
    if result.swot:
        story.append(Paragraph("SWOT Analysis", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        sw = result.swot

        def swot_cell(title, items, fill):
            content = [Paragraph(title, ParagraphStyle(
                "sh", fontSize=9, fontName="Helvetica-Bold",
                textColor=NAVY, spaceAfter=4))]
            for item in items:
                content.append(Paragraph(f"• {item}", ParagraphStyle(
                    "si", fontSize=8.5, fontName="Helvetica", leading=12)))
            return content, fill

        s_content, s_fill = swot_cell("Strengths", sw.strengths, TEAL_LIGHT)
        w_content, w_fill = swot_cell("Weaknesses", sw.weaknesses, CORAL_LIGHT)
        o_content, o_fill = swot_cell("Opportunities", sw.opportunities, PURPLE_LIGHT)
        t_content, t_fill = swot_cell("Threats", sw.threats, AMBER_LIGHT)

        swot_data = [[s_content, w_content], [o_content, t_content]]
        swot_table = Table(swot_data, colWidths=[8.2*cm, 8.2*cm], rowHeights=None)
        swot_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), TEAL_LIGHT),
            ("BACKGROUND", (1, 0), (1, 0), CORAL_LIGHT),
            ("BACKGROUND", (0, 1), (0, 1), PURPLE_LIGHT),
            ("BACKGROUND", (1, 1), (1, 1), AMBER_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ]))
        story.append(swot_table)
        story.append(Spacer(1, 0.3*cm))

    # ── Business Model ───────────────────────────────────────────────────────
    if result.business_model:
        story.append(Paragraph("Business Model Recommendation", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        for line in result.business_model.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith(("1.", "2.", "3.", "4.", "5.", "**", "##", "#")):
                clean = line.lstrip("0123456789.#* ").strip()
                story.append(Paragraph(clean, s["h3"]))
            else:
                story.append(Paragraph(line, s["body"]))
        story.append(Spacer(1, 0.3*cm))

    # ── MVP Roadmap ───────────────────────────────────────────────────────────
    if result.roadmap:
        story.append(Paragraph("MVP Roadmap", s["h2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
        story.append(Spacer(1, 0.2*cm))
        phase_fills = [TEAL_LIGHT, PURPLE_LIGHT, AMBER_LIGHT]
        for i, phase in enumerate(result.roadmap):
            fill = phase_fills[i % len(phase_fills)]
            phase_data = [
                [Paragraph(phase.phase, ParagraphStyle(
                    "ph", fontSize=10, fontName="Helvetica-Bold",
                    textColor=NAVY)),
                 Paragraph(phase.duration, ParagraphStyle(
                     "pd", fontSize=9, fontName="Helvetica",
                     textColor=HexColor("#5F5E5A"), alignment=TA_LEFT))],
                *[[Paragraph(f"• {m}", ParagraphStyle(
                    "pm", fontSize=9, fontName="Helvetica", leading=13)), ""]
                  for m in phase.milestones],
            ]
            phase_table = Table(phase_data, colWidths=[10*cm, 6.5*cm])
            phase_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), fill),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
                ("SPAN", (0, 1), (-1, -1)),
            ]))
            story.append(KeepTogether([phase_table, Spacer(1, 0.2*cm)]))
        story.append(Spacer(1, 0.3*cm))

    # ── Footer note ──────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#CCCCCC")))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Generated by IdeaForge AI · For educational and planning purposes only.",
        ParagraphStyle("footer", fontSize=7.5, textColor=HexColor("#888780"),
                       alignment=TA_CENTER)
    ))

    doc.build(story)
    return str(pdf_path)
