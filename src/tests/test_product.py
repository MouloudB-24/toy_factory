import pytest
from toy_factory.product import Product
from utils.logger import config_logging

logger = config_logging("TestProduct.log")


class TestProduct:
    """Tests pour la classe Product"""
    
    def test_product_creation(self):
        """Test que la creation de produit fonctionne"""
        
        p = Product(logger)
        
        assert p.validate_id() == True
        assert p.get_status() == p.STATUS_IN_CREATED
        assert p.get_production_time() == 0.0
        assert p.get_retry_count() == 0
        assert len(p.get_history()) == 0
        
        p.mark_in_progress()
        assert p.get_status() == Product.STATUS_IN_PROGRESS
        
        p.add_production_step("Assemblage", 10.0)
        assert p.get_production_time() == 10.0
        assert len(p.get_history()) == 1
    
    
    def test_rejected_product(self):
        """
        Teste le mécanisme du produit jeté.
        """
        
        p = Product(logger)
        
        p.increment_retry()
        p.mark_defective()
        assert p.get_retry_count() == 1
        assert p.get_status() == Product.STATUS_IN_DEFECTIVE
        
        p.mark_rejected()
        assert p.get_status() == Product.STATUS_REJECTED

        
        
