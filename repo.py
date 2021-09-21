from dagster import op, graph, repository, ScheduleDefinition

basic_schedule = ScheduleDefinition(cron_schedule="*/5 * * * *", pipeline_name="basic")


@op
def foo():
    return 5


@graph
def basic():
    foo()


@repository
def my_repo():
    return [basic.to_job(), basic_schedule]
