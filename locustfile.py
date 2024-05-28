from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):
    wait_time = between(1, 5) 

    @task
    def get_coordinates(self):
        self.client.get("/get_coordinates/?city_name=Lima")

    @task
    def get_distance(self):
        self.client.get("/get_distance/?lat1=51.5074&lon1=-0.1278&lat2=48.8566&lon2=2.3522")
