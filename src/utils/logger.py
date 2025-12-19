import logging


def config_logging(
    filename: str = "factory.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Fonction permettant de configurer le logging en fonction du niveau de debug.

    :param filename (str): Nom du fichier.
    :param console_level (int): Niveau de debug dans la console.
    :param file_level (int): Niveau de debug dans le fichier.
    :return (Logger): Function de logging.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Evite de créer plusieurs logger
    if logger.handlers:
        return logger
    
    # Console handler
    if console_level is not None:
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    # File hander
    if file_level is not None:
        fh = logging.FileHandler(filename)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
