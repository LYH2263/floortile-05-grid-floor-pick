"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    max_mode: bool = False,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_base: raw_count, or max(raw_count, grid_count) when max_mode is on
    order_count: ceil(order_base * (1 + waste_pct/100))
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    grid_count = layout["grid_count"]
    order_base = max(raw, grid_count) if max_mode else raw
    with_waste = ceil_units(order_base * (1 + float(waste_pct) / 100.0))
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "grid_count": grid_count,
        "max_mode": bool(max_mode),
        "order_base": order_base,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
