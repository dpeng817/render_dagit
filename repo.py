from dagster import op, graph, repository, ScheduleDefinition

basic_schedule = ScheduleDefinition(cron_schedule="*/20 * * * *", pipeline_name="basic")


@op
def foo():
    return 5


@graph
def basic():
    foo()


@repository
def my_repo():
    return [basic.to_job(), basic_schedule]
