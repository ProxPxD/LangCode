import logging
import sys

from src.log_conf import configure_logging
lazy from src.app_manager import AppManager


def main() -> None:
    configure_logging()
    logger = logging.getLogger(__name__)
    try:
        app_manager = AppManager()
        app_manager.run()
    except Exception as e:
        logger.debug(f'Exiting app: {e}')
        raise


if __name__ == '__main__':
    main()


sys.exit(0)

uid = uuid1
query = f'''
PREFIX owl: <http://www.w3.org/2002/07/owl#>

PREFIX : <{URI_PREFIX}>

############
# Ontology #
############
INSERT DATA {{
    :is owl:inverseOf :ex .
}}

########
# Rels #
########
INSERT {{
    ?latin
        :name "latin";
        :is :str;
        :ex
            [:val 'a'],
            [:val 'b'],
            [:val 'c'],
            [:val 'd'],
            [:val 'e'],
            [:val 'f'],
            [:val 'g'],
            [:val 'h'],
            [:val 'i'],
            [:val 'j'],
            [:val 'k'],
            [:val 'l'],
            [:val 'm'],
            [:val 'n'],
            [:val 'o'],
            [:val 'p'],
            [:val 'q'],
            [:val 'r'],
            [:val 's'],
            [:val 't'],
            [:val 'u'],
            [:val 'v'],
            [:val 'w'],
            [:val 'x'],
            [:val 'y'],
            [:val 'z']
WHERE {{
    BIND([] AS ?latin)
}}
'''


print(query)

# lcm.gdm.raw_query(query)

