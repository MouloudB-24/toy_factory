"""
Au contrôle qualité : 20% de chance d'être défectueux
Détecté par : random.random() < 0.20
Stocké dans la pile LIFO (Last In First Out)
Max 3 tentatives avant rejet définitif
retourne à la station précédente et le produit défectueux
"""
from logging import Logger
import random
from typing import Tuple
from toy_factory.product import Product


class DefectStack:
    """
    Pile LIFO pour les produits déféctueux.
    """
    # ordre toujours : ["Assemblage", "Peinture", "Contrôle qualité", "Emballage"]
    # 20% de change d'être défectueux
    # detecter par random
    # stock dans la pile
    # Max 3 tentatives
    
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.stack = [] # Pile LIFO
        self.station_order = ["Assemblage", "Peinture", "Contrôle qualité", "Emballage"]
        
        self.logger.info("Pile de défauts initialisée")
    
    def push(self, product: Product, defect_type: str, origine_station: str) -> None:
        """
        Envoi le produit défetueux dans la pile LIFO
        """
        
        # Vérifier que le produit est bien Product
        if isinstance(product, Product):
            item = {
                "product": product,
                "defect_type": defect_type,
                "origine_station": origine_station
            }
            self.stack.append(item)
        
        
    def pop(self) -> Tuple:
        """
        Envoyer pour le retraitement ou jeter le produit défectueux.
        """
        
        if not self.stack:
            return None, None
        
        item = self.stack.pop()
        product = item["product"]
        defect_type = item["defect_type"]
        origine_station = item["origine_station"]
        
        product.increment_retry()
        current_retry = product.get_retry_count()
        
        self.logger.info(f"Produit {product.get_id()} renvoyé pour le retraitement...")
        
        if current_retry > 3:
            product.mark_rejected()
            return None, None
        
        try :
            index = self.station_order.index(origine_station)
        except ValueError:
            index = 0
            self.logger.warning(f"Station inconnue: {origine_station} - Valide: {self.station_order}")
            return None, None
            
        if index == 0:
            return_station = origine_station
        else:
            return_station = random.choice(self.station_order[:index])
        
        self.logger.info(f"Produit {product.get_id()} retourne à la station '{return_station}' - Station d'origine '{origine_station}'")
    
        return product, return_station
        
        
if __name__ == "__main__":
    from utils.logger import config_logging
    logger = config_logging()
    stack = DefectStack(logger)
    p = Product(logger)
    print("Pile des produits défectueux: ", stack.stack)
    stack.push(p, "Peinture enrayée", "Peinture")
    print("Pile des produits défectueux: ", stack.stack)
    stack.pop()