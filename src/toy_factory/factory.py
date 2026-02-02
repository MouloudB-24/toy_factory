from functools import reduce
from logging import Logger
import random

from src.toy_factory.defect_stack import DefectStack
from src.toy_factory.product import Product
from src.toy_factory.station import Station, StationState


class Factory:
    
    def __init__(self, logger: Logger, production_rate: float=0.5, time_scale: int=10):
        """
        Initialise l'usine de jouets
        
        Args:
            logger (Logger): Logger configuré
            production_rate (float, optional): rendement de l'usine par seconde simulée (ex: 1produit/2secondes)
            time_scale (int, optional): Echelle d'accélération (1 seconde réelle = 10 sécondes simulées)
        """
        
        self.logger = logger
        self.production_rate = production_rate
        self.time_scale = time_scale
        
        # Temps écoulé dans la simulation (secondes simulées)
        self.simulated_time = 0.0
        self.time_since_last_product = 0.0
        
        self.stations = {
            "assemblage": Station(logger, "Assemblage", average_time=2.0),
            "peinture": Station(logger, "Peinture", average_time=3.0),
            "controle_qualite": Station(logger, "Contrôle qualité", average_time=1.0),
            "emballage": Station(logger, "Emballage", average_time=1.0)
        }
        
        # L'ordre des stations dans le flux
        self.station_order = ["assemblage", "peinture", "controle_qualite", "emballage"]
        
        # Pile de défauts
        self.defect_stack = DefectStack(logger)
        
        # Stats
        self.produced_count = 0
        self.finished_products = []
        self.rejected_products = []
        
        # Pour la création continue de produits
        self.time_since_last_product = 0.0
        self.next_product_id = 1
        
        self.logger.info("Usine de fabrication de jouets initialisée")
        
    def update(self, delta_time_real: float) -> None:
        """
        Fait avancer la simulation de delta_time_real seondes réelles.
        
        :param delta_time_real (float): Temps réel écoulé en seconde
        """
        # conversion en temps simulé
        delta_time_simulated = delta_time_real * self.time_scale
        self.simulated_time += delta_time_simulated
        
        # créer de nouveau produits
        self._create_new_products(delta_time_simulated)
        
        # Faire avancer toutes les stations
        finished_products = self._advance_stations(delta_time_simulated)
        
        # transferer les produits entre les stations
        self._transfer_products(finished_products)
        
        # traiter la pile de défauts
        self._process_defects()
    
    def _create_new_products(self, delta_time_simulated: float) -> None:
        """
        créer de nouveaux produits selon le rendement de l'usine.
        """
        self.time_since_last_product += delta_time_simulated
        
        # calcule l'interval entre les produits
        if self.production_rate > 0:
            interval = 1 / self.production_rate
        else:
            self.logger.warning("Attention à la valeur de production_rate !")
            # interval = float("inf")
        
        
        while self.time_since_last_product >= interval:
            # creer un nouveau produit
            new_product = Product(self.logger)
            
            # ajouter à la 1er station
            self.stations["assemblage"].add_product(new_product)
            
            # mettre les compteurs
            self.produced_count += 1
            self.time_since_last_product -= interval
            
            self.logger.debug(f"Nouveau produit crée: {new_product.get_id()}")
    
    def _advance_stations(self, delta_time_simulated: float):
        """
        Fait avancer toutes les stations en retourne les produits terminés.
        """
        current_finished_products = {}
        for station_name, station in self.stations.items():
            products = station.advance_treatment(delta_time_simulated)
            if products:
                current_finished_products[station_name] = products
                self.logger.debug(f"Avancement du traitement des stations...")
        return current_finished_products
    
    def _transfer_products(self, current_finished_products: dict) -> None:
        """
        Transferer les produits d'une station à la station suivante sous certains conditions.
        """
        for station_name, products in current_finished_products.items():
            if station_name == self.station_order[-1]:
                for product in products:
                    product.mark_finished()
                    self.logger.info(f"Produit {product.get_id()} :  fabrication terminée (temps total : {product.get_production_time()}s)")
                    self.finished_products.append(product)
            
            else:
                index = self.station_order.index(station_name)
                next_station = self.station_order[index +1]
                
                for product in products:
                    if station_name == self.station_order[-2] and random.random() < 0.2:
                        product.mark_defective()
                        self.logger.warning(f"Produit {product.get_id()} détecté comme déféctueux")
                        self.defect_stack.push(product, station_name)
                    else:
                        self.stations[next_station].add_product(product)
        
    def _process_defects(self) -> None:
        """
        Traite les produits défectueux
        """
        product, station = self.defect_stack.peek()
        if product is None or self.stations[station].state == StationState.BROKEN:
            return
        
        product, station = self.defect_stack.pop()
        
        if station:
            self.stations[station].add_product(product)
            self.logger.info(f"Produit {product.get_id()} réinjecté en station {station}")
        else:
            self.rejected_products.append(product)
            self.logger.info(f"Produit {product.get_id()} définitivement rejeté!")
                
    
    def generate_report(self):
        """
        Genere un rapport de données de l'usine.
        """
        self.logger.info("")
        self.logger.info("Génération du rapport de production")
        
        all_products = self.finished_products + self.rejected_products
        
        if not all_products:
            self.logger.info("Aucune donnée de production disponible!")
            return
        
        self.logger.info(f"Nombre total de produits crées : {Product.SERIAL_NUMBER}")
        self.logger.info(f"Nombres total de produits traités : {len(all_products)}")
        self.logger.info(f"Nombres total de produits finis : {len(self.finished_products)}")
        self.logger.info(f"Nombres total de produits rejetés : {len(self.rejected_products)}")
        
        if self.finished_products:
            total_time = reduce(lambda total, product: total + product.get_production_time(), self.finished_products, 0)
            avg_time = total_time / len(self.finished_products)
            self.logger.info(f"Temps moyen de production : {avg_time} secondes/produit")
        
        repaired_products = list(filter(lambda product: product.get_retry_count() >= 1, all_products))
        percent_repaired = round(len(repaired_products) / len(all_products) * 100, 2)
        self.logger.info(f"Taux de produits ayant nécessité une reprise : {percent_repaired}")
        
        self.logger.info("Cinq derniers produits finis :")
        last_id = map(lambda p: f"ID: {p.get_id()} | Temps : {p.get_production_time()}s", self.finished_products[-5:])
        for product_id in  last_id:
            self.logger.info(f"{product_id}")
        
        
        

if __name__  == "__main__":
    import time
    from utils.logger import config_logging
    logger = config_logging()
    
    # Simule 5 secondes simulées
    usine = Factory(logger, production_rate=0.5, time_scale=10)
    
    # 2. Boucle de simulation
    sim_duration = 3  # secondes réelles
    start_time = time.time()
    last_tick = start_time
    
    while time.time() - start_time < sim_duration:
        now = time.time()
        # delta = now - last_tick
        delta = 1
        
        # On met à jour l'usine
        usine.update(delta)
        
        last_tick = now
        time.sleep(0.1) # Petite pause pour laisser respirer le processeur
    
    # 3. Le moment de vérité !
    usine.generate_report()