"""Monthly statement export (a sample project for the dependency check; constructed for teaching)."""
import csv
import json

import invented_csvtidy
from najm_utils import round_half_up  # an invented name, not in the lockfile or the allow-list (never install an unvetted name)


def export(path):
    rows = invented_csvtidy.clean(path, drop_blank=True)
    return json.dumps([{"amount": str(round_half_up(r["amount"]))} for r in rows])
