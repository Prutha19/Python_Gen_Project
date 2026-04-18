import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.controller.product_controller import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

class TestProductController:
    @patch('app.controller.product_controller.product_service')
    @patch('app.controller.product_controller.has_any_role')
    def test_upload_product(self, mock_auth, mock_service):
        mock_auth.return_value = {"user": "admin"}
        mock_service.create_product.return_value = {"message": "Product created successfully"}

        response = client.post("/products/upload", data={"product_name": "Test", "product_price": "100.00"}, files={"file": ("test.jpg", b"fake image")})

        assert response.status_code == 200
        assert response.json() == {"message": "Product created successfully"}

    @patch('app.controller.product_controller.product_service')
    @patch('app.controller.product_controller.has_any_role')
    def test_get_all_products(self, mock_auth, mock_service):
        mock_auth.return_value = {"user": "user"}
        mock_service.get_all_products.return_value = [{"id": 1, "product_name": "Test"}]

        response = client.get("/products/get-product")

        assert response.status_code == 200
        assert response.json() == [{"id": 1, "product_name": "Test"}]

    @patch('app.controller.product_controller.product_service')
    @patch('app.controller.product_controller.has_any_role')
    def test_get_product_by_name_found(self, mock_auth, mock_service):
        mock_auth.return_value = {"user": "user"}
        mock_service.get_product_by_name.return_value = {"id": 1, "product_name": "Test"}

        response = client.get("/products/search/Test")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "product_name": "Test"}

    @patch('app.controller.product_controller.product_service')
    @patch('app.controller.product_controller.has_any_role')
    def test_get_product_by_name_not_found(self, mock_auth, mock_service):
        mock_auth.return_value = {"user": "user"}
        mock_service.get_product_by_name.return_value = None

        response = client.get("/products/search/Nonexistent")

        assert response.status_code == 200
        assert response.json() == {"message": "Product not found"}