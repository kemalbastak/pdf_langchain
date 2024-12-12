# PDF Chat API

This is a FastAPI-based backend service designed to handle PDF file uploads, store their data in a PostgreSQL database,
and provide AI-generated responses. Additionally, it logs interactions and events in Elasticsearch for easy retrieval
and monitoring. PDF files are stored in **MinIO** for object storage.

## Architecture

- **FastAPI**: Used as the backend service.
- **PostgreSQL**: Storing PDF data and AI-generated responses.
- **Elasticsearch**: Used for storing logs created by the backend service.
- **Kibana**: A search and analytics engine used for storing logs created by the backend service.
- **MinIO**: An object storage service used to store uploaded PDF files.

## Features

- Upload PDF files and store their metadata in PostgreSQL.
- Store PDF text as cleaned plain text.
- Generate AI responses based on PDF content and store these responses in PostgreSQL.
- Log interactions with Elasticsearch for monitoring and analysis.
- Store PDF files in MinIO for scalable object storage.
- Efficient and asynchronous processing of requests.

## Setup

### Prerequisites

- Docker and Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kemalbastak/pdf_langchain.git
    cd pdf_langchain
    ```

2. Set up environment variables:
    - Copy the `.dev.env` file to `.env` for development settings:

      ```bash
      cp dev.env .env
      ```

    - Make sure to update values for the environment variables in the `.env` file, especially the following:

        ```
        DATABASE_URL=postgresql://user:password@localhost/dbname
        ELASTICSEARCH_URL=http://localhost:9200
        MINIO_URL=http://localhost:9000
        MINIO_ACCESS_KEY=minioaccesskey
        MINIO_SECRET_KEY=miniosecretkey
        ```

3. Set up Docker containers:

   The project uses Docker Compose to set up the environment. Run the following command to build and start the services:

    ```bash
    docker-compose up --build -d
    ```
4. Access the MinIO admin console:

   Open your browser and navigate to the MinIO admin console at `http://localhost:9000`. Log in using the credentials
   specified in the `.env` file:

    ```
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin
    ```

5. Create a MinIO bucket:

    - Once logged in, navigate to the **Buckets** section in the MinIO admin console.
    - Click **Create Bucket** and enter the name `pdf-bucket` (or the value specified in `MINIO_BUCKET_NAME` in your
      `.env` file).
    - Save the bucket configuration.

6. Generate access and secret keys (optional):

   If you want to generate new access and secret keys, navigate to the **Access Keys** section in the MinIO console and
   create a new set of credentials. Update the `.env` file with these keys:

    ```
    MINIO_ACCESS_KEY=new-access-key
    MINIO_SECRET_KEY=new-secret-key
    ```

## Usage

- **Upload a PDF**:
  Send a `POST` request to `/pdf/` with a PDF file. The file will be stored in the PostgreSQL database and MinIO.

  Example request (using `curl`):

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/pdf/' \
      -F 'file=@/path/to/your/file.pdf'
    ```
  
    Example response:
  ```json
    {"pdf_id": "unique_pdf_identifier"}
    ```

  - **Get AI response**:
    Send a `GET` request to `/pdf/{pdf_id}/` to retrieve the AI-generated response for a specific PDF.

    Example request:

      ```bash
      curl -X 'GET' 'http://localhost:8000/v1/chat/pdf_id:UUID/'
      ```

    Example response:
      ```json
    {"response": "The main topic of this PDF is..."}
    ```

## Logs

- Logs are stored in Elasticsearch and can be queried for monitoring or troubleshooting purposes.
- Example log query in Elasticsearch:

    ```bash
    curl -X GET "localhost:9200/your_index/_search?q=error"
    ```

## Development

### Running the Tests

To run the tests, use `pytest`:

```bash
pytest
