from decimal import Decimal

from disquant.definitions.conventions import DayCount
from disquant.definitions.date import Date

"""
All examples are coming from the following ISDA educational spreadsheet
https://www.isda.org/a/mIJEE/30-360-2006ISDADefs.xls
"""

ISDA_EXAMPLES = [
    # 30/360 BOND BASIS examples
    (Date(2007, 1, 15), Date(2007, 1, 30), DayCount.THIRTY_360, Decimal(15) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 2, 15), DayCount.THIRTY_360, Decimal(30) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 7, 15), DayCount.THIRTY_360, Decimal(180) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 3, 31), DayCount.THIRTY_360, Decimal(180) / Decimal(360)),
    (Date(2007, 9, 30), Date(2007, 10, 31), DayCount.THIRTY_360, Decimal(30) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 9, 30), DayCount.THIRTY_360, Decimal(360) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 1, 31), DayCount.THIRTY_360, Decimal(16) / Decimal(360)),
    (Date(2007, 1, 31), Date(2007, 2, 28), DayCount.THIRTY_360, Decimal(28) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 31), DayCount.THIRTY_360, Decimal(33) / Decimal(360)),
    (Date(2006, 8, 31), Date(2007, 2, 28), DayCount.THIRTY_360, Decimal(178) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 8, 31), DayCount.THIRTY_360, Decimal(183) / Decimal(360)),
    (Date(2007, 2, 14), Date(2007, 2, 28), DayCount.THIRTY_360, Decimal(14) / Decimal(360)),
    (Date(2007, 2, 26), Date(2008, 2, 29), DayCount.THIRTY_360, Decimal(363) / Decimal(360)),
    (Date(2008, 2, 29), Date(2009, 2, 28), DayCount.THIRTY_360, Decimal(359) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 30), DayCount.THIRTY_360, Decimal(31) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 31), DayCount.THIRTY_360, Decimal(32) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 5), DayCount.THIRTY_360, Decimal(7) / Decimal(360)),
    (Date(2007, 10, 31), Date(2007, 11, 28), DayCount.THIRTY_360, Decimal(28) / Decimal(360)),
    (Date(2007, 8, 31), Date(2008, 2, 29), DayCount.THIRTY_360, Decimal(179) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 8, 31), DayCount.THIRTY_360, Decimal(182) / Decimal(360)),
    (Date(2008, 8, 31), Date(2009, 2, 28), DayCount.THIRTY_360, Decimal(178) / Decimal(360)),
    (Date(2009, 2, 28), Date(2009, 8, 31), DayCount.THIRTY_360, Decimal(183) / Decimal(360)),

    # 30/360 EUROBOND BASIS examples
    (Date(2007, 1, 15), Date(2007, 1, 30), DayCount.THIRTY_E_360, Decimal(15) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 2, 15), DayCount.THIRTY_E_360, Decimal(30) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 7, 15), DayCount.THIRTY_E_360, Decimal(180) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 3, 31), DayCount.THIRTY_E_360, Decimal(180) / Decimal(360)),
    (Date(2007, 9, 30), Date(2007, 10, 31), DayCount.THIRTY_E_360, Decimal(30) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 9, 30), DayCount.THIRTY_E_360, Decimal(360) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 1, 31), DayCount.THIRTY_E_360, Decimal(15) / Decimal(360)),
    (Date(2007, 1, 31), Date(2007, 2, 28), DayCount.THIRTY_E_360, Decimal(28) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 31), DayCount.THIRTY_E_360, Decimal(32) / Decimal(360)),
    (Date(2006, 8, 31), Date(2007, 2, 28), DayCount.THIRTY_E_360, Decimal(178) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 8, 31), DayCount.THIRTY_E_360, Decimal(182) / Decimal(360)),
    (Date(2007, 2, 14), Date(2007, 2, 28), DayCount.THIRTY_E_360, Decimal(14) / Decimal(360)),
    (Date(2007, 2, 26), Date(2008, 2, 29), DayCount.THIRTY_E_360, Decimal(363) / Decimal(360)),
    (Date(2008, 2, 29), Date(2009, 2, 28), DayCount.THIRTY_E_360, Decimal(359) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 30), DayCount.THIRTY_E_360, Decimal(31) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 31), DayCount.THIRTY_E_360, Decimal(31) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 5), DayCount.THIRTY_E_360, Decimal(7) / Decimal(360)),
    (Date(2007, 10, 31), Date(2007, 11, 28), DayCount.THIRTY_E_360, Decimal(28) / Decimal(360)),
    (Date(2007, 8, 31), Date(2008, 2, 29), DayCount.THIRTY_E_360, Decimal(179) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 8, 31), DayCount.THIRTY_E_360, Decimal(181) / Decimal(360)),
    (Date(2008, 8, 31), Date(2009, 2, 28), DayCount.THIRTY_E_360, Decimal(178) / Decimal(360)),
    (Date(2009, 2, 28), Date(2009, 8, 31), DayCount.THIRTY_E_360, Decimal(182) / Decimal(360)),

    # ACTUAL/360 ISDA examples
    (Date(2007, 1, 15), Date(2007, 1, 30), DayCount.ACTUAL_360, Decimal(15) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 2, 15), DayCount.ACTUAL_360, Decimal(31) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 7, 15), DayCount.ACTUAL_360, Decimal(181) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 3, 31), DayCount.ACTUAL_360, Decimal(183) / Decimal(360)),
    (Date(2007, 9, 30), Date(2007, 10, 31), DayCount.ACTUAL_360, Decimal(31) / Decimal(360)),
    (Date(2007, 9, 30), Date(2008, 9, 30), DayCount.ACTUAL_360, Decimal(366) / Decimal(360)),
    (Date(2007, 1, 15), Date(2007, 1, 31), DayCount.ACTUAL_360, Decimal(16) / Decimal(360)),
    (Date(2007, 1, 31), Date(2007, 2, 28), DayCount.ACTUAL_360, Decimal(28) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 31), DayCount.ACTUAL_360, Decimal(31) / Decimal(360)),
    (Date(2006, 8, 31), Date(2007, 2, 28), DayCount.ACTUAL_360, Decimal(181) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 8, 31), DayCount.ACTUAL_360, Decimal(184) / Decimal(360)),
    (Date(2007, 2, 14), Date(2007, 2, 28), DayCount.ACTUAL_360, Decimal(14) / Decimal(360)),
    (Date(2007, 2, 26), Date(2008, 2, 29), DayCount.ACTUAL_360, Decimal(368) / Decimal(360)),
    (Date(2008, 2, 29), Date(2009, 2, 28), DayCount.ACTUAL_360, Decimal(365) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 30), DayCount.ACTUAL_360, Decimal(30) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 3, 31), DayCount.ACTUAL_360, Decimal(31) / Decimal(360)),
    (Date(2007, 2, 28), Date(2007, 3, 5), DayCount.ACTUAL_360, Decimal(5) / Decimal(360)),
    (Date(2007, 10, 31), Date(2007, 11, 28), DayCount.ACTUAL_360, Decimal(28) / Decimal(360)),
    (Date(2007, 8, 31), Date(2008, 2, 29), DayCount.ACTUAL_360, Decimal(182) / Decimal(360)),
    (Date(2008, 2, 29), Date(2008, 8, 31), DayCount.ACTUAL_360, Decimal(184) / Decimal(360)),
    (Date(2008, 8, 31), Date(2009, 2, 28), DayCount.ACTUAL_360, Decimal(181) / Decimal(360)),
    (Date(2009, 2, 28), Date(2009, 8, 31), DayCount.ACTUAL_360, Decimal(184) / Decimal(360))
]