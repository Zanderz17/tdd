from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app 

client = TestClient(app)

def test_get_coordinates_lima_success():
    with patch('requests.get') as mock_get:
        # Mocking the JSON response to simulate a successful API response for Lima.
        mock_get.return_value.json.return_value = [{'lat': '-12.0464', 'lon': '-77.0428'}]
        response = client.get("/get_coordinates/?city_name=Lima")
        assert response.status_code == 200
        # Asserting that the returned JSON matches the expected values.
        assert response.json() == {"latitude": '-12.0464', "longitude": '-77.0428'}

def test_get_coordinates_lima_fail():
    with patch('requests.get') as mock_get:
        # Mocking response to simulate an API response with incorrect coordinates.
        mock_get.return_value.json.return_value = [{'lat': '100.52437', 'lon': '-77.0428'}]
        response = client.get("/get_coordinates/?city_name=Lima")
        assert response.status_code == 200
        # Verifying that the JSON response does not match the incorrect coordinates.
        assert response.json() != {"latitude": '-12.0464', "longitude": '-77.0428'}

def test_get_coordinates_city_not_found_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = []  
        response = client.get("/get_coordinates/?city_name=UnknownCity")
        assert response.status_code == 404

def test_calculate_distance_success():
    with patch('app.geodesic') as mock_geodesic:
        mock_instance = mock_geodesic.return_value
        mock_instance.kilometers = 2451  # Sample distance between Lima and Santiago, Chile
        response = client.get("/get_distance/?lat1=-12.0464&lon1=-77.0428&lat2=-33.4569&lon2=-70.6483")
        assert response.status_code == 200
        assert response.json() == {"distance": 2451}

def test_full_fetching_coordinates_and_calculate_distance():
    # Mock 'requests.get' for fetching coordinates.
    with patch('requests.get') as mock_get, \
         patch('app.geodesic') as mock_geodesic:  # Mock 'geodesic' for distance calculation

        # Mocking the JSON response to simulate successful API responses for two cities.
        # Simulate Lima coordinates
        mock_get.return_value.json.side_effect = [
            [{'lat': '-12.0464', 'lon': '-77.0428'}],  # First call for Lima
            [{'lat': '-33.4569', 'lon': '-70.6483'}]   # Second call for Santiago, Chile
        ]

        # Getting coordinates for Lima
        lima_response = client.get("/get_coordinates/?city_name=Lima")
        assert lima_response.status_code == 200
        assert lima_response.json() == {"latitude": '-12.0464', "longitude": '-77.0428'}

        # Getting coordinates for Santiago, Chile
        santiago_response = client.get("/get_coordinates/?city_name=Santiago")
        assert santiago_response.status_code == 200
        assert santiago_response.json() == {"latitude": '-33.4569', "longitude": '-70.6483'}

        # Mocking 'geodesic' to control the distance calculation.
        # Assuming the mocked distance between Lima and Santiago is 2451 kilometers.
        mock_instance = mock_geodesic.return_value
        mock_instance.kilometers = 2451

        # Calculate the distance using the fetched coordinates.
        distance_response = client.get("/get_distance/?lat1=-12.0464&lon1=-77.0428&lat2=-33.4569&lon2=-70.6483")
        assert distance_response.status_code == 200
        assert distance_response.json() == {"distance": 2451}
