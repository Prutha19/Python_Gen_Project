from app.models import Enquiry
from ..database import get_db_session


class EnquireService:
    def __init__(self):
        self.db = get_db_session()
    def create_enquiry(self,user_name:str,bike_name :str,model_name :str,location:str) -> dict:
        enquiry = Enquiry(
            user_name = user_name,
            bike_name =bike_name,
            model_name = model_name,
            location =  location,
        )
        self._save_enquiry(enquiry)
        return{"message" : "Enquiry is been made"}
    
    def get_enquiry(self,user_name:str) ->dict:
        enquiry =(
            self.db.query(Enquiry).filter(Enquiry.user_name ==user_name).first()

        )
        if enquiry :
            return {
               "user_name": enquiry.user_name,
                "bike_name" : enquiry.bike_name,
                "model_name":enquiry.model_name,
                "location":enquiry.location,


            }
        else:
            return{"message":"Enquiry not found"}


    def get_all_enquiry(self) -> list :
        enquiries = self.db.query(Enquiry).all()
        return [
            {
                "user_name": e.user_name,
                "bike_name" :e.bike_name,
                "model_name":e.model_name,
                "location":  e.location,

            }
            for e in enquiries  
        ]    
    
    def del_enquiry(self, bike_name :str) -> dict:
        enquiry = self.db.query(Enquiry).filter(Enquiry.bike_name ==bike_name).first()

        if not enquiry:
            return {"message":"No Enquiry found"}
        
        self.db.delete(enquiry)
        self.db.commit()

        return{"message":"Enquiry deleted successfully"}
    
    def _save_enquiry(self,enquiry):
        self.db.add(enquiry)
        self.db.commit()
        self.db.refresh(enquiry)
        return enquiry


       