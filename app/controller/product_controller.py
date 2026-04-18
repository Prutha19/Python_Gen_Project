from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from ..service.ProductService import ProductService
from ..service.AuthService import has_any_role

router = APIRouter(prefix="/products", tags=["Products"])

product_service = ProductService()

@router.post("/upload")
def upload_product(
    file: UploadFile = File(...),
    product_name: str = Form(...),
    product_price: str = Form(...),
    _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))
):
    print(f"Uploading product: {product_name} with price: {product_price}")
    return product_service.create_product(file, product_name, product_price)


@router.get("/get-product")
def get_all_products(_auth: dict = Depends(has_any_role(["ROLE_USER", "ROLE_ADMIN"]))):
    print("Fetching all products")
    return product_service.get_all_products()

@router.get("/search/{product_name}")
def get_product_by_name(product_name: str, _auth: dict = Depends(has_any_role(["ROLE_USER", "ROLE_ADMIN"]))):
    print(f"Searching for product: {product_name}")
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
    _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))
):
    print(f"Updating product with ID: {product_id}")
    return product_service.update_product(
        product_id,
        file=file,
        product_name=product_name,
        product_price=product_price
    )

@router.delete("/{product_id}")
def delete_product(product_id: int, _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))):
    print(f"Deleting product with ID: {product_id}")
    return product_service.delete_product(product_id)
