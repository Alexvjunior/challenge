# Challenge API

The main aim of this project is to develop a voice assistant platform capable of understanding and translating into multiple languages. The platform should process audio inputs, translate, and convert back to the user via Text-to-Speech (TTS) technology. This multilingual capability would cater to a diverse user base and find applications in customer service, education, and accessibility solutions. With this platform, users can communicate in their preferred language, and the system will translate and provide a real-time response, making communication more accessible and efficient in various contexts.

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

The project includes Swagger for API documentation. After starting the containers, you can access the Swagger UI at [http://localhost:8000/docs/](http://localhost:8000/docs/) or [http://localhost:8000/redoc/](http://localhost:8000/redoc/).

## **Available Makefile Commands**
The project includes a Makefile with several useful commands:

- make lint: Run flake8 for linting the code.
- make security: Perform a security check on the project dependencies using Safety.
- make run: Run the application using docker compose.
- make clean: Clean up the project by removing the virtual environment and cached files.


## **API Endpoints**

### Endpoint 1: `/`

#### Método HTTP:
`GET`


### Response
`200`


### Endpoint 2: `/translate`

#### Método HTTP:
`POST`

### Payload
```json
{
  "source_language": "string",
  "target_language": "string",
  "audio_file": <File Object>,
}
```


### Response

`200`
```json
{
  "message": "string",
}
```
`500`
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

### Endpoint 3: `/Download`

#### Método HTTP:
`GET`



### Response

`200`
```file
<File Object>
```
`500`
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