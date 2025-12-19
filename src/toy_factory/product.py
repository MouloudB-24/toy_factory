from datetime import datetime
import logging
import random
import re
import time
from typing import Dict, List

   
class Product:
    """Représente un jouet dans l'usine."""

    SERIAL_NUMBER = 0
    COLORS = ["Red", "Blue", "Green", "Yellow", "Mauve", "Orange"]
    
    STATUS_IN_CREATED = "Created"
    STATUS_IN_PROGRESS = "In_progress"
    STATUS_IN_DEFECTIVE = "Defective"
    STATUS_IN_FINISHED = "Finished"

    def __init__(self, logger: logging.Logger) -> None:
        Product.SERIAL_NUMBER += 1
        self._product_color = random.choice(Product.COLORS)
        self._status = Product.STATUS_IN_CREATED
        self._production_time = .0
        self.logger = logger
        self._id = f"TOY-{Product.SERIAL_NUMBER:03d}-{self._product_color.upper()}"
        self._history: List[Dict] = []
        
        self.logger.info(f"Début de fabrication du produit {self._id}.")

    def __str__(self) -> str:
        return f"{self._id} (Status: {self._status} - Times: {self._production_time}s)"
    
    def __repr__(self) -> str:
        return f"Product(id={self._id}, status={self._status})"
    
    def get_status(self) -> None:
        return self._status
    
    def get_id(self) -> str:
        return self._id
    
    def get_serial_number(self) -> str:
        """Extrait le numéro de serie du produit dans l'id."""
        res = re.search(r"\d{3}", self._id)
        return res.group() if res else "000"
    
    def get_history(self) -> List:
        return self._history.copy() # Retourner une copie pour éviter une modif de l'originale
    
    def validate_id(self) -> bool:
        return re.match(r"TOY-\d{3}-[A-Z]+", self._id) is not None
    
    def mark_in_progress(self) -> None:
        self._status = Product.STATUS_IN_PROGRESS
        self.logger.info(f"Produit {self._id} en cours de traitement.")
        
    def mark_defective(self) -> None:
        self._status = Product.STATUS_IN_DEFECTIVE
        self.logger.warning(f"Produit {self._id} marqué comme déféctueux.")
    
    def mark_finished(self) -> None:
        self._status = Product.STATUS_IN_FINISHED
        self.logger.info(f"Produit {self._id} marqué comme fini en {self._production_time}s")
    
    def _update_production_time(self, duration: float) -> float:
        """Mettre à jour le temps total de production"""
        self._production_time += duration
        return self._production_time
    
    def add_production_step(self, station_name: str, duration: float) -> None:
        """Ajoute une étape de production à l"historique"""
        step = {
            "timestamp": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "station": station_name,
            "duration": duration,
            "production_time": self._update_production_time(duration)
        }
        self._history.append(step)
        self.logger.info(f"Produit {self._id} a terminé l'étape {station_name.upper()} en {duration}s.")


if __name__ == "__main__":
    from utils.logger import config_logging
    
    logger = config_logging()
    p1 = Product(logger)
    print(p1)
    print(p1.__repr__())
    print(f"Details du produit :")
    print("     Status :", p1.get_status())
    print("     ID :", p1.get_id())
    print("     Numéro de série :", p1.get_serial_number())
    print("     Historique :", p1.get_history())
    print("     Format de l'ID :", p1.validate_id())
    p1.mark_in_progress()
    p1.mark_defective()
    p1.mark_finished()
    p1.add_production_step("Assemblage", 2.3)
    p1.add_production_step("Peinture", 2.3)
    print("Historique :" )
    print(p1.get_history())
    