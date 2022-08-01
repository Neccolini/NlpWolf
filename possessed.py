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
import re
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
    Status,
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
import utils


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

    def get_alive(self) -> List[int]:
        alive_list = []
        for i in range(1, 6):
            agent = Agent(i)
            if self.game_info.status_map[agent] == Status.ALIVE:
                alive_list.append(i)
        return alive_list

    def get_fake_judge(self) -> Judge:
        """Generate a fake judgement."""
        target: Agent = AGENT_NONE
        if self.fake_role == Role.SEER:  # Fake seer chooses a target randomly.
            if self.game_info.day != 0:
                target = self.random_select(self.get_alive())
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
        talk_this_turn = ""
        for _talk in self.game_info.talk_list:
            talk = _talk.text
            cnt = 0
            cnt += bool(re.match(talk, r"Agent[0\d]が白")) * 2
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
            cnt -= "だれ" in talk
            cnt -= ("把握" in talk) * 2
            cnt -= ("ok" in talk) * 2
            cnt -= ("了解" in talk) * 2
            cnt -= ("承知" in talk) * 2
            cnt -= ("なるほど" in talk) * 2
            cnt -= ("わかった" in talk) * 2
            cnt -= ("わかりました" in talk) * 2
            if cnt >= 3 and _talk.agent.agent_idx not in self.seer_co_list:  # 占い師の発言
                self.seer_co_list.append(_talk.agent.agent_idx)
                talk_target = utils.extract_agent_int(_talk.text)
                white = (
                    ("シロ" in talk)
                    | ("白" in talk)
                    | ("人狼じゃな" in talk)
                    | ("人間" in talk)
                    | ("人狼ではな" in talk)
                )
                result = Species.HUMAN if white else Species.WEREWOLF

                if result == Species.WEREWOLF and talk_target != self.me.agent_idx:
                    self.vote_candidates.append(Agent(talk_target))
                judge: Judge = Judge(
                    Agent(_talk.agent.agent_idx),
                    self.game_info.day,
                    Agent(utils.extract_agent_int(_talk.text)),
                    result,
                )
                if _talk.agent.agent_idx not in self.divination_reports.keys():
                    self.divination_reports[_talk.agent.agent_idx] = []
                self.divination_reports[_talk.agent.agent_idx].append(judge)
            if (
                cnt >= 3
                and self.game_info.day == 2
                and len(self.divination_reports[_talk.agent.agent_idx]) < 2
            ):
                talk_target = utils.extract_agent_int(_talk.text)
                white = (
                    ("シロ" in talk)
                    | ("白" in talk)
                    | ("人狼じゃな" in talk)
                    | ("人間" in talk)
                    | ("人狼ではな" in talk)
                )
                result = Species.HUMAN if white else Species.WEREWOLF

                if result == Species.WEREWOLF and talk_target != self.me.agent_idx:
                    # print("self.vote_candidates ", talk_target)
                    self.vote_candidates.append(Agent(talk_target))
                judge: Judge = Judge(
                    Agent(_talk.agent.agent_idx),
                    self.game_info.day,
                    Agent(utils.extract_agent_int(_talk.text)),
                    result,
                )
                """
                if _talk.agent.agent_idx not in self.divination_reports.keys():
                    self.divination_reports[_talk.agent.agent_idx] = []
                """
                self.divination_reports[_talk.agent.agent_idx].append(judge)
            # 自分が疑われていた場合反論する
            if (
                ">>" + self.me.__str__()
            ) in talk and _talk.agent.agent_idx != self.me.agent_idx:
                suspected_cnt = 0
                suspected_cnt += "黒" in talk
                suspected_cnt += "クロ" in talk
                suspected_cnt += "人狼だ" in talk
                suspected_cnt += "人狼でしょ" in talk
                suspected_cnt += "吊" in talk
                suspected_cnt -= ("把握" in talk) * 2
                suspected_cnt -= ("ok" in talk) * 2
                suspected_cnt -= ("了解" in talk) * 2
                suspected_cnt -= ("承知" in talk) * 2
                suspected_cnt -= ("なるほど" in talk) * 2
                suspected_cnt -= ("わかった" in talk) * 2
                suspected_cnt -= ("わかりました" in talk) * 2
                suspected_cnt -= ("だれ" in talk) * 3
                suspected_cnt -= ("見てる？" in talk) * 3
                suspected_cnt -= ("誰" in talk) * 3
                suspected_cnt -= ("？" in talk) * 2
                suspected_cnt -= ("who" in talk) * 2
                if suspected_cnt > 0 and talk not in self.list_replied:
                    self.list_replied.append(talk)
                    talk_this_turn = self.generator.deny_wolf(Role.POSSESSED, _talk)
                elif suspected_cnt < 0 and talk not in self.list_replied:
                    self.list_replied.append(talk)
                    talk_this_turn = self.generator.answer_whois(self, _talk)
        content: Content = Content(ContentBuilder())
        if talk_this_turn == "":
            talk_this_turn = self.generator.generate(self, Role.POSSESSED)
        content.text = talk_this_turn
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
