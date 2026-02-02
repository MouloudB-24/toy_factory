from logging import Logger
import random
from typing import Tuple
from src.toy_factory.product import Product


class DefectStack:
    """
    Pile LIFO pour les produits déféctueux.
    """
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.stack = [] # Pile LIFO
        self.station_order = ["assemblage", "peinture", "controle_qualite", "emballage"]
        
        self.logger.info("Systèm de gestion des défauts initialisé")
    
    def push(self, product: Product, origine_station: str, defect_type: str="Défaut inconnu") -> None:
        """
        Envoi le produit défetueux dans la pile LIFO
        """
        
        # Vérifier que le produit est bien Product
        if isinstance(product, Product):
            item = {
                "product": product,
                "origine_station": origine_station,
                "defect_type": defect_type
            }
            self.stack.append(item)
        
    def pop(self) -> Tuple:
        """
        Envoyer un produit défectueux pour le retraitement ou le jeter.
        """
        product, station = self.peek()
        if product:
            product.increment_retry()
            self.logger.debug(f"Produit {product.get_id()}: {product.get_retry_count()} tentatives")
            current_retry = product.get_retry_count()
            del self.stack[-1]
    
            if current_retry > 3:
                product.mark_rejected()
                self.logger.warning(f"Produit {self.get_id()} rejecté après {self.get_retry_count()} tentatives de correction")
                return product, None
        self.logger.info(f"Produit {product.get_id()} envoyé en retraitement")
        return product, station

    
    def peek(self) -> Tuple:
        """
        Retourne le produit et la station de retour potentielle sans modification de la pile.
        """
        if not self.stack:
            return None, None
        
        item = self.stack[-1]
        product = item["product"]
        origine_station = item["origine_station"]
        
        index = self.station_order.index(origine_station)
        if index == 0:
            return_station = origine_station
        else:
            return_station = random.choice(self.station_order[:index])
        return product, return_station
    
    
if __name__ == "__main__":
    pass
