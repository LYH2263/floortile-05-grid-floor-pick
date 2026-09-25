import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="floortile-test-")

from app import seed  # noqa: E402
from app.engines.tile_math import tile_count  # noqa: E402
from app.repositories import history, settings_repo  # noqa: E402
from app.services import estimate_service  # noqa: E402

seed.init_db()

# seed data: room 1 = 客餐厅 6.0 x 4.5, tile 1 = 600x600 (0.6 x 0.6), waste default 8
# area method: raw = ceil(27 / 0.36) = 75; grid = 10 cols x 8 rows = 80


def test_engine_max_mode_picks_grid_as_base():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, max_mode=True)
    assert r["raw_count"] == 75
    assert r["grid_count"] == 80
    assert r["max_mode"] is True
    assert r["order_base"] == 80
    assert r["order_count"] == 87  # ceil(80 * 1.08)


def test_engine_off_matches_legacy_formula():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, max_mode=False)
    assert r["max_mode"] is False
    assert r["order_base"] == 75
    assert r["order_count"] == 81  # ceil(75 * 1.08), same as before the change
    # default argument keeps the old call signature working
    assert tile_count(6.0, 4.5, 0.6, 0.6, 8.0)["order_count"] == 81


def test_engine_max_mode_corridor_strip():
    r = tile_count(8.0, 1.2, 0.8, 0.8, 8.0, max_mode=True)
    assert r["raw_count"] == 15
    assert r["grid_count"] == 20
    assert r["order_base"] == 20
    assert r["order_count"] == 22  # ceil(20 * 1.08)


def test_service_save_stores_mode_and_three_counts():
    res = estimate_service.run_estimate(1, 1, None, True, "择大保存", max_mode=True)
    assert res["run_id"] is not None
    assert res["max_mode"] is True
    assert res["raw_count"] == 75
    assert res["grid_count"] == 80
    assert res["order_base"] == 80
    assert res["order_count"] == 87

    run = history.get_run(res["run_id"])
    assert run["result"]["max_mode"] is True
    assert run["result"]["raw_count"] == 75
    assert run["result"]["grid_count"] == 80
    assert run["result"]["order_base"] == 80
    assert run["result"]["order_count"] == 87


def test_service_max_mode_defaults_to_settings():
    settings_repo.set_values({"max_mode": "1"})
    try:
        res = estimate_service.run_estimate(1, 1, None, False, "", max_mode=None)
        assert res["max_mode"] is True
        assert res["order_count"] == 87
    finally:
        settings_repo.set_values({"max_mode": "0"})
    res = estimate_service.run_estimate(1, 1, None, False, "", max_mode=None)
    assert res["max_mode"] is False
    assert res["order_count"] == 81


def test_changing_default_does_not_rewrite_old_runs():
    settings_repo.set_values({"max_mode": "0"})
    saved = estimate_service.run_estimate(1, 1, None, True, "旧口径", max_mode=None)
    assert saved["max_mode"] is False
    assert saved["order_count"] == 81

    settings_repo.set_values({"max_mode": "1"})
    try:
        run = history.get_run(saved["run_id"])
        assert run["result"]["max_mode"] is False
        assert run["result"]["order_count"] == 81
        # new previews follow the new default
        preview = estimate_service.run_estimate(1, 1, None, False, "", max_mode=None)
        assert preview["max_mode"] is True
    finally:
        settings_repo.set_values({"max_mode": "0"})
