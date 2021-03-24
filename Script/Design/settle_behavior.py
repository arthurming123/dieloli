import datetime
from functools import wraps
from types import FunctionType
from Script.Core import cache_control, constant, game_type, get_text, text_handle
from Script.Design import game_time, talk, map_handle
from Script.UI.Moudle import panel, draw
from Script.Config import game_config, normal_config

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
width = normal_config.config_normal.text_width
""" 屏幕宽度 """
_: FunctionType = get_text._
""" 翻译api """


def handle_settle_behavior(character_id: int, now_time: datetime.datetime):
    """
    处理结算角色行为
    Keyword arguments:
    character_id -- 角色id
    now_time -- 结算时间
    """
    now_character_data: game_type.Character = cache.character_data[character_id]
    status_data = game_type.CharacterStatusChange()
    start_time = now_character_data.behavior.start_time
    add_time = int((now_time - start_time).seconds / 60)
    behavior_id = now_character_data.behavior.behavior_id
    if behavior_id in game_config.config_behavior_effect_data:
        for effect_id in game_config.config_behavior_effect_data[behavior_id]:
            constant.settle_behavior_effect_data[effect_id](character_id, add_time, status_data, now_time)
    change_character_favorability_for_time(character_id, now_time)
    change_character_social(character_id, status_data)
    now_judge = False
    if character_id:
        return
    if status_data == None:
        return
    if status_data.mana_point:
        now_judge = True
    if status_data.hit_point:
        now_judge = True
    if len(status_data.knowledge):
        now_judge = True
    if len(status_data.language):
        now_judge = True
    if len(status_data.status):
        now_judge = True
    if len(status_data.sex_experience):
        now_judge = True
    if len(status_data.target_change) and not character_id:
        now_judge = True
    if now_judge:
        now_text_list = []
        now_draw = draw.NormalDraw()
        now_draw.text = "\n" + now_character_data.name + ": "
        now_draw.width = width
        now_draw.draw()
        if status_data.hit_point and round(status_data.hit_point, 2) != 0:
            now_text_list.append(
                _("体力:") + text_handle.number_to_symbol_string(round(status_data.hit_point, 2))
            )
        if status_data.mana_point and round(status_data.mana_point, 2) != 0:
            now_text_list.append(
                _("气力:") + text_handle.number_to_symbol_string(round(status_data.mana_point, 2))
            )
        if len(status_data.status):
            now_text_list.extend(
                [
                    f"{game_config.config_character_state[i].name}:{text_handle.number_to_symbol_string(round(status_data.status[i],2))}"
                    for i in status_data.status
                ]
            )
        if len(status_data.knowledge):
            now_text_list.extend(
                [
                    f"{game_config.config_knowledge[i].name}:{text_handle.number_to_symbol_string(round(status_data.knowledge[i],2))}"
                    for i in status_data.knowledge
                ]
            )
        if len(status_data.language):
            now_text_list.extend(
                [
                    f"{game_config.config_language[i].name}:{text_handle.number_to_symbol_string(round(status_data.language[i],2))}"
                    for i in status_data.language
                ]
            )
        if len(status_data.sex_experience):
            now_text_list.extend(
                [
                    game_config.config_organ[i].name
                    + _("经验:")
                    + text_handle.number_to_symbol_string(round(status_data.sex_experience[i], 2))
                    for i in status_data.sex_experience
                ]
            )
        if len(status_data.target_change):
            for target_character_id in status_data.target_change:
                if character_id and target_character_id:
                    continue
                target_change: game_type.TargetChange = status_data.target_change[target_character_id]
                target_data: game_type.Character = cache.character_data[target_character_id]
                now_text = f"\n{target_data.name}:"
                judge = 0
                if target_change.favorability:
                    now_text += _(" 对{character_name}好感").format(
                        character_name=now_character_data.name
                    ) + text_handle.number_to_symbol_string(round(target_change.favorability, 2))
                    judge = 1
                if target_change.new_social != target_change.old_social:
                    now_text += (
                        " "
                        + game_config.config_social_type[target_change.old_social].name
                        + "->"
                        + game_config.config_social_type[target_change.new_social].name
                    )
                    judge = 1
                if len(target_change.status):
                    for status_id in target_change.status:
                        if target_change.status[status_id]:
                            now_text += (
                                " "
                                + game_config.config_character_state[status_id].name
                                + text_handle.number_to_symbol_string(
                                    round(target_change.status[status_id], 2)
                                )
                            )
                            judge = 1
                if len(target_change.sex_experience):
                    for organ in target_change.sex_experience:
                        if target_change.sex_experience[organ]:
                            now_text += (
                                " "
                                + game_config.config_organ[organ].name
                                + _("经验:")
                                + text_handle.number_to_symbol_string(
                                    round(target_change.sex_experience[organ], 2)
                                )
                            )
                            judge = 1
                if judge:
                    now_text_list.append(now_text)
        now_panel = panel.LeftDrawTextListPanel()
        now_panel.set(now_text_list, width, 8)
        now_panel.draw()
        wait_draw = draw.WaitDraw()
        wait_draw.draw()


def add_settle_behavior_effect(behavior_effect_id: int):
    """
    添加行为结算处理
    Keyword arguments:
    behavior_id -- 行为id
    """

    def decorator(func):
        @wraps(func)
        def return_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        constant.settle_behavior_effect_data[behavior_effect_id] = return_wrapper
        return return_wrapper

    return decorator


def get_cut_down_favorability_for_consume_time(consume_time: int):
    """
    从经过的时间计算出扣除的好感度
    Keyword arguments:
    consume_time -- 经过时间
    """
    if consume_time < 10:
        return consume_time
    elif consume_time >= 10 and consume_time < 100:
        return (consume_time - 9) * 10 + 9
    elif consume_time >= 100 and consume_time < 1000:
        return (consume_time - 99) * 100 + 909
    else:
        return (consume_time - 999) * 1000 + 90909


def change_character_favorability_for_time(character_id: int, now_time: datetime.datetime):
    """
    按最后社交时间扣除角色好感度
    Keyword arguments:
    character_id -- 角色id
    now_time -- 当前时间
    """
    character_data: game_type.Character = cache.character_data[character_id]
    for now_character in character_data.favorability:
        character_data.social_contact_last_time.setdefault(now_character, now_time)
        last_add_time: datetime.datetime = character_data.social_contact_last_time[now_character]
        now_consume_time = int((now_time - last_add_time).seconds / 60)
        if now_consume_time < 60:
            continue
        now_cut_down = get_cut_down_favorability_for_consume_time(int(now_consume_time / 60))
        if now_character in character_data.social_contact_last_cut_down_time:
            last_cut_down_time: datetime.datetime = character_data.social_contact_last_cut_down_time[
                now_character
            ]
            old_consume_time = int((last_cut_down_time - last_add_time).seconds / 60)
            old_cut_down = get_cut_down_favorability_for_consume_time(int(old_consume_time / 60))
            now_cut_down -= old_cut_down
        character_data.favorability[now_character] -= now_cut_down
        if character_data.favorability[now_character] < 0:
            character_data.favorability[now_character] = 0


def change_character_social(character_id: int, change_data: game_type.CharacterStatusChange):
    """
    处理角色关系变化
    Keyword argumenys:
    character_id -- 状态变化数据所属角色id
    change_data -- 状态变化数据
    """
    character_data: game_type.Character = cache.character_data[character_id]
    for now_character in character_data.favorability:
        if now_character in change_data.target_change:
            target_change: game_type.TargetChange = change_data.target_change[now_character]
        now_character_data: game_type.Character = cache.character_data[now_character]
        old_social = 0
        new_social = 0
        if character_id in now_character_data.social_contact_data:
            old_social = now_character_data.social_contact_data[character_id]
        now_favorability = now_character_data.favorability[character_id]
        if now_favorability < 500:
            new_social = 0
        elif now_favorability < 10000:
            new_social = 1
        elif now_favorability < 200000:
            new_social = 2
        elif now_favorability < 4000000:
            new_social = 3
        elif now_favorability < 80000000:
            new_social = 4
        elif now_favorability >= 1600000000:
            new_social = 5
        if new_social != old_social:
            if now_character in change_data.target_change:
                target_change.old_social = old_social
                target_change.new_social = new_social
            now_character_data.social_contact.setdefault(old_social, set())
            if character_id in now_character_data.social_contact[old_social]:
                now_character_data.social_contact[old_social].remove(character_id)
            now_character_data.social_contact.setdefault(new_social, set())
            now_character_data.social_contact[new_social].add(character_id)
            now_character_data.social_contact_data[character_id] = new_social
