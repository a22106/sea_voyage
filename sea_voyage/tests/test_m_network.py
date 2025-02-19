import pytest
import geojson

from sea_voyage.classes.m_network import MNetwork

@pytest.fixture
def marine_network_100km():
    marnet = MNetwork()
    marnet.load_geojson("sea_voyage/data/marnet/marnet_plus_100km.geojson")
    return marnet


@pytest.fixture
def marine_network_5km():
    marnet = MNetwork()
    marnet.load_geojson("sea_voyage/data/marnet/marnet_plus_5km.geojson")
    return marnet

@pytest.fixture
def net_node():
    return (129.165, 35.070)

@pytest.fixture
def net_nodes():
    return [
        (129.170, 35.075),
        (129.180, 35.080),
        (129.175, 35.070)
    ]

@pytest.fixture
def geojson_point():
    return geojson.Point((129.1299055052927, 35.02979966028465))

@pytest.fixture
def geojson_multipoint():
    points = [
        geojson.Point((129.1299055052927, 35.02979966028465)),
        geojson.Point((129.1399055052927, 35.03979966028465)),
        geojson.Point((129.1499055052927, 35.04979966028465)),
        geojson.Point((129.1599055052927, 35.05979966028465)),
    ]
    multi_point = geojson.MultiPoint(points)
    return multi_point

@pytest.fixture
def geojson_feature_collection():
    points = [
        geojson.Point((129.1299055052927, 35.02979966028465)),
        geojson.Point((129.1399055052927, 35.03979966028465)),
        geojson.Point((129.1499055052927, 35.04979966028465)),
        geojson.Point((129.1599055052927, 35.05979966028465)),
    ]
    points_feature_collection = geojson.FeatureCollection(points)
    return points_feature_collection


@pytest.mark.django_db
class TestSearoute:
    def test_searoute_100km(self, marine_network_100km: MNetwork):
        assert marine_network_100km.nodes is not None and len(marine_network_100km.nodes) > 5000
        assert marine_network_100km.edges is not None and len(marine_network_100km.edges) > 10000

    def test_searoute_5km(self, marine_network_5km: MNetwork):
        assert marine_network_5km.nodes is not None and len(marine_network_5km.nodes) > 42000
        assert marine_network_5km.edges is not None and len(marine_network_5km.edges) > 78000

    def test_add_node_with_edges(self, marine_network_5km: MNetwork, net_node: tuple[float, float]):
        # 1개 노드 추가 후 엣지 자동 생성 테스트
        # Arrange
        nodes_num = len(marine_network_5km.nodes)
        edges_num = len(marine_network_5km.edges)
        
        # Act
        created_edges = marine_network_5km.add_node_with_edges(net_node, threshold=100.0)
        
        # Assert
        assert created_edges is not None and len(created_edges) > 0
        assert len(marine_network_5km.nodes) == nodes_num + 1
        assert len(marine_network_5km.edges) >= edges_num + 1

    def test_add_nodes_with_edges(self, marine_network_5km: MNetwork, net_nodes: list[tuple[float, float]]):
        # 여러 노드 추가 후 엣지 자동 생성 테스트
        # Arrange
        nodes_num = len(marine_network_5km.nodes)
        edges_num = len(marine_network_5km.edges)
        
        # Act
        created_edges = marine_network_5km.add_nodes_with_edges(net_nodes, threshold=100.0)
        
        # Assert
        assert created_edges is not None and len(created_edges) > 0
        assert len(marine_network_5km.nodes) == nodes_num + 3
        assert len(marine_network_5km.edges) >= edges_num + 3

    def test_add_node_with_edges_invalid_input(self, marine_network_5km: MNetwork):
        # 유효하지 않은 입력 테스트
        # Arrange
        invalid_node = "invalid_node"
        
        # Act
        with pytest.raises(TypeError):
            marine_network_5km.add_node_with_edges(invalid_node, threshold=100.0)
            
        # Assert
        assert True

    def test_add_node_with_edges_invalid_threshold(self, marine_network_5km: MNetwork, net_node: tuple[float, float]):
        # 유효하지 않은 입력 테스트
        # Arrange
        invalid_threshold = -100.0
        
        # Act
        with pytest.raises(ValueError):
            marine_network_5km.add_node_with_edges(net_node, threshold=invalid_threshold)
        
        # Assert
        assert True


    def test_add_nodes_with_edges_geojson_point(
        self, marine_network_5km: MNetwork, 
        geojson_point: geojson.Point):
        # Arrange
        nodes_num = len(marine_network_5km.nodes)
        edges_num = len(marine_network_5km.edges)
        
        # Act
        created_edges = marine_network_5km.add_geojson_point(geojson_point, threshold=100.0)
        
        # Assert
        assert created_edges is not None and len(created_edges) > 0
        assert len(marine_network_5km.nodes) == nodes_num + 1
        assert len(marine_network_5km.edges) >= edges_num + 1

    def test_add_nodes_with_edges_geojson_multipoint(
        self, marine_network_5km: MNetwork, 
        geojson_multipoint: geojson.MultiPoint):
        # Arrange
        nodes_num = len(marine_network_5km.nodes)
        edges_num = len(marine_network_5km.edges)
        points_num = len(geojson_multipoint.coordinates)
        
        # Act
        created_edges = marine_network_5km.add_geojson_multipoint(geojson_multipoint, threshold=100.0)
        
        # Assert
        assert created_edges is not None and len(created_edges) > 0
        assert len(marine_network_5km.nodes) == nodes_num + points_num
        assert len(marine_network_5km.edges) >= edges_num + points_num

    # def test_add_nodes_with_edges_geojson_feature_collection(
    #     self, marine_network_5km: MarnetExtend, 
    #     geojson_feature_collection: geojson.FeatureCollection):
    #     # Arrange
    #     nodes_num = len(marine_network_5km.nodes)
    #     edges_num = len(marine_network_5km.edges)
    #     points_num = len(geojson_feature_collection.features)

    #     # Act
    #     created_edges = marine_network_5km.add_geojson_feature_collection(geojson_feature_collection, threshold=100.0)
        
    #     # Assert
    #     assert created_edges is not None and len(created_edges) > 0
    #     assert len(marine_network_5km.nodes) == nodes_num + points_num
    #     assert len(marine_network_5km.edges) >= edges_num + points_num

    def test_add_geojson_feature_collection(self, marine_network_5km: MNetwork):
        # Arrange
        geojson_file_path = "apps/pathfinding/data/additional_points.geojson"
        feature_collection = geojson.load(open(geojson_file_path))
        nodes_num = len(marine_network_5km.nodes)
        edges_num = len(marine_network_5km.edges)
        points_num = len(feature_collection.features)

        # Act
        created_edges = marine_network_5km.add_geojson_feature_collection(feature_collection, threshold=100.0)
        
        # Assert
        assert created_edges is not None and len(created_edges) > 0
        assert len(marine_network_5km.nodes) == nodes_num + points_num
        assert len(marine_network_5km.edges) >= edges_num + points_num

