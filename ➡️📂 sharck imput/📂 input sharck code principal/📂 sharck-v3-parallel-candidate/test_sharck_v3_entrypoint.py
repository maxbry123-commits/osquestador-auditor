from sharck_v3_entrypoint import RUNTIME_CLASS, Runtime, create_runtime
from sharck_v3_presearch import PresearchStrictSharckV3Runtime


def test_entrypoint():
    assert Runtime is PresearchStrictSharckV3Runtime
    assert RUNTIME_CLASS is PresearchStrictSharckV3Runtime
    assert callable(create_runtime)


if __name__ == "__main__":
    test_entrypoint()
    print("1 entrypoint test PASS")
