import os

from dagster import check, EventMetadataEntry, Field, StringSource
from dagster.cli.api import ExecuteRunArgs
from dagster.core.events import EngineEventData
from dagster.core.launcher import LaunchRunContext, RunLauncher
from dagster.serdes import ConfigurableClass, ConfigurableClassData, serialize_dagster_namedtuple

RENDER_SERVICE_ID_ENVIRONMENT_KEY = "RENDER_SERVICE_ID"


class RenderRunLauncher(RunLauncher, ConfigurableClass):
    """RunLauncher that starts a Render Job for each pipeline run.
 d
    Encapsulates each pipeline run in a separate, isolated invocation of ``dagster api execute_run``.

    You may configure a Dagster instance to use this RunLauncher by adding a section to your
    ``dagster.yaml`` like the following:

    .. code-block:: yaml

        run_launcher:
            module: dagster_render.launcher
            class: RenderRunLauncher
            config:
    """

    def __init__(
        self, render_api_token: str, render_service_id: str, inst_data: ConfigurableClassData
    ):
        check.str_param(render_api_token, "render_api_token")
        check.str_param(render_service_id, "render_service_id")
        check.inst_param(inst_data, "inst_data", ConfigurableClassData)

        self._render_api_token = render_api_token
        self._render_service_id = render_service_id
        self._inst_data = inst_data
        self._

        super().__init__()

    @classmethod
    def config_type(cls):
        return {
            "render_api_token": Field(str),
            "render_service_id": Field(
                StringSource, default_value={"env": RENDER_SERVICE_ID_ENVIRONMENT_KEY}
            ),
        }

    @property
    def inst_data(self):
        return self._inst_data

    @classmethod
    def from_config_value(cls, inst_data, config_value):
        return cls(inst_data=inst_data, **config_value)

    # test: dagster.yaml with config blob for run launcher and check into render_dagit project
    # make sure dagster_render is installed in the running process
    # add this to the dagster_render project

    def launch_run(self, context: LaunchRunContext) -> None:
        run = context.pipeline_run

        pipeline_origin = context.pipeline_code_origin
        repository_origin = pipeline_origin.repository_origin

        input_json = serialize_dagster_namedtuple(
            ExecuteRunArgs(
                pipeline_origin=pipeline_origin, pipeline_run_id=run.run_id, instance_ref=None,
            )
        )

        endpoint = f"https://api.render.com/v1/services/{self._render_service_id}/jobs"
        start_command = f"dagster api execute_run {input_json}"
        payload = {"startCommand": start_command}
        headers = {"Authorization": f"Bearer {self._render_api_token}"}

        self._instance.report_engine_event(
            "Creating Render run worker job",
            run,
            EngineEventData([EventMetadataEntry.text(run.run_id, "Run ID"),]),
            cls=self.__class__,
        )

        result = requests.post(endpoint, json=payload, headers=headers)

        if result.status_code != 201:
            self._instance.report_engine_event(
                "Render run worker job failed",
                run,
                EngineEventData(
                    [
                        EventMetadataEntry.int(status_code, "Render status_code"),
                        EventMetadataEntry.json(result.json(), "Render JSON response"),
                    ]
                ),
                cls=self.__class__,
            )
            self._instance.report_run_failed(run, message="Render run worker job creation failed")
            return

        result_json = result.json()

        self._instance.report_engine_event(
            "Render run worker job created",
            run,
            EngineEventData(
                [
                    EventMetadataEntry.text(result_json['id'], "Render job id"),
                    EventMetadataEntry.text(result_json['serviceId'], "Render service id"),
                    EventMetadataEntry.text(result_json['planId'], "Render plan id"),
                ]
            ),
            cls=self.__class__,
        )
        return

    def can_terminate(self, run_id):
        return False

    def terminate(self, run_id):
        return False

    def join(self, timeout=30):
        return
