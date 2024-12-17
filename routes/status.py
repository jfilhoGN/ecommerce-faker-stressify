from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import psutil
import json
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response 

router = APIRouter()

# Métricas
cpu_usage = Gauge('system_cpu_usage', 'System CPU Usage')
memory_usage = Gauge('system_memory_usage', 'System Memory Usage')
disk_usage = Gauge('system_disk_usage', 'System Disk Usage')

@router.get("/metrics")
async def metrics():
    cpu_usage.set(psutil.cpu_percent(interval=1))
    memory = psutil.virtual_memory()
    memory_usage.set(memory.percent)
    disk = psutil.disk_usage('/')
    disk_usage.set(disk.percent)
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Mantém o endpoint JSON para outras integrações, se necessário
@router.get("/api/status")
async def get_status_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    system_info = {
        "CPU Usage": cpu_usage,
        "Memory": memory.percent,
        "Disk": disk.percent
    }
    return JSONResponse(content=system_info)