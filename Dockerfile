# Stage 1: Build the React frontend
FROM node:20-slim as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build the FastAPI backend
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY api/ ./api
COPY core/ ./core
COPY db/ ./db
COPY model/ ./model
COPY utils/ ./utils
COPY alembic/ ./alembic
COPY alembic.ini .

# Copy built frontend from Stage 1
COPY --from=frontend-build /app/frontend/dist ./static

# Expose port
EXPOSE 8001

# Start the application
# Note: In production, we'd use a server to serve the static frontend
# For now, we'll keep the decoupled orchestration in docker-compose
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
