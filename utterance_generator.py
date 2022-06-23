import random
from aiwolf import (
    Role,
    GameInfo,
    Species
)

HELLO_LIST = [
    "よろしく！",
    "よろしくお願いします。",
    "よろでーす",
    "こんにちは！！",
    "お手柔らかに",
    "おはようございます。",
    "はじめまして！お願いします！！",
]


class Generator:
    def __init__(self):
        pass

    def hello(self) -> str:
        return random.choice(HELLO_LIST)

    def generate(self, agent, role: Role) -> str:
        if agent.game_info.day == 0:  # Day0
            return self.hello()

        if role == Role.SEER:
            return self.seer_utter(agent)
        if role == Role.POSSESSED:
            return self.possessed_utter(agent)
        return "test"

    def seer_utter(self, agent):
        # 1-1 CO白黒, 1-2 投票先
        # 2-1 白黒, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        if agent.game_info.day == 1:
            if talk_len < 5:
                target = agent.game_info.divine_result.target.__str__()
                judge = "白" if agent.game_info.divine_result.result == Species.HUMAN else "黒"
                utter: str = "私は占い師です。占い結果は{}が{}でした".format(target, judge)
                return utter
            elif 5 < talk_len and talk_len < 10:
                # 投票先
                return "投票先は~~にします" # todo 文脈理解
            else:
                return "Skip"
        if agent.game_info.divine_result:
            target = agent.game_info.divine_result.target.__str__()
            judge: str = "白" if agent.game_info.divine_result.result == Species.HUMAN else "黒"
            utter: str = "占い結果は{}が{}でした".format(target, judge)
            return utter
        return "Skip"
    def possessed_utter(self, agent):
        # 1-1 占いCO白黒, 1-2 投票先
        # 2-1 狂人CO, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        if agent.game_info.day == 1:
            if talk_len < 5:
                lst = [alive_agent.__str__() for alive_agent in agent.game_info.alive_agent_list]
                lst.remove(agent.game_info.me.__str__())
                target = random.choice(lst)
                judge = "白"
                utter: str = "私は占い師です。占い結果は{}が{}でした".format(target, judge)
                return utter
            elif 5 < talk_len and talk_len < 10:
                # 投票先
                return "投票先は~~にします" # todo 文脈理解
            else:
                return "SKIP"
        return "SKIP_DAY2"
    def villager_utter(self, agent):
        # 1-1 CO要求orCO対抗要求or白黒に反応* 1-2 * and 投票
        # * w,w -> グレーを疑う bがあればその人を疑う
        # 2-1
        talk_len: int = len(agent.game_info.talk_list)
        if agent.game_info.day == 1:
            if talk_len < 5: # 占い師がCOしていたら
                utter: str = "占い師〇〇把握、〇〇白把握" # NLPで解釈し、発言
                return utter
            else:
                utter: str = "占い師COお願いします"
                return utter
        return "test"
