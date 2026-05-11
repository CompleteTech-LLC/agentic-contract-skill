# Agentic Contract & Certificate Skill

A configurable, branded PDF skill for CompleteTech LLC. Two generators share one INI-driven brand and palette:

1. **`generate_contract.py`** — Agentic Development Services Agreement (multi-page, letterhead, watermark, signatures, optional #10 envelope).
2. **`generate_certificate.py`** — Certificate of Attendance (single landscape page, script signature, CT-circuit official seal).

Both pull `[provider]`, `[branding]`, and color palette from the same `config.ini` so the brand stays consistent across artifacts.

## Quick Start

```bash
pip install -r requirements.txt

# Contract
python generate_contract.py --config config.ini \
  --out output/agentic_development_contract_demo.pdf

# Certificate (defaults to recipient defined in [certificate] of config.ini)
python generate_certificate.py

# Certificate for a specific attendee — minimum inputs:
python generate_certificate.py \
  --recipient-name "Jane Smith" \
  --recipient-email "jane@example.com"
```

The output PDFs land in `output/`; rendered previews live in `preview/`.

## Certificate Auto-Fill

The certificate generator minimizes per-run inputs. Leave these blank in `[certificate]` and they auto-fill:

| Field | Auto behavior |
|---|---|
| `issue_date` | Defaults to today (`date.today().isoformat()`) |
| `certificate_id` | Deterministic `COMP-{course-prefix}-{YYYYMMDD}-{sha1[:6]}` from course + name + email + date |

CLI flags (`--issue-date`, `--certificate-id`) still override if you need a specific value.

Per-attendee, you only need: `recipient_name`, `recipient_email`. Course title, signatory, seal, signature font, and branding all live in config.

## Branding Assets

- `assets/logo.png` — CompleteTech LLC primary logo (cloud + lightbulb + text). Used on contract letterhead and certificate header.
- `assets/stamp_ct.png` — Isolated CT-circuit mark (from inside the lightbulb). Used as the certificate's official seal, clipped inside a circular badge.
- `assets/fonts/GreatVibes-Regular.ttf` — Free Google Fonts script (SIL OFL) for the signature. Falls back to Times-Italic if missing.

## Toggles

In `[branding]` (contract):

```ini
watermark_enabled = yes
watermark_text = DEMO DRAFT
cover_page_enabled = yes
letterhead_enabled = yes
header_enabled = yes
footer_enabled = yes
envelope_enabled = yes
```

In `[certificate]`:

```ini
course_title = Agentic Skills and Using Them with OpenClaw
course_subtitle = A hands-on class by CompleteTech LLC
intro_line = This is to certify that
attestation_line = has attended and completed the class
signatory_name = Timothy Gregg
signatory_title = Agent Whisperer, CompleteTech LLC
# Leave blank to auto-fill:
issue_date =
certificate_id =
```

## Overrides

Pass multiple INI files; later ones override earlier ones:

```bash
python generate_contract.py \
  --config config.ini examples/minimum_client_override.ini \
  --out output/acme_contract.pdf

python generate_certificate.py \
  --config config.ini examples/certificate_recipient_override.ini
```

## Legal Note

The contract template is a **demonstration template, not legal advice**. Replace with your own counsel-reviewed terms before any real engagement. The certificate is suitable for class/training use as-is.
