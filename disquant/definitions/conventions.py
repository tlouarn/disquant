from decimal import Decimal
from enum import Enum

from disquant.definitions.date import Date, DateRange


# Some useful definitions
# https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
# https://www.isda.org/a/mIJEE/30-360-2006ISDADefs.xls


class DayCount(str, Enum):
    """
    Day-count conventions.
    30E/360: Eurobond Basis
    30I/360: Bond basis
    """

    THIRTY_E_360 = "30E/360"
    THIRTY_360 = "30/360"
    ACTUAL_360 = "ACT/360"
    ACTUAL_365_FIXED = "ACT/365F"
    ACTUAL_ACTUAL_ISDA = "ACT/ACT ISDA"


def year_fraction(start: Date, end: Date, day_count: DayCount) -> Decimal:
    """
    Compute the fraction of year between two dates.
    Used to compute the accrued interests on a wide range of financial instruments.
    """
    calendar_days = end - start

    match day_count:
        case DayCount.THIRTY_E_360:
            """
            This implementation follows the 30E/360 "Eurobond Basis" definition.
            2006 ISDA definitions 4.16g
            """
            # Cap both start and end dates to 30
            start_day = min(start.day, 30)
            end_day = min(end.day, 30)

            days = 360 * (end.year - start.year)
            days += 30 * (end.month - start.month)
            days += end_day - start_day
            return Decimal(days) / Decimal(360)

        case DayCount.THIRTY_360:
            """
            This implementation follows the 30/360 "Bond basis" definition.
            2006 ISDA definitions 4.16f
            - D1 is the first calendar day, expressed as a number, of the Calculation Period
              or Compounding Period, unless such number would be 31, in which case D1 will be 30
            - D2 is the calendar day, expressed as a number, immediately following the last day
              included in the Calculation Period or Compounding Period, unless such number would be
              31 and D1 is greater than 29, in which case D2 will be 30
            """
            start_day = min(start.day, 30)
            end_day = min(end.day, 30) if start_day > 29 else end.day

            days = 360 * (end.year - start.year)
            days += 30 * (end.month - start.month)
            days += end_day - start_day
            return Decimal(days) / Decimal(360)

        case DayCount.ACTUAL_360:
            """
            The actual number of days is always divided by 360.
            """
            return Decimal(calendar_days) / Decimal(360)

        case DayCount.ACTUAL_365_FIXED:
            """
            The actual number of days is always divided by 365.
            2006 ISDA definitions 4.16d.
            
            Also known as "ACT/365" or "English". 
            Used in GBP money markets.
            """
            return Decimal(calendar_days) / Decimal(365)

        case DayCount.ACTUAL_ACTUAL_ISDA:
            """
            This implementation follows the ACT/ACT ISDA definition.
            https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
            """
            leap = sum(1 for x in DateRange(start, end) if x.is_leap)
            non_leap = calendar_days - leap
            return Decimal(leap) / Decimal(366) + Decimal(non_leap) / Decimal(365)

        case _:
            raise NotImplementedError
