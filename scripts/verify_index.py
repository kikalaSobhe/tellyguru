#!/usr/bin/env python3
"""Executable acceptance verifier for the tellyguru "Sarcastic wisdom" section.

Asserts real structural properties of the built site sources and emits a JUnit
XML report into $AGENTFLOW_REPORT_DIR (filename index-wisdom.xml, report id
"index-wisdom" in .agentflow/config.yaml). Exit code 1 if any check fails.

Checks (classname index.wisdom):
  1. wisdom section sits between doctrine and oracle sections
  2. wisdom section contains exactly six quotes (blockquotes)
  3. wisdom section quotes are pairwise distinct
  4. wisdom section follows eyebrow heading pattern (section-heading, p over h2)
  5. wisdom section uses reveal animation
  6. wisdom section is styled in assets/css/main.css
  7. sarcastic wisdom title present
"""

import os
import re
import sys
from xml.sax.saxutils import escape, quoteattr

CLASSNAME = "index.wisdom"

failures = []


def section_tag(html, sec_id):
    idx = html.find('id="%s"' % sec_id)
    if idx == -1:
        return None, -1
    start = html.rfind("<section", 0, idx)
    if start == -1:
        return None, idx
    end = html.find(">", idx)
    return html[start : end + 1], idx


def read(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        failures.append("%s: unreadable (%s)" % (path, exc))
        return ""


def main():
    html = read("layouts/index.html")
    css = read("assets/css/main.css")
    md = read("content/_index.md")

    results = []

    def check(name, ok, detail):
        results.append((name, bool(ok), detail))
        if not ok:
            failures.append("%s: %s" % (name, detail))

    # 1. Section presence and position between doctrine and oracle.
    _, doctrine_idx = section_tag(html, "doctrine")
    _, oracle_idx = section_tag(html, "oracle")
    wisdom_tag, wisdom_idx = section_tag(html, "wisdom")
    check(
        "wisdom section sits between doctrine and oracle sections",
        wisdom_idx != -1 and doctrine_idx != -1 and oracle_idx != -1
        and doctrine_idx < wisdom_idx < oracle_idx,
        "layouts/index.html must contain a wisdom section after #doctrine and before #oracle",
    )

    # Extract the full wisdom section body for structural checks.
    wisdom_body = ""
    if wisdom_idx != -1:
        close = html.find("</section>", wisdom_idx)
        if close != -1:
            wisdom_body = html[wisdom_idx:close]

    # 2. Exactly six quotes, wrapped in <blockquote>.
    quotes = re.findall(r"<blockquote\b[^>]*>(.*?)</blockquote>", wisdom_body, re.S)
    check(
        "wisdom section contains exactly six quotes",
        len(quotes) == 6,
        "expected exactly 6 <blockquote> quotes in the wisdom section, found %d" % len(quotes),
    )

    # 3. Quotes pairwise distinct after normalizing whitespace.
    normalized = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", q)).strip().lower() for q in quotes]
    check(
        "wisdom section quotes are pairwise distinct",
        len(normalized) == 6 and len(set(normalized)) == 6,
        "quote texts must be pairwise distinct",
    )

    # 4. Eyebrow heading pattern: section-heading header with <p> before <h2>.
    header = re.search(r'<header\b[^>]*class="[^"]*section-heading[^"]*"[^>]*>(.*?)</header>', wisdom_body, re.S)
    eyebrow_ok = False
    if header:
        p_idx = header.group(1).find("<p")
        h2_idx = re.search(r"<h2\b", header.group(1))
        eyebrow_ok = p_idx != -1 and h2_idx is not None and p_idx < h2_idx.start()
    check(
        "wisdom section follows eyebrow heading pattern",
        eyebrow_ok,
        'wisdom section needs <header class="section-heading"> with a <p> label before the <h2>',
    )

    # 5. Reveal animation, consistent with the other sections.
    check(
        "wisdom section uses reveal animation",
        bool(wisdom_tag) and re.search(r'class="[^"]*\breveal\b[^"]*"', wisdom_tag) is not None,
        'wisdom <section> tag must carry the reveal class like the other sections',
    )

    # 6. Styled in main.css (.wisdom selector).
    check(
        "wisdom section is styled in main.css",
        re.search(r"\.wisdom[\s,{.:>\[]", css) is not None,
        "assets/css/main.css must contain .wisdom style rules",
    )

    # 7. Title present (layout or content).
    check(
        "sarcastic wisdom title present",
        re.search(r"sarcastic wisdom", html + md, re.I) is not None,
        'the section title "Sarcastic wisdom" must appear in the layout or content',
    )

    # JUnit report into AGENTFLOW_REPORT_DIR.
    report_dir = os.environ.get("AGENTFLOW_REPORT_DIR")
    if report_dir:
        cases_xml = []
        for name, ok, detail in results:
            if ok:
                cases_xml.append(
                    '  <testcase classname=%s name=%s/>' % (quoteattr(CLASSNAME), quoteattr(name))
                )
            else:
                cases_xml.append(
                    '  <testcase classname=%s name=%s><failure type="AssertionError" message=%s>%s</failure></testcase>'
                    % (quoteattr(CLASSNAME), quoteattr(name), quoteattr(detail), escape(detail))
                )
        n_fail = sum(1 for _, ok, _ in results if not ok)
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<testsuite name="tellyguru.index-wisdom" tests="%d" failures="%d" errors="0" skipped="0">\n'
            "%s\n</testsuite>\n" % (len(results), n_fail, "\n".join(cases_xml))
        )
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "index-wisdom.xml"), "w", encoding="utf-8") as fh:
            fh.write(xml)

    if failures:
        sys.stderr.write("index-wisdom verification FAILED:\n- " + "\n- ".join(failures) + "\n")
        return 1
    sys.stdout.write("index-wisdom verification passed (%d checks)\n" % len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
