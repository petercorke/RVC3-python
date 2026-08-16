"""Shared pytest configuration.

Notebook and example-script tests are real but slow (image/vision chapters,
animation loops) -- they're marked `slow` and skipped by default so a plain
`pytest tests/` stays a fast smoke test. Run the full suite with `--runall`.
"""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runall",
        action="store_true",
        default=False,
        help="also run slow tests (notebooks, RVC3/examples scripts)",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow test, skipped unless --runall is passed")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runall"):
        return
    skip_slow = pytest.mark.skip(reason="slow test -- pass --runall to run it")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
