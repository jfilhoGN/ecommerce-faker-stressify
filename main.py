from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from database.database import initialize_data
from routes import products, users, orders, status

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_data()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(status.router)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
        <head>
            <title>Welcome to the Ecommerce API Faker - Stressify.jl</title>
        </head>
        <body>
            <h1>Welcome to the Ecommerce API Faker!</h1>
            <p>Explore our endpoints:</p>
            <ul>
                <li><a href="/docs">Documentation</a></li>
                <li><a href="/products">Products</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/metrics", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content="""
    <html>
        <head>
            <title>Machine Status</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Machine Status</h1>
            <canvas id="myChart"></canvas>
            <script>
                var ctx = document.getElementById('myChart').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['CPU', 'Memory', 'Disk'],
                        datasets: [{
                            label: 'Usage',
                            data: [],
                            backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)'],
                            borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });

                function updateChart() {
                    fetch('/api/status')
                        .then(response => response.json())
                        .then(data => {
                            myChart.data.datasets[0].data = [data['CPU Usage'], data['Memory'], data['Disk']];
                            myChart.update();
                        });
                }

                // Primeira atualização imediata
                updateChart();
                // Atualizações subsequentes a cada 5 segundos
                setInterval(updateChart, 5000);
            </script>
        </body>
    </html>
    """)