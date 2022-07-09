#
# villager.py
#
# Copyright 2022 Neccolini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import datetime
import time
from typing import Dict, List

from aiwolf import (
    AbstractPlayer,
    Agent,
    Content,
    GameInfo,
    GameSetting,
    Judge,
    Role,
    Species,
    Status,
    Talk,
    Topic,
    Utterance,
    ContentBuilder,
    VoteContentBuilder,
)

from aiwolf.constant import AGENT_NONE

from utterance_generator import (
    Generator,
)
from utterance_recognizer import (
    Recognizer,
)
import utils


class NlpWolfVillager(AbstractPlayer):
    """NlpWolf villager agent."""
    
    me: Agent
    """Myself."""
    # vote_candidate: Agent
    """Candidate for voting."""
    game_info: GameInfo
    """Information about current game."""
    game_setting: GameSetting
    """Settings of current game."""
    comingout_map: Dict[Agent, Role]
    """Mapping between an agent and the role it claims that it is."""
    divination_reports: Dict[int, List[Judge]]
    """Time series of divination reports."""
    identification_reports: List[Judge]
    """Time series of identification reports."""
    talk_list_head: int
    """Index of the talk to be analysed next."""
    long_uttrs: list
    """List of little tweets in the game"""
    short_uter: list
    """List of little tweets(shorter) in the game"""
    seer_co_list: List[int]
    """List of who came out as seer."""
    talk_lst_idx: int
    """どこまでtalk_listの中身を見たか"""
    recognizer: Recognizer
    generator: Generator

    def __init__(self) -> None:
        """Initialize a new instance of NlpWolfVillager."""

        # 乱数の設定
        now = datetime.datetime.now()
        random.seed(int(time.mktime(now.timetuple())))

        self.me = AGENT_NONE
        self.vote_candidate = AGENT_NONE
        self.game_info = None  # type: ignore
        self.comingout_map = {}
        self.divination_reports = []
        self.identification_reports = []
        self.talk_list_head = 0
        self.seer_co_list = []
        self.divination_reports = {}
        for i in range(1, 6):
            self.divination_reports[i] = []
        self.talk_end = False

        self.recognizer = Recognizer()
        self.generator = Generator()

    def is_alive(self, agent: Agent) -> bool:
        """Return whether the agent is alive.

        Args:
            agent: The agent.

        Returns:
            True if the agent is alive, otherwise false.
        """
        return self.game_info.status_map[agent] == Status.ALIVE

    def get_others(self, agent_list: List[Agent]) -> List[Agent]:
        """Return a list of agents excluding myself from the given list of agents.

        Args:
            agent_list: The list of agent.

        Returns:
            A list of agents excluding myself from agent_list.
        """
        return [a for a in agent_list if a != self.me]

    def get_alive(self, agent_list: List[Agent]) -> List[Agent]:
        """Return a list of alive agents contained in the given list of agents.

        Args:
            agent_list: The list of agents.

        Returns:
            A list of alive agents contained in agent_list.
        """
        return [a for a in agent_list if self.is_alive(a)]

    def get_alive_others(self, agent_list: List[Agent]) -> List[Agent]:
        """Return a list of alive agents that is contained in the given list of agents
        and is not equal to myself.

        Args:
            agent_list: The list of agents.

        Returns:
            A list of alie agents that is contained in agent_list
            and is not equal to mysef.
        """
        return self.get_alive(self.get_others(agent_list))

    def random_select(self, agent_list: List[Agent]) -> Agent:
        """Return one agent randomly chosen from the given list of agents.

        Args:
            agent_list: The list of agents.

        Returns:
            A agent randomly chosen from agent_list.
        """
        return random.choice(agent_list) if agent_list else AGENT_NONE

    def initialize(self, game_info: GameInfo, game_setting: GameSetting) -> None:
        self.game_info = game_info
        self.game_setting = game_setting
        self.me = game_info.me
        # Clear fields not to bring in information from the last game.
        self.comingout_map.clear()
        self.divination_reports.clear()
        self.identification_reports.clear()
        self.seer_co_list.clear()

    def day_start(self) -> None:
        self.talk_list_head = 0
        self.talk_end = False
        self.vote_candidate = AGENT_NONE

    def update(self, game_info: GameInfo) -> None:
        self.game_info = game_info
        # ここで、他人の発言を見て、それを解釈し、次にあてられたときに発言する内容を決定、また投票先の情報などを変更したりする
        # self.recognizer.recognize(game_info)

    def talk(self) -> Content:
        if self.game_info.day == 1:
            for _talk in self.game_info.talk_list:
                talk = _talk.text
                cnt = 0
                cnt += "白" in talk
                cnt += "シロ" in talk
                cnt += "黒" in talk
                cnt += "クロ" in talk
                cnt += "人狼" in talk
                cnt += "人間" in talk
                cnt += "占った" in talk
                cnt += "占い" in talk
                cnt += "結果" in talk
                cnt += "Agent" in talk
                cnt -= ("把握" in talk) * 2
                cnt -= ("ok" in talk) * 2
                cnt -= ("了解" in talk) * 2
                cnt -= ("承知" in talk) * 2
                cnt -= ("なるほど" in talk) * 2
                cnt -= ("わかった" in talk) * 2
                cnt -= ("わかりました" in talk) * 2
                if (
                    cnt >= 3 and _talk.agent.agent_idx not in self.seer_co_list
                ):  # 占い師の発言
                    self.seer_co_list.append(_talk.agent.agent_idx)
                    white = (
                        ("シロ" in talk)
                        | ("白" in talk)
                        | ("人狼じゃな" in talk)
                        | ("人間" in talk)
                        | ("人狼ではな" in talk)
                    )
                    result = Species.HUMAN if white else Species.WEREWOLF
                    judge: Judge = Judge(
                        Agent(_talk.agent.agent_idx),
                        self.game_info.day,
                        Agent(utils.extract_agent_int(_talk.text)),
                        result,
                    )
                    if _talk.agent.agent_idx not in self.divination_reports.keys():
                        self.divination_reports[_talk.agent.agent_idx] = []
                    self.divination_reports[_talk.agent.agent_idx].append(judge)
        content: Content = Content(ContentBuilder())
        content.text = self.generator.generate(self, Role.VILLAGER)
        return content

    def vote(self) -> Agent:
        # todo
        return self.vote_candidate if self.vote_candidate != AGENT_NONE else self.me

    def attack(self) -> Agent:
        raise NotImplementedError()

    def divine(self) -> Agent:
        raise NotImplementedError()

    def guard(self) -> Agent:
        raise NotImplementedError()

    def whisper(self) -> Content:
        raise NotImplementedError()

    def finish(self) -> None:
        pass
