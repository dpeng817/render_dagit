import requests

f = requests.post(
    "https://api.render.com/v1/services/srv-c5bo7gc6fj3e1haccvn0/jobs",
    json={"startCommand": "dagit --version"},
    headers={"Authorization": "Bearer rnd_QdNyC4eWg6xaH0qbJCqbKleIBMqs"},
)

f
