#
# possessed.py
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
from collections import deque
from typing import Dict, List

from aiwolf import (
    Agent,
    ComingoutContentBuilder,
    Content,
    DivinedResultContentBuilder,
    GameInfo,
    GameSetting,
    IdentContentBuilder,
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

from const import CONTENT_SKIP, JUDGE_EMPTY
from villager import NlpWolfVillager


class NlpWolfPossessed(NlpWolfVillager):
    """NlpWolf possessed agent."""

    fake_role: Role
    """Fake role."""
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
        """Initialize a new instance of NlpWolfPossessed."""
        super().__init__()
        self.fake_role = Role.SEER
        self.co_date = 0
        self.has_co = False
        self.my_judgee_queue = deque()
        self.not_judged_agents = []
        self.num_wolves = 0
        self.werewolves = []
        self.seer_co_list = []
        self.divination_reports = {}
        self.vote_candidates = []

        self.generator = Generator()

    def initialize(self, game_info: GameInfo, game_setting: GameSetting) -> None:
        super().initialize(game_info, game_setting)
        self.fake_role = Role.SEER
        self.co_date = 1
        self.has_co = False
        self.my_judgee_queue.clear()
        self.not_judged_agents = self.get_others(self.game_info.agent_list)
        self.num_wolves = game_setting.role_num_map.get(Role.WEREWOLF, 0)
        self.werewolves.clear()
        self.seer_co_list.clear()
        self.divination_reports.clear()
        self.vote_candidates.clear()

    def get_fake_judge(self) -> Judge:
        """Generate a fake judgement."""
        target: Agent = AGENT_NONE
        if self.fake_role == Role.SEER:  # Fake seer chooses a target randomly.
            if self.game_info.day != 0:
                target = self.random_select(self.get_alive(self.not_judged_agents))
        elif self.fake_role == Role.MEDIUM:
            target = (
                self.game_info.executed_agent
                if self.game_info.executed_agent is not None
                else AGENT_NONE
            )
        if target == AGENT_NONE:
            return JUDGE_EMPTY
        # Determine a fake result.
        # If the number of werewolves found is less than the total number of werewolves,
        # judge as a werewolf with a probability of 0.5.
        result: Species = (
            Species.WEREWOLF
            if len(self.werewolves) < self.num_wolves and random.random() < 0.5
            else Species.HUMAN
        )
        return Judge(self.me, self.game_info.day, target, result)

    def day_start(self) -> None:
        super().day_start()
        # Process the fake judgement.
        judge: Judge = self.get_fake_judge()
        if judge != JUDGE_EMPTY:
            self.my_judgee_queue.append(judge)
            if judge.target in self.not_judged_agents:
                self.not_judged_agents.remove(judge.target)
            if judge.result == Species.WEREWOLF:
                self.werewolves.append(judge.target)

    def talk(self) -> Content:
        content: Content = Content(ContentBuilder())
        content.text = self.generator.generate(self, Role.POSSESSED)
        return content

    def update(self, game_info: GameInfo) -> None:
        self.game_info = game_info

    def vote(self) -> Agent:
        # todo
        return (
            random.choice(self.vote_candidates)
            if len(self.vote_candidates)
            else Agent(random.choice([1, 2, 3, 4, 5]))
        )
