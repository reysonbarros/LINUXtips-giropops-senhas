FROM cgr.dev/chainguard/python:latest-dev as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --user


FROM cgr.dev/chainguard/python:latest

LABEL org.opencontainers.image.authors="Reyson Barros <reysonbarros@gmail.com>" \
      stack="Python" \
      version="3.12.0"                         

COPY --from=builder /home/nonroot/.local/lib/python3.12/site-packages /home/nonroot/.local/lib/python3.12/site-packages

COPY --from=builder /home/nonroot/.local/bin  /home/nonroot/.local/bin

ENV PATH=$PATH:/home/nonroot/.local/bin

COPY app.py .

COPY templates/ templates/

COPY static/ static/

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]

