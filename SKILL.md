# Agentic Contract & Certificate Skill

## Purpose

Generate two CompleteTech LLC PDF artifacts from a shared `config.ini`:

1. **Agentic Development Services Agreement** — multi-page contract with letterhead, watermark, signature block, and optional #10 addressed envelope.
2. **Certificate of Attendance** — single-page landscape certificate with script signature, CT-circuit official seal, and auto-generated date + ID.

Both share `[provider]`, `[branding]`, and color palette so the brand stays consistent.

## Files

### Contract
- `generate_contract.py` — contract + envelope generator.
- `templates/agentic_development_agreement.md.j2` — contract template with Jinja2 placeholders.
- `output/agentic_development_contract_demo.pdf` / `.md` — compiled demo + filled Markdown source.
- `output/addressed_envelope.pdf` — printable #10 envelope.

### Certificate
- `generate_certificate.py` — certificate generator (imports brand helpers from `generate_contract.py`).
- `output/certificate_<recipient_slug>.pdf` — compiled certificate (filename auto-slugged from recipient name).

### Shared assets
- `assets/logo.png` — primary CompleteTech logo (cloud + lightbulb + "COMPLETETECH LLC").
- `assets/stamp_ct.png` — isolated CT-circuit mark used as the certificate's official seal.
- `assets/fonts/GreatVibes-Regular.ttf` — script font for the certificate signature.

### Config
- `config.ini` — declarative provider, client, agreement, agentic-development, branding, envelope, and certificate settings.
- `client_config.example.ini`, `examples/minimum_client_override.ini` — contract override examples.
- `examples/certificate_recipient_override.ini` — per-attendee override example.

## Required Inputs

### For a contract
1. Provider business details: legal name, trade name, entity type, formation state, mailing address, email, phone, website, signatory name and title.
2. Client details: legal name, entity type, address, signatory name and title.
3. Project details: contract ID, effective date, project name, services summary, timeline, fee amount, payment terms.
4. Agentic development details: system description, autonomy level, human-in-the-loop requirements, model or stack, deployment environment, evaluation plan, monitoring plan, excluded uses.
5. Branding and rendering settings: watermark text, monogram, accent color, letterhead on/off, header on/off, footer on/off, envelope on/off.

### For a certificate (minimum)
Just: `recipient_name` and `recipient_email`. Everything else (date, certificate ID, course title, signatory) comes from `[certificate]` in `config.ini` and auto-fill rules below.

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

In `[certificate]`:

```ini
course_title = Agentic Skills and Using Them with OpenClaw
course_subtitle = A hands-on class by CompleteTech LLC
recipient_name = ...
recipient_email = ...
signatory_name = Timothy Gregg
signatory_title = Agent Whisperer, CompleteTech LLC
# Auto-fills when blank:
issue_date =
certificate_id =
```

## Certificate Auto-Fill

- `issue_date` blank → today's date.
- `certificate_id` blank → `COMP-{course-prefix}-{YYYYMMDD}-{sha1[:6]}` derived deterministically from course title + recipient name + email + date.

CLI flags `--issue-date` / `--certificate-id` override if you need to pin specific values.

## How to Run

```bash
pip install -r requirements.txt

# Contract (demo)
python generate_contract.py --config config.ini \
  --out output/agentic_development_contract.pdf

# Contract (with client override)
python generate_contract.py \
  --config config.ini examples/minimum_client_override.ini \
  --out output/acme_agentic_development_contract.pdf \
  --envelope-out output/acme_envelope.pdf

# Skip the envelope for one run
python generate_contract.py --config config.ini --out output/no_envelope_contract.pdf --no-envelope

# Certificate (uses recipient from config.ini)
python generate_certificate.py

# Certificate for a specific attendee
python generate_certificate.py \
  --recipient-name "Jane Smith" \
  --recipient-email "jane@example.com"
```

## Expected Outputs

Each contract run creates:
- A PDF contract at the `--out` path.
- A filled Markdown source file beside the PDF unless `--markdown-out` is provided.
- A separate printable envelope PDF unless disabled.

Each certificate run creates one PDF at `output/certificate_<slug>.pdf` (slug auto-derived from recipient name).

## Agent Operating Guidance

When used as an agent skill:

### For a contract
1. Read the user's business profile or provided inputs.
2. Update `config.ini` or create an override INI. Keep unknown details as `TBD`.
3. Ensure demonstration disclaimers remain visible unless the user supplies replacement legal text.
4. Run `generate_contract.py`.
5. Return links to the PDF, Markdown source, and ZIP or folder as appropriate.
6. Remind the user that the document is a demonstration template, not legal advice, unless the user already states that their own reviewed legal terms are being inserted.

### For a certificate
1. Confirm or collect `recipient_name` and `recipient_email`.
2. Run `generate_certificate.py --recipient-name "..." --recipient-email "..."`. **Do not** set `issue_date` or `certificate_id` unless the user explicitly asks — both auto-fill.
3. Return the output PDF path. The certificate is suitable as-is; no legal disclaimer needed.

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

The generators use `reportlab` for PDF creation and `jinja2` for contract template rendering.
