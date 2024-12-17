# Ecommerce Faker - Stressify - FastAPI

The Ecommerce Faker API is a free software project focused on learning about performance testing. Its execution format is intuitive and can be used both locally and on servers.

## Usage

To use Ecommerce Faker you only need the latest version of docker installed, after installation just run the command `docker compose up --build`.

After the command is executed, the API will be available at:

- API: `http://localhost:8000`.
- Docs Swagger: `http://localhost:8000/docs`.
- Metrics: `http://localhost:8000/metrics`.
- Status: `http://localhost:8000/api/status`.
- Grafana: `http://localhost:3000` (user: admin, password: admin).
- Prometheus: `http://localhost:9090`.

### Endpoints

- `/status`: Returns the status of the API.
- `/products`: Returns a list of products.
- `/products/{product_id}`: Returns a product by id.
- `/users`: Returns a list of users.
- `/users/{user_id}`: Returns a user by id.
- `/orders`: Returns a list of orders.
- `/orders/{order_id}`: Returns an order by id.

## Stressify

Stressify Performance Test is a performance testing tool written in Julia, inspired by tools like K6. Its primary focus is on collecting, analyzing, and generating customizable metrics to help developers gain deeper insights into the performance of APIs under various load conditions. With Stressify, you can easily track performance indicators and extend the tool to create new metrics tailored to your needs.

This API was also created for you to practice using the Stressify.jl tool, which allows you to run your scripts in the Julia language. To learn more about the Stressify.jl tool, access the links:

- [Stressify.jl](https://github.com/jfilhoGN/Stressify.jl)
- [Documentation](https://stressifyjl.readthedocs.io/en/latest/)
- [Examples](https://github.com/jfilhoGN/Stressify.jl/tree/main/examples)
- [Community](https://app.gitter.im/#/room/#stressify:gitter.im)
- [X](https://x.com/Stressifyjl) 
