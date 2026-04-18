from app.models import TestRide
from ..database import get_db_session
from sqlalchemy.orm import Session
from datetime import datetime


class TestRideService:
    def __init__(self):
        self.db = get_db_session()

    def create_test_ride(self, username: str, bike_name: str, location: str) -> dict:
        test_ride = TestRide(
            username=username,
            bike_name=bike_name,
            time=datetime.now(),
            location=location,
        )
        self._save_product(test_ride)
        return {"message": "Test ride created successfully"}

    def get_test_ride_by_username(self, username: str) -> dict:
        test_ride = (
            self.db.query(TestRide).filter(TestRide.username == username).first()
        )
        if test_ride:
            return {
                "username": test_ride.username,
                "bike_name": test_ride.bike_name,
                "time": test_ride.time,
                "location": test_ride.location,
            }
        else:
            return {"message": "Test ride not found"}

    def get_all_test_rides(self) -> list:
        test_rides = self.db.query(TestRide).all()
        return [
            {
                "username": test_ride.username,
                "bike_name": test_ride.bike_name,
                "time": test_ride.time,
                "location": test_ride.location,
            }
            for test_ride in test_rides
        ]

    def get_test_ride_by_location(self, location: str) -> list:
        test_rides = self.db.query(TestRide).filter(TestRide.location == location).all()
        return [
            {
                "username": test_ride.username,
                "bike_name": test_ride.bike_name,
                "time": test_ride.time,
                "location": test_ride.location,
            }
            for test_ride in test_rides
        ]

    def delete_test_ride(self, username: str) -> dict:
        test_ride = (
            self.db.query(TestRide).filter(TestRide.username == username).first()
        )
        if test_ride:
            self.db.delete(test_ride)
            self.db.commit()
            return {"message": "Test ride deleted successfully"}
        else:
            return {"message": "Test ride not found"}

    def _save_product(self, product: TestRide) -> None:
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
