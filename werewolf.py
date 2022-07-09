#
# werewolf.py
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
from typing import Dict, List

from aiwolf import (
    Agent,
    AttackContentBuilder,
    ComingoutContentBuilder,
    Content,
    GameInfo,
    GameSetting,
    Judge,
    Role,
    Species,
    ContentBuilder,
)
from utterance_generator import (
    Generator,
)
from utterance_recognizer import (
    Recognizer,
)
from aiwolf.constant import AGENT_NONE

from const import CONTENT_SKIP, JUDGE_EMPTY
from possessed import NlpWolfPossessed
import utils

class NlpWolfWerewolf(NlpWolfPossessed):
    """NlpWolf werewolf agent."""

    allies: List[Agent]
    """Allies."""
    humans: List[Agent]
    """Humans."""
    attack_vote_candidate: Agent
    """The candidate for the attack voting."""
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
    recognizer: Recognizer
    generator: Generator

    def __init__(self) -> None:
        """Initialize a new instance of NlpWolfWerewolf."""
        super().__init__()
        self.allies = []
        self.humans = []
        self.seer_co_list = []
        self.divination_reports = {}
        for i in range(1, 6):
            self.divination_reports[i] = []
        self.attack_vote_candidate = AGENT_NONE

        self.recognizer = Recognizer()
        self.generator = Generator()

    def initialize(self, game_info: GameInfo, game_setting: GameSetting) -> None:
        super().initialize(game_info, game_setting)
        self.allies = list(self.game_info.role_map.keys())
        self.humans = [a for a in self.game_info.agent_list if a not in self.allies]
        # Do comingout on the day that randomly selected from the 1st, 2nd and 3rd day.
        self.co_date = random.randint(1, 3)
        # Choose fake role randomly.
        self.fake_role = random.choice(
            [
                r
                for r in [Role.VILLAGER, Role.SEER, Role.MEDIUM]
                if r in self.game_info.existing_role_list
            ]
        )

    def get_fake_judge(self) -> Judge:
        """Generate a fake judgement."""
        # Determine the target of the fake judgement.
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
        # If the target is a human
        # and the number of werewolves found is less than the total number of werewolves,
        # judge as a werewolf with a probability of 0.3.
        result: Species = (
            Species.WEREWOLF
            if target in self.humans
            and len(self.werewolves) < self.num_wolves
            and random.random() < 0.3
            else Species.HUMAN
        )
        return Judge(self.me, self.game_info.day, target, result)

    def day_start(self) -> None:
        super().day_start()
        self.attack_vote_candidate = AGENT_NONE

    def whisper(self) -> Content:
        # Declare the fake role on the 1st day,
        # and declare the target of attack vote after that.
        if self.game_info.day == 0:
            return Content(ComingoutContentBuilder(self.me, self.fake_role))
        # Choose the target of attack vote.
        # Vote for one of the agent that did comingout.
        candidates = [a for a in self.get_alive(self.humans) if a in self.comingout_map]
        # Vote for one of the alive human agents if there are no candidates.
        if not candidates:
            candidates = self.get_alive(self.humans)
        # Declare which to vote for if not declare yet or the candidate is changed.
        if (
            self.attack_vote_candidate == AGENT_NONE
            or self.attack_vote_candidate not in candidates
        ):
            self.attack_vote_candidate = self.random_select(candidates)
            if self.attack_vote_candidate != AGENT_NONE:
                return Content(AttackContentBuilder(self.attack_vote_candidate))
        return CONTENT_SKIP

    def attack(self) -> Agent:
        return (
            self.attack_vote_candidate
            if self.attack_vote_candidate != AGENT_NONE
            else self.me
        )

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
                if cnt >= 3 and _talk.agent.agent_idx not in self.seer_co_list:  # 占い師の発言
                    self.seer_co_list.append(_talk.agent.agent_idx)
                    white = ("シロ" in talk) | ("白" in talk) | ("人狼じゃな" in talk) | ("人間" in talk) | ("人狼ではな" in talk)
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
        content.text = self.generator.generate(self, Role.WEREWOLF)
        return content
