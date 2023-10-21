from enum import StrEnum

from disquant.definitions.period import Period, Unit


class Frequency(StrEnum):
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"

    def to_period(self) -> Period:
        mapping = {
            Frequency.ANNUAL: Period(1, Unit.YEAR),
            Frequency.SEMI_ANNUAL: Period(6, Unit.MONTH),
            Frequency.QUARTERLY: Period(3, Unit.MONTH),
            Frequency.MONTHLY: Period(1, Unit.MONTH),
            Frequency.WEEKLY: Period(1, Unit.WEEK),
            Frequency.DAILY: Period(1, Unit.DAY),
        }

        if self not in mapping:
            raise NotImplementedError

        return mapping[self]

    def per_year(self) -> int:
        mapping = {
            Frequency.ANNUAL: 1,
            Frequency.SEMI_ANNUAL: 2,
            Frequency.QUARTERLY: 4,
            Frequency.MONTHLY: 12,
            Frequency.WEEKLY: 52,
            Frequency.DAILY: 365,
        }

        if self not in mapping:
            raise NotImplementedError

        return mapping[self]
