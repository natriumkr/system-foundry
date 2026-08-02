from __future__ import annotations

import hashlib
import hmac
import html
import os
import secrets
from datetime import date, timedelta
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.domain import ValidationError, create_case, init_db, list_cases, parse_case, update_status

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("CLAIMCLOCK_DB_PATH", ROOT / "data" / "claimclock.db"))
ACCESS_KEY = os.getenv("CLAIMCLOCK_ACCESS_KEY", "")
SESSION_SECRET = os.getenv("CLAIMCLOCK_SESSION_SECRET", "")
HOST = os.getenv("CLAIMCLOCK_HOST", "127.0.0.1")
PORT = int(os.getenv("CLAIMCLOCK_PORT", "8080"))

TYPE_LABELS = {"return": "반품", "exchange": "교환", "refund": "환불"}
STATUS_LABELS = {"open": "접수", "waiting": "대기", "resolved": "완료"}
RISK_LABELS = {"overdue": "기한 초과", "urgent": "긴급", "watch": "주의", "safe": "안전", "done": "완료"}


def signature(label: str) -> str:
    return hmac.new(SESSION_SECRET.encode(), label.encode(), hashlib.sha256).hexdigest()


def page(title: str, body: str) -> bytes:
    return f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>
<link rel='stylesheet' href='/fonts.css'><link rel='stylesheet' href='/styles.css'></head><body>{body}</body></html>""".encode()


class Handler(BaseHTTPRequestHandler):
    server_version = "ClaimClock/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_bytes(self, content: bytes, status: int = 200, content_type: str = "text/html; charset=utf-8", headers: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)

    def redirect(self, target: str, headers: dict[str, str] | None = None) -> None:
        self.send_response(303)
        self.send_header("Location", target)
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()

    def form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 16_384:
            raise ValidationError("요청이 너무 큽니다.")
        values = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        return {key: items[-1] for key, items in values.items()}

    def authenticated(self) -> bool:
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        token = jar.get("claimclock_session")
        return bool(token and secrets.compare_digest(token.value, signature("admin-session")))

    def valid_csrf(self, form: dict[str, str]) -> bool:
        return secrets.compare_digest(form.get("csrf", ""), signature("csrf-token"))

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/styles.css", "/fonts.css"}:
            self.send_bytes((ROOT / "app" / path.lstrip("/")).read_bytes(), content_type="text/css; charset=utf-8")
            return
        if path in {"/fonts/noto-sans-kr-regular.ttf", "/fonts/noto-sans-kr-bold.ttf"}:
            self.send_bytes((ROOT / "app" / path.lstrip("/")).read_bytes(), content_type="font/ttf")
            return
        if path == "/health":
            self.send_bytes(b'{"status":"ok"}', content_type="application/json")
            return
        if path == "/login":
            self.login_page()
            return
        if not self.authenticated():
            self.redirect("/login")
            return
        if path == "/":
            self.dashboard()
            return
        self.send_bytes(page("찾을 수 없음", "<main><h1>404</h1></main>"), status=404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            form = self.form()
            if path == "/login":
                if secrets.compare_digest(form.get("access_key", ""), ACCESS_KEY):
                    cookie = f"claimclock_session={signature('admin-session')}; HttpOnly; SameSite=Strict; Path=/"
                    self.redirect("/", {"Set-Cookie": cookie})
                else:
                    self.login_page("접속 코드를 확인하세요.", 401)
                return
            if not self.authenticated():
                self.redirect("/login")
                return
            if not self.valid_csrf(form):
                self.send_bytes(page("요청 거부", "<main><h1>요청을 확인할 수 없습니다.</h1></main>"), status=403)
                return
            if path == "/logout":
                self.redirect("/login", {"Set-Cookie": "claimclock_session=; Max-Age=0; Path=/"})
                return
            if path == "/cases":
                create_case(DB_PATH, parse_case(form))
                self.redirect("/?notice=created")
                return
            if path.startswith("/cases/") and path.endswith("/status"):
                case_id = int(path.split("/")[2])
                if not update_status(DB_PATH, case_id, form.get("status", "")):
                    raise ValidationError("처리 건을 찾을 수 없습니다.")
                self.redirect("/?notice=updated")
                return
            self.send_bytes(page("찾을 수 없음", "<main><h1>404</h1></main>"), status=404)
        except (ValidationError, ValueError) as exc:
            self.dashboard(str(exc), 400)

    def login_page(self, error: str = "", status: int = 200) -> None:
        alert = f"<p class='alert'>{html.escape(error)}</p>" if error else ""
        body = f"""<main class='login-shell'><section class='login-card'>
<div class='brand-mark'>CC</div><p class='eyebrow'>OPERATIONS DESK</p><h1>ClaimClock</h1>
<p class='muted'>교환·환불 처리기한을 한눈에 관리하세요.</p>{alert}
<form method='post' action='/login'><label>접속 코드<input name='access_key' type='password' required autofocus></label>
<button type='submit'>대시보드 열기</button></form></section></main>"""
        self.send_bytes(page("ClaimClock 로그인", body), status=status)

    def dashboard(self, error: str = "", status: int = 200) -> None:
        cases = list_cases(DB_PATH)
        active = [item for item in cases if item["status"] != "resolved"]
        urgent = [item for item in active if item["risk"] in {"overdue", "urgent"}]
        exposure = sum(int(item["amount_krw"]) for item in active)
        notice = "<div class='toast'>변경사항을 저장했습니다.</div>" if "notice=" in self.path else ""
        if error:
            notice = f"<div class='toast error'>{html.escape(error)}</div>"
        rows = "".join(self.case_row(item) for item in cases) or "<tr><td colspan='7' class='empty'>첫 처리 건을 등록해 보세요.</td></tr>"
        csrf = signature("csrf-token")
        min_date = date.today().isoformat()
        default_deadline = (date.today() + timedelta(days=3)).isoformat()
        body = f"""<header><div class='brand'><span>CC</span><div><b>ClaimClock</b><small>CLAIM OPERATIONS</small></div></div>
<form method='post' action='/logout'><input type='hidden' name='csrf' value='{csrf}'><button class='ghost'>로그아웃</button></form></header>
<main class='shell'>{notice}<section class='hero'><div><p class='eyebrow'>TODAY'S CONTROL TOWER</p><h1>놓치기 전에,<br><em>먼저 처리하세요.</em></h1><p>교환·반품·환불 건의 기한과 상태를 하나의 업무판에서 관리합니다.</p></div>
<div class='date-chip'><span>기준일</span><b>{date.today().strftime('%Y.%m.%d')}</b></div></section>
<section class='stats'><article><span>진행 중</span><b>{len(active)}</b><small>ACTIVE CASES</small></article>
<article class='danger'><span>긴급 처리</span><b>{len(urgent)}</b><small>DUE IN 48H</small></article>
<article><span>처리 대상 금액</span><b>₩{exposure:,}</b><small>OPEN EXPOSURE</small></article></section>
<section class='workspace'><article class='panel cases'><div class='panel-head'><div><p class='eyebrow'>CASE QUEUE</p><h2>처리 현황</h2></div><span>{len(cases)}건</span></div>
<div class='table-wrap'><table><thead><tr><th>위험도</th><th>주문번호</th><th>유형</th><th>금액</th><th>기한</th><th>상태</th><th>갱신</th></tr></thead><tbody>{rows}</tbody></table></div></article>
<aside class='panel create'><p class='eyebrow'>NEW CASE</p><h2>처리 건 등록</h2><form method='post' action='/cases'>
<input type='hidden' name='csrf' value='{csrf}'><label>주문번호<input name='order_ref' maxlength='40' placeholder='ORD-2026-0182' required></label>
<label>고객 별칭 <small>선택</small><input name='customer_alias' maxlength='30' placeholder='김**'></label>
<div class='split'><label>유형<select name='case_type'><option value='return'>반품</option><option value='exchange'>교환</option><option value='refund'>환불</option></select></label>
<label>금액<input name='amount_krw' type='number' min='0' max='100000000' value='0' required></label></div>
<label>처리기한<input name='deadline' type='date' min='{min_date}' value='{default_deadline}' required></label>
<label>메모<textarea name='note' maxlength='240' rows='3' placeholder='검수 후 환불 예정'></textarea></label>
<button type='submit'>처리 건 추가</button><p class='privacy'>고객 실명 대신 별칭 사용을 권장합니다.</p></form></aside></section></main>"""
        self.send_bytes(page("ClaimClock 대시보드", body), status=status)

    def case_row(self, item: dict[str, object]) -> str:
        csrf = signature("csrf-token")
        days = int(item["days_left"])
        due_text = "오늘" if days == 0 else (f"D-{days}" if days > 0 else f"{abs(days)}일 초과")
        options = "".join(
            f"<option value='{value}'{' selected' if item['status'] == value else ''}>{label}</option>"
            for value, label in STATUS_LABELS.items()
        )
        return f"""<tr><td><span class='risk {item['risk']}'>{RISK_LABELS[str(item['risk'])]}</span></td>
<td><b>{html.escape(str(item['order_ref']))}</b><small>{html.escape(str(item['customer_alias'])) or '별칭 없음'}</small></td>
<td>{TYPE_LABELS[str(item['case_type'])]}</td><td>₩{int(item['amount_krw']):,}</td>
<td><b>{due_text}</b><small>{item['deadline']}</small></td><td>{STATUS_LABELS[str(item['status'])]}</td>
<td><form class='status-form' method='post' action='/cases/{item['id']}/status'><input type='hidden' name='csrf' value='{csrf}'><select name='status'>{options}</select><button>저장</button></form></td></tr>"""


def main() -> None:
    if len(ACCESS_KEY) < 12 or len(SESSION_SECRET) < 24:
        raise SystemExit("CLAIMCLOCK_ACCESS_KEY(12자 이상)와 CLAIMCLOCK_SESSION_SECRET(24자 이상)을 설정하세요.")
    init_db(DB_PATH)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"ClaimClock running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
