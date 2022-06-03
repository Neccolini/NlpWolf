from aiwolf import (
    Role,
)


def generate(role: Role):
    if role == Role.VILLAGER:
        return "こんにちは！私は村人です！！！！"
    if role == Role.SEER:
        return "こんにちは！私は占い師です！！！！"
    if role == Role.POSSESSED:
        return "こんにちは！私は狂人です！！！！"
    if role == Role.WEREWOLF:
        return "こんにちは！私は人狼です！！！！"
    return "こんにちは！私は？？です！！！！"
