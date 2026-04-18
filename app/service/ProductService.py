import shutil
from decimal import Decimal, InvalidOperation
from pathlib import Path
from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db_session
from ..models.Products import Product

class ProductService:
    def __init__(self, upload_dir: str = "ProductImage"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    def create_product(self, file: UploadFile, product_name: str, product_price: str) -> dict:
        file_path = self._save_image(file)
        price = self._parse_price(product_price)
        product = Product(
            product_name=product_name,
            product_price=price,
            product_image=str(file_path),
        )
        print(f"Creating product: {product_name} with price: {price} and image path: {file_path}")
        self._save_product(product)
        return {
            "message": "Product created successfully",
            "product_name": product_name,
            "product_price": str(price),
            "product_image_url": str(file_path),
        }

    def get_all_products(self) -> List[dict]:
        db: Session = get_db_session()
        try:
            products = db.query(Product).all()
            return [self._serialize_product(product) for product in products]
        finally:
            db.close()

    def get_product_by_name(self, product_name: str) -> Optional[dict]:
        db: Session = get_db_session()
        try:
            product = db.query(Product).filter(Product.product_name == product_name).first()
            return self._serialize_product(product) if product else None
        finally:
            db.close()

    def _save_image(self, file: UploadFile) -> Path:
        destination = self.upload_dir / file.filename
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return destination

    def _parse_price(self, price: str) -> Decimal:
        try:
            return Decimal(price)
        except (InvalidOperation, ValueError):
            raise ValueError("product_price must be a valid number")

    def _save_product(self, product: Product) -> None:
        db: Session = get_db_session()
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def _serialize_product(self, product: Product) -> dict:
        return {
            "id": product.id,
            "product_name": product.product_name,
            "product_price": str(product.product_price),
            "product_image": product.product_image,
        }