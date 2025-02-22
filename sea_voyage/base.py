# -*- coding: utf-8 -*-
from searoute import searoute
from sea_voyage.classes import MNetwork
from sea_voyage.utils import get_m_network_20km

def searoute(start: tuple[float, float], end: tuple[float, float], network: MNetwork = None, **kwargs):
    """
    두 지점 간의 해상 경로를 계산합니다.
    
    Args:
        start (tuple[float, float]): 시작점의 (경도, 위도) 좌표
        end (tuple[float, float]): 도착점의 (경도, 위도) 좌표
        **kwargs: searoute 함수에 전달할 추가 인자
        
    Returns:
        list[tuple[float, float]]: 경로를 구성하는 좌표점들의 리스트
    """
    if not network:
        network = get_m_network_20km()
    return searoute(start, end, network=network, **kwargs)
