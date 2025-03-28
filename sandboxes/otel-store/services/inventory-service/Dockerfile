FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/inventory-service ./cmd/main.go

# Use a smaller image for the final stage
FROM alpine:latest

WORKDIR /app

# Create non-root user
RUN adduser -D -g '' appuser

# Copy the binary from builder
COPY --from=builder /app/inventory-service .

# Set production mode
ENV GIN_MODE=release

# Expose port
EXPOSE 8080

# Switch to non-root user
USER appuser

# Run the application
CMD ["./inventory-service"] 