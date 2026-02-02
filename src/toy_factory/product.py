from datetime import datetime
import logging
import random
import re
from typing import Dict, List

   
class Product:
    """Représente un produit dans l'usine."""

    SERIAL_NUMBER = 0
    COLORS = ["Red", "Blue", "Green", "Yellow", "Mauve", "Orange"]
    
    STATUS_IN_CREATED = "Created"
    STATUS_IN_PROGRESS = "In_progress"
    STATUS_IN_DEFECTIVE = "Defective"
    STATUS_IN_FINISHED = "Finished"
    STATUS_REJECTED = "Rejected"

    def __init__(self, logger: logging.Logger) -> None:
        Product.SERIAL_NUMBER += 1
        self.logger = logger
        self._product_color = random.choice(Product.COLORS)
        self._status = Product.STATUS_IN_CREATED
        self._production_time = 0
        self.retry_count = 0
        self._id = f"TOY-{Product.SERIAL_NUMBER:03d}-{self._product_color.upper()}"
        self._history: List[Dict] = []
        
        self.logger.info(f"Produit {self._id} créé")

    def __str__(self) -> str:
        return f"{self._id} (Status: {self._status} - Production-time: {self._production_time}s)"
    
    def __repr__(self) -> str:
        return f"Product(id={self._id}, status={self._status})"
    
    def get_status(self) -> str:
        return self._status
    
    def get_id(self) -> str:
        return self._id
    
    def get_serial_number(self) -> str:
        """Extrait le numéro de serie du produit dans l'id."""
        res = re.search(r"\d{3}", self._id)
        return res.group() if res else "000"
    
    def get_history(self) -> List:
        return self._history.copy() # Retourner une copie pour éviter une modif de l'originale
    
    def get_retry_count(self) -> int:
        return self.retry_count
    
    def get_production_time(self) -> float:
        return round(self._production_time, 2)
    
    def _update_production_time(self, duration: float) -> float:
        """Mettre à jour le temps total de production"""
        self._production_time += duration
        return self._production_time
    
    def validate_id(self) -> bool:
        return re.match(r"TOY-\d{3}-[A-Z]+", self._id) is not None
    
    def increment_retry(self) -> None:
        self.retry_count += 1
    
    def mark_in_progress(self) -> None:
        self._status = Product.STATUS_IN_PROGRESS
        
    def mark_defective(self) -> None:
        self._status = Product.STATUS_IN_DEFECTIVE
    
    def mark_finished(self) -> None:
        self._status = Product.STATUS_IN_FINISHED
    
    def mark_rejected(self) -> None:
        self._status = Product.STATUS_REJECTED
    
    def add_production_step(self, station_name: str, duration: float) -> None:
        """Ajoute une étape de production à l"historique"""
        step = {
            "station": station_name,
            "start_date": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "duration": duration,
        }
        self._history.append(step)
        self._update_production_time(duration)
        self.logger.debug(f"Produit {self._id} : étape {station_name} terminée (durée : {duration}s)")


if __name__ == "__main__":
    pass
    