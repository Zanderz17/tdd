from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app 

client = TestClient(app)

def test_get_coordinates_berlin_success():
    with patch('requests.get') as mock_get:
        # Mocking the JSON response to simulate a successful API response for Berlin.
        mock_get.return_value.json.return_value = [{'lat': '52.52437', 'lon': '13.41053'}]
        response = client.get("/get_coordinates/?city_name=Berlin")
        assert response.status_code == 200
        # Asserting that the returned JSON matches the expected values.
        assert response.json() == {"latitude": '52.52437', "longitude": '13.41053'}

def test_get_coordinates_berlin_fail():
    with patch('requests.get') as mock_get:
        # Mocking response to simulate an API response with incorrect coordinates.
        mock_get.return_value.json.return_value = [{'lat': '100.52437', 'lon': '13.41053'}]
        response = client.get("/get_coordinates/?city_name=Berlin")
        assert response.status_code == 200
        # Verifying that the JSON response does not match the incorrect coordinates.
        assert response.json() != {"latitude": '52.52437', "longitude": '13.41053'}

def test_get_coordinates_city_not_found_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = []  
        response = client.get("/get_coordinates/?city_name=UnknownCity")
        assert response.status_code == 404

def test_calculate_distance_success():
    with patch('app.geodesic') as mock_geodesic:
        mock_instance = mock_geodesic.return_value
        mock_instance.kilometers = 200  
        response = client.get("/get_distance/?lat1=52.52437&lon1=13.41053&lat2=48.8566&lon2=2.3522")
        assert response.status_code == 200
        assert response.json() == {"distance": 200}

def test_full_flow_from_fetching_coordinates_to_calculating_distance():
    # Mock 'requests.get' for fetching coordinates.
    with patch('requests.get') as mock_get, \
         patch('app.geodesic') as mock_geodesic:  # Mock 'geodesic' for distance calculation

        # Mocking the JSON response to simulate successful API responses for two cities.
        # Simulate Berlin coordinates
        mock_get.return_value.json.side_effect = [
            [{'lat': '52.52437', 'lon': '13.41053'}],  # First call for Berlin
            [{'lat': '48.8566', 'lon': '2.3522'}]       # Second call for Paris
        ]

        # Getting coordinates for Berlin
        berlin_response = client.get("/get_coordinates/?city_name=Berlin")
        assert berlin_response.status_code == 200
        assert berlin_response.json() == {"latitude": '52.52437', "longitude": '13.41053'}

        # Getting coordinates for Paris
        paris_response = client.get("/get_coordinates/?city_name=Paris")
        assert paris_response.status_code == 200
        assert paris_response.json() == {"latitude": '48.8566', "longitude": '2.3522'}

        # Mocking 'geodesic' to control the distance calculation.
        # Assuming the mocked distance between Berlin and Paris is 878 kilometers.
        mock_instance = mock_geodesic.return_value
        mock_instance.kilometers = 800

        # Calculate the distance using the fetched coordinates.
        distance_response = client.get("/get_distance/?lat1=52.52437&lon1=13.41053&lat2=48.8566&lon2=2.3522")
        assert distance_response.status_code == 200
        assert distance_response.json() == {"distance": 800}