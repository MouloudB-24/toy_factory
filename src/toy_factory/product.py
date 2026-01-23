from datetime import datetime
import logging
import random
import re
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
        self.logger = logger
        self._product_color = random.choice(Product.COLORS)
        self._status = Product.STATUS_IN_CREATED
        self._production_time = .0
        self._id = f"TOY-{Product.SERIAL_NUMBER:03d}-{self._product_color.upper()}"
        self._history: List[Dict] = []
        
        self.logger.info(f"Creation du produit {self._id}.")

    def __str__(self) -> str:
        return f"{self._id} (Status: {self._status} - Production-time: {self._production_time}s)"
    
    def __repr__(self) -> str:
        return f"Product(id={self._id}, status={self._status}, Production-time={self._production_time})"
    
    def _update_production_time(self, duration: float) -> float:
        """Mettre à jour le temps total de production"""
        self._production_time += duration
        return self._production_time
    
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
    
    def add_production_step(self, station_name: str, duration: float) -> None:
        """Ajoute une étape de production à l"historique"""
        step = {
            "station": station_name,
            "start_date": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "duration": duration,
        }
        self._history.append(step)
        self._update_production_time(duration)
        self.logger.info(f"Produit {self._id} a terminé l'étape '{station_name}' en {duration}s.")


if __name__ == "__main__":
    from utils.logger import config_logging
    
    logger = config_logging()
    print("Initialisation du produit :")
    p1 = Product(logger)
    print("\nAffichger pour l'utilisateur via la méthode __str__ :")
    print(p1)
    print("\nAffichger pour le développeur via la méthode __repr__ :")
    print(p1.__repr__())
    print(f"\nDetails du produit :")
    print("     Status :", p1.get_status())
    print("     ID :", p1.get_id())
    print("     Numéro de série :", p1.get_serial_number())
    print("     Historique :", p1.get_history())
    print("     Format de l'ID ? :", p1.validate_id())
    print("\nProduit en cours de traitement :")
    p1.mark_in_progress()
    print("\nProduit déféctueux :")
    p1.mark_defective()
    print("\nProduit fini :")
    p1.mark_finished()
    print("\nStations :")
    p1.add_production_step("Assemblage", 2.3)
    p1.add_production_step("Peinture", 2.3)
    print("\nHistorique :" )
    print(p1.get_history())
    