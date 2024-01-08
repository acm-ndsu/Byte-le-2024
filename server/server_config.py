

class Config:
    __NUMBER_OF_GAMES_AGAINST_SAME_TEAM: int = 1
    __SLEEP_TIME_SECONDS_BETWEEN_RUNS: int = 150
    __END_DATETIME: str = "2030-01-01 00:00"  # Adjust this for every competition!!!!!
    __SLEEP_TIME_SECONDS_BETWEEN_VIS: int = 10

    @property
    def NUMBER_OF_GAMES_AGAINST_SAME_TEAM(self) -> int:
        return self.__NUMBER_OF_GAMES_AGAINST_SAME_TEAM

    @property
    def SLEEP_TIME_SECONDS_BETWEEN_RUNS(self) -> int:
        return self.__SLEEP_TIME_SECONDS_BETWEEN_RUNS

    @property
    def END_DATETIME(self) -> str:
        return self.__END_DATETIME

    @property
    def SLEEP_TIME_SECONDS_BETWEEN_VIS(self) -> int:
        return self.__SLEEP_TIME_SECONDS_BETWEEN_VIS
