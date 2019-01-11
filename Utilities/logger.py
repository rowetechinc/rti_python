import logging


class RtiLogger:
    """
    This is used to initialize the Logging.  This just sets the logging options.
    If you want to also log to a file, then give the file path.
    To Log:

    import logging
    logging.debug("DEBUG MESSAGE")
    """

    def __init__(self, file_path=None, log_level=logging.DEBUG, log_format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s'):
        # Set the logging level
        logging.basicConfig(level=log_level,
                            format=log_format)

        # If a file path is given, then also log to a file
        if file_path:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(file_handler)
