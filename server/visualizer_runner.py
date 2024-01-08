# IMPORTANT NOTE: DO **NOT** REMOVE IMPORTS THAT APPEAR UNUSED. They are still needed for the SQLAlchemy DB connection

import datetime
import sys
import time
import json
import os
import shutil
import subprocess
import schedule

from server.crud import crud_tournament
from server.database import SessionLocal
from server.models.run import Run
from server.models.tournament import Tournament
from server.models.turn import Turn
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.university import University
from server.models.submission import Submission
from server.server_config import Config


class DB:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        self.db.begin()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


class visualizer_runner:
    def __init__(self):

        # Current tournament id of logs
        self.tournament_id: int = 0

        self.logs_path: str = os.path.join('server', 'vis_temp')

        (schedule.every(Config().SLEEP_TIME_SECONDS_BETWEEN_VIS).seconds
         .until(Config().END_DATETIME)
         .do(self.internal_runner))

        (schedule.every().day.at(str(Config().END_DATETIME.split()[-1]))
         .do(self.delete_vis_temp))

        try:
            while 1:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f'Ending visualizer due to KeyboardInterrupt')
        except Exception as e:
            print(f'Ending visualizer due to {e}')

    # Get new logs from the latest tournament
    def internal_runner(self) -> None:
        tournament: Tournament | None = self.get_latest_tournament()

        if tournament is None:
            print('No tournament is in the database.')
            return

        if self.tournament_id != tournament.tournament_id:
            print("Getting new logs")
            self.get_latest_log_files(tournament)
            self.tournament_id = tournament.tournament_id
            print(f'Tournament id: {self.tournament_id}')
        self.visualizer_loop()

    # Delete visual logs path at end of competition
    def delete_vis_temp(self) -> None:
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        else:
            shutil.rmtree(self.logs_path)
            os.mkdir(self.logs_path)

    def get_latest_log_files(self, tournament: Tournament) -> None:
        self.delete_vis_temp()

        print("Getting latest log files")
        run: Run
        logs: dict[Run, list[Turn]] = {run: run.turns for run in tournament.runs if len(run.turns) > 0}

        log: list[Turn]
        for run, log in logs.items():
            # Take logs and copy into directory
            id_dir = os.path.join(self.logs_path, str(log[0].run_id))
            os.mkdir(id_dir)
            logs_dir = os.path.join(id_dir, 'logs')
            os.mkdir(logs_dir)
            for turn in log:
                with open(os.path.join(logs_dir, f'turn_{turn.turn_number:04d}.json'), "w") as fl:
                    fl.write(str(turn.turn_data, 'utf-8'))
            with open(os.path.join(logs_dir, 'results.json'), 'x') as fl:
                json.dump(json.loads(run.results.decode('utf-8')), fl)

            shutil.copy(os.path.join(os.getcwd(), 'launcher.pyz'), id_dir)
            shutil.copy(os.path.join(os.getcwd(), 'server', 'runners', 'vis_runner.sh'), id_dir)
            shutil.copy(os.path.join(os.getcwd(), 'server', 'runners', 'vis_runner.bat'), id_dir)
            shutil.copytree(os.path.join(os.getcwd(), 'visualizer'), os.path.join(id_dir, 'visualizer'))
        else:
            print('No logs for tournament\n')

    def get_latest_tournament(self) -> Tournament | None:
        print("Getting Latest Tournament")
        with DB() as db:
            return crud_tournament.get_latest_tournament(db, with_turns=True) if not None else None

    def visualizer_loop(self) -> None:
        print('in visualizer_loop()')

        try:
            print('trying to open os.devnull')
            f = open(os.devnull, 'w')
            print('opened os.devnull')
            for id in os.listdir(self.logs_path):
                print(f'ID in for loop: {id}')
                idpath = os.path.join(self.logs_path, str(id))
                print(f'ID path made from id: {idpath}')

                p = subprocess.Popen('bash vis_runner.sh', stdout=f, cwd=idpath, shell=True) \
                    if sys.platform != 'win32' \
                    else subprocess.Popen('vis_runner.bat', stdout=f, cwd=idpath, shell=True)

                print('Created p object to start running visualizer')

                stdout, stderr = p.communicate()

                print('made it past creating stdout and stderr')

                print(f'stdout: {stdout}\nstderr: {stderr}')
            else:
                print('No ids in log path')

        except PermissionError:
            print("Whoops")

        finally:
            print('Job done\n')

if __name__ == "__main__":
    visualizer_runner()
