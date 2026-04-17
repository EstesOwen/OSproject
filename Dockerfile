FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir numpy

COPY cpu.py memory.py io.py ./

CMD ["sh", "-c", "python3 cpu.py && python3 io.py && python3 memory.py"]