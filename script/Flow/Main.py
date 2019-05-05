from script.Core import CacheContorl,GameInit,PyCmd
from script.Design import AttrHandle
from script.Panel import MainFramePanel
from script.Flow import SeeCharacterAttr,SeeCharacterList,Shop,ChangeClothes,GameSetting,SaveHandleFrame,InScene,GameHelp

mainFrameGotoData = {
    "0":'in_scene',
    "1":'see_character_list',
    "2":'change_clothes',
    "3":'shop',
    "4":'game_setting',
    "5":'game_help',
    "6":'establish_save',
    "7":'load_save',
}

# 游戏主页
def mainFrame_func():
    inputS = []
    flowReturn = MainFramePanel.mainFramePanel()
    inputS = inputS + flowReturn
    characterId = CacheContorl.characterData['characterId']
    characterData = AttrHandle.getAttrData(characterId)
    characterName = characterData['Name']
    ans = GameInit.askfor_All(inputS)
    PyCmd.clr_cmd()
    CacheContorl.oldFlowId = 'main'
    if ans == characterName:
        CacheContorl.nowFlowId = 'see_character_attr'
    else:
        CacheContorl.nowFlowId = mainFrameGotoData[ans]
