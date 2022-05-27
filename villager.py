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
    VoteContentBuilder,
)
from aiwolf.constant import AGENT_NONE

from const import CONTENT_SKIP


class NlpWolfVillager(AbstractPlayer):
    """NlpWolf villager agent."""

    me: Agent
    """Myself."""
    vote_candidate: Agent
    """Candidate for voting."""
    game_info: GameInfo
    """Information about current game."""
    game_setting: GameSetting
    """Settings of current game."""
    comingout_map: Dict[Agent, Role]
    """Mapping between an agent and the role it claims that it is."""
    divination_reports: List[Judge]
    """Time series of divination reports."""
    identification_reports: List[Judge]
    """Time series of identification reports."""
    talk_list_head: int
    """Index of the talk to be analysed next."""
    long_uttrs: list
    """List of little tweets in the game"""
    short_uter: list
    """List of little tweets(shorter) in the game"""
    talk_end: bool
    """Whether there is nothing to say"""
    seer_co_list: list
    """List of who COed Seer"""

    def __init__(self) -> None:
        """Initialize a new instance of NlpWolfVillager."""

        # 乱数の設定
        now = datetime.datetime.now()
        random.sed(int(time.mktime(now.timetuple())))

        self.me = AGENT_NONE
        self.vote_candidate = AGENT_NONE
        self.game_info = None  # type: ignore
        self.comingout_map = {}
        self.divination_reports = []
        self.identification_reports = []
        self.talk_list_head = 0

        self.talk_end = False

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

    def day_start(self) -> None:
        self.talk_list_head = 0
        self.talk_end = False
        self.vote_candidate = AGENT_NONE

    def update(self, game_info: GameInfo) -> None:
        self.game_info = game_info  # Update game information.
        for i in range(
            self.talk_list_head, len(game_info.talk_list)
        ):  # Analyze talks that have not been analyzed yet.
            tk: Talk = game_info.talk_list[i]  # The talk to be analyzed.
            talker: Agent = tk.agent
            if talker == self.me:  # Skip my talk.
                continue
            content: Content = Content.compile(tk.text)
            if content.topic == Topic.COMINGOUT:
                self.comingout_map[talker] = content.role
            elif content.topic == Topic.DIVINED:
                self.divination_reports.append(
                    Judge(talker, game_info.day, content.target, content.result)
                )
            elif content.topic == Topic.IDENTIFIED:
                self.identification_reports.append(
                    Judge(talker, game_info.day, content.target, content.result)
                )
        self.talk_list_head = len(game_info.talk_list)  # All done.

    def talk(self, talk_history) -> Content:
        changed_state = False
        uttr = ""
        for talk in talk_history:
            if talk["agent"] == self.me:
                continue
            r_result = self.rg.recognize(talk["text"])
            if len(r_result) == 0:
                continue
            for res in r_result:
                if res[0] == "CO":
                    if res[1] == "占" and talk["agent"]:
                        self.seer_co_list.append(talk["agent"])
                        changed_state = True
        if uttr != "" and uttr is not None:
            return uttr

        # 挨拶発話(1日目)
        if self.game_info["day"] == 0 and len(talk_history) == 0:
            greetings: list = ["よろです", "こんにちは!", "よろ～～", "こにゃにちは～"]
            random.shuffle(greetings)
            return greetings[0]
        elif self.game_info["day"] == 0 and len(talk_history[0]["turn"]) > 5:
            return "Over"

        elif self.game_info["day"] > 0 and len(talk_history) == 0:
            if (
                self.game_info["attackedAgent"] != self.game_info["executedAgent"]
                and self.game_info["attackedAgent"] > 0
            ):
                return ""
                """
                lib.util.random_select(self.templates["襲撃"]["あり"]).replace(
                    "《AGENTNAME》", lib.util.agent_name(self.game_info["attackedAgent"])
                )
                """
        """
        if changed_state:
            if self.game_info["day"] <= 1:
                self.ug.set_data(
                    self.seer_co_list,
                    self.divine_list,
                    None,
                    None,
                    my_id=self.my_id,
                    my_role=lib.util.role_name(self.role),
                )
            elif self.game_info["day"] >= 2:
                self.ug.set_data(
                    self.seer_co_list,
                    self.divine_list,
                    self.vote_list,
                    self.dead_id_list,
                    my_id=self.my_id,
                    my_role=lib.util.role_name(self.role),
                )
        """
        uttr = self.ug.generate_estimate_uttr()
        if uttr is None:
            uttr = ""

        if len(uttr) > 0 and uttr is not None:
            return uttr

        if len(talk_history) > 0:
            if (
                talk_history[0]["turn"] > 7
                and self.vote_target_id < 0
                and self.game_info["day"] >= 1
            ):
                uttr, self.vote_target_id = self.ug.generate_vote_uttr(
                    self.game_info["day"]
                )
                return uttr
        uttr = "Skip"

        # Choose an agent to be voted for while talking.
        #
        # The list of fake seers that reported me as a werewolf.
        """
        fake_seers: List[Agent] = [
            j.agent
            for j in self.divination_reports
            if j.target == self.me and j.result == Species.WEREWOLF
        ]
        # Vote for one of the alive agents that were judged as werewolves by non-fake seers.
        reported_wolves: List[Agent] = [
            j.target
            for j in self.divination_reports
            if j.agent not in fake_seers and j.result == Species.WEREWOLF
        ]
        candidates: List[Agent] = self.get_alive_others(reported_wolves)
        # Vote for one of the alive fake seers if there are no candidates.
        if not candidates:
            candidates = self.get_alive(fake_seers)
        # Vote for one of the alive agents if there are no candidates.
        if not candidates:
            candidates = self.get_alive_others(self.game_info.agent_list)
        # Declare which to vote for if not declare yet or the candidate is changed.
        if self.vote_candidate == AGENT_NONE or self.vote_candidate not in candidates:
            self.vote_candidate = self.random_select(candidates)
            if self.vote_candidate != AGENT_NONE:
                return Content(VoteContentBuilder(self.vote_candidate))
        return CONTENT_SKIP
        """

    def vote(self) -> Agent:
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
