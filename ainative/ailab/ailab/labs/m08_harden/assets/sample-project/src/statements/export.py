"""Monthly statement export (a sample project for the dependency check; constructed for teaching)."""
import csv
import json

import csvtidy
from najm_utils import round_half_up  # an invented name, not in the lockfile or the allow-list (never install an unvetted name)


def export(path):
    rows = csvtidy.clean(path, drop_blank=True)
    return json.dumps([{"amount": str(round_half_up(r["amount"]))} for r in rows])
