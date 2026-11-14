from typing import Annotated, Any

from pydantic import Field, StringConstraints

type Alphanumeric = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9_-]+$')]
type ConfType = dict[str, Any]
