from db import ArtKartDB as db
from bson.objectid import ObjectId

class UserModel:
    def __init__(self):
        self.collection = db['users']

        self.schema = {
            "first_name": str,
            "last_name": str,
            "dob": str,
            "username": str,
            "email": str,
            "password": str,
            
        }
    def _validate_user(self, data, partial=False):
        """
        Validate the user data against the schema.
        If partial=True, allow partial updates.
        """
        for key, value_type in self.schema.items():
            if key in data:
                if not isinstance(data[key], value_type):
                    return False,key
            elif not partial:  # For full validation, ensure all keys are present
                return False, key
        return True, None
    
    def create_user(self, user):
        print(user)
        is_valid, key = self._validate_user(user)   
        if not is_valid:
            return False, f"Invalid user data structure. Invalid {key} value"
        return True, self.collection.insert_one(user).inserted_id

    def get_user_by_id(self, user_id):
        """
        Retrieve a user document by its ID.
        """
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def get_user_by_username(self, username):
        """
        !todo: Remove this once the authentication system is in place.
        We are retrieving user using email too
        """
        if '@' in username:
            return self.collection.find_one({"email": username})
        return self.collection.find_one({"username": username})
    
    def update_user(self, user_id, update_data):
        """
        Update a user's information.
        Validates the update_data against the schema.
        """
        if not self._validate_user(update_data, partial=True):
            raise ValueError("Invalid update data structure.")
        
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        ).modified_count

    def delete_user(self, user_id):
        """
        Delete a user document by its ID.
        """
        return self.collection.delete_one({"_id": ObjectId(user_id)}).deleted_count

    def get_all_users(self):
        """
        Retrieve all user documents.
        """
        return list(self.collection.find())
