"""The labs. One folder per lab: ``mNN_slug/`` with ``lab.py`` (defining ``LAB``), ``task.md``,
optional ``assets/``, ``solution/`` and ``hidden/``.

Discovery lives in ``ailab.framework`` (``discover()``, ``load_lab()``); this package only
re-exports it, so ``from ailab.labs import discover`` works. Labs are found by folder name and
imported one at a time, so a lab that does not import cannot hide the others.
"""
from ailab.framework import LabEntry, discover, lab_dirnames, load_lab

__all__ = ["LabEntry", "discover", "lab_dirnames", "load_lab"]
