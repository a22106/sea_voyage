import pytest
import sea_voyage as sv

@pytest.fixture
def start_point():
    return (129.165, 35.070)

@pytest.fixture
def end_point():
    return (129.170, 35.075)


class TestSeavoyage:
    def test_seavoyage(self, start_point, end_point):
        route = sv.searoute(start_point, end_point)
        assert route is not None
        assert len(route) > 0

