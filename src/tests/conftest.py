"""conftest"""
import pytest


@pytest.fixture(autouse=True)
def reset_singletons():
    """Singleton インスタンスをテスト間でリセットする"""
    yield
    import common.config.config as cfg_module
    cls = cfg_module.Config
    if hasattr(cls, "_instance"):
        delattr(cls, "_instance")
