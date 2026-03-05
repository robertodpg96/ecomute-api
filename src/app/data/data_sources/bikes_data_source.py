from typing import List, Dict, Any, Optional

BIKES: List[Dict[str, Any]] = []

# ==========================
# BIKE OPERATIONS
# ==========================
class BikesDataSource:
    def get_all_bikes(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all bikes."""
        if status is None:
            return BIKES
        return [bike for bike in BIKES if bike.get("status") == status]

    def get_bike(self, bike_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single bike by ID."""
        for bike in BIKES:
            if bike["id"] == bike_id:
                return bike
        return None

    def create_bike(self, bike_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new bike and auto-increment the ID."""
        # simple logic to find max ID + 1
        new_id = 1
        if BIKES:
            new_id = max(bike["id"] for bike in BIKES) + 1
        
        # Add ID to the new data
        new_bike = {**bike_data, "id": new_id}
        BIKES.append(new_bike)
        return new_bike

    def update_bike(self, bike_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a bike. Returns the updated bike or None if not found."""
        bike = self.get_bike(bike_id)
        if bike:
            # Update the dictionary with new values
            bike.update(update_data)
            return bike
        return None

    def delete_bike(self, bike_id: int) -> bool:
        """Delete a bike. Returns True if deleted, False if not found."""
        bike = self.get_bike(bike_id)
        if bike:
            BIKES.remove(bike)
            return True
        return False

def get_bike_datasource() -> BikesDataSource:
    return BikesDataSource()