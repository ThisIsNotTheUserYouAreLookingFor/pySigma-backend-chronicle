from sigma.pipelines.common import \
    logsource_windows, \
    generate_windows_logsource_items
from sigma.processing.transformations import FieldMappingTransformation, RuleFailureTransformation
from sigma.processing.conditions import LogsourceCondition, RuleProcessingItemAppliedCondition
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline

def logsource_windows() -> LogsourceCondition:
    return LogsourceCondition(
        product="windows"
    )

def chronicle_windows_pipeline():
    return ProcessingPipeline(
        name="Chronicle Windows log source conditions",
        allowed_backends={"chronicle"},
        priority=20,
        items=generate_windows_logsource_items("source", "WinEventLog:{source}") + [
            ProcessingItem(     # Field mappings
                identifier="chronicle_windows_field_mapping",
                transformation=FieldMappingTransformation({
                    "EventID": "metadata.product_event_type",
                })
            )
        ],
    )

