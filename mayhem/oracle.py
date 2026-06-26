#!/usr/bin/env python3
"""Behavioral oracle (known-answer test) for python-xbrl.

Exercises the SAME parsing pipeline the fuzzer drives — XBRLParser.parse -> parseGAAP ->
GAAPSerializer().dump — on a real SEC filing shipped in the repo (tests/sam-20130629.xml) and
ASSERTS specific extracted GAAP figures (the same known answers as the upstream test
tests/test_parse.py::test_parse_GAAP10Q_RRDonnelley). A no-op / neutered program (which prints
nothing) FAILS test.sh, because the SELFTEST_PASS marker and its asserted values are only printed
when every assertion holds.
"""
import io
import os

from xbrl import XBRLParser, GAAPSerializer, XBRLParserException

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "tests", "sam-20130629.xml")
EMPTY = os.path.join(HERE, "..", "tests", "nothing.xml")

# 1) Parse a known filing and extract GAAP figures, then assert specific decoded values.
parser = XBRLParser(0)
xbrl = parser.parse(SAMPLE)
gaap = parser.parseGAAP(xbrl, "20130629", "current")
result = GAAPSerializer().dump(gaap)
assert isinstance(result, dict), type(result)

expected = {
    "liabilities": 98032.0,
    "income_tax_expense_benefit": 12107.0,
    "non_current_assets": 5417.0,
    "income_loss": 19715.0,
    "liabilities_and_equity": 60263.0,
    "operating_expenses": 65084.0,
}
for key, want in expected.items():
    got = result.get(key)
    assert got == want, "%s: got %r expected %r" % (key, got, want)

# 2) Reject clearly malformed input (an empty document must raise XBRLParserException).
try:
    parser.parse(EMPTY)
    raise SystemExit("BUG: empty input was accepted by parse")
except XBRLParserException:
    pass

print(
    "SELFTEST_PASS liabilities=%s income_tax=%s noncurrent=%s opex=%s"
    % (
        result["liabilities"],
        result["income_tax_expense_benefit"],
        result["non_current_assets"],
        result["operating_expenses"],
    )
)
