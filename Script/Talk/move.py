from typing import List
from types import FunctionType
from Script.Core import constant, get_text
from Script.Design import talk

_: FunctionType = get_text._
""" 翻译api """


@talk.add_talk(constant.Behavior.MOVE, 1, {constant.Premise.IS_PLAYER})
def talk_move_1() -> List[str]:
    """
    玩家限定的基础移动口上
    Return arguments:
    list -- 返回的口上列表
    """
    return [
        _("{NickName}来到了{SceneName}"),
        _("{NickName}移动到了{SceneName}"),
        _("{NickName}走到了{SceneName}"),
    ]


@talk.add_talk(
    constant.Behavior.MOVE,
    2,
    {constant.Premise.NO_PLAYER, constant.Premise.IN_PLAYER_SCENE},
)
def talk_move_2() -> List[str]:
    """
    npc移动至玩家所在场景时的基础口上
    Return arguments:
    list -- 返回的口上列表
    """
    return [
        _("{Name}来到了{SceneName}"),
        _("{Name}走了过来"),
        _("{Name}冲着{PlayerNickName}打了个招呼"),
    ]


@talk.add_talk(
    constant.Behavior.MOVE,
    3,
    {constant.Premise.NO_PLAYER, constant.Premise.LEAVE_PLAYER_SCENE},
)
def talk_move_3() -> List[str]:
    """
    npc离开玩家所在场景时的基础口上
    Return arguments:
    list -- 返回的口上列表
    """
    return [
        _("{Name}朝着{SceneName}离开了"),
        _("{Name}走向了{SceneName}"),
        _("{Name}去了{SceneName}"),
        _("{Name}前往了{SceneName}"),
    ]


@talk.add_talk(
    constant.Behavior.MOVE,
    4,
    {
        constant.Premise.NO_PLAYER,
        constant.Premise.IN_PLAYER_SCENE,
        constant.Premise.PLAYER_IS_ADORE,
        constant.Premise.IS_WOMAN,
        constant.Premise.IS_STUDENT,
    },
)
def talk_move_4() -> List[str]:
    """
    爱慕玩家的萝莉npc移动至玩家所在场景时的口上
    Return arguments:
    list -- 返回的口上列表
    """
    talk_1 = _(
        "{Name}来到了{SceneName}\n她看见{PlayerNickName}的第一时间便扑了过来\n{Name}紧紧的抱住了{PlayerNickName},小脸不停的蹭着{PlayerNickName}的胸"
    )
    return [talk_1]
