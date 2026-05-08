"""Inject 'View Full Stage' CTA at the bottom of each phase section."""
import re
from pathlib import Path

ROADMAP = Path("roadmap.html")
content = ROADMAP.read_text(encoding='utf-8')

PHASES = {
    "concept": "stage-concept.html",
    "foundation": "stage-foundation.html",
    "architecture": "stage-architecture.html",
    "vertical-slice": "stage-vertical-slice.html",
    "funding": "stage-funding.html",
    "production": "stage-production.html",
    "early-access": "stage-early-access.html",
    "full-release": "stage-full-release.html",
}

def inject_cta(match):
    phase_id = match.group(1)
    body = match.group(2)
    if phase_id not in PHASES:
        return match.group(0)
    href = PHASES[phase_id]
    cta = (
        '\n            <div class="phase-cta-wrap">'
        f'<a class="phase-cta" href="{href}">View Full Stage <span class="phase-cta-arrow">→</span></a>'
        '</div>'
    )
    last_close_idx = body.rfind('</div>')
    new_body = body[:last_close_idx] + cta + '\n        ' + body[last_close_idx:]
    return f'<section class="phase" id="{phase_id}">{new_body}</section>'

pattern = re.compile(r'<section class="phase" id="([\w-]+)">(.*?)</section>', re.DOTALL)
new_content = pattern.sub(inject_cta, content)

cta_anchor_count = new_content.count('class="phase-cta"')
assert cta_anchor_count == 8, f"Expected 8 CTAs, got {cta_anchor_count}"

ROADMAP.write_text(new_content, encoding='utf-8')
print(f"Done. {cta_anchor_count} CTAs injected. File size: {len(new_content)} bytes")
