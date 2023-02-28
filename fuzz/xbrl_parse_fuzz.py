#!/usr/local/bin/python3
import atheris
import sys
import io
import os

# with atheris.instrument_imports():
from xbrl import XBRLParser
from xbrl.xbrl import XBRLParserException

@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    in_string = fdp.ConsumeUnicodeNoSurrogates(len(data))
    xbrl_parser = XBRLParser()
    try:
        xbrl = xbrl_parser.parse(io.StringIO(in_string))
        xbrl_parser.parseGAAP(xbrl)
    except XBRLParserException:
        pass
        
        
atheris.Setup(sys.argv, TestOneInput)
atheris.instrument_all()
atheris.Fuzz()