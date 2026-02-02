from collections import deque
from enum import Enum
import logging
import random
from typing import List

from src.toy_factory.product import Product


class StationState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    PROCESSING = "processing"
    BROKEN = "broken"


class Station:
    """Represente une étape de fabrication dans l'usine (ex: Assemblage)"""
    
    def __init__(self, logger: logging.Logger, station_name: str, average_time: float) -> None:
        self.logger = logger
        self.station_name = station_name
        self.average_time = average_time
        self.state = StationState.IDLE
        
        # File d'attente
        self.queue = deque() # ajouter/retirer des items rapidement au début/fin
        
        # Etat courant
        self.current_product = None
        self.initial_processing_time = 0.0
        self.processing_remaining_time = 0.0
        
        # Pannes
        self.breakdown_remaining_time = 0.0
        self.proba_breakdown = 0.05
        self.min_breakdown_duration = 5
        self.max_breakdown_duration = 10
        
        self.logger.info(f"Station {self.station_name} initialisée")
    
    def get_station_name(self) -> str:
        return self.station_name
    
    def get_station_state(self) -> str:
        return self.state
    
    def get_queue(self) -> deque:
        return self.queue.copy()
    
    def add_product(self, product: object) -> None:
        if isinstance(product, Product):
            self.queue.append(product)
            if self.state == StationState.IDLE:
                self._set_state(StationState.WAITING)
            self.logger.debug(f"Produit {product.get_id()} ajouté à la file d'attente de la station {self.station_name}")
    
    def advance_treatment(self, delta_time: float) -> List:
        """
        Fait avancer le temps et retourner tous les produits terminés.
        """
        finished_products = []
        
        if self.state == StationState.BROKEN:
            self.breakdown_remaining_time -= delta_time
            if self.breakdown_remaining_time <= 0:
                self._repair()
                self.logger.info(f"Station {self.station_name} remise en service")
            return finished_products
        
        if self.state == StationState.PROCESSING:
            self.processing_remaining_time -= delta_time
            if self.processing_remaining_time <= 0:
                finished_products.append(self.current_product)
                self._finish_processing()
            return finished_products
        
        # Lancer à traiter un produit
        if self._check():
            self._start_processing()
        return finished_products
    
    def _start_processing(self) -> None:
        """
        Demarre le traitement d'un produit.
        """
        self.current_product = self.queue.popleft()
        self.initial_processing_time = round(random.uniform(self.average_time * 0.5, self.average_time * 1.5), 2)
        self.processing_remaining_time = self.initial_processing_time
        self.current_product.mark_in_progress()
        self._set_state(StationState.PROCESSING)
        
        self.logger.debug(f"Station {self.get_station_name()} : début du traitement du produit {self.current_product.get_id()}")
    
    def _check(self) -> bool:
        """
        Détermine si une station peut démarrer un traitement.
        """
         # station en panne
        if self.state == StationState.BROKEN:
            self.logger.warning(f"Station {self.get_station_name()} hors service")
            return False
        
        # station déjà occupée
        if self.state == StationState.PROCESSING:
            self.logger.debug(f"Station {self.get_station_name()} : indisponible (traitement en cours)")
            return False
        
        # aucun produit à traiter
        if not self.queue:
            self.logger.debug(f"Station {self.get_station_name()} inactive (aucun produit en attente).")
            return False
       
        # Panne aléatoire
        if random.random() < self.proba_breakdown:
            self._trigger_breakdown()
            self.logger.critical(f"Station {self.get_station_name()}: panne détectée!")
            return False
        
        self._set_state(StationState.WAITING)
        return True

    def _set_state(self, new_state: StationState) -> None:
        """
        Change l'état et logge la transition.
        """
        if self.state != new_state:
            self.state = new_state
            self.logger.debug(f"_set_state - Station {self.station_name}: {self.state}")
    
    def _initialize_state(self) -> None:
        if self.queue:
            self._set_state(StationState.WAITING)
        else:
            self._set_state(StationState.IDLE)
    
    def _trigger_breakdown(self) -> None:
       """
       Déclencher une panne de la station.
       """
       self.breakdown_remaining_time = round(random.uniform(self.min_breakdown_duration, self.max_breakdown_duration), 2)
       self._set_state(StationState.BROKEN)
       
    def _repair(self) -> None:
        """
        Répare la station après une panne.
        """
        self.breakdown_remaining_time = 0.0
        self._initialize_state()
            
    def _finish_processing(self) -> None:
        """
        Termine le traitement du produit en cours.
        """
        self.processing_remaining_time = 0.0
        self.current_product.add_production_step(self.station_name, self.initial_processing_time)
        self.current_product = None
        self._initialize_state()
    
    
if __name__ == "__main__":
    pass
    
   
