from searoute import searoute
from seavoyage.classes import MNetwork
from seavoyage.utils import get_m_network_20km

def seavoyage(start: tuple[float, float], end: tuple[float, float], **kwargs):
    if not kwargs.get("M"):
        kwargs["M"] = get_m_network_20km()
    return searoute(start, end, **kwargs)
