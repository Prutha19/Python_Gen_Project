from fastapi import APIRouter, Form, Depends
from ..service.EnquireService import EnquireService
from ..service.AuthService import has_any_role

router = APIRouter(prefix="/enquiry",tags=["Enquiry"])
enquiry = EnquireService()

@router.post("/create-enquiry")
def create_enquiry(
    user_name  : str =Form(...),
    bike_name : str= Form(...),
    model_name :str = Form(...),
    location :str = Form(...),
     _auth: dict = Depends(has_any_role(["ROLE_USER", "ROLE_ADMIN"])),
):
    return enquiry.create_enquiry(user_name, bike_name,model_name, location)

@router.get("/get-enquiry/{user_name}")
def get_enquiry_by_bike_name(
    user_name: str, _auth: dict = Depends(has_any_role(["ROLE_ADMIN", "ROLE_USER"]))
):
    print(f"Getting test ride for username: {user_name}")
    return enquiry.get_enquiry_by_username(user_name)

@router.get("/get-all-enquiries")
def get_all_enquiries(_auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))):
    print("Getting all test rides")
    return enquiry.get_all_enquiry()


@router.delete("/delete-enquiry/{bike_name}")
def delete_enquiry_by_bike(
    bike_name: str,
    _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))
):
    return enquiry.del_enquiry_by_bike_name(bike_name)