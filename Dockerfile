FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir numpy

COPY cpu.py better_memory.py io.py ./

CMD ["sh", "-c", "python cpu.py && python io.py && python better_memory.py"]