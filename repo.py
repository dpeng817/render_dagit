from dagster import op, graph, repository


@op
def foo():
    return 5


@graph
def basic():
    foo()


@repository
def my_repo():
    return [basic.to_job()]
