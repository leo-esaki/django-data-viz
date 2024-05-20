import time
import uuid
from datetime import datetime
from typing import Dict, Optional

import pandas as pd

from .config import VIZ_CYCLE_LOOKBACK


def is_valid_uuid(val: str) -> bool:
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def last_cycle() -> datetime:
    """
    Returns the datetime for the last cycle based on VIZ_CYCLE_LOOKBACK.
    """
    return datetime.utcfromtimestamp(int(time.time() - VIZ_CYCLE_LOOKBACK))


def build_insert(
    for_time: datetime, period: str = "5Min", last_count: float = 0.0
) -> pd.DataFrame:
    rounded_time = pd.to_datetime(for_time).floor(period).to_pydatetime()

    return pd.DataFrame(
        [
            {
                "count": last_count,
                "period": rounded_time,
                "count_smoothed": last_count,
            }
        ]
    )


def build_empty(key_sum: Optional[str] = None) -> pd.DataFrame:
    to_build: Dict = {
        "_id": "NOTHING_TO_SHOW",
        "created": datetime.now().timestamp(),
    }

    if key_sum:
        to_build[key_sum] = 0

    return pd.DataFrame(pd.DataFrame([to_build]))
