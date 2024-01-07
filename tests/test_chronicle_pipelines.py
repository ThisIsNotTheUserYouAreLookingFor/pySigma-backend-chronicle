import pytest
from sigma.collection import SigmaCollection
from sigma.pipelines.common import windows_logsource_mapping
from sigma.backends.chronicle.chronicle import ChronicleBackend
from sigma.pipelines.chronicle import chronicle_windows_pipeline
from sigma.exceptions import SigmaTransformationError
