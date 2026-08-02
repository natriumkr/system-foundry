import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from app.domain import ValidationError, create_case, init_db, list_cases, parse_case, risk_level, update_status


class ClaimClockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "test.db"
        init_db(self.db)
        self.today = date(2026, 8, 2)

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, **overrides):
        base = {
            "order_ref": "ORD-1001",
            "customer_alias": "김**",
            "case_type": "return",
            "amount_krw": "28900",
            "deadline": "2026-08-05",
            "note": "검수 후 환불",
        }
        base.update(overrides)
        return base

    def test_parses_and_normalizes_case_input(self):
        result = parse_case(self.payload(order_ref="  ORD-1001  ", note="검수  후   환불"), self.today)
        self.assertEqual(result["order_ref"], "ORD-1001")
        self.assertEqual(result["note"], "검수 후 환불")
        self.assertEqual(result["amount_krw"], 28900)

    def test_rejects_invalid_amount_and_type(self):
        with self.assertRaises(ValidationError):
            parse_case(self.payload(amount_krw="-1"), self.today)
        with self.assertRaises(ValidationError):
            parse_case(self.payload(case_type="chargeback"), self.today)

    def test_rejects_past_or_excessive_deadline(self):
        with self.assertRaises(ValidationError):
            parse_case(self.payload(deadline="2026-08-01"), self.today)
        with self.assertRaises(ValidationError):
            parse_case(self.payload(deadline="2028-01-01"), self.today)

    def test_classifies_deadline_risk(self):
        self.assertEqual(risk_level("2026-08-01", "open", self.today)[0], "overdue")
        self.assertEqual(risk_level("2026-08-04", "open", self.today)[0], "urgent")
        self.assertEqual(risk_level("2026-08-07", "open", self.today)[0], "watch")
        self.assertEqual(risk_level("2026-08-12", "open", self.today)[0], "safe")

    def test_resolved_case_is_always_done(self):
        self.assertEqual(risk_level("2026-07-01", "resolved", self.today)[0], "done")

    def test_creates_lists_and_updates_case(self):
        case_id = create_case(self.db, parse_case(self.payload(), self.today))
        cases = list_cases(self.db, self.today)
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0]["risk"], "watch")
        self.assertTrue(update_status(self.db, case_id, "resolved"))
        self.assertEqual(list_cases(self.db, self.today)[0]["status"], "resolved")

    def test_rejects_duplicate_order_reference(self):
        parsed = parse_case(self.payload(), self.today)
        create_case(self.db, parsed)
        with self.assertRaises(ValidationError):
            create_case(self.db, parsed)

    def test_rejects_unknown_status(self):
        with self.assertRaises(ValidationError):
            update_status(self.db, 1, "deleted")


if __name__ == "__main__":
    unittest.main()
