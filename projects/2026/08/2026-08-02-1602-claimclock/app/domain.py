from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path

CASE_TYPES = {"return", "exchange", "refund"}
STATUSES = {"open", "waiting", "resolved"}


class ValidationError(ValueError):
    pass


def clean_text(value: str, field: str, *, max_length: int, required: bool = True) -> str:
    cleaned = " ".join((value or "").split())
    if required and not cleaned:
        raise ValidationError(f"{field} 항목을 입력하세요.")
    if len(cleaned) > max_length:
        raise ValidationError(f"{field} 항목은 {max_length}자 이하여야 합니다.")
    return cleaned


def parse_case(form: dict[str, str], today: date | None = None) -> dict[str, object]:
    today = today or date.today()
    order_ref = clean_text(form.get("order_ref", ""), "주문번호", max_length=40)
    customer_alias = clean_text(form.get("customer_alias", ""), "고객 별칭", max_length=30, required=False)
    note = clean_text(form.get("note", ""), "메모", max_length=240, required=False)
    case_type = form.get("case_type", "")
    if case_type not in CASE_TYPES:
        raise ValidationError("올바른 요청 유형을 선택하세요.")
    try:
        amount_krw = int(form.get("amount_krw", "0"))
    except ValueError as exc:
        raise ValidationError("금액은 정수로 입력하세요.") from exc
    if amount_krw < 0 or amount_krw > 100_000_000:
        raise ValidationError("금액은 0원 이상 1억원 이하여야 합니다.")
    try:
        deadline = date.fromisoformat(form.get("deadline", ""))
    except ValueError as exc:
        raise ValidationError("올바른 처리기한을 입력하세요.") from exc
    if deadline < today or deadline > today.replace(year=today.year + 1):
        raise ValidationError("처리기한은 오늘부터 1년 이내여야 합니다.")
    return {
        "order_ref": order_ref,
        "customer_alias": customer_alias,
        "case_type": case_type,
        "amount_krw": amount_krw,
        "deadline": deadline.isoformat(),
        "note": note,
    }


def risk_level(deadline: str, status: str, today: date | None = None) -> tuple[str, int]:
    today = today or date.today()
    days = (date.fromisoformat(deadline) - today).days
    if status == "resolved":
        return "done", days
    if days < 0:
        return "overdue", days
    if days <= 2:
        return "urgent", days
    if days <= 5:
        return "watch", days
    return "safe", days


def connect(db_path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: str | Path) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_ref TEXT NOT NULL UNIQUE,
                customer_alias TEXT NOT NULL DEFAULT '',
                case_type TEXT NOT NULL CHECK(case_type IN ('return','exchange','refund')),
                amount_krw INTEGER NOT NULL CHECK(amount_krw BETWEEN 0 AND 100000000),
                deadline TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','waiting','resolved')),
                note TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


def create_case(db_path: str | Path, payload: dict[str, object]) -> int:
    now = datetime.now().isoformat(timespec="seconds")
    try:
        with connect(db_path) as db:
            cursor = db.execute(
                """INSERT INTO cases
                (order_ref, customer_alias, case_type, amount_krw, deadline, note, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    payload["order_ref"], payload["customer_alias"], payload["case_type"],
                    payload["amount_krw"], payload["deadline"], payload["note"], now, now,
                ),
            )
            return int(cursor.lastrowid)
    except sqlite3.IntegrityError as exc:
        raise ValidationError("이미 등록된 주문번호입니다.") from exc


def list_cases(db_path: str | Path, today: date | None = None) -> list[dict[str, object]]:
    with connect(db_path) as db:
        rows = db.execute(
            "SELECT * FROM cases ORDER BY CASE status WHEN 'resolved' THEN 1 ELSE 0 END, deadline, id DESC"
        ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["risk"], item["days_left"] = risk_level(item["deadline"], item["status"], today)
        result.append(item)
    return result


def update_status(db_path: str | Path, case_id: int, status: str) -> bool:
    if status not in STATUSES:
        raise ValidationError("올바른 상태를 선택하세요.")
    with connect(db_path) as db:
        cursor = db.execute(
            "UPDATE cases SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(timespec="seconds"), case_id),
        )
        return cursor.rowcount == 1
