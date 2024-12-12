# import os
# import hashlib
# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# logger = logging.getLogger(__name__)


#     challengeflag_2 = os.environ.get("CHALLENGEKEY_2")
#     teamflag = os.environ.get("TEAMKEY")
#     combined_flag_2 = challengeflag_2 + teamflag

# #! Second flag (robots.txt)
#     if combined_flag:
#         hashed_flag_2 = "FF{" + hashlib.sha256(combined_flag_2.encode()).hexdigest() + "}"
#         logger.info("Flag successfully created and hashed for team %s: %s", team_id, hashed_flag_2)
#     else:
#         logger.error(
#             "Failed to create flag. Ensure TEAMKEY and CHALLENGEKEY are set in environment variables."
#         )
#         hashed_flag = "FLAG_NOT_DEFINED"