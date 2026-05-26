---
name: agentic-contract-skill
description: >-
  Generate branded CompleteTech Agentic Development Services Agreement packages from approved provider, client, project, commercial, and governance terms. Use when the user wants configurable contract PDFs, filled Markdown source, and optional envelope output for agentic workflow engagements.
version: 1.0.4
metadata:
  openclaw:
    skillKey: agentic-contract-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-contract-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: pyyaml==6.0.3
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: jinja2==3.1.6
---

# Agentic Contract Skill

## At a Glance

| What it creates | Best for | Output |
|---|---|---|
| Agentic development agreement packages | Approved service terms, pilot agreements, governance clauses, and signature-ready review packets | Branded PDF, filled Markdown, optional addressed envelope |

This skill turns verified provider, client, scope, fee, timeline, human-review, evaluation, monitoring, and excluded-use facts into a CompleteTech-style agreement package. It is local-only and does not replace legal review, commercial approval, billing, or delivery acceptance.

## Included Contract Artifacts

- Agentic Development Services Agreement PDF.
- Filled Markdown source for review and redline workflows.
- Configurable branding with cover, letterhead, header, footer, and watermark.
- Optional #10 addressed envelope PDF for physical delivery packages.

## Purpose

Generate a configurable CompleteTech LLC Agentic Development Services Agreement PDF with optional cover page, letterhead, header, footer, watermark, and legacy #10 addressed envelope output.

## System Boundary

This skill owns agreement content and contract package generation from approved terms. Use `agentic-proposal-skill` for commercial scope before signature, `agentic-invoice-skill` for payment requests, `agentic-envelope-skill` for recipient metadata, attachment manifests, delivery-readiness, and standalone mailing packages, `agentic-delivery-skill` after approval, and counsel-reviewed source terms for real legal commitments. Do not use this skill to invent legal terms, client facts, pricing, authority, or signature approval.

## Resource Guide

- `generate_contract.py` - contract and envelope generator.
- `references/agentic_development_agreement.md` - packaged contract template with Jinja2 placeholders.
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

## Quality Rules

- Do not invent legal terms, company facts, client facts, authority, acceptance, pricing, or signature approval.
- Preserve demonstration disclaimers unless the user supplies replacement counsel-reviewed terms.
- Keep unknown provider, client, agreement, delivery, and agentic-development values as `TBD`.
- Treat generated PDFs and Markdown as draft artifacts until the user confirms the terms and facts.
- Keep contract generation separate from proposals, invoices, delivery records, security signoff, customer success notes, email copy, and delivery packaging decisions.
- Do not overwrite user-specific config or generated output without checking whether it contains client-specific facts that should be preserved.

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

## Generator

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
7. Preserve existing client-specific outputs unless the user asks to regenerate or replace them.

## Customizing the Contract

Edit `references/agentic_development_agreement.md` to change clauses, add jurisdiction-specific language, or include business-specific statement-of-work text. The generator supports a practical Markdown subset:

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

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts contract run metadata to an external service.
