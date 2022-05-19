FROM drozdetskiy/popug-system:0.0.1 as builder

COPY ./.meta /home/httpd/app/src/.meta/
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    libssl-dev \
    libxslt-dev \
    libpq-dev \
    python3-psycopg2 \
    zlib1g-dev \
    g++ \
    vim

RUN pip install --prefix=/install --no-cache-dir -r .meta/packages

FROM drozdetskiy/popug-system:0.0.1

LABEL maintainers="m.drozdetskiy@gmail.com"

COPY ./ /home/httpd/app/src/
ENV PYTHONPATH "${PYTHONPATH}:/home/httpd/app/src/src"
COPY --from=builder /install /usr/local
