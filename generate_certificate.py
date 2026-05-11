#!/usr/bin/env python3
"""Generate a Certificate of Attendance PDF.

Reads [provider], [branding], and [certificate] sections from config.ini
(plus optional override INIs) and produces a single-page landscape PDF.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from datetime import date
from pathlib import Path
from typing import Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdf_canvas

from generate_contract import (
    BASE_DIR,
    DEFAULT_CONFIG,
    palette,
    read_config,
    resolve_logo_path,
    resolve_path,
    section_dict,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Certificate of Attendance PDF.")
    parser.add_argument("--config", nargs="+", default=[str(DEFAULT_CONFIG)])
    parser.add_argument("--out", default=str(BASE_DIR / "output" / "certificate.pdf"))
    parser.add_argument("--recipient-name", default=None)
    parser.add_argument("--recipient-email", default=None)
    parser.add_argument("--course-title", default=None)
    parser.add_argument("--issue-date", default=None)
    parser.add_argument("--certificate-id", default=None)
    return parser.parse_args()


SIGNATURE_FONT_NAME = "SignatureScript"
SIGNATURE_FONT_PATH = BASE_DIR / "assets" / "fonts" / "GreatVibes-Regular.ttf"
_signature_font_loaded = False


def ensure_signature_font() -> str:
    """Register the script signature font once. Returns the font name to use,
    falling back to Times-Italic if the TTF is missing."""
    global _signature_font_loaded
    if _signature_font_loaded:
        return SIGNATURE_FONT_NAME
    if not SIGNATURE_FONT_PATH.exists():
        return "Times-Italic"
    try:
        pdfmetrics.registerFont(TTFont(SIGNATURE_FONT_NAME, str(SIGNATURE_FONT_PATH)))
        _signature_font_loaded = True
        return SIGNATURE_FONT_NAME
    except Exception:
        return "Times-Italic"


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return slug or "recipient"


def course_prefix(course_title: str) -> str:
    """Build a short, stable code from the course title, e.g. 'Agentic Skills...' -> 'AGSK'."""
    words = re.findall(r"[A-Za-z0-9]+", course_title.upper())
    if not words:
        return "CERT"
    letters = "".join(w[0] for w in words if w[0].isalpha())[:5]
    return letters or "CERT"


def auto_certificate_id(certificate: Dict[str, str], issue_date: str) -> str:
    """Deterministic ID from course + recipient + date. No state file needed."""
    seed = "|".join([
        certificate.get("course_title", ""),
        certificate.get("recipient_email", ""),
        certificate.get("recipient_name", ""),
        issue_date,
    ]).lower()
    short = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:6].upper()
    date_compact = issue_date.replace("-", "")
    prefix = course_prefix(certificate.get("course_title", ""))
    return f"COMP-{prefix}-{date_compact}-{short}"


def draw_border(c: pdf_canvas.Canvas, width: float, height: float,
                pal: Dict[str, colors.Color]) -> None:
    outer_inset = 0.32 * inch
    inner_inset = 0.50 * inch
    c.saveState()
    c.setStrokeColor(pal["accent"])
    c.setLineWidth(3.0)
    c.rect(outer_inset, outer_inset, width - 2 * outer_inset, height - 2 * outer_inset,
           stroke=1, fill=0)
    c.setStrokeColor(pal["accent_dark"])
    c.setLineWidth(0.7)
    c.rect(inner_inset, inner_inset, width - 2 * inner_inset, height - 2 * inner_inset,
           stroke=1, fill=0)

    # Corner accent dots
    c.setFillColor(pal["accent"])
    for cx, cy in [
        (outer_inset, outer_inset),
        (width - outer_inset, outer_inset),
        (outer_inset, height - outer_inset),
        (width - outer_inset, height - outer_inset),
    ]:
        c.circle(cx, cy, 0.08 * inch, stroke=0, fill=1)
    c.restoreState()


def draw_logo(c: pdf_canvas.Canvas, branding: Dict[str, str], cx: float, top_y: float,
              max_width: float, max_height: float) -> float:
    """Draw the logo centered horizontally at cx, top-aligned at top_y.

    Returns the y-coordinate of the bottom of the drawn logo (so caller can stack below).
    """
    logo_path = resolve_logo_path(branding)
    if not logo_path:
        return top_y
    try:
        reader = ImageReader(str(logo_path))
        iw, ih = reader.getSize()
    except Exception:
        return top_y
    scale = min(max_width / iw, max_height / ih)
    draw_w = iw * scale
    draw_h = ih * scale
    x = cx - draw_w / 2.0
    y = top_y - draw_h
    c.drawImage(reader, x, y, width=draw_w, height=draw_h,
                preserveAspectRatio=True, mask="auto")
    return y


def draw_centered(c: pdf_canvas.Canvas, x: float, y: float, text: str,
                  font: str, size: float, color: colors.Color) -> None:
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(x, y, text)


def build_certificate(out_path: Path, branding: Dict[str, str],
                      certificate: Dict[str, str]) -> None:
    width, height = landscape(LETTER)
    c = pdf_canvas.Canvas(str(out_path), pagesize=(width, height))
    c.setTitle("Certificate of Attendance")
    c.setAuthor(branding.get("brand_name", "CompleteTech LLC"))

    pal = palette(branding)
    center_x = width / 2.0

    draw_border(c, width, height, pal)

    logo_top = height - 0.85 * inch
    logo_bottom = draw_logo(c, branding, center_x, logo_top,
                            max_width=2.4 * inch, max_height=1.05 * inch)

    # Title (brand name omitted — logo already includes "COMPLETETECH LLC")
    title_y = logo_bottom - 0.55 * inch
    draw_centered(c, center_x, title_y, "Certificate of Attendance",
                  "Times-Bold", 34, pal["ink"])

    # Decorative rule under title
    rule_y = title_y - 0.18 * inch
    c.setStrokeColor(pal["accent"])
    c.setLineWidth(1.4)
    c.line(center_x - 1.6 * inch, rule_y, center_x + 1.6 * inch, rule_y)
    c.setFillColor(pal["accent"])
    c.circle(center_x, rule_y, 0.05 * inch, stroke=0, fill=1)

    # Intro
    intro = certificate.get("intro_line", "This is to certify that")
    draw_centered(c, center_x, rule_y - 0.55 * inch, intro,
                  "Times-Italic", 14, pal["ink_soft"])

    # Recipient name
    recipient_name = certificate.get("recipient_name", "TBD")
    name_y = rule_y - 1.15 * inch
    draw_centered(c, center_x, name_y, recipient_name,
                  "Times-BoldItalic", 30, pal["accent_dark"])

    # Underline under name
    name_underline_y = name_y - 0.10 * inch
    c.setStrokeColor(pal["border"])
    c.setLineWidth(0.6)
    c.line(center_x - 3.0 * inch, name_underline_y, center_x + 3.0 * inch, name_underline_y)

    # Email
    email = certificate.get("recipient_email", "")
    if email:
        draw_centered(c, center_x, name_underline_y - 0.22 * inch, email,
                      "Helvetica", 10.5, pal["muted"])

    # Attestation line
    attest = certificate.get("attestation_line", "has attended and completed the class")
    draw_centered(c, center_x, name_underline_y - 0.62 * inch, attest,
                  "Times-Roman", 13, pal["ink_soft"])

    # Course title
    course_title = certificate.get("course_title", "TBD")
    course_y = name_underline_y - 1.10 * inch
    draw_centered(c, center_x, course_y, course_title,
                  "Helvetica-Bold", 18, pal["ink"])

    course_subtitle = certificate.get("course_subtitle", "")
    if course_subtitle:
        draw_centered(c, center_x, course_y - 0.28 * inch, course_subtitle,
                      "Helvetica-Oblique", 10.5, pal["muted"])

    # Signature block (bottom-left), date (bottom-center), certificate id (bottom-right)
    base_y = 1.20 * inch
    sig_x_left = 1.50 * inch
    sig_x_right = sig_x_left + 2.6 * inch

    # Signature line
    c.setStrokeColor(pal["ink"])
    c.setLineWidth(0.8)
    c.line(sig_x_left, base_y + 0.10 * inch, sig_x_right, base_y + 0.10 * inch)

    # Signature script — handwriting font if available, else fallback italic
    sig_font = ensure_signature_font()
    sig_size = 28 if sig_font == SIGNATURE_FONT_NAME else 16
    sig_baseline = base_y + (0.14 * inch if sig_font == SIGNATURE_FONT_NAME else 0.18 * inch)
    c.setFillColor(pal["accent_dark"])
    c.setFont(sig_font, sig_size)
    c.drawString(sig_x_left + 0.10 * inch, sig_baseline,
                 certificate.get("signatory_name", ""))

    # Signature labels
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(sig_x_left, base_y - 0.05 * inch, "SIGNATURE")

    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(sig_x_left, base_y - 0.22 * inch, certificate.get("signatory_name", ""))
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 9.5)
    c.drawString(sig_x_left, base_y - 0.38 * inch, certificate.get("signatory_title", ""))

    # Date in the center
    issue_date = certificate.get("issue_date", "")
    if issue_date:
        c.setFillColor(pal["muted"])
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(center_x, base_y - 0.05 * inch, "DATE OF ISSUE")
        c.setFillColor(pal["ink"])
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(center_x, base_y - 0.22 * inch, issue_date)

    # Certificate ID bottom-right
    cert_id = certificate.get("certificate_id", "")
    right_x = width - 1.50 * inch
    if cert_id:
        c.setFillColor(pal["muted"])
        c.setFont("Helvetica-Bold", 7.5)
        c.drawRightString(right_x, base_y - 0.05 * inch, "CERTIFICATE ID")
        c.setFillColor(pal["ink"])
        c.setFont("Helvetica-Bold", 10.5)
        c.drawRightString(right_x, base_y - 0.22 * inch, cert_id)

    # Seal: right edge flush with the certificate ID's right edge, nudged up
    seal_r = 0.72 * inch
    seal_cx = right_x - seal_r
    seal_cy = base_y + 0.95 * inch
    inner_r = seal_r - 0.16 * inch  # leaves a rim for OFFICIAL / SEAL labels
    stamp_path = resolve_path(certificate.get("stamp_path", "assets/stamp_ct.png"))

    c.saveState()
    # Outer + inner rim rings
    c.setStrokeColor(pal["accent"])
    c.setLineWidth(1.8)
    c.circle(seal_cx, seal_cy, seal_r, stroke=1, fill=0)
    c.setStrokeColor(pal["accent_dark"])
    c.setLineWidth(0.6)
    c.circle(seal_cx, seal_cy, inner_r, stroke=1, fill=0)

    if stamp_path.exists():
        c.saveState()
        clip = c.beginPath()
        clip.circle(seal_cx, seal_cy, inner_r - 0.01 * inch)
        c.clipPath(clip, stroke=0, fill=0)
        img_size = inner_r * 2.0
        c.drawImage(ImageReader(str(stamp_path)),
                    seal_cx - img_size / 2.0, seal_cy - img_size / 2.0,
                    width=img_size, height=img_size,
                    preserveAspectRatio=True, mask="auto")
        c.restoreState()
    else:
        monogram = (branding.get("logo_monogram") or "CT")[:3]
        c.setFillColor(pal["accent_dark"])
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(seal_cx, seal_cy - 0.14 * inch, monogram)

    # Rim labels (in the ring between inner_r and seal_r)
    c.setFillColor(pal["accent_dark"])
    c.setFont("Helvetica-Bold", 6)
    rim_y = (seal_r + inner_r) / 2.0
    c.drawCentredString(seal_cx, seal_cy + rim_y - 0.05 * inch, "OFFICIAL")
    c.drawCentredString(seal_cx, seal_cy - rim_y - 0.01 * inch, "SEAL")
    c.restoreState()

    c.showPage()
    c.save()


def main() -> int:
    args = parse_args()
    config = read_config([Path(p) for p in args.config])
    branding = section_dict(config, "branding")
    certificate = section_dict(config, "certificate")

    if args.recipient_name:
        certificate["recipient_name"] = args.recipient_name
    if args.recipient_email:
        certificate["recipient_email"] = args.recipient_email
    if args.course_title:
        certificate["course_title"] = args.course_title
    if args.issue_date:
        certificate["issue_date"] = args.issue_date
    if args.certificate_id:
        certificate["certificate_id"] = args.certificate_id

    if not certificate.get("issue_date", "").strip():
        certificate["issue_date"] = date.today().isoformat()
    if not certificate.get("certificate_id", "").strip():
        certificate["certificate_id"] = auto_certificate_id(certificate, certificate["issue_date"])

    out_path = resolve_path(args.out)
    if args.out == str(BASE_DIR / "output" / "certificate.pdf"):
        # Add recipient slug to default filename so re-runs don't overwrite blindly.
        slug = slugify(certificate.get("recipient_name", "recipient"))
        out_path = out_path.with_name(f"certificate_{slug}.pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    build_certificate(out_path, branding, certificate)
    print(f"Certificate PDF: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
