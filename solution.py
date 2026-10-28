# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _is_day(x):
    # bool은 int의 하위 타입이지만 정수로 보지 않음
    return isinstance(x, int) and not isinstance(x, bool) and x >= 1


class LibraryLoan:
    def __init__(self):
        # book_id -> (name, 빌린 날, 반납 기한)
        self._loans = {}
        # name -> [(정지 시작일, 정지 마지막 날), ...]
        # 겹치는 정지는 합쳐서 보므로 결국 더 늦게 끝나는 쪽을 따름 (기간을 더하지 않음)
        self._bans = {}

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS or not _is_day(day):
            return False
        if book_id in self._loans:
            return False

        mine = [due for n, _, due in self._loans.values() if n == name]
        if len(mine) >= MAX_LOANS:
            return False
        if any(day > due for due in mine):
            return False
        # 날짜 순서는 검사하지 않음: 실제 정지 기간에 들어가는 날만 막음
        if any(s <= day <= e for s, e in self._bans.get(name, [])):
            return False

        self._loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or not _is_day(day):
            return -1
        loan = self._loans.get(book_id)
        if loan is None:
            return -1
        borrower, borrowed_day, due = loan
        if borrower != name or day < borrowed_day:
            return -1

        del self._loans[book_id]
        overdue = max(0, day - due)
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 정지 (정지 중에도 반납은 가능)
            self._bans.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        mine = [(b, due) for b, (n, _, due) in self._loans.items() if n == name]
        return sorted(mine, key=lambda x: (x[1], x[0]))
