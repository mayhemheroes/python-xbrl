FROM python:3.8-bullseye
RUN pip3 install atheris

COPY . /python-xbrl
WORKDIR /python-xbrl
RUN python3 -m pip install . && chmod +x fuzz/xbrl_parse_fuzz.py

ENTRYPOINT [ ]
CMD ["/python-xbrl/fuzz/xbrl_parse_fuzz.py"]