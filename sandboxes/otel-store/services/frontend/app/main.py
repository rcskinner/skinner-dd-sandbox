from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests

# Initialize FastAPI app
app = FastAPI(title="Order System Frontend")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

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
    
    # Call inventory service (OpenTelemetry)
    try:
        response = requests.post(
            "http://inventory-service.otel-store.svc.cluster.local/api/v1/inventory",
            json=order_data,
            verify=False,
            timeout=3
        )
        inventory_result = response.json()
    except Exception as e:
        raise Exception(f"Error connecting to inventory service: {str(e)}")
    
    return templates.TemplateResponse(
        "order_result.html",
        {
            "request": request,
            "order": inventory_result,
            "title": "Order Result"
        }
    ) 