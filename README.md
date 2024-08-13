# Library App :books:

Project based on the awesome course [FastAPI do Zero](https://fastapidozero.dunossauro.com/).

## Requirements / tools used
- Python 3.12
- Poetry
- FastAPI
- SQLAlchemy
- PostgreSQL (to do)
- Docker (to do)
- Vue (in progress)

## fastapi

### Project Setup
```sh
poetry install
poetry shell
```
#### Run tests
See the tests and run.
```sh
task test
```
#### Compile and Hot-Reload for Development
```sh
task run
```

## vue

### Project Setup
```sh
cd vue
npm install
```
#### Using test data
Use to preview the frontend without the need of the backend data.
```sh
npm run serve-data
```
Books and Authors List are created on Endpoints: https://localhost:3000/books and https://localhost:3000/authors.

#### Compile and Hot-Reload for Development
```sh
npm run dev
```
Click on 'Buscar' on Livros or Romancistas page to see the test data.