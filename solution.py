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
        # name -> 대출 정지 마지막 날 (이 날까지 대출 불가)
        self._banned_until = {}

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
        if day <= self._banned_until.get(name, 0):
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
            # 반납한 날부터 연체 일수만큼 정지, 겹치면 더 늦게 끝나는 쪽
            last = day + overdue - 1
            self._banned_until[name] = max(self._banned_until.get(name, 0), last)
        return overdue

    def get_loans(self, name):
        mine = [(b, due) for b, (n, _, due) in self._loans.items() if n == name]
        return sorted(mine, key=lambda x: (x[1], x[0]))
