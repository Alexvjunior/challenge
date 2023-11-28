# Challenge API

API Challenge

## **Requiriments**
- Docker

## **Setup**

1. Clone the repository.

2. Navigate to the project directory:
```bash
cd challenge
```

3. Build the Docker images:
```bash
docker-compose build
docker-compose up -d
```
Or
```bash
make run
```


## **Code Quality and Security**

To ensure code quality and enhance security, the following tools are integrated into the project:

### isort

[isort](https://pycqa.github.io/isort/) is a Python utility that sorts imports alphabetically and automatically separates them into sections.

To run isort and automatically format your imports, use the following command:

```bash
isort .
```


### flake8

flake8 is a code linter that checks Python code for style and programming errors.

To run flake8 and check your code, use the following command:
```bash
flake8 apps
```
Or
```bash
make lint
```

### safety

safety is a command-line tool that checks your Python dependencies for known security vulnerabilities.

To run safety and check for vulnerabilities, use the following command:
```bash
safety check
or
make security
```


## **Swagger API Documentation**

The project includes Swagger for API documentation. After starting the containers, you can access the Swagger UI at [http://localhost:8080/docs/](http://localhost:8080/docs/) or [http://localhost:8080/redoc/](http://localhost:8080/redoc/).

## **Available Makefile Commands**
The project includes a Makefile with several useful commands:

- make lint: Run flake8 for linting the code.
- make security: Perform a security check on the project dependencies using Safety.
- make run: Run the application using docker compose.
- make clean: Clean up the project by removing the virtual environment and cached files.


## **API Endpoints**

### Endpoint 1: `/role/{role_id}`

#### Método HTTP:
`GET`


### Response
`200`
```json
{
  "id": 0,
  "description": "string"
}
```
`422`
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
`404`
```json
{
  "detail": "Role not found"
}
```

### Endpoint 2: `/users/`

#### Método HTTP:
`POST`

### Payload
```json
{
  "name": "string",
  "email": "string",
  "role_id": 0,
  "password": "string"
}
```


### Response

`200`
```json
{
  "name": "string",
  "email": "string",
  "role_id": 0,
  "password": "string"
}
```
`400`
```json
{
  "detail": "Role not found"
}
```
`422`
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## **License**

This project is licensed under the [MIT License](LICENSE).