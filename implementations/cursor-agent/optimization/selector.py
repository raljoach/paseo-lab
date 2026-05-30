# optimization/selector.py

def select_with_budget(items, score_fn, max_budget):
    sorted_items = sorted(items, key=score_fn, reverse=True)

    selected = []
    remaining = max_budget

    for item in sorted_items:
        cost = getattr(item, "price_usd", 0)

        if cost <= remaining:
            selected.append(item)
            remaining -= cost

    return selected