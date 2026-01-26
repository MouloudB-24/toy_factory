from collections import deque
from enum import Enum
import logging
import random

from toy_factory.product import Product


class StationState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    PROCESSING = "processing"
    BROKEN = "broken"


class Station:
    """Represente une étape de fabrication dans l'usine (ex: Assemblage)"""
    
    def __init__(self, logger: logging.Logger, name: str, average_time: float) -> None:
        self.logger = logger
        self.name = name
        self.average_time = average_time
        self.state = StationState.IDLE
        
        # File d'attente
        self.queue = deque() # ajouter/retirer des items rapidement au début/fin
        
        # Etat courant
        self.current_product = None
        self.initial_processing_time = 0.0
        self.processing_remaining = 0.0
        
        # Pannes
        self.breakdown_remaining = 0.0
        self.proba_breakdown = 0.05
        self.min_breakdown_duration = 5
        self.max_breakdown_duration = 10
        
        self.logger.info(f"Station '{self.name}' créée")
    
    def add_product(self, product: object) -> None:
        if isinstance(product, Product):
            self.queue.append(product)
            if self.state == StationState.IDLE:
                self._set_state(StationState.WAITING)
            self.logger.info(f"Le {product.get_id()} est ajouté à la file d'attente de la station '{self.name}'.")
    
    def try_start_processing(self) -> bool:
        """
        Essaie de démarrer un traitement.
        """
        # Verifier l'etat de la station et la file d'attente
        if self.state != StationState.WAITING or not self.queue:
            return False
        
        # Vérifier panne aléatoire
        if random.random() < self.proba_breakdown:
            self._trigger_breakdown()
            return False
        
        self._start_processing()
        return True
    
    def update(self, delta_time: float):
        """Fait avancer le temps."""
        
        if self.state == StationState.BROKEN:
            self.breakdown_remaining -= delta_time
            if self.breakdown_remaining <= 0:
                self._repair()
            
        elif self.state == StationState.PROCESSING:
            self.processing_remaining -= delta_time
            if self.processing_remaining <= 0:
                self._finish_processing()
    
    def _set_state(self, new_state: StationState) -> None:
        """
        Change l'état et logge la transition.
        """
        if self.state != new_state:
            self.state = new_state
            self.logger.info(f"Station {self.name}: {self.state}")
    
    def _initialize_state(self) -> None:
        if self.queue:
            self._set_state(StationState.WAITING)
        else:
            self._set_state(StationState.IDLE)
                      
    def _start_processing(self) -> None:
        """
        Demarre le traitement d'un produit.
        """
        self.current_product = self.queue.popleft()
        self.initial_processing_time = round(random.uniform(self.average_time * 0.5, self.average_time * 1.5), 2)
        self.processing_remaining = self.initial_processing_time
        self._set_state(StationState.PROCESSING)
        
        self.logger.info(f"Le produit {self.current_product.get_id()} est en cours de traitement dans la station '{self.name}'.")
    
    def _trigger_breakdown(self) -> None:
       """
       Déclencher une panne de la station.
       """
       self.breakdown_remaining = round(random.uniform(self.min_breakdown_duration, self.max_breakdown_duration), 2)
       self._set_state(StationState.BROKEN)
       
       self.logger.critical(f"La station {self.name} est en panne!")
       
    def _repair(self) -> None:
        """
        Répare la station après une panne.
        """
        self.breakdown_remaining = 0.0
        self._initialize_state()
        
        self.logger.info(f"La station {self.name} a été réparée.")
    
    def _finish_processing(self) -> None:
        """
        Termine le traitement du produit en cours.
        """
        self.processing_remaining = 0.0
        self.current_product.add_production_step(self.name, self.initial_processing_time)
        self.logger.info(f"Le traitement du produit {self.current_product.get_id()} est terminé.")
        self.current_product = None
        self._initialize_state()
    
    
    
    
if __name__ == "__main__":
    from utils.logger import config_logging
    
    logger = config_logging()
    # Créer un produit et une station
    # product = Product(logger)
    station = Station(logger, "Assemblage", 2.4)
    print("\nTests attributs :")
    print("Nom de la station: ", station.name)
    print("Temps moyenne de traitement: ", station.average_time)
    print("State : ", station.state)
    print("File attente initiale : ", station.queue)
    print("Temps traitement initiale : ", station.initial_processing_time)
    print("Temps traitement restant : ", station.processing_remaining)
    print("Temps panne restant : ", station.breakdown_remaining)
    print("proba panne : ", station.proba_breakdown)
    
    print("\nTests methodes :")
    station.add_product(None)
    print("State : ", station.state)
    print("File attente : ", station.queue)
    
    print("\ntry_start_processing")
    station.try_start_processing()
    print("State : ", station.state)
    print("File attente initiale : ", station.queue)
    print("Temps traitement du produit : ", station.initial_processing_time)
    print("Temps traitement restant : ", station.processing_remaining)
    print("Temps panne restant : ", station.breakdown_remaining)
    print("proba panne : ", station.proba_breakdown)
    
    print("Avancer le traitement:")
    station.update(1)
    print("Temps traitement restant : ", station.processing_remaining)
    station.update(1)
    print("Temps traitement restant : ", station.processing_remaining)
    station.update(1)
    print("Temps traitement restant : ", station.processing_remaining)
    # print(product.get_history())
    
    
    
    
    
    
    
    
    
    
    #  def get_name(self) -> str:
    #         return self.name
        
    # def get_average_time(self) -> float:
    #     return self.average_time
    
    # def get_queue(self) -> List:
    #     return list(self.queue)
       
   
