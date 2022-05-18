import logging


def to_txt(results, file_name):
    """
    Return text file from dict
    Args:
        results:
        file_name:

    Returns:

    """
    logger = logging.getLogger('hfinger')
    name = file_name.split(".txt")
    file = open(name[0], "w+")
    try:
        for result in results:
            logger.info("Fingerprint found : {}".format(result.get("fingerprint")))
            file.write(result.get("fingerprint") + "\n")
    except IOError:
        logger.exception("Error opening file to write output in")
    finally:
        file.close()
