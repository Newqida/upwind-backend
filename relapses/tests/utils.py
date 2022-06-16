from relapses.models import Relapse

def get_expected_relapse_list(relapse_list: list[Relapse]):
    result = []

    for relapse in relapse_list:
        result.append({'datetime': relapse.datetime, 'reason': relapse.reason})

    return result