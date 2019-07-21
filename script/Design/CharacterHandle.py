import os,random,datetime
from script.Core import CacheContorl,ValueHandle,GameData,TextLoading,GamePathConfig,GameConfig,JsonHandle
from script.Design import AttrCalculation,MapHandle,AttrText

language = GameConfig.language
gamepath = GamePathConfig.gamepath
featuresList = AttrCalculation.getFeaturesList()
sexList = list(TextLoading.getTextData(TextLoading.rolePath, 'Sex'))
ageTemList = list(TextLoading.getTextData(TextLoading.attrTemplatePath,'AgeTem'))
characterList = list(GameData._gamedata[language]['character'].keys())

# 初始化角色数据
def initCharacterList():
    time1 = datetime.datetime.now()
    initCharacterTem()
    time2 = datetime.datetime.now()
    print(time2-time1)
    i = 1
    for character in CacheContorl.npcTemData:
        initCharacter(i,character)
        i += 1
    initCharacterDormitory()
    initCharacterPosition()

# 按id生成角色属性
def initCharacter(nowId,character):
    AttrCalculation.initTemporaryCharacter()
    characterId = str(nowId)
    CacheContorl.characterData['character'][characterId] = CacheContorl.temporaryCharacter.copy()
    AttrCalculation.setDefaultCache()
    characterName = character['Name']
    characterSex = character['Sex']
    CacheContorl.characterData['character'][characterId]['Sex'] = characterSex
    defaultAttr = AttrCalculation.getAttr(characterSex)
    defaultAttr['Name'] = characterName
    defaultAttr['Sex'] = characterSex
    AttrCalculation.setSexCache(characterSex)
    defaultAttr['Features'] = CacheContorl.featuresList.copy()
    if 'MotherTongue' in character:
        defaultAttr['Language'][character['MotherTongue']] = 10000
        defaultAttr['MotherTongue'] = character['MotherTongue']
    else:
        defaultAttr['Language']['Chinese'] = 10000
    if 'Age' in character:
        ageTem = character['Age']
        characterAge = AttrCalculation.getAge(ageTem)
        defaultAttr['Age'] = characterAge
        characterAgeFeatureHandle(ageTem,characterSex)
        defaultAttr['Features'] = CacheContorl.featuresList.copy()
    elif 'Features' in character:
        AttrCalculation.setAddFeatures(character['Features'])
        defaultAttr['Features'] = CacheContorl.featuresList.copy()
    temList = AttrCalculation.getTemList()
    if 'Features' in character:
        height = AttrCalculation.getHeight(characterSex, defaultAttr['Age'],character['Features'])
    else:
        height = AttrCalculation.getHeight(characterSex, defaultAttr['Age'],{})
    defaultAttr['Height'] = height
    if 'Weight' in character:
        weightTemName = character['Weight']
    else:
        weightTemName = 'Ordinary'
    if 'BodyFat' in character:
        bodyFatTem = character['BodyFat']
    else:
        bodyFatTem = weightTemName
    bmi = AttrCalculation.getBMI(weightTemName)
    weight = AttrCalculation.getWeight(bmi, height['NowHeight'])
    defaultAttr['Weight'] = weight
    if defaultAttr['Age'] <= 18 and defaultAttr['Age'] >= 7:
        classGradeMax = 12
        classGrade = str(defaultAttr['Age'] - 6)
        defaultAttr['Class'] = random.choice(CacheContorl.placeData["Classroom_" + classGrade])
    bodyFat = AttrCalculation.getBodyFat(characterSex,bodyFatTem)
    measurements = AttrCalculation.getMeasurements(characterSex, height['NowHeight'], weight,bodyFat,bodyFatTem)
    defaultAttr['Measirements'] = measurements
    defaultAttr['Knowledge'] = {}
    CacheContorl.temporaryCharacter.update(defaultAttr)
    CacheContorl.featuresList = {}
    CacheContorl.characterData['character'][characterId] = CacheContorl.temporaryCharacter.copy()
    CacheContorl.temporaryCharacter = CacheContorl.temporaryCharacterBak.copy()

# 处理角色年龄特性
def characterAgeFeatureHandle(ageTem,characterSex):
    if ageTem == 'SchoolAgeChild':
        if characterSex == sexList[0]:
            CacheContorl.featuresList['Age'] = featuresList["Age"][0]
        elif characterSex == sexList[1]:
            CacheContorl.featuresList['Age'] = featuresList["Age"][1]
        else:
            CacheContorl.featuresList['Age'] = featuresList["Age"][2]
    elif ageTem == 'OldAdult':
        CacheContorl.featuresList['Age'] = featuresList["Age"][3]

# 初始化角色数据
def initCharacterTem():
    npcData = getRandomNpcData()
    nowCharacterList = characterList.copy()
    npcData += [getDirCharacterTem(character) for character in nowCharacterList]
    CacheContorl.npcTemData = npcData

# 获取目录中的角色模板
def getDirCharacterTem(character):
    return TextLoading.getCharacterData(character)['AttrTemplate']

randomNpcMax = int(GameConfig.random_npc_max)
randomTeacherProportion = int(GameConfig.proportion_teacher)
randomStudentProportion = int(GameConfig.proportion_student)
ageWeightData = {
    "Teacher":randomTeacherProportion,
    "Student":randomStudentProportion
}
ageWeightReginData = ValueHandle.getReginList(ageWeightData)
ageWeightReginList = list(map(int,ageWeightReginData.keys()))
# 获取随机npc数据
def getRandomNpcData():
    if CacheContorl.randomNpcList == []:
        ageWeightMax = 0
        for i in ageWeightData:
            ageWeightMax += int(ageWeightData[i])
        for i in range(0,randomNpcMax):
            nowAgeWeight = random.randint(-1,ageWeightMax - 1)
            nowAgeWeightRegin = ValueHandle.getNextValueForList(nowAgeWeight,ageWeightReginList)
            ageWeightTem = ageWeightReginData[str(nowAgeWeightRegin)]
            randomNpcSex = getRandNpcSex()
            randomNpcName = AttrText.getRandomNameForSex(randomNpcSex)
            randomNpcAgeTem = getRandNpcAgeTem(ageWeightTem)
            fatTem = getRandNpcFatTem(ageWeightTem)
            bodyFatTem = getRandNpcBodyFatTem(ageWeightTem,fatTem)
            randomNpcNewData = {
                "Name":randomNpcName,
                "Sex":randomNpcSex,
                "Age":randomNpcAgeTem,
                "Position":["0"],
                "AdvNpc":"1",
                "Weight":fatTem,
                "BodyFat":bodyFatTem
            }
            CacheContorl.randomNpcList.append(randomNpcNewData)
        return CacheContorl.randomNpcList

sexWeightData = TextLoading.getTextData(TextLoading.attrTemplatePath,'RandomNpcSexWeight')
sexWeightMax = 0
for i in sexWeightData:
    sexWeightMax += int(sexWeightData[i])
sexWeightReginData = ValueHandle.getReginList(sexWeightData)
sexWeightReginList = list(map(int,sexWeightReginData.keys()))
# 按权重随机获取npc性别
def getRandNpcSex():
    nowWeight = random.randint(0,sexWeightMax - 1)
    weightRegin = ValueHandle.getNextValueForList(nowWeight,sexWeightReginList)
    return sexWeightReginData[str(weightRegin)]

fatWeightData = TextLoading.getTextData(TextLoading.attrTemplatePath,'FatWeight')
# 按权重随机获取npc体重模板
def getRandNpcFatTem(agejudge):
    nowFatWeightData = fatWeightData[agejudge]
    nowFatTem = ValueHandle.getRandomForWeight(nowFatWeightData)
    return nowFatTem

bodyFatWeightData = TextLoading.getTextData(TextLoading.attrTemplatePath,'BodyFatWeight')
# 按权重随机获取npc体脂率模板
def getRandNpcBodyFatTem(ageJudge,bmiTem):
    nowBodyFatData = bodyFatWeightData[ageJudge][bmiTem]
    return ValueHandle.getRandomForWeight(nowBodyFatData)

ageTemWeightData = TextLoading.getTextData(TextLoading.attrTemplatePath,'AgeWeight')
# 按权重获取npc年龄模板
def getRandNpcAgeTem(agejudge):
    nowAgeWeightData  = ageTemWeightData[agejudge]
    nowAgeTem = ValueHandle.getRandomForWeight(nowAgeWeightData)
    return nowAgeTem

# 获取角色最大数量
def getCharacterIndexMax():
    characterData = CacheContorl.characterData['character']
    characterDataMax = len(characterData.keys()) - 1
    return characterDataMax

# 获取角色id列表
def getCharacterIdList():
    characterData = CacheContorl.characterData['character']
    return list(characterData.keys())

# 分配角色宿舍
def initCharacterDormitory():
    pass

# 初始化角色的位置
def initCharacterPosition():
    for character in CacheContorl.characterData['character']:
        characterPosition = CacheContorl.characterData['character'][character]['Position']
        MapHandle.characterMoveScene(characterPosition,'0',character)
