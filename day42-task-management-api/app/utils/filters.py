def apply_search_filter(items: list[dict], search: str | None, field: str = "name"):
    if not search:
        return items
    search_lower = search.lower()
    return [item for item in items if search_lower in str(item.get(field, "")).lower()]