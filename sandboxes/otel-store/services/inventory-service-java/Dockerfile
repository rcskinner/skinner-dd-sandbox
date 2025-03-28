# Build stage
FROM maven:3.9 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Download OpenTelemetry Java agent
FROM curlimages/curl:8.6.0 AS otel
WORKDIR /otel
RUN curl -L -o opentelemetry-javaagent.jar https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v1.32.1/opentelemetry-javaagent.jar

# Final stage
FROM openjdk:17-slim
WORKDIR /app

# Copy the OpenTelemetry agent
COPY --from=otel /otel/opentelemetry-javaagent.jar /app/opentelemetry-javaagent.jar

# Copy the built application
COPY --from=builder /app/target/inventory-service-1.0.0.jar /app/app.jar

# Run the application with the OpenTelemetry agent
ENTRYPOINT ["java", \
    "-javaagent:/app/opentelemetry-javaagent.jar", \
    "-jar", "/app/app.jar"] 