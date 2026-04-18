import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from decimal import Decimal
from app.service.ProductService import ProductService
from app.models.Products import Product

class TestProductService:
    @pytest.fixture
    def product_service(self):
        return ProductService(upload_dir="test_images")

    @patch('app.service.ProductService.get_db_session')
    def test_create_product(self, mock_get_db, product_service):
        # Mock file upload
        mock_file = Mock()
        mock_file.filename = "test_image.jpg"
        mock_file.file = Mock()

        # Mock database session
        mock_db = Mock()
        mock_get_db.return_value = mock_db

        # Mock product save
        with patch.object(product_service, '_save_image', return_value=Path("test_images/test_image.jpg")) as mock_save_image, \
             patch.object(product_service, '_parse_price', return_value=Decimal('100.00')) as mock_parse_price, \
             patch.object(product_service, '_save_product') as mock_save_product:

            result = product_service.create_product(mock_file, "Test Product", "100.00")

            assert result == {
                "message": "Product created successfully",
                "product_name": "Test Product",
                "product_price": "100.00",
                "product_image_url": "test_images/test_image.jpg",
            }
            mock_save_image.assert_called_once_with(mock_file)
            mock_parse_price.assert_called_once_with("100.00")
            mock_save_product.assert_called_once()

    @patch('app.service.ProductService.get_db_session')
    def test_get_all_products(self, mock_get_db, product_service):
        mock_db = Mock()
        mock_get_db.return_value = mock_db

        mock_product = Mock()
        mock_product.id = 1
        mock_product.product_name = "Test Product"
        mock_product.product_price = Decimal('50.00')
        mock_product.product_image = "image.jpg"

        mock_db.query.return_value.all.return_value = [mock_product]

        with patch.object(product_service, '_serialize_product', return_value={"id": 1, "product_name": "Test Product", "product_price": "50.00", "product_image": "image.jpg"}) as mock_serialize:
            result = product_service.get_all_products()

            assert result == [{"id": 1, "product_name": "Test Product", "product_price": "50.00", "product_image": "image.jpg"}]
            mock_serialize.assert_called_once_with(mock_product)

    @patch('app.service.ProductService.get_db_session')
    def test_get_product_by_name_found(self, mock_get_db, product_service):
        mock_db = Mock()
        mock_get_db.return_value = mock_db

        mock_product = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product

        with patch.object(product_service, '_serialize_product', return_value={"id": 1, "product_name": "Test Product"}) as mock_serialize:
            result = product_service.get_product_by_name("Test Product")

            assert result == {"id": 1, "product_name": "Test Product"}
            mock_serialize.assert_called_once_with(mock_product)

    @patch('app.service.ProductService.get_db_session')
    def test_get_product_by_name_not_found(self, mock_get_db, product_service):
        mock_db = Mock()
        mock_get_db.return_value = mock_db

        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = product_service.get_product_by_name("Nonexistent Product")

        assert result is None

    def test_parse_price_valid(self, product_service):
        result = product_service._parse_price("123.45")
        assert result == Decimal('123.45')

    def test_parse_price_invalid(self, product_service):
        with pytest.raises(ValueError, match="product_price must be a valid number"):
            product_service._parse_price("invalid")

    @patch('app.service.ProductService.get_db_session')
    def test_save_product(self, mock_get_db, product_service):
        mock_db = Mock()
        mock_get_db.return_value = mock_db

        mock_product = Mock()

        product_service._save_product(mock_product)

        mock_db.add.assert_called_once_with(mock_product)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_product)

    @patch('app.service.ProductService.get_db_session')
    def test_save_product_rollback_on_error(self, mock_get_db, product_service):
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        mock_db.commit.side_effect = Exception("DB Error")

        mock_product = Mock()

        with pytest.raises(Exception, match="DB Error"):
            product_service._save_product(mock_product)

        mock_db.rollback.assert_called_once()

    def test_serialize_product(self, product_service):
        mock_product = Mock()
        mock_product.id = 1
        mock_product.product_name = "Test"
        mock_product.product_price = Decimal('10.00')
        mock_product.product_image = "img.jpg"

        result = product_service._serialize_product(mock_product)

        expected = {
            "id": 1,
            "product_name": "Test",
            "product_price": "10.00",
            "product_image": "img.jpg",
        }
        assert result == expected