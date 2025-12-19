import pytest
from toy_factory.product import Product
from utils.logger import config_logging

logger_ = config_logging("tests.log")


class TestProduct:
    """Tests pour la classe Product"""
    
    def test_product_creation(self):
        """Test que la creation de produit fonctionne"""
        
        product = Product(logger_)
        
        assert product._id.startswith("TOY-")
        assert product._status == "Created"
        assert product._production_time == 0.0
        assert len(product._history) == 0
    
    def test_add_production_step(self):
        """Test l'ajout d'une étape de production"""
        
        product = Product(logger_)
        
        product.add_production_step("Assemblage", 2.2)
        
        assert len(product._history) == 1
        assert product._history[0]["station"] == "Assemblage"
        assert product._production_time == 2.2
