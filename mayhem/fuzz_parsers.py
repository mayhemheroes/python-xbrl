#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers
import random

with atheris.instrument_imports(include=['xbrl']):
    import xbrl


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        parser = xbrl.XBRLParser()
        to_gaap = fdp.ConsumeBool()
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as fp:
            parser.parse(fp)
            if to_gaap:
                gaap = parser.parseGAAP(xbrl)
                xbrl.GAAPSerializer().dump(gaap)
    except xbrl.XBRLParserException:
        return -1
    except (IndexError, AttributeError) as e:
        if random.random() > 0.99:
            raise e
        return 0


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
