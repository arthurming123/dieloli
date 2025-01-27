from Script.Design import handle_premise, attr_calculation
from Script.Core import constant, game_type, cache_control

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """


@handle_premise.add_premise(constant.Premise.CHINESE_SKILLS_IS_HEIGHT)
def handle_chinese_skills_is_height(character_id: int) -> int:
    """
    校验角色是否汉语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[0]
    if 0 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[0])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.CHINESE_SKILLS_IS_LOW)
def handle_chinese_skills_is_low(character_id: int) -> int:
    """
    校验角色是否汉语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 0 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[0])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.ENGLISH_SKILLS_IS_HEIGHT)
def handle_english_skills_is_height(character_id: int) -> int:
    """
    校验角色是否英语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[1]
    if 1 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[1])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.ENGLISH_SKILLS_IS_LOW)
def handle_english_skills_is_low(character_id: int) -> int:
    """
    校验角色是否英语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 1 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[1])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.FRENCH_SKILLS_IS_HEIGHT)
def handle_french_skills_is_height(character_id: int) -> int:
    """
    校验角色是否法语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[2]
    if 2 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[2])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.FRENCH_SKILLS_IS_LOW)
def handle_french_skills_is_low(character_id: int) -> int:
    """
    校验角色是否法语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 2 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[2])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.SPANISH_SKILLS_IS_HEIGHT)
def handle_spanish_skills_is_height(character_id: int) -> int:
    """
    校验角色是否西班牙语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[3]
    if 3 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[3])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.SPANISH_SKILLS_IS_LOW)
def handle_spanish_skills_is_low(character_id: int) -> int:
    """
    校验角色是否西班牙语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 3 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[3])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.ARABIC_SKILLS_IS_HEIGHT)
def handle_arabic_skills_is_height(character_id: int) -> int:
    """
    校验角色是否阿拉伯语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[4]
    if 4 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[4])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.ARABIC_SKILLS_IS_LOW)
def handle_arabic_skills_is_low(character_id: int) -> int:
    """
    校验角色是否阿拉伯语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 4 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[4])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.RUSSIAN_SKILLS_IS_HEIGHT)
def handle_russian_skills_is_height(character_id: int) -> int:
    """
    校验角色是否俄语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[5]
    if 5 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[5])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.RUSSIAN_SKILLS_IS_LOW)
def handle_russian_skills_is_low(character_id: int) -> int:
    """
    校验角色是否俄语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 5 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[5])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.JAPANESE_SKILLS_IS_HEIGHT)
def handle_japanese_skills_is_height(character_id: int) -> int:
    """
    校验角色是否日语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[6]
    if 6 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[6])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.JAPANESE_SKILLS_IS_LOW)
def handle_japanese_skills_is_low(character_id: int) -> int:
    """
    校验角色是否日语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 6 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[6])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.HINDI_SKILLS_IS_HEIGHT)
def handle_hindi_skills_is_height(character_id: int) -> int:
    """
    校验角色是否印地语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[7]
    if 7 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[7])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.HINDI_SKILLS_IS_LOW)
def handle_hindi_skills_is_low(character_id: int) -> int:
    """
    校验角色是否印地语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 7 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[7])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.OLD_LATIN_SKILLS_IS_HEIGHT)
def handle_old_latin_skills_is_height(character_id: int) -> int:
    """
    校验角色是否古拉丁语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[8]
    if 8 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[8])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.OLD_LATIN_SKILLS_IS_LOW)
def handle_old_latin_skills_is_low(character_id: int) -> int:
    """
    校验角色是否古拉丁语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 8 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[8])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.LATIN_SKILLS_IS_HEIGHT)
def handle_latin_skills_is_height(character_id: int) -> int:
    """
    校验角色是否拉丁语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[9]
    if 9 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[9])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.LATIN_SKILLS_IS_LOW)
def handle_latin_skills_is_low(character_id: int) -> int:
    """
    校验角色是否拉丁语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 9 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[9])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.ANCIENT_CHINESE_SKILLS_IS_HEIGHT)
def handle_ancient_chinese_skills_is_height(character_id: int) -> int:
    """
    校验角色是否古汉语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[10]
    if 10 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[10])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.ANCIENT_CHINESE_SKILLS_IS_LOW)
def handle_ancient_chinese_skills_is_low(character_id: int) -> int:
    """
    校验角色是否古汉语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 10 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[10])
        if level <= 2:
            return 1
        return 0
    return 1


@handle_premise.add_premise(constant.Premise.OLD_SINITIC_SKILLS_IS_HEIGHT)
def handle_old_sinitic_skills_is_height(character_id: int) -> int:
    """
    校验角色是否上古汉语水平高
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    weight = 1 + character_data.language_interest[11]
    if 11 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[11])
        return weight * level
    return weight


@handle_premise.add_premise(constant.Premise.OLD_SINITIC_SKILLS_IS_LOW)
def handle_old_sinitic_skills_is_low(character_id: int) -> int:
    """
    校验角色是否上古汉语水平低
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if 11 in character_data.language:
        level = attr_calculation.get_experience_level_weight(character_data.language[11])
        if level <= 2:
            return 1
        return 0
    return 1
