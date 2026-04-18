from fastapi import APIRouter, File, Form, Depends

from app.service.ProductService import ProductService
from ..service.TestRideService import TestRideService
from ..service.AuthService import has_any_role

router = APIRouter(prefix="/test-rides", tags=["Test Rides"])

test_ride_service = TestRideService()

@router.post("/create-test-ride")
def create_test_ride(
    username: str = Form(...),
    bike_name: str = Form(...),
    location: str = Form(...),
    _auth: dict = Depends(has_any_role(["ROLE_USER", "ROLE_ADMIN"]))
):
    return test_ride_service.create_test_ride(username, bike_name, location)
@router.get("/get-test-ride/{username}")
def get_test_ride_by_username(username: str, _auth: dict = Depends(has_any_role([ "ROLE_ADMIN", "ROLE_USER"]))):
    print(f"Getting test ride for username: {username}")
    return test_ride_service.get_test_ride_by_username(username)

@router.get("/get-all-test-rides")
def get_all_test_rides(_auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))):
    print("Getting all test rides")
    return test_ride_service.get_all_test_rides()

@router.get("/get-test-rides-by-location/{location}")
def get_test_ride_by_location(location: str, _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))):
    print(f"Getting test rides for location: {location}")
    return test_ride_service.get_test_ride_by_location(location)

@router.delete("/delete-test-ride/{username}")
def delete_test_ride(username: str, _auth: dict = Depends(has_any_role(["ROLE_ADMIN","ROLE_USER"]))):
    print(f"Deleting test ride for username: {username}")
    return test_ride_service.delete_test_ride(username)