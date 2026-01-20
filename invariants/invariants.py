# invariantgate/invariants.py
from __future__ import annotations

from typing import Mapping
from invariantgate.interfaces import Invariant, Variable, Value


class INV1_PostDiscountRevenueGteCost(Invariant):
    """
    INV-1: Post-Discount Revenue >= Cost
    
    Verifica que el revenue después del descuento sea >= al costo.
    Support: {list_price, discount_pct, cost}
    """

    @property
    def id(self) -> str:
        return "INV1_PostDiscountRevenueGteCost"

    def support(self) -> frozenset[Variable]:
        return frozenset({"list_price", "discount_pct", "cost"})

    def evaluate(self, completion: Mapping[Variable, Value]) -> bool:
        """
        Lógica: (list_price * (1 - discount_pct/100)) >= cost
        """
        try:
            list_price = float(completion["list_price"])
            discount_pct = float(completion["discount_pct"])
            cost = float(completion["cost"])

            post_discount_revenue = list_price * (1 - discount_pct / 100)
            return post_discount_revenue >= cost
        except (KeyError, TypeError, ValueError):
            # Variables faltantes o tipos incorrectos
            return False


class INV2_DiscountWithinSegmentCap(Invariant):
    """
    INV-2: Discount Within Segment Cap
    
    Verifica que el descuento esté dentro del límite del segmento.
    Support: {discount_pct, segment, max_discount_by_segment}
    """

    @property
    def id(self) -> str:
        return "INV2_DiscountWithinSegmentCap"

    def support(self) -> frozenset[Variable]:
        return frozenset({"discount_pct", "segment", "max_discount_by_segment"})

    def evaluate(self, completion: Mapping[Variable, Value]) -> bool:
        """
        Lógica: discount_pct <= max_discount_by_segment[segment]
        """
        try:
            discount_pct = float(completion["discount_pct"])
            segment = str(completion["segment"])
            max_discount = float(completion["max_discount_by_segment"])

            return discount_pct <= max_discount
        except (KeyError, TypeError, ValueError):
            # Variables faltantes o tipos incorrectos
            return False


class INV3_CashflowNonNegative90d(Invariant):
    """
    INV-3: Cashflow 
    
    Verifica que el cashflow a 90 días sea no negativo.
    Support: {cashflow_90d}
    """

    @property
    def id(self) -> str:
        return "INV3_CashflowNonNegative90d"

    def support(self) -> frozenset[Variable]:
        return frozenset({"cashflow_90d"})

    def evaluate(self, completion: Mapping[Variable, Value]) -> bool:
        """
        Lógica: cashflow_90d >= 0
        """
        try:
            cashflow_90d = float(completion["cashflow_90d"])
            return cashflow_90d >= 0
        except (KeyError, TypeError, ValueError):
            # Variables faltantes o tipos incorrectos
            return False
