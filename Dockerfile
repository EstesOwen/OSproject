FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir numpy

COPY cpu.py memory.py io_test.py main.py idkhowelsetofixthis.txt ./

CMD ["sh", "-c", "python3 main.py < idkhowelsetofixthis.txt"]