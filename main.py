import time
from src.toy_factory.factory import Factory
from src.utils.logger import config_logging

logger = config_logging()

def main():
    logger.info("Démarrage de la simulation de production")
    usine = Factory(logger, 0.5, 10)
    
    simulation_duration = 10
    delta_time = 0.1
    
    remainning_time = simulation_duration
    while remainning_time > 0:
        usine.update(delta_time)
        time.sleep(0.1)
        remainning_time -= delta_time
        
    usine.generate_report()
    logger.info("")
    logger.info("Fin de la simulation de production")


if __name__ == "__main__":
    main()