"""One catalogue view for the answering agent and its evaluator."""


def build_product_context(products: list[dict]) -> str:
    """Include the same available evidence in both prompts; omit unknown specs."""
    if not products:
        return "No relevant products found in the catalogue."
    lines = ["AVAILABLE PRODUCTS:\n"]
    for index, product in enumerate(products, 1):
        specs = product.get("specs") or {}
        details = []
        for key, value in specs.items():
            if value is None:
                continue
            formatted = ", ".join(str(item) for item in value) if isinstance(value, list) else str(value)
            details.append(f"{key}: {formatted}")
        lines.append(
            f"{index}. {product['name']}\n"
            f"   Price: £{product.get('price', 'N/A')} | Rating: {product.get('rating', 'N/A')}/5 | Brand: {product.get('brand', 'N/A')}\n"
            f"   {' | '.join(details) if details else 'N/A'}\n"
            f"   Description: {product.get('description', '')}\n"
        )
    return "\n".join(lines)
