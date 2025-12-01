import requests

API_URL = "http://localhost:8080"

class ControllerProbManager:
    def __init__(self):
        self.session = requests.Session()

    def get_problems(self):
        r = self.session.get(f"{API_URL}/problems")
        return r.json()

    def add_problem(self, title, description, input_ex, output_ex):
        data = {
            "title": title,
            "description": description,
            "inputExample": input_ex,
            "outputExample": output_ex
        }
        r = self.session.post(f"{API_URL}/problems", json=data)
        return r.json()

    def delete_problem(self, title):
        r = self.session.delete(f"{API_URL}/problems/{title}")
        return r.json()

    def evaluate_code(self, code, expected):
        data = {
            "code": code,
            "expected": expected
        }
        r = self.session.post(f"{API_URL}/evaluate", json=data)
        return r.json()
    def evaluate_problem(self, data):
        try:
            r = self.session.post(f"{API_URL}/evaluate", json=data, timeout=10)
            return r.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
