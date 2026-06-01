def filter_by_budget(items, max_budget: float | None):
    if max_budget is None:
        return items

    filtered = []
    for item in items:
        price = getattr(item.item, "price_usd", None)
        if price is None or price <= max_budget:
            filtered.append(item)

    return filtered
