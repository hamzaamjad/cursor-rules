#!/usr/bin/env python3
"""Debug version - check MDC files"""

import re
import logging
from pathlib import Path

rules_dir = Path('./rules')
files_with_frontmatter = []
files_without = []

for mdc_file in rules_dir.rglob("*.mdc"):
    with open(mdc_file) as f:
        content = f.read()
    
    if content.startswith('---\n'):
        files_with_frontmatter.append(mdc_file)
    else:
        files_without.append(mdc_file)

logging.info(f"Files WITH frontmatter: {len(files_with_frontmatter)}")
for f in sorted(files_with_frontmatter)[:10]:
    logging.info(f"  - {f.relative_to(rules_dir)}")

logging.info(f"\nFiles WITHOUT frontmatter: {len(files_without)}")
logging.info(f"\nTOTAL MDC files: {len(files_with_frontmatter) + len(files_without)}")
