import sys
from pathlib import Path

from src.lcm import LCM
from src.log_conf import configure_logging

configure_logging(Path.home() / '.local/state/langcode/logs')

lcm = LCM()
lcm.run()

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

