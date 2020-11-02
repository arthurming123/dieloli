import os
from types import FunctionType
from Script.Config import normal_config
from Script.UI.Moudle import panel, draw
from Script.Design import handle_panel
from Script.Core import constant, get_text, flow_handle, cache_contorl

config_normal = normal_config.config_normal
_: FunctionType = get_text._
""" 翻译api """


@handle_panel.add_panel(constant.Panel.TITLE)
def title_panel():
    """ 绘制游戏标题菜单 """
    clear_screen = panel.ClearScreenPanel()
    clear_screen.draw()
    width = config_normal.text_width
    title_info = panel.TitleAndRightInfoListPanel()
    game_name = config_normal.game_name
    info_list = [config_normal.author, config_normal.verson, config_normal.verson_time]
    title_info.set(config_normal.game_name, info_list, width)
    title_info.draw()
    lineFeed = draw.NormalDraw()
    lineFeed.max_width = 1
    lineFeed.text = "\n"
    info = _("人类是可以被驯化的")
    lineFeed.draw()
    info_draw = draw.CenterDraw()
    info_draw.text = info
    info_draw.max_width = width
    info_draw.draw()
    lineFeed.draw()
    lineFeed.draw()
    line = draw.LineDraw("=", width)
    line.draw()
    now_list = [_("开始游戏"), _("读取存档"), _("退出游戏")]
    button_panel = panel.OneMessageAndSingleColumnButton()
    button_panel.set(now_list, "", 0)
    button_panel.draw()
    return_list = button_panel.get_return_list()
    ans = flow_handle.askfor_all(return_list.keys())
    now_key = return_list[ans]
    if now_key == now_list[0]:
        cache_contorl.now_panel_id = constant.Panel.CREATOR_CHARACTER
    elif now_key == now_list[2]:
        os._exit(0)
