from sigma.rule import SigmaRule
from sigma.conversion.base import TextQueryBackend
from sigma.types import SigmaRegularExpressionFlag
from sigma.conditions import ConditionItem, ConditionAND, ConditionNOT, ConditionOR
import sigma
from typing import Any, Callable, ClassVar, Dict, Optional, List, Tuple


class ChronicleBackend(TextQueryBackend):
    name: ClassVar[
        str
    ] = "Chronicle Backend that can provide plain UDM queries"  # A descriptive name of the backend
    formats: ClassVar[
        Dict[str, str]
    ] = {  # Output formats provided by the backend as name -> description mapping. The name should match to finalize_output_<name>.
        "default": "Plain UDM queries",
    }
    requires_pipeline: ClassVar[
        bool
    ] = True  # Does the backend requires that a processing pipeline is provided?
    group_expression: ClassVar[str] = "({expr})"
    or_token: ClassVar[str] = "OR"
    and_token: ClassVar[str] = "AND"
    not_token: ClassVar[str] = "NOT"
    eq_token: ClassVar[str] = "="
    str_quote: ClassVar[str] = '"'
    bool_values: ClassVar[
        Dict[bool, Optional[str]]
    ] = {  # Values to which boolean values are mapped.
        True: "true",
        False: "false",
    }
    precedence: ClassVar[Tuple[ConditionItem, ConditionItem, ConditionItem]] = (
        ConditionNOT,
        ConditionOR,
        ConditionAND,
    )
    re_expression: ClassVar[str] = "{field}=/{regex}/ {flag_i}"
    re_escape_char: ClassVar[str] = "\\"
    re_flags: ClassVar[Dict[SigmaRegularExpressionFlag, str]] = {
        SigmaRegularExpressionFlag.IGNORECASE: "nocase",
    }

    def __init__(
        self,
        processing_pipeline: Optional[
            "sigma.processing.pipeline.ProcessingPipeline"
        ] = None,
        collect_errors: bool = False,
        min_time: str = "-30d",
        max_time: str = "now",
        query_settings: Callable[[SigmaRule], Dict[str, str]] = lambda x: {},
        output_settings: Dict = {},
        **kwargs,
    ):
        super().__init__(processing_pipeline, collect_errors, **kwargs)
        self.query_settings = query_settings
        self.output_settings = {
            "dispatch.earliest_time": min_time,
            "dispatch.latest_time": max_time,
        }
        self.output_settings.update(output_settings)
