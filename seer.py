#
# seer.py
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

from collections import deque
from typing import Dict, List, Optional
import random
from aiwolf import (
    Agent,
    ComingoutContentBuilder,
    Content,
    DivinedResultContentBuilder,
    GameInfo,
    GameSetting,
    Judge,
    Role,
    Species,
    ContentBuilder,
    VoteContentBuilder,
)
from utterance_generator import (
    Generator,
)
from aiwolf.constant import AGENT_NONE

from const import CONTENT_SKIP
from villager import NlpWolfVillager


class NlpWolfSeer(NlpWolfVillager):
    """NlpWolf seer agent."""

    me: Agent
    """Myself."""
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
    vote_candidates: List[Agent]
    """List of who to vote"""
    generator: Generator

    def __init__(self) -> None:
        """Initialize a new instance of NlpWolfSeer."""
        super().__init__()
        self.co_date = 0
        self.has_co = False
        self.my_judge_queue = deque()
        self.not_divined_agents = []
        self.werewolves = []
        self.seer_co_list = []
        self.divination_reports = {}
        self.vote_candidates = []
        self.generator = Generator()

    def initialize(self, game_info: GameInfo, game_setting: GameSetting) -> None:
        super().initialize(game_info, game_setting)
        self.co_date = 3
        self.has_co = False
        self.my_judge_queue.clear()
        self.not_divined_agents = self.get_others(self.game_info.agent_list)
        self.werewolves.clear()
        self.seer_co_list.clear()
        self.divination_reports.clear()
        self.vote_candidates.clear()

    def day_start(self) -> None:
        super().day_start()
        # Process a divination result.
        judge: Optional[Judge] = self.game_info.divine_result
        if judge is not None:
            self.my_judge_queue.append(judge)
            if judge.target in self.not_divined_agents:
                self.not_divined_agents.remove(judge.target)
            if judge.result == Species.WEREWOLF:
                self.werewolves.append(judge.target)

    def update(self, game_info: GameInfo) -> None:
        self.game_info = game_info


    def talk(self) -> Content:
        content: Content = Content(ContentBuilder())
        content.text = self.generator.generate(self, Role.SEER)
        return content

    def divine(self) -> Agent:
        # Divine a agent randomly chosen from undivined agents.
        target: Agent = self.random_select(self.not_divined_agents)
        return target if target != AGENT_NONE else self.me

    def vote(self) -> Agent:
        # todo
        return (
            random.choice(self.vote_candidates)
            if len(self.vote_candidates)
            else Agent(random.choice([1,2,3,4,5]))
        )