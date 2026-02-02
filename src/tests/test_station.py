import pytest
from unittest.mock import patch, MagicMock

from toy_factory.product import Product
from toy_factory.station import Station, StationState
from utils.logger import config_logging

logger = config_logging("TestStation.log")

class TestStation:
    """Tests pour la classe Station"""

    def test_station_simple_processing(self):
        # Création d'une station avec un temps fixe moyen de 5.0s
        station = Station(logger, "Assemblage", average_time=5.0)
        station.proba_breakdown = 0.0
        
        # Vérification de l'etat avant l'ajout
        assert station.get_station_state() == StationState.IDLE
        assert len(station.get_queue()) == 0
        
        product = Product(logger)
        station.add_product(product)

        # Vérification de l'état après ajout
        assert station.state == StationState.WAITING
        assert len(station.get_queue()) == 1       
       
    def test_station_finish_processing_single_product(self):
        """
        Teste la production d'un produit finit.
        """
        station = Station(logger, "assemblage", 2)
        station.proba_breakdown = 0.0
        
        product = Product(logger)
        station.add_product(product)
        product.add_production_step = MagicMock()
        
        with patch("toy_factory.station.random.uniform", return_value=5):
            finished = station.advance_treatment(10)
        
        assert station.processing_remaining_time == 0
        assert station.state == StationState.IDLE
        assert len(finished) == 1
        assert finished[0] == product
        assert station.current_product is None
        product.add_production_step.assert_called_once_with("assemblage", 5)
        
    