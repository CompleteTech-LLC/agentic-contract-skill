---
name: agentic-contract-skill
description: Generate configurable CompleteTech LLC Agentic Development Services Agreement PDFs with optional cover page, letterhead, header, footer, watermark, filled Markdown source, and printable addressed envelope. Use when Codex needs to create or customize agentic development contracts, contract templates, client override configs, or branded contract/envelope artifacts.
---

# Agentic Contract Skill

## Purpose

Generate a configurable CompleteTech LLC Agentic Development Services Agreement PDF with optional cover page, letterhead, header, footer, watermark, and #10 addressed envelope.

## Files

- `generate_contract.py` - contract and envelope generator.
- `templates/agentic_development_agreement.md.j2` - contract template with Jinja2 placeholders.
- `config.ini` - declarative provider, client, agreement, agentic-development, branding, and envelope settings.
- `client_config.example.ini`, `examples/minimum_client_override.ini` - override examples.
- `assets/logo.png` - primary CompleteTech logo.

## Required Inputs

1. Provider business details: legal name, trade name, entity type, formation state, mailing address, email, phone, website, signatory name and title.
2. Client details: legal name, entity type, address, signatory name and title.
3. Project details: contract ID, effective date, project name, services summary, timeline, fee amount, payment terms.
4. Agentic development details: system description, autonomy level, human-in-the-loop requirements, model or stack, deployment environment, evaluation plan, monitoring plan, excluded uses.
5. Branding and rendering settings: watermark text, monogram, accent color, letterhead on/off, header on/off, footer on/off, envelope on/off.

Do not invent real legal or company facts. Use `TBD` for unknown values unless the user explicitly asks for a demo placeholder.

## Configuration Toggles

In `[branding]`:

```ini
watermark_enabled = yes
watermark_text = DEMO DRAFT
letterhead_enabled = yes
header_enabled = yes
footer_enabled = yes
envelope_enabled = yes
```

Set any toggle to `no` to disable that feature. The envelope is generated as a separate #10 envelope PDF when `envelope_enabled = yes`.

## How to Run

```bash
pip install -r requirements.txt

python generate_contract.py --config config.ini \
  --out output/agentic_development_contract.pdf

python generate_contract.py \
  --config config.ini examples/minimum_client_override.ini \
  --out output/acme_agentic_development_contract.pdf \
  --envelope-out output/acme_envelope.pdf

python generate_contract.py --config config.ini --out output/no_envelope_contract.pdf --no-envelope
```

## Agent Operating Guidance

1. Read the user's business profile or provided inputs.
2. Update `config.ini` or create an override INI. Keep unknown details as `TBD`.
3. Ensure demonstration disclaimers remain visible unless the user supplies replacement legal text.
4. Run `generate_contract.py`.
5. Return links to the PDF, Markdown source, and ZIP or folder as appropriate.
6. Remind the user that the document is a demonstration template, not legal advice, unless the user already states that their own reviewed legal terms are being inserted.

## Customizing the Contract

Edit `templates/agentic_development_agreement.md.j2` to change clauses, add jurisdiction-specific language, or include business-specific statement-of-work text. The generator supports a practical Markdown subset:

- `#`, `##`, and `###` headings.
- Paragraphs.
- `-` bullet lists.
- Simple Markdown tables.
- `**bold**` inline emphasis.
- Block quotes beginning with `>`.
- `[PAGE_BREAK]` for manual page breaks.

## Dependencies

Install dependencies with:

```bash
pip install -r requirements.txt
```

The generator uses `reportlab` for PDF creation and `jinja2` for contract template rendering.
