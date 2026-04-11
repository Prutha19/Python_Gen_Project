from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from ..service.ProductService import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

product_service = ProductService()

@router.post("/upload")
def upload_product(
    file: UploadFile = File(...),
    product_name: str = Form(...),
    product_price: str = Form(...)
):
    return product_service.create_product(file, product_name, product_price)

@router.get("/get-product")
def get_all_products():
    return product_service.get_all_products()

@router.get("/search/{product_name}")
def get_product_by_name(product_name: str):
    product = product_service.get_product_by_name(product_name)
    if product is None:
        return {"message": "Product not found"}
    return product

@router.put("/{product_id}")
def update_product(
    product_id: int,
    file: Optional[UploadFile] = File(None),
    product_name: Optional[str] = Form(None),
    product_price: Optional[str] = Form(None),
):
    return product_service.update_product(
        product_id,
        file=file,
        product_name=product_name,
        product_price=product_price
    )

@router.delete("/{product_id}")
def delete_product(product_id: int):
    return product_service.delete_product(product_id)
