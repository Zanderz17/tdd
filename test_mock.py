from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app 

client = TestClient(app)

def test_get_coordinates_berlin():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = [{'lat': '52.52437', 'lon': '13.41053'}]
        response = client.get("/get_coordinates/?city_name=Berlin")
        assert response.status_code == 200
        assert response.json() == {"latitude": '52.52437', "longitude": '13.41053'}

def test_get_coordinates_city_not_found():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = []  
        response = client.get("/get_coordinates/?city_name=UnknownCity")
        assert response.status_code == 404

def test_calculate_distance():
    with patch('app.geodesic') as mock_geodesic:  
        mock_instance = mock_geodesic.return_value
        mock_instance.kilometers = 200  
        response = client.get("/get_distance/?lat1=52.52437&lon1=13.41053&lat2=48.8566&lon2=2.3522")
        assert response.status_code == 200
        assert response.json() == {"distance": 200}
