import random
from aiwolf import Role, GameInfo, Species, Agent

import utterance_phrases

DAY1_NUM_PLAYER = 5
DAY2_NUM_PLAYER = 3


class Generator:
    def __init__(self):
        pass

    def generate(self, agent, role: Role) -> str:
        if agent.game_info.day == 0:
            if len(agent.game_info.talk_list) < 10:  # Day0
                return self.hello()
            else:
                return "Over"
        if role == Role.SEER:
            return self.seer_utter(agent)
        if role == Role.POSSESSED:
            return self.possessed_utter(agent)
        if role == Role.VILLAGER:
            return self.villager_utter(agent)
        if role == Role.WEREWOLF:
            return self.werewolf_utter(agent)
        return self.random_utterance(agent)

    def hello(self) -> str:
        return random.choice(utterance_phrases.HELLO_LIST)

    def ask_whois(self, agent) -> str:
        agent_nums = agent.get_alive()
        agent_nums.remove(agent.me.agent_idx)
        return random.choice(utterance_phrases.ASK_WHOIS_WEREWOLF).replace(
            "_target", f"Agent[0{random.choice(agent_nums)}]"
        )

    def answer_whois(self, agent, talk) -> str:
        if len(agent.vote_candidates) > 0:
            return (
                random.choice(utterance_phrases.ANSWER_WHOIS_WEREWOLF)
                .replace("_agent", talk.agent.__str__())
                .replace("_target", random.choice(agent.vote_candidates).__str__())
            )
        elif random.random() < 0.3:
            agent_nums = agent.get_alive()
            agent_nums.remove(agent.me.agent_idx)
            return (
                random.choice(utterance_phrases.ANSWER_WHOIS_WEREWOLF)
                .replace("_agent", talk.agent.__str__())
                .replace("_target", f"Agent[0{random.choice(agent_nums)}]")
            )
        else:
            return random.choice(
                utterance_phrases.ANSWER_WHOIS_WEREWOLF_NOIDEA
            ).replace("_agent", talk.agent.__str__())

    def deny_wolf(self, role, talk) -> str:
        if role == Role.WEREWOLF:
            return random.choice(utterance_phrases.WEREWOLF_DENY).replace(
                "_agent", talk.agent.__str__()
            )
        if role == Role.SEER or role == Role.POSSESSED:
            return random.choice(utterance_phrases.SEER_DENY).replace(
                "_agent", talk.agent.__str__()
            )
        else:
            return random.choice(utterance_phrases.VILLAGER_DENY).replace(
                "_agent", talk.agent.__str__()
            )

    def seer_ack(self, agent) -> str:
        if agent.game_info.day == 1:
            if len(agent.seer_co_list) == 1:
                seer = Agent(agent.seer_co_list[0]).__str__()
                div_res = agent.divination_reports[agent.seer_co_list[0]][0]
                # 自分に黒出しされたら
                if (
                    div_res.target.agent_idx == agent.me.agent_idx
                    and div_res.result == Species.WEREWOLF
                ):
                    utter = random.choice(utterance_phrases.DENY).replace("_seer", seer)
                else:
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
                seer1 = Agent(agent.seer_co_list[0]).__str__()
                seer2 = Agent(agent.seer_co_list[1]).__str__()
                if agent.divination_reports == {}:
                    return self.random_utterance(agent)
                div_res1 = agent.divination_reports[agent.seer_co_list[0]][0]
                div_res2 = agent.divination_reports[agent.seer_co_list[1]][0]
                if (
                    div_res1.target.agent_idx == agent.me.agent_idx
                    and div_res1.result == Species.WEREWOLF
                ):
                    return random.choice(utterance_phrases.DENY).replace("_seer", seer1)
                elif (
                    div_res2.target.agent_idx == agent.me.agent_idx
                    and div_res2.result == Species.WEREWOLF
                ):
                    return random.choice(utterance_phrases.DENY).replace("_seer", seer2)
                else:
                    utter = (
                        random.choice(utterance_phrases.SEER2_ACK_LIST)
                        .replace("_seer1", seer1)
                        .replace(
                            "_target1",
                            div_res1.target.__str__(),
                        )
                        .replace(
                            "_result1",
                            "白" if div_res1.result == Species.HUMAN else "黒",
                        )
                        .replace("_seer2", seer2)
                        .replace(
                            "_target2",
                            div_res2.target.__str__(),
                        )
                        .replace(
                            "_result2",
                            "白" if div_res2.result == Species.HUMAN else "黒",
                        )
                    )
                    # 自分に黒だしされた
                    if (
                        div_res1.result == Species.WEREWOLF
                        and div_res1.target.agent_idx == agent.me.agent_idx
                    ):
                        utter = random.choice(utterance_phrases.DENY).replace(
                            "_seer", div_res1.agent.__str__()
                        ) 
                    if (
                        div_res2.result == Species.WEREWOLF
                        and div_res2.target.agent_idx == agent.me.agent_idx
                    ):
                        utter = random.choice(utterance_phrases.DENY).replace(
                            "_seer", div_res2.agent.__str__()
                        )
                if (
                    div_res1.result == Species.HUMAN
                    and div_res2.result == Species.HUMAN
                    and div_res1.target == div_res2.target
                    and random.random() < 0.4
                ):
                    utter = random.choice(utterance_phrases.WHITE_CERTIFIED).replace(
                        "_white", div_res1.target.__str__()
                    )
                return utter
            elif len(agent.seer_co_list) > 2:
                utter = "占い多すぎない？"
                return utter
        if agent.game_info.day == 2:
            if len(agent.seer_co_list) == 1:
                reports = agent.divination_reports[agent.seer_co_list[0]]
                seer_alive = agent.is_alive(agent.seer_co_list[0])
                if seer_alive:
                    # 占い生存
                    if len(reports) == 2:
                        # 占い結果を了解する
                        target = reports[1].target.__str__()
                        result = "白" if reports[1].result == Species.HUMAN else "黒"
                        return (
                            random.choice(utterance_phrases.SEER1_DAY2_ACK)
                            .replace("_target", target)
                            .replace("_result", result)
                        )
                    else:
                        return random.choice(utterance_phrases.SEER1_DAY2_REQ).replace(
                            "_seer", Agent(agent.seer_co_list[0]).__str__()
                        )
                else:
                    return random.choice(utterance_phrases.SEER1_DAY2_DEAD).replace(
                        "_seer", Agent(agent.seer_co_list[0]).__str__()
                    )

            elif len(agent.seer_co_list) == 2:
                reports1 = agent.divination_reports[agent.seer_co_list[0]]
                reports2 = agent.divination_reports[agent.seer_co_list[1]]

                match (
                    agent.is_alive(Agent(agent.seer_co_list[0])),
                    agent.is_alive(Agent(agent.seer_co_list[1])),
                ):
                    case (True, True):
                        match (len(reports1), len(reports2)):
                            case (2, 2):
                                utter = (
                                    random.choice(
                                        utterance_phrases.SEER2_DAY2_TWO_ALIVE_TWO_RESULT
                                    )
                                    .replace(
                                        "_seer1", Agent(agent.seer_co_list[0]).__str__()
                                    )
                                    .replace(
                                        "_seer2", Agent(agent.seer_co_list[1]).__str__()
                                    )
                                    .replace("_target1", reports1[1].target.__str__())
                                    .replace("_target2", reports2[1].target.__str__())
                                    .replace(
                                        "_result1",
                                        "白"
                                        if reports1[1].result == Species.HUMAN
                                        else "黒",
                                    )
                                    .replace(
                                        "_result2",
                                        "白"
                                        if reports1[1].result == Species.HUMAN
                                        else "黒",
                                    )
                                )
                                #自分に黒だしされたら
                                if (
                                    reports1[1].result == Species.WEREWOLF
                                    and reports1[1].target.agent_idx
                                    == agent.me.agent_idx
                                ):
                                    utter = random.choice(
                                        utterance_phrases.DENY
                                    ).replace("_seer", reports1[1].agent.__str__())
                                if (
                                    reports2[1].result == Species.WEREWOLF
                                    and reports2[1].target.agent_idx
                                    == agent.me.agent_idx
                                ):
                                    utter = random.choice(
                                        utterance_phrases.DENY
                                    ).replace("_seer", reports2[1].agent.__str__())
                                if (
                                    reports1[1].result == Species.HUMAN
                                    and reports2[1].result == Species.HUMAN
                                    and reports1[1].target == reports2[1].target
                                    and random.random() < 0.4
                                ):
                                    utter = random.choice(
                                        utterance_phrases.WHITE_CERTIFIED
                                    ).replace("_white", reports[1].target.__str__())
                                return utter
                            case (1, 2):
                                utter = (
                                    random.choice(
                                        utterance_phrases.SEER2_DAY2_TWO_ALIIVE_ONE_RESULT
                                    )
                                    .replace(
                                        "_seer1", Agent(agent.seer_co_list[0]).__str__()
                                    )
                                    .replace(
                                        "_seer2", Agent(agent.seer_co_list[1]).__str__()
                                    )
                                    .replace("_target1", reports2[1].target.__str__())
                                    .replace(
                                        "_result1",
                                        "白"
                                        if reports2[1].result == Species.HUMAN
                                        else "黒",
                                    )
                                )
                                #自分に黒だし
                                if (
                                    reports2[1].result == Species.WEREWOLF
                                    and reports2[1].target.agent_idx == agent.me.agent_idx
                                ):
                                    utter = random.choice(utterance_phrases.DENY).replace(
                                        "_seer", reports2[1].agent.__str__()
                                    )
                                return utter
                            case (2, 1):
                                utter = (
                                    random.choice(
                                        utterance_phrases.SEER2_DAY2_TWO_ALIIVE_ONE_RESULT
                                    )
                                    .replace(
                                        "_seer1", Agent(agent.seer_co_list[0]).__str__()
                                    )
                                    .replace(
                                        "_seer2", Agent(agent.seer_co_list[1]).__str__()
                                    )
                                    .replace("_target1", reports1[1].target.__str__())
                                    .replace(
                                        "_result1",
                                        "白"
                                        if reports1[1].result == Species.HUMAN
                                        else "黒",
                                    )
                                )
                                #自分に黒だし
                                if (
                                    reports1[1].result == Species.WEREWOLF
                                    and reports1[1].target.agent_idx == agent.me.agent_idx
                                ):
                                    utter = random.choice(utterance_phrases.DENY).replace(
                                        "_seer", reports1[1].agent.__str__()
                                    )
                                return utter
                            case (1, 1):
                                return (
                                    random.choice(
                                        utterance_phrases.SEER2_DAY2_TWO_ALIE_NO_RESULT
                                    )
                                    .replace(
                                        "_seer1", Agent(agent.seer_co_list[0]).__str__()
                                    )
                                    .replace(
                                        "_seer2", Agent(agent.seer_co_list[1]).__str__()
                                    )
                                )
                    case (True, False):
                        if len(reports1) == 2:
                            utter = (
                                random.choice(
                                    utterance_phrases.SEER2_DAY2_ONE_DEAD_YES_RESULT
                                )
                                .replace("_target", reports1[1].target.__str__())
                                .replace(
                                    "_result",
                                    "白" if reports1[1].result == Species.HUMAN else "黒",
                                )
                            )
                            #自分に黒だしされた
                            if (
                                reports1[1].result == Species.WEREWOLF
                                and reports1[1].target.agent_idx == agent.me.agent_idx
                            ):
                                utter = random.choice(utterance_phrases.DENY).replace(
                                    "_seer", reports1[1].agent.__str__()
                                )
                            return utter
                        else:
                            return (
                                random.choice(
                                    utterance_phrases.SEER2_DAY2_ONE_DEAD_NO_RESULT
                                )
                                .replace(
                                    "_seer_dead", Agent(agent.seer_co_list[1]).__str__()
                                )
                                .replace(
                                    "_seer_alive",
                                    Agent(agent.seer_co_list[0]).__str__(),
                                )
                            )
                    case (False, True):
                        if len(reports2) == 2:
                            utter = (
                                random.choice(
                                    utterance_phrases.SEER2_DAY2_ONE_DEAD_YES_RESULT
                                )
                                .replace("_target", reports2[1].target.__str__())
                                .replace(
                                    "_result",
                                    "白" if reports2[1].result == Species.HUMAN else "黒",
                                )
                            )
                            #自分に黒だしされた
                            if (
                                reports2[1].result == Species.WEREWOLF
                                and reports2[1].target.agent_idx == agent.me.agent_idx
                            ):
                                utter = random.choice(utterance_phrases.DENY).replace(
                                    "_seer", reports2[1].agent.__str__()
                                )
                            return utter
                        else:
                            return (
                                random.choice(
                                    utterance_phrases.SEER2_DAY2_ONE_DEAD_NO_RESULT
                                )
                                .replace(
                                    "_seer_dead", Agent(agent.seer_co_list[0]).__str__()
                                )
                                .replace(
                                    "_seer_alive",
                                    Agent(agent.seer_co_list[1]).__str__(),
                                )
                            )
                    case (False, False):
                        return (
                            random.choice(utterance_phrases.SEER2_DAY2_TWO_DEAD)
                            .replace("_seer1", Agent(agent.seer_co_list[0]).__str__())
                            .replace("_seer2", Agent(agent.seer_co_list[1]).__str__())
                        )
        print("WHYWEJKRFLWJEKRFLW+JERFLK+")
        return self.random_utterance(agent)

    def try_find_wolf(self, agent):
        if agent.game_info.day == 1:
            if agent.divination_reports == {}:
                return self.random_utterance(agent)
            div_res1 = agent.divination_reports[agent.seer_co_list[0]][0]
            div_res2 = agent.divination_reports[agent.seer_co_list[1]][0]
            match (div_res1.result, div_res2.result):
                case (Species.HUMAN, Species.HUMAN):
                    set_idx = set()
                    set_idx.add(div_res1.target.agent_idx)
                    set_idx.add(div_res2.target.agent_idx)
                    set_idx.add(agent.seer_co_list[0])
                    set_idx.add(agent.seer_co_list[1])
                    all = {1, 2, 3, 4, 5}
                    gray_list = list(all - set_idx)
                    if len(gray_list) == 3:
                        if agent.me.agent_idx in gray_list:
                            gray_list.remove(agent.me.agent_idx)
                        return random.choice(utterance_phrases.GRAY3).replace(
                            "_gray", f"Agent[0{random.choice(gray_list)}]"
                        )
                    elif len(gray_list) == 2:
                        if agent.me.agent_idx in gray_list:
                            gray_list.remove(agent.me.agent_idx)
                            return random.choice(utterance_phrases.GRAY2_AND_IM_GRAY).replace("_gray", Agent(gray_list[0]).__str__())
                        return (
                            random.choice(utterance_phrases.GRAY2)
                            .replace("_gray1", f"Agent[0{gray_list[0]}]")
                            .replace("_gray2", f"Agent[0{gray_list[1]}]")
                        )
                    elif len(gray_list) == 1:
                        if agent.me.agent_idx in gray_list:
                            target = random.choice(agent.get_alive_others())
                            return random.choice(utterance_phrases.GRAY1_AND_IM_GRAY).replace("_target", Agent(target).__str__())
                        return random.choice(utterance_phrases.GRAY1).replace(
                            "_gray", f"Agent[0{gray_list[0]}]"
                        )
                    else:
                        if random.random() < 2:
                            return self.ask_whois(agent)
                        return self.random_utterance(agent)
                case (Species.WEREWOLF, Species.HUMAN):
                    werewlf = div_res1.target.__str__()
                    return random.choice(
                        utterance_phrases.SEER1_ACK_LIST_WEREWOLF
                    ).replace("_target", werewlf)
                case (Species.HUMAN, Species.WEREWOLF):
                    werewlf = div_res2.target.__str__()
                    return random.choice(
                        utterance_phrases.SEER1_ACK_LIST_WEREWOLF
                    ).replace("_target", werewlf)
                case (Species.WEREWOLF, Species.WEREWOLF):
                    return (
                        random.choice(utterance_phrases.SEER2_ACK_LIST_WEREWOLF)
                        .replace("_target2", div_res2.target.__str__())
                        .replace("_target1", div_res1.target.__str__())
                    )
        if agent.game_info.day == 2:
            if random.random() < 0.2:
                return self.ask_whois(agent)
            return self.random_utterance(agent)
    def deep_learning(self, agent):
        return "Skip"

    def random_utterance(self, agent):
        if len(agent.vote_candidates) == 0 and random.random() < 0.271828:
            i = 0
            for talk in agent.game_info.talk_list:
                text = talk.text
                cnt = 0
                cnt += "Agent" in text
                cnt += "グレー" in text
                cnt += "吊" in text
                cnt += "本物" in text
                cnt += "グレラン" in text
                cnt += "人狼" in text
                cnt -= ("?" in text) * 3
                cnt -= ("？" in text) * 3
                cnt -= ("だれ" in text) * 3
                cnt -= ("誰" in text) * 3
                cnt -= ("なに" in text) * 2
                cnt -= ("どうして" in text) * 2
                cnt -= ("なんで" in text) * 2
                cnt -= ("理由" in text) * 2
                i += 1
                if cnt > 1 and len(agent.game_info.talk_list) - i < 3:
                    return random.choice(utterance_phrases.REQ_REASON).replace("_target", talk.agent.__str__())
                cnt = 0
                cnt -= ("どうして" in text) * 2
                cnt -= ("なんで" in text) * 2
                cnt -= ("理由" in text) * 2
                cnt -= ("なぜ" in text) * 2
                cnt -= ("根拠" in text) * 2
                if (f">>{agent.me.__str__()}" in text)  and (text in utterance_phrases.REQ_REASON or cnt < 0):
                    return random.choice(utterance_phrases.ANSWER_REASON1).replace("_target", talk.agent.__str__())
        return self.deep_learning(agent)

    def seer_utter(self, agent):
        # 1-1 CO白黒, 1-2 投票先
        # 2-1 白黒, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        if agent.game_info.day == 1:
            if talk_len < DAY1_NUM_PLAYER:
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
            else:
                if talk_len < 2 * DAY1_NUM_PLAYER:
                    return self.try_find_wolf(agent)
        if agent.game_info.day == 2 and agent.game_info.divine_result:
            if talk_len < DAY2_NUM_PLAYER * 2:
                target = agent.game_info.divine_result.target.__str__()
                judge: str = (
                    "白"
                    if agent.game_info.divine_result.result == Species.HUMAN
                    else "黒"
                )
                utter: str = (
                    random.choice(utterance_phrases.SEER_UTTER_LIST_DAY2)
                    .replace("_target", target)
                    .replace("_result", judge)
                )
                return utter
            else:
                if talk_len < 3 * DAY2_NUM_PLAYER:
                    return self.try_find_wolf(agent)
        return self.random_utterance(agent)

    def possessed_utter(self, agent):
        # 1-1 占いCO白黒, 1-2 投票先
        # 2-1 狂人CO, 2-2 投票先
        talk_len: int = len(agent.game_info.talk_list)
        # Day1
        if agent.game_info.day == 1:
            if talk_len < DAY1_NUM_PLAYER:
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
            else:
                if talk_len < 2 * DAY1_NUM_PLAYER:
                    return self.try_find_wolf(agent)
        # day2
        elif agent.game_info.day == 2:
            if talk_len < DAY2_NUM_PLAYER:
                lst = [
                    alive_agent.__str__()
                    for alive_agent in agent.game_info.alive_agent_list
                ]
                lst.remove(agent.game_info.me.__str__())
                target = random.choice(lst)
                judge = "白"
                utter: str = (
                    random.choice(utterance_phrases.SEER_UTTER_LIST_DAY2)
                    .replace("_target", target)
                    .replace("_result", judge)
                )
                return utter
        return self.random_utterance(agent)

    def villager_utter(self, agent):
        # 1-1 CO要求orCO対抗要求or白黒に反応* 1-2 * and 投票
        # * w,w -> グレーを疑う bがあればその人を疑う
        # 2-1
        talk_len: int = len(agent.game_info.talk_list)
        # print("seer_co_list v", len(agent.seer_co_list))
        if len(agent.seer_co_list) == 0:
            utter = random.choice(utterance_phrases.SEER_RESULT_REQ_LIST)
            return utter
        if len(agent.game_info.talk_list) < 10:
            return self.seer_ack(agent)
        if len(agent.game_info.talk_list) < 30:
            return self.try_find_wolf(agent)
        return self.random_utterance(agent)

    def werewolf_utter(self, agent):
        if len(agent.seer_co_list) == 0:
            utter = random.choice(utterance_phrases.SEER_RESULT_REQ_LIST)
            return utter
        if len(agent.game_info.talk_list) < 6:
            return self.seer_ack(agent)
        if len(agent.game_info.talk_list) < 18:
            return self.try_find_wolf(agent)
        return self.random_utterance(agent)
