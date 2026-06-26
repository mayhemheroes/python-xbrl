#!/usr/bin/env python3
# NOTE: this file MUST stay executable (mode 0755). Mayhem runs libFuzzer in FORK mode, where the
# engine re-launches itself for every job via sys.argv[0]. The ELF launcher exec's `python3
# fuzz_parsers.py`, so sys.argv[0] becomes THIS script's path; libFuzzer then re-execs it directly
# (effectively `sh -c "/mayhem/mayhem/fuzz_parsers.py ..."`). If the file is not executable that
# re-exec fails with EACCES, every fork child dies before running a single input, and Mayhem records
# 0 edges (the fuzzer still "runs" for the full budget, just relaunching dead workers). chmod +x.
import atheris
import sys
import fuzz_helpers

# Bare instrument_imports(): instrument the xbrl wrapper AND every parsing backend it
# pulls in transitively (bs4, marshmallow, six, ...). Using include=['xbrl'] only
# instruments the thin wrapper, leaving the real parsing edges uninstrumented -> ~0 new
# coverage. Nothing that pulls in the backend is imported before this block, so no module
# gets cached uninstrumented.
with atheris.instrument_imports():
    import xbrl
    from xbrl.xbrl import XBRLParserException


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        parser = xbrl.XBRLParser()
        to_gaap = fdp.ConsumeBool()
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as fp:
            doc = parser.parse(fp)
            if to_gaap:
                # Auxiliary GAAP parse + serialize round-trip: guarded on its own so
                # library encoder/serializer quirks on fuzz data never abort the run.
                try:
                    gaap = parser.parseGAAP(doc)
                    xbrl.GAAPSerializer().dump(gaap)
                except Exception:
                    pass
    except (XBRLParserException, IndexError, AttributeError, ValueError, KeyError, TypeError):
        # Expected parse-domain failures on garbage input. Return instead of re-raising so
        # the fuzzer runs its full budget.
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
