import ddtrace
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx

# Initialize FastAPI app
app = FastAPI(title="Order System Frontend")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Configure Datadog tracer
ddtrace.patch_all()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page showing order form"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Order System"}
    )

@app.post("/order", response_class=HTMLResponse)
async def create_order(request: Request):
    """Handle order submission"""
    form_data = await request.form()
    order_data = {
        "product": form_data.get("product"),
        "quantity": int(form_data.get("quantity", 1))
    }
    
    # Call order service (OpenTelemetry)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://order-service:8080/orders",
            json=order_data
        )
        order_result = response.json()
    
    return templates.TemplateResponse(
        "order_result.html",
        {
            "request": request,
            "order": order_result,
            "title": "Order Result"
        }
    ) 