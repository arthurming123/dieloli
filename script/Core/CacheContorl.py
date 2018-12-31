from script.Core import TextLoading

# 流程用变量组
flowContorl = {}

# 主页监听控制流程用变量组
wframeMouse = {'wFrameUp': 2, 'mouseRight': 0, 'mouseLeaveCmd': 1, 'wFrameLinesUp': 2, 'wFrameLineState': 2,'wFrameRePrint': 0}

# cmd存储
cmd_map = {}

# 角色对象数据缓存组
playObject = {}

# 等待回车
waitEnter = '0'

# 默认属性模板数据读取
temObjectDefault = {}

# 默认属性模板数据备份
temporaryObjectBak = {}

# 素质数据临时缓存
featuresList = {}

# 临时角色数据控制对象
temporaryObject = {}

# 输入记录（最大20）
inputCache = []

# 回溯输入记录用定位
inputPosition = {}

# 富文本记录输出样式临时缓存
outputTextStyle = ''

# 富文本回溯样式记录用定位
textStylePosition = {}

# 富文本样式记录
textStyleCache = []

# 富文本精确样式记录
textOneByOneRichCache = {}

lastcursor = [0]

# 图片id
imageid = 0

# cmd数据
cmdData = {}

# 游戏时间
gameTime = {}

# 时间增量
subGameTime = 0

# 面板状态
panelState = {}

# 存档页面最大数量
maxSavePage = 0

textWait = 0

sceneData = {}

mapData = {}

pathList = []

pathTimeList = []

nowMapId = 0

randomNpcList = []

class CacheHandle():
    def getTemObjectDefault(self):
        from script.Design import MapHandle
        temObject = TextLoading.getTextData(TextLoading.roleId, 'Default')
        temPositionDirList = temObject['Position']
        temPosition = MapHandle.getSceneIdForDirList(temPositionDirList)
        temObject['Position'] = temPosition
        return temObject