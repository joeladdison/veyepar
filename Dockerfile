FROM python:3.13-bookworm AS builder

RUN mkdir /veyepar
WORKDIR /veyepar

# Optimise Python via environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
COPY setup/requirements.txt  /veyepar/
COPY setup/requirements_www.txt  /veyepar/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_www.txt

# Backend: veyepar under gunicorn.
FROM python:3.13-bookworm AS veyepar-app

# Setup non-root user
RUN useradd -m -r appuser && \
    mkdir /veyepar && \
    chown -R appuser /veyepar

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Optimise Python via environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /veyepar

# Copy the Django project to the container then finish setup
COPY --chown=appuser:appuser dj /veyepar/
RUN python3 ./manage.py collectstatic

# Switch to non-root user
USER appuser

# Expose the Django port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "dj.wsgi:application"]

# Frontend: Veyepar static content and reverse proxy.
FROM nginx:1.26-alpine AS veyepar-frontend

# Create directory and assign ownership to non-root nginx user
RUN mkdir -p /veyepar/logs && \
    chown -R nginx /veyepar

COPY setup/container/veyepar_nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=veyepar-app --chown=nginx:nginx /veyepar/static /veyepar/static
