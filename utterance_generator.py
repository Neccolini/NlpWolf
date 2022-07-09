import random
from aiwolf import Role, GameInfo, Species, Agent

import utterance_phrases


class Generator:
    seer_ack_send: bool
    """if true, already sended seer_ack"""

    def __init__(self):
        self.seer_ack_send = False

    def hello(self) -> str:
        return random.choice(utterance_phrases.HELLO_LIST)

    def seer_ack(self, agent) -> str:
        if agent.game_info.day == 1:
            if len(agent.seer_co_list) == 1:
                seer = Agent(agent.seer_co_list[0]).__str__()
                div_res = agent.divination_reports[agent.seer_co_list[0]][0]
                utter = (
                    random.choice(utterance_phrases.SEER1_ACK_LIST)
                    .replace("_seer", seer)
                    .replace(
                        "_target",
                        div_res.target.__str__(),
                    )
                    .replace(
                        "_result",
                        "白" if div_res.result == Species.HUMAN else "黒",
                    )
                )
                return utter
            elif len(agent.seer_co_list) == 2:
                seer = Agent(agent.seer_co_list[0]).__str__()
                if agent.divination_reports == {}:
                    return "OK"
                div_res = agent.divination_reports[agent.seer_co_list[0]][0]
                utter = (
                    random.choice(utterance_phrases.SEER1_ACK_LIST)
                    .replace("_seer", seer)
                    .replace(
                        "_target",
                        div_res.target.__str__(),
                    )
                    .replace(
                        "_result",
                        "白" if div_res.result == Species.HUMAN else "黒",
                    )
                )
                return utter
            elif len(agent.seer_co_list) > 2:
                utter = "占い多すぎない？"
                return utter
        return "OK????"

    def generate(self, agent, role: Role) -> str:
        if agent.game_info.day == 0:  # Day0
            return self.hello()
        if role == Role.SEER:
            return self.seer_utter(agent)
        if role == Role.POSSESSED:
            return self.possessed_utter(agent)
        if role == Role.VILLAGER:
            return self.villager_utter(agent)
        if role == Role.WEREWOLF:
            return self.werewolf_utter(agent)
        return "test"

    def seer_utter(self, agent):
        # 1-1 CO白黒, 1-2 投票先
        # 2-1 白黒, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        if agent.game_info.day == 1:
            if talk_len < 5:
                target = agent.game_info.divine_result.target.__str__()
                judge = (
                    "白"
                    if agent.game_info.divine_result.result == Species.HUMAN
                    else "黒"
                )
                utter: str = (
                    random.choice(utterance_phrases.SEER_UTTER_LIST_DAY1)
                    .replace("_target", target)
                    .replace("_result", judge)
                )
                return utter
            elif 5 < talk_len and talk_len < 10:
                # 投票先
                return "投票先は~~にします"  # todo 文脈理解
            else:
                return "Skip"
        if agent.game_info.divine_result:
            target = agent.game_info.divine_result.target.__str__()
            judge: str = (
                "白" if agent.game_info.divine_result.result == Species.HUMAN else "黒"
            )
            utter: str = (
                random.choice(utterance_phrases.SEER_UTTER_LIST_DAY1)
                .replace("_target", target)
                .replace("_result", judge)
            )
            return utter
        return "Skip"

    def possessed_utter(self, agent):
        # 1-1 占いCO白黒, 1-2 投票先
        # 2-1 狂人CO, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        # Day1
        if agent.game_info.day == 1:
            if talk_len < 5:
                lst = [
                    alive_agent.__str__()
                    for alive_agent in agent.game_info.alive_agent_list
                ]
                lst.remove(agent.game_info.me.__str__())
                target = random.choice(lst)
                judge = "白"
                utter: str = (
                    random.choice(utterance_phrases.SEER_UTTER_LIST_DAY1)
                    .replace("_target", target)
                    .replace("_result", judge)
                )
                return utter
            elif 5 < talk_len and talk_len < 10:
                # 投票先
                return "投票先は~~にします"  # todo 文脈理解
            else:
                return "SKIP"
        # day2
        elif agent.game_info.day == 2:
            pass
        return "SKIP_DAY2"

    def villager_utter(self, agent):
        # 1-1 CO要求orCO対抗要求or白黒に反応* 1-2 * and 投票
        # * w,w -> グレーを疑う bがあればその人を疑う
        # 2-1
        talk_len: int = len(agent.game_info.talk_list)
        # print("seer_co_list v", len(agent.seer_co_list))
        if len(agent.seer_co_list) == 0:
            utter = random.choice(utterance_phrases.SEER_RESULT_REQ_LIST)
            return utter
        return self.seer_ack(agent)

    def werewolf_utter(self, agent):
        utter = "Skip WOLF"
        if len(agent.seer_co_list) == 0:
            utter = random.choice(utterance_phrases.SEER_RESULT_REQ_LIST)
            return utter
        return self.seer_ack(agent)
