import requests

# f = requests.post(
#     "https://api.render.com/v1/services/srv-c5bo7gc6fj3e1haccvn0/jobs",
#     json={"startCommand": "dagit --version"},
#     headers={"Authorization": "Bearer rnd_QdNyC4eWg6xaH0qbJCqbKleIBMqs"},
# )

# f = requests.post(
#     "https://api.render.com/v1/services/",
#     headers={"Authorization": "Bearer rnd_QdNyC4eWg6xaH0qbJCqbKleIBMqs"},
# )

# job_id job-c5its6v6d9kpo8jo7t2g

f = requests.get(
    "https://api.render.com/v1/services/srv-c5bo7gc6fj3e1haccvn0/jobs/job-c5its6v6d9kpo8jo7t2g",
    json={"startCommand": "dagit --version"},
    headers={"Authorization": "Bearer rnd_QdNyC4eWg6xaH0qbJCqbKleIBMqs"},
)

f
