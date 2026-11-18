"""Starter tests for the mini Najm Assist lab. Run: python3 -m unittest test_assist.py
Each test sends the malicious call itself, so it passes only if the *code* refuses."""
import unittest
import assist

EVIL = {"tool": "freeze_card", "card_id": "C-2002", "customer_id": "cust-2002"}

class FreezeCard(unittest.TestCase):
    def test_vulnerable_handler_acts_for_another_customer(self):
        db = assist.new_db()
        ok, _ = assist.freeze_vulnerable(db, EVIL, "cust-1001", confirmed=True)
        self.assertTrue(ok)                                   # the bug, demonstrated
        self.assertTrue(db["cards"]["C-2002"]["frozen"])

    def test_fixed_handler_refuses_another_customers_card(self):
        db = assist.new_db()
        ok, why = assist.freeze_fixed(db, EVIL, "cust-1001", confirmed=True)
        self.assertFalse(ok)
        self.assertIn("denied", why)
        self.assertFalse(db["cards"]["C-2002"]["frozen"])    # state unchanged

    def test_fixed_handler_needs_confirmation(self):
        db = assist.new_db()
        own = {"tool": "freeze_card", "card_id": "C-1001", "customer_id": "cust-1001"}
        ok, why = assist.freeze_fixed(db, own, "cust-1001", confirmed=False)
        self.assertFalse(ok)
        self.assertIn("pending", why)

    def test_kill_switch_stops_retrieval(self):
        db = assist.new_db()
        answer, _ = assist.handle(db, "what are the card fees", "cust-1001", retrieval=False)
        self.assertNotIn("From ", answer)

if __name__ == "__main__":
    unittest.main()
