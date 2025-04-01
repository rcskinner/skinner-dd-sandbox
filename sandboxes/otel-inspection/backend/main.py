from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace.status import Status, StatusCode
from typing import List, Dict, Any, Callable, Awaitable
from contextlib import asynccontextmanager
import json
import functools
import time

class MemorySpanExporter(SpanExporter):
    def __init__(self):
        self.spans: List[Dict[str, Any]] = []
    
    def export(self, spans: List[Any], timeout_millis: float = None) -> bool:
        for span in spans:
            # Convert span to dict format
            span_dict = {
                "name": span.name,
                "context": {
                    "trace_id": format(span.context.trace_id, '032x'),
                    "span_id": format(span.context.span_id, '016x'),
                    "trace_state": str(span.context.trace_state),
                },
                "kind": str(span.kind),
                "parent_id": format(span.parent.span_id, '016x') if span.parent else None,
                "start_time": span.start_time,  # Keep as integer timestamp
                "end_time": span.end_time,      # Keep as integer timestamp
                "status": {
                    "status_code": str(span.status.status_code),
                    "description": span.status.description,
                },
                "attributes": dict(span.attributes),
                "events": [
                    {
                        "name": event.name,
                        "timestamp": event.timestamp,  # Keep as integer timestamp
                        "attributes": dict(event.attributes),
                    }
                    for event in span.events
                ],
                "links": [],
                "resource": {
                    "attributes": dict(span.resource.attributes),
                    "schema_url": span.resource.schema_url,
                }
            }
            self.spans.append(span_dict)
        return True
    
    def shutdown(self) -> None:
        pass
    
    def force_flush(self, timeout_millis: float = None) -> bool:
        return True

@asynccontextmanager
async def request_spans():
    # Create a new MemorySpanExporter for this request
    memory_exporter = MemorySpanExporter()
    span_processor = SimpleSpanProcessor(memory_exporter)
    
    # Add the processor to the tracer provider
    tracer_provider = trace.get_tracer_provider()
    tracer_provider.add_span_processor(span_processor)
    
    try:
        yield memory_exporter
    finally:
        # Force flush any remaining spans
        span_processor.force_flush()
        # Shutdown the processor
        span_processor.shutdown()

def with_request_spans(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with request_spans() as memory_exporter:
            # Execute the endpoint function
            response = await func(*args, **kwargs)
            
            # If the response is a dict, add the spans to it
            if isinstance(response, dict):
                response["spans"] = memory_exporter.spans
            
            return response
    
    return wrapper

# Create a resource with service information
resource = Resource.create({
    "service.name": "hello-world-service"
})

# Initialize the tracer provider
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Create FastAPI app
app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

def get_current_span_context():
    current_span = trace.get_current_span()
    ctx = current_span.get_span_context()
    return {
        "trace_id": format(ctx.trace_id, '032x'),
        "span_id": format(ctx.span_id, '016x'),
        "trace_flags": format(ctx.trace_flags, '02x'),
    }

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    trace_context = get_current_span_context()
    # Get the current span and add error information
    current_span = trace.get_current_span()
    current_span.set_status(Status(StatusCode.ERROR, str(exc)))
    current_span.record_exception(exc, attributes={
        "exception.type": type(exc).__name__,
        "exception.message": str(exc),
        "exception.escaped": "False"
    })
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "trace_context": trace_context,
            "type": type(exc).__name__
        }
    )

@app.get("/")
@with_request_spans
async def root():
    with trace.get_tracer(__name__).start_as_current_span("root_operation") as span:
        span.set_attribute("endpoint", "/")
        
        # Simulate some database operation
        with trace.get_tracer(__name__).start_as_current_span("database_operation") as db_span:
            db_span.set_attribute("operation", "fetch_user_data")
            # Simulate some work
            time.sleep(0.1)
        
        # Simulate some external API call
        with trace.get_tracer(__name__).start_as_current_span("external_api_call") as api_span:
            api_span.set_attribute("operation", "fetch_weather_data")
            api_span.set_attribute("endpoint", "https://api.weather.com")
            # Simulate some work
            time.sleep(0.2)
            
            # Add an event to the API span
            api_span.add_event("api_response_received", attributes={
                "status_code": 200,
                "response_time": 200
            })
        
        return {
            "message": "Hello World",
            "spans": [
                {"name": "root_operation", "type": "main"},
                {"name": "database_operation", "type": "database"},
                {"name": "external_api_call", "type": "api"}
            ]
        }

@app.get("/error")
@with_request_spans
async def error_endpoint():
    with trace.get_tracer(__name__).start_as_current_span("error_operation") as span:
        span.set_attribute("error_type", "test_error")
        raise Exception("This is a test error for OpenTelemetry error tracking")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="error",  # Only show errors
        access_log=False    # Disable access logs
    ) 
