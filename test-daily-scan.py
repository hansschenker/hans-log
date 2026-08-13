#!/usr/bin/env python3
"""Tests for daily-scan.py — run with `python test-daily-scan.py`.

No test framework in this repo, so this is a plain script: it exits 0 when
everything passes and 1 (with the failures printed) otherwise.

The dedup cases exist because `log eod` silently loses items when the check is
wrong: an item wrongly marked "already logged" never reaches the drafts, so it
is never seen again. On 2026-08-13 a substring test skipped `js-fp` because it
occurs inside `rxjs-fp`.
"""
import importlib.util, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "daily_scan", os.path.join(SCRIPT_DIR, "daily-scan.py"))
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)

failures = []


def check(got, want, why):
    ok = got == want
    print("  %s  %-46s got %r" % ("PASS" if ok else "FAIL", why, got))
    if not ok:
        failures.append("%s — wanted %r, got %r" % (why, want, got))


SAMPLE_LOG = """
### 2026-08-13 Thu
- rxjs | rxjs-fp | rxjs-fp — from-scratch functional RxJS | RxJS/FP | https://github.com/hansschenker/rxjs-fp
- ai | ai-claude-agentic-rag | Agentic RAG — retrieval notes | AI/RAG | https://example.com
- cs | fp-combinators | crocks Combinators — helpers | FP/JavaScript | https://crocks.dev/x
- ytl | ytl-rxjs-operators | RxJS Operators Playlist — deep dives | RxJS | https://youtube.com/playlist
- yt | universal-algebra | Universal Algebra — operations & laws | Algebra/Theory | https://example.com

Prose mentioning js-fp and combinators that must not count as a logged entry.
"""


def test_logged_slugs():
    print("logged_slugs")
    slugs = ds.logged_slugs(SAMPLE_LOG)
    check(sorted(slugs), ["ai-claude-agentic-rag", "fp-combinators", "rxjs-fp",
                          "universal-algebra", "ytl-rxjs-operators"],
          "indexes the slug field of every entry line")
    check("prose mentioning js-fp and combinators" in " ".join(slugs), False,
          "ignores prose lines that are not entries")
    check(ds.logged_slugs(""), set(), "empty log yields no slugs")
    return slugs


def test_match_logged(slugs):
    print("\nmatch_logged")
    check(ds.match_logged("js-fp", slugs), "",
          "substring of rxjs-fp is not a duplicate")
    check(ds.match_logged("combinators", slugs), "",
          "hyphen-suffix of fp-combinators is not a duplicate")
    check(ds.match_logged("fp", slugs), "",
          "bare fragment is not a duplicate")
    check(ds.match_logged("rxjs", slugs), "",
          "prefix fragment of rxjs-fp is not a duplicate")
    check(ds.match_logged("rxjs-fp", slugs), "rxjs-fp",
          "exact slug is a duplicate")
    check(ds.match_logged("fp-combinators", slugs), "fp-combinators",
          "exact slug is a duplicate (second case)")
    check(ds.match_logged("universal-Algebra", slugs), "universal-algebra",
          "header case is normalised before matching")
    check(ds.match_logged("Agentic RAG", slugs), "ai-claude-agentic-rag",
          "prose header is slugified before matching")
    check(ds.match_logged("agentic-rag", slugs), "ai-claude-agentic-rag",
          "ai- provider prefix on the stored slug is tolerated")
    check(ds.match_logged("rxjs-operators", slugs), "ytl-rxjs-operators",
          "ytl- prefix on the stored slug is tolerated")
    check(ds.match_logged("from-option-to-observable", slugs), "",
          "unlogged header is new")
    check(ds.match_logged("", slugs), "", "empty header is never a duplicate")
    check(ds.match_logged("  ", slugs), "", "blank header is never a duplicate")


def test_slugify():
    print("\nslugify")
    check(ds.slugify("From Options to Observables"), "from-options-to-observables",
          "spaces become hyphens, case folded")
    check(ds.slugify("fp-monoids"), "fp-monoids", "already-slug passes through")
    check(ds.slugify("  RxJS: switchMap!  "), "rxjs-switchmap",
          "punctuation collapses, edges trimmed")


def test_parse_record():
    print("\nparse_record")
    check(ds.parse_record("fp-guide, brian lonsdorf, https://github.com/x"),
          ("fp-guide", "https://github.com/x", "brian lonsdorf"),
          "link found by pattern, not position (legacy link-last)")
    check(ds.parse_record("fp-guide, https://github.com/x, brian lonsdorf"),
          ("fp-guide", "https://github.com/x", "brian lonsdorf"),
          "standard header, link, description")
    check(ds.parse_record("from-option-to-observable, D:\\Learning-Local-Hanss\\Rxjs, Option Monad"),
          ("from-option-to-observable", "D:\\Learning-Local-Hanss\\Rxjs", "Option Monad"),
          "windows path counts as the link")
    check(ds.parse_record("fp-monoids"), ("fp-monoids", "", ""),
          "header alone parses with empty link and description")


def main():
    slugs = test_logged_slugs()
    test_match_logged(slugs)
    test_slugify()
    test_parse_record()
    print()
    if failures:
        print("%d FAILED:" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1
    print("all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
