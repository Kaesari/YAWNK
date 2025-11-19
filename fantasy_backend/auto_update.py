
# import time
# import os
# import traceback
# import subprocess
# import logging

# from contests.views import get_current_game_week_data, group_matches_by_day

# # Always run inside the project directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Set up logging to track the script's activity
# logging.basicConfig(filename='game_week_update.log', level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# while True:
#     try:
#         # Fetch current game week data
#         current_game_week = get_current_game_week_data()
#         fixtures_by_day, has_started, has_ended = group_matches_by_day(current_game_week['id'] - 1)

#         # print(has_started)
#         # print(has_ended)

#         # Check if the game has both started and ended, then update scores
#         if has_started and has_ended:
#             logging.info("Running update_scores...")
#             subprocess.run(['python', 'manage.py', 'update_scores'], cwd=BASE_DIR)
#             logging.info("Scores updated successfully.")

#         logging.info("Sleeping for 2 minutes...")
#         time.sleep(60 * 2)

#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#         logging.error(traceback.format_exc())
#         logging.info("Sleeping for 30 seconds before retrying...")
#         time.sleep(30)


import time
import os
import traceback
import subprocess
import logging

from contests.views import get_current_game_week_data, group_matches_by_day
from contests.payouts import payout_all_league_winners_for_gameweek  # <-- Import the batch payout function

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename='game_week_update.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

while True:
    try:
        # Fetch current game week data
        current_game_week = get_current_game_week_data()
        fixtures_by_day, has_started, has_ended = group_matches_by_day(current_game_week['id'] - 1)

        # Check if the game has both started and ended, then update scores
        if has_started and has_ended:
            logging.info("Running update_scores...")
            subprocess.run(['python', 'manage.py', 'update_scores'], cwd=BASE_DIR)
            logging.info("Scores updated successfully.")

            # Run payouts for all leagues in the ended gameweek
            logging.info("Running payouts for completed gameweek...")
            payout_results = payout_all_league_winners_for_gameweek(current_game_week['id'] - 1)
            logging.info(f"Payout results: {payout_results}")

        logging.info("Sleeping for 2 minutes...")
        time.sleep(60 * 2)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.error(traceback.format_exc())
        logging.info("Sleeping for 30 seconds before retrying...")
        time.sleep(30)

