import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from apps.core.app import app  # Import the FastAPI app


# Mocking external dependencies
@pytest.fixture
def mock_pdf_service():
    mock_service = MagicMock()
    # Mock methods in PDFService that interact with the database and MinIO
    mock_service.create_pdf.return_value = MagicMock(id="pdf_id_123")
    mock_service.create_chunked_pdf.return_value = MagicMock(id="chunk_id_123")
    return mock_service


@pytest.fixture
def mock_minio_client():
    mock_client = MagicMock()
    # Mock MinIO client upload method
    mock_client.upload_object.return_value = "uploaded_file_name"
    return mock_client


@pytest.fixture
def client():
    # Return a TestClient instance for FastAPI
    return TestClient(app)


@pytest.mark.asyncio
async def test_upload_file(client, mock_pdf_service, mock_minio_client):
    # Mock the service dependency
    app.dependency_overrides[get_pdf_service] = lambda: mock_pdf_service
    app.dependency_overrides[minio_client] = mock_minio_client  # Mock MinIO client

    # Prepare the test data
    test_file = {
        "file": ("test_file.pdf", b"test content", "application/pdf"),
    }

    # Send a POST request to the /v1/pdf endpoint
    response = client.post("/v1/pdf", files=test_file)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the expected pdf_id
    assert response.json() == {"pdf_id": "pdf_id_123"}

    # Check that the mocked service methods were called as expected
    mock_pdf_service.create_pdf.assert_called_once()
    mock_pdf_service.create_chunked_pdf.assert_called_once()

    # Check that the MinIO client upload method was called
    mock_minio_client.upload_object.assert_called_once_with("test_file.pdf", b"test content")

    # Check if the PDF upload and chunk creation methods are called with the expected arguments
    mock_pdf_service.create_pdf.assert_called_with(MagicMock(path="test_file.pdf", file="test_file.pdf"))
    mock_pdf_service.create_chunked_pdf.assert_called_with("pdf_id_123", MagicMock(id="chunk_id_123"))


@pytest.mark.asyncio
async def test_upload_file_error(client, mock_pdf_service, mock_minio_client):
    # Simulate an error in the file upload process
    mock_pdf_service.create_pdf.side_effect = Exception("Database error")

    # Prepare the test data
    test_file = {
        "file": ("test_file.pdf", b"test content", "application/pdf"),
    }

    # Send a POST request to the /v1/pdf endpoint
    response = client.post("/v1/pdf", files=test_file)

    # Assert that the response status code is 500 (Internal Server Error)
    assert response.status_code == 500

    # Check if the error message matches the expected one
    assert response.json() == {"detail": "Internal server error"}

    # Check that the create_pdf method was called even though it raised an error
    mock_pdf_service.create_pdf.assert_called_once()
