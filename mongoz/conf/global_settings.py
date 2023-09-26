from functools import cached_property
from typing import TYPE_CHECKING, Dict, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from mongoz.exceptions import OperatorInvalid

if TYPE_CHECKING:
    from mongoz import Expression


class MongozSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", ignored_types=(cached_property,))
    ipython_args: List[str] = ["--no-banner"]
    ptpython_config_file: str = "~/.config/ptpython/config.py"

    filter_operators: Dict[str, str] = {
        "exact": "eq",
        "nexact": "neq",
        "contains": "contains",
        "in": "in_",
        "nin": "not_in",
        "or": "or_",
        "pattern": "pattern",
        "where": "where",
        "and": "and_",
        "gte": "gte",
        "gt": "gt",
        "lt": "lt",
        "lte": "lte",
    }

    def get_operator(self, name: str) -> "Expression":
        """
        Returns the operator associated to the given expression passed.
        """
        from mongoz.core.db.querysets.operators import Q

        if name not in self.filter_operators:
            raise OperatorInvalid(f"`{name}` is not a valid operator.")
        return getattr(Q, self.filter_operators[name])
