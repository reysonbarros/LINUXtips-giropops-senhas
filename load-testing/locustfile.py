from locust import HttpUser, task

class GiropopsSenhasTestPerformance(HttpUser):
    @task
    def test_performance(self):
        self.client.post("/") # Criar senhas automaticamente
        self.client.get("/api/senhas") # Listar senhas