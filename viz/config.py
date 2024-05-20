#!/usr/bin/env python3.9

# import os
# import sys
import uuid
# from typing import Any
from decimal import Decimal, getcontext as get_decimal_context
# from dotenv import load_dotenv
# from threading import current_thread, main_thread
# from multiprocessing import current_process

# from loguru import logger

# from src.utils import round_for_bittensor

# PATH = os.path.expanduser("~/discord_api_keys.env")
# load_dotenv(PATH)

# Setup Decimal so that it's
# using 9 decimal places of detail
# get_decimal_context().prec = 9

# DEBUG = is_develop()

# DEBUG = DEBUG or feature_enabled("DEBUG")
# should be local, dev or prod
# ENV = load_env_var("ENV", required=True)
# IS_DEV = ENV.lower() == "dev"
# IS_LOCAL = ENV.lower() == "local"
# IS_PROD = ENV.lower() == "prod"
# TEMPLATE_PATH = "./static"

WALLET_LATENCY_MINIMUM = 3600
VOTE_LATENCY_MINIMUM = 5
COMPUTE_MINIMUM_VOTES = 3
ROUND_WINNERS = 3
ROUND_DURATION = 3600
ROUND_CURRENT_LOOKBACK = 3600 * 3

MINIMUM_COMPUTES_FOR_ROUND = 3
LOG_LEVEL = "INFO"

API_PORT = 5000


API_LOGFILE = "~/logs/api.log"
BOT_LOGFILE = "~/logs/bot.log"
VIZ_LOGFILE = "~/logs/viz.log"
PAY_LOGFILE = "~/logs/pay.log"
# os.makedirs(os.path.dirname(API_LOGFILE), exist_ok=True)
# os.makedirs(os.path.dirname(BOT_LOGFILE), exist_ok=True)
# os.makedirs(os.path.dirname(VIZ_LOGFILE), exist_ok=True)
# os.makedirs(os.path.dirname(PAY_LOGFILE), exist_ok=True)


# DISCORD STUFF
# DISCORD_TOKEN = load_env_var("DISCORD_TOKEN", "DISCORD_TOKEN_NOT_DEFINED")
# DISCORD_WALLET_HELP = load_env_var("DISCORD_WALLET_HELP", required=True).strip()
# DISCORD_WALLET_CUSTOM = load_env_var("DISCORD_WALLET_CUSTOM", required=True).strip()
# DISCORD_WALLET_CUSTOM_CONFIRM = load_env_var(
#     "DISCORD_WALLET_CUSTOM_CONFIRM", required=True
# ).strip()
# DISCORD_WALLET_MNEMONIC = load_env_var("DISCORD_WALLET_MNEMONIC", required=True).strip()
# DISCORD_ERROR = load_env_var("DISCORD_ERROR", required=True).strip()
# DISCORD_WALLET_INFORMATION = load_env_var(
#     "DISCORD_WALLET_INFORMATION", required=True
# ).strip()
# DISCORD_VERIFY_INFORMATION = load_env_var(
#     "DISCORD_VERIFY_INFORMATION", required=True
# ).strip()
# DISCORD_VERIFY_PENDING = load_env_var("DISCORD_VERIFY_PENDING", required=True).strip()
# DISCORD_VERIFY_SUCCESS = load_env_var("DISCORD_VERIFY_SUCCESS", required=True).strip()
# DISCORD_VERIFY_FAILURE = load_env_var("DISCORD_VERIFY_FAILURE", required=True).strip()


# DISCORD_FREQUENCY = int(load_env_var("DISCORD_FREQUENCY", 60))
# from bot.helpers import parse_discord_channels
from typing import List

# DISCORD_POSSIBLE_CHANNELS: List[str] = parse_discord_channels(
#     load_env_var(
#         #
#         "DISCORD_CHANNELS",
#         # Required, ...Optional keys
#         "(general, every=60, rand_min=60, rand_max=60)",
#     )
# )

# DISCORD_FUND_ALERT_CHANNEL = load_env_var("DISCORD_FUND_ALERT_CHANNEL", "alerts-dev")

IMAGE_FONT_SHADOW = 3
# IMAGE_FONT = load_env_var("IMAGE_FONT", required=True)


# Visualise stuff
VIZ_PORT = 5001

VIZ_CYCLE_DELAY = 30
VIZ_CHART_INTERVAL = "5Min"
VIZ_CYCLE_LOOKBACK = 86400

VIZ_CHART_SMOOTH = 3
VIZ_CHART_INTERVAL = "5Min"

VIZ_CHART_FOREGROUND = "white"
VIZ_CHART_BACKGROUND = "#1380af"

VIZ_CHART_FOREGROUND_BAD = "white"
VIZ_CHART_BACKGROUND_BAD = "#9b2226"

VIZ_CHART_FOREGROUND_NONE = "white"
VIZ_CHART_BACKGROUND_NONE = "#00000000"

VIZ_CHART_WIDTH = 1024
VIZ_CHART_HEIGHT = 512
VIZ_CHART_CACHE = 30

# Payout stuff
PAYOUT_WINNER_RATIO = Decimal(2.0)
PAYOUT_DAILY_MAXIMUM = Decimal( 1.0)
PAYOUT_BASIC_MAXIMUM = Decimal( 0.000075)
PAYOUT_USER_DAILY_MAX = Decimal(0.1)

# Maximum payment allowed for each vote or each winning vote
# PAYOUT_BASIC_MAXIMUM = round_for_bittensor(PAYOUT_BASIC_MAXIMUM)
# PAYOUT_WINNER_MAXIMUM = round_for_bittensor(PAYOUT_BASIC_MAXIMUM * PAYOUT_WINNER_RATIO)

# HR Of the day for payout creation
PAYOUT_CREATION_HOUR = "09:00",  # UTC

# HR Of the day for payout transaction
PAYOUT_TASK_HOUR = "09:25",  # UTC

# API Stuff
SUBMIT_BATCH_STAKE = 100_000
MINIMUM_COMPUTES_FOR_ROUND = 5
MINIMUM_COMPUTES_FOR_SUBMIT = 3

# BITTENSOR_NETWORK = load_env_var("BITTENSOR_NETWORK", required=True)
# BITTENSOR_SUBNET = int(load_env_var("BITTENSOR_SUBNET", required=True))
# BITTENSOR_WALLET_NAME = load_env_var("BITTENSOR_WALLET_NAME", required=True)

# GOOGLE_CREDS_LOCATION = load_env_var("GOOGLE_CREDS_LOCATION", required=True)
# GOOGLE_BUCKET = load_env_var("GOOGLE_BUCKET", required=True)

MONGO_DB = "test"
# MONGO_URL = load_env_var("MONGO_URL", required=True)
# DB_NO_INDEX = bool(load_env_var("MONGO_URL", False))

# REDIS_URL = load_env_var("REDIS_URL", "redis://localhost:6379")

# AUTH_SECRET = load_env_var("AUTH_SECRET", required=True)
# AUTH_SECRET_LOGIN = load_env_var("AUTH_SECRET_LOGIN", required=True)
# AUTH_WHITELIST = load_env_var("AUTH_WHITELIST", "")
# AUTH_ACCESS_TOKEN_EXPIRATION_TIME: int = int(
#     load_env_var("AUTH_ACCESS_TOKEN_EXPIRATION_TIME", 72 * 3600)
# )

# BASIC_AUTH_USERNAME = load_env_var("BASIC_AUTH_USERNAME", required=True)
# BASIC_AUTH_PASSWORD = load_env_var("BASIC_AUTH_PASSWORD", required=True)


WEIGHTS_MAX_AVERAGE_HOURS = 30


CHEATER_DELAY = 3600 * 12
CHEATER_THRESHOLD = 0.3
CHEATER_LOOKBACK = 86400 * 7


# Sanitize users but keep their sanitized ID the same
ID_NAMESPACE = uuid.UUID("aefe7ded-2411-4ab2-8458-97468b6d4c36")
VERIFICATION_NAMESPACE = uuid.UUID("8e075006-9304-40d2-a278-a4f6d919e6df")


def id_to_namespace(inbound_id: str, which_namespace: uuid.UUID = ID_NAMESPACE) -> str:
    return str(uuid.uuid5(which_namespace, str(inbound_id)))


MANAGE_URL = "https://manage.tensoralchemy.ai"
VERIFY_URL = "https://verify.tensoralchemy.ai"

# BACKEND_SENTRY_DSN: str = load_env_var("BACKEND_SENTRY_DSN", required=True)
