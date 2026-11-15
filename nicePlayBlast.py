import maya.cmds as cmds
import pathlib

class NicePlayblast:
    WINDOW_NAME="NicePlayblast"
    WINDOW_TITLE="NicePlayBlast"
    WIDTH_HEIGHT=(500, 400)

    DEFAULT_FORM_VALUE={
        "NPB_SavePath":"",
        "NPB_VideoSize":[960, 540],
        "NPB_SelectCam":"persp",
        "NPB_isSequenceTime":False,
    }

    def __init__(self):
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        initialValue=self.getInitialValue()
    
        self.window=cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=self.WIDTH_HEIGHT
            )    
        
        my_form=cmds.formLayout(numberOfDivisions=100)

        # ファイルのパスやファイルの名前を入力させる
        self.label_save_file=cmds.text(label="Save File :")
        self.save_file_path=cmds.textField(
            width=300,
            height=25,
            placeholderText="Enter your file name",
            text=initialValue["NPB_SavePath"]
        )
        self.file_search_button=cmds.button(label='SearchFile', command=self.selectFile)
        self.folder_search_button=cmds.button(label='SearchFolder', command=self.selectFolder)

        # Playblastを実行するカメラを指定するドロップダウンリスト
        self.cam_select_menu=cmds.optionMenu(label='Select Camera :',
                                             beforeShowPopup=lambda *args: self.refreshSelectCamMenu(self.cam_select_menu))
        cams=self.getSceneCams()
        for cam in cams:
            cmds.menuItem(label=cam)
        # デフォルトor保存されたカメラを選択
        if initialValue["NPB_SelectCam"] in cams:
            cmds.optionMenu(self.cam_select_menu,
                            edit=True,
                            value=initialValue["NPB_SelectCam"]
                            )

        # 出力される動画のサイズ
        self.label_video_size=cmds.text(label="Video Size (Width x Height) :")
        self.label_video_size_multiplier=cmds.text(label="x")
        self.videoWidth=cmds.intField(annotation="Width", width=100, value=initialValue["NPB_VideoSize"][0])
        self.videoHeight=cmds.intField(annotation="Height", width=100, value=initialValue["NPB_VideoSize"][1])

        # SequenceTimeを使用するかどうか
        self.label_is_sequence_time=cmds.text(label="Use Sequence Time :")
        self.is_sequence_time=cmds.checkBox(
            label="",
            value=initialValue["NPB_isSequenceTime"]
        )

        self.playblast_button=cmds.button(label='Playblast', command=self.executePlayBlast)
        self.close_button=cmds.button(label='Close', command=lambda *args: cmds.deleteUI(self.WINDOW_NAME))

        cmds. formLayout(my_form, edit=True,
                            attachPosition=[(self.label_save_file, 'top',5, 20),

                                            (self.save_file_path, 'left', 0, 30),
                                            (self.save_file_path, 'top', 0, 20),

                                            (self.file_search_button, 'top', 0, 20),
                                            (self.folder_search_button, 'top', 0, 20),

                                            (self.playblast_button, 'left', 0, 0),
                                            (self.playblast_button, 'right', 0, 50),
                                            (self.playblast_button, 'bottom', 0, 100),

                                            (self.close_button, 'right', 0, 100),
                                            (self.close_button, 'left', 0, 50),
                                            (self.close_button, 'bottom', 0, 100)
                                            
                            ],
                            attachControl=[(self.file_search_button, 'left', 10, self.save_file_path),
                                           (self.folder_search_button, 'left', 10, self.file_search_button),

                                           (self.label_save_file, 'right', 10, self.save_file_path),

                                           (self.cam_select_menu, 'top', 10, self.save_file_path),

                                           (self.label_video_size, 'top', 15, self.cam_select_menu),

                                           (self.videoWidth, 'top', 10, self.cam_select_menu),
                                           (self.videoWidth, 'left', 10, self.label_video_size),

                                           (self.label_video_size_multiplier, 'top', 15, self.cam_select_menu),
                                           (self.label_video_size_multiplier, 'left',5 ,self.videoWidth),

                                           (self.videoHeight, 'top', 10, self.cam_select_menu),
                                           (self.videoHeight, 'left', 5, self.label_video_size_multiplier),

                                           (self.label_is_sequence_time, 'top', 10, self.videoWidth),
                                           (self.is_sequence_time, 'top', 10, self.videoWidth),
                                           (self.is_sequence_time, 'left', 10, self.label_is_sequence_time)
                            ],
                            attachOppositeControl=[(self.cam_select_menu, 'left', 0, self.label_save_file),
                                                   (self.label_video_size, 'left', 0, self.cam_select_menu),
                                                   (self.label_is_sequence_time, 'left', 0, self.label_video_size)

                            ]
        )
        cmds.showWindow()

    # 特定の値はoptionVarに保存して値を取り出せるようにする
    def getInitialValue(self):
        retDic={}
        for name, item in self.DEFAULT_FORM_VALUE.items():
            retDic[name]=None

        for name, item in retDic.items():
            isExists=cmds.optionVar(exists=name)
            if isExists:
                # デフォルトの値でキャスト
                defaultType=type(self.DEFAULT_FORM_VALUE[name])
                retDic[name]=defaultType(cmds.optionVar(query=name))
            else:
                retDic[name]=self.DEFAULT_FORM_VALUE[name]

        return retDic

    def selectFile(self, *args):
        filePath=cmds.fileDialog2(
            caption="Select File",
            fileMode=1,
            dialogStyle=2
        )
        if filePath:
            path=pathlib.Path(filePath[0]).resolve()
            cmds.textField(
                self.save_file_path,
                edit=True,
                text=path
            )

    def selectFolder(self, *args):
        filePath=cmds.fileDialog2(
            caption="Select Folder",
            fileMode=3,
            dialogStyle=2
        )
        if filePath:
            path=pathlib.Path(filePath[0]).resolve()
            cmds.textField(
                self.save_file_path,
                edit=True,
                text=path
            )

    # メニューをリフレッシュ
    def refreshSelectCamMenu(self, menuName):
        currentValue=cmds.optionMenu(
            menuName,
            query=True,
            value=True
        )
        newValueList=self.getSceneCams()
        cmds.optionMenu(
            menuName,
            edit=True,
            deleteAllItems=True
        )
        for val in newValueList:
            cmds.menuItem(
                parent=menuName,
                label=val
            )
        if currentValue in newValueList:
            cmds.optionMenu(
                menuName,
                edit=True,
                value=currentValue
            )

    def validatePath(self):
        savePath=cmds.textField(
            self.save_file_path,
            query=True,
            text=True
        )
        # パスが入力されていない場合は実行しない
        if savePath == "":
            cmds.warning(f'please enter file path.')
            return None

        savePath=pathlib.Path(savePath)
        savePathDir=savePath.parent
        absPath=None
        try:
            absPath=savePathDir.resolve()
        except OSError as e:
            cmds.warning(f'save folder is incorrect. please confirm your path. detail:{e}')
            return None
        # 一つ上の階層までの絶対パスと末尾を結合
        savePath=absPath / savePath.name
        # ファイル名が無い場合は実行しない(<DateTime>.xxxで実行するようにしてもいいかも？)
        if savePath.is_dir():
            cmds.warning('please enter your \"file name\".')
            return None
        return savePath

    def getVideoSize(self):
        width=height=0
        width=cmds.intField(self.videoWidth, query=True, value=True)
        height=cmds.intField(self.videoHeight, query=True, value=True)
        return [width, height]
    
    def saveFormValue(self):
        saveDir={}
        saveDir["NPB_SavePath"]=str(self.validatePath())
        saveDir["NPB_VideoSize"]=self.getVideoSize()
        saveDir["NPB_SelectCam"]=cmds.optionMenu(self.cam_select_menu, query=True, value=True)
        saveDir["NPB_isSequenceTime"]=cmds.checkBox(self.is_sequence_time, query=True, value=True)

        for name, item in saveDir.items():
            typeJudgeItem=item
            # optionVarが存在する場合はその型を参照
            if cmds.optionVar(exists=name):
                typeJudgeItem=cmds.optionVar(query=name)

            # bool値はintで保存
            if isinstance(typeJudgeItem, int) or isinstance(typeJudgeItem, bool):
                cmds.optionVar(category="NicePlayBlast", intValue=(name, int(item)))    
            elif isinstance(typeJudgeItem, float):
                cmds.optionVar(category="NicePlayBlast", floatValue=(name, float(item)))
            elif isinstance(typeJudgeItem, str):
                cmds.optionVar(category="NicePlayBlast", stringValue=(name, str(item)))
            elif isinstance(typeJudgeItem, list):
                if isinstance(typeJudgeItem[0], int):
                    args={"category":"NicePlayBlast", f'intValue{len(typeJudgeItem)}':[name, *typeJudgeItem]}
                    cmds.optionVar(**args)
            else:
                cmds.warning("save value type is incorrect.")
        cmds.savePrefs()

    # フォームで指定されたカメラを使って一時的にmodelPanelを作成する
    # 戻り値はwindowとpanel
    def createTmpModelPanel(self):
        windowName="tmpCamWindow"
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)

        # widthHeightがうまく使えない
        tmpWindow=cmds.window(windowName)
        cmds.window(
            tmpWindow,
            edit=True,
            widthHeight=self.getVideoSize()
            )
        cmds.paneLayout()
        tmpPanel=cmds.modelPanel()
        cmds.modelEditor(
            tmpPanel,
            edit=True,
            camera=cmds.optionMenu(self.cam_select_menu, query=True, value=True),
            # 以下を非表示にする
            joints=False,
            cameras=False,
            lights=False,
            locators=False,
            nurbsCurves=False,
            ikHandles=False,
            deformers=False,
            dynamics=False,
            grid=False,
            manipulators=False,
            dimensions=False,
            handles=False,
            pivots=False,

            # 表示の設定
            displayAppearance="smoothShaded",
            displayTextures=True,
            headsUpDisplay=False,
            selectionHiliteDisplay=False
        )

        cmds.showWindow(tmpWindow)
        return tmpWindow, tmpPanel

    # カメラが存在するかを確認
    def isCameraExists(self):
        camName=cmds.optionMenu(self.cam_select_menu, query=True, value=True)
        if not cmds.ls(camName, type="transform"):
            return False
        camShape=cmds.listRelatives(camName, shapes=True, type="camera")
        return bool(camShape)

    # qtが使用できる環境であればqt, それ以外ならaviで書き出し
    # windows以外は知らん
    def getPlayblastFormat(self):
        formatList=cmds.playblast(query=True, format=True) or []
        if 'qt' in formatList:
            return ('qt', 'H.264')
        return ('avi', 'IYUV')

    def clearVision(self):
        selectedCam=cmds.optionMenu(self.cam_select_menu, query=True, value=True)
        selectedCamShape=cmds.listRelatives(selectedCam, shapes=True)[0]
        preResoGateValue=cmds.getAttr(f'{selectedCamShape}.displayResolution')
        preGateMaskValue=cmds.getAttr(f'{selectedCamShape}.displayGateMask')

        # GateMask, ResolutionGateを無効化
        cmds.setAttr(f'{selectedCamShape}.displayResolution', 0)
        cmds.setAttr(f'{selectedCamShape}.displayGateMask', 0)

        return {"displayResolution":preResoGateValue, "displayGateMask":preGateMaskValue}

    def recoverVision(self, preValueDic):
        selectedCam=cmds.optionMenu(self.cam_select_menu, query=True, value=True)
        selectedCamShape=cmds.listRelatives(selectedCam, shapes=True)[0]
        cmds.setAttr(f'{selectedCamShape}.displayResolution', preValueDic["displayResolution"])
        cmds.setAttr(f'{selectedCamShape}.displayGateMask', preValueDic["displayGateMask"])

    def executePlayBlast(self, *args):
        savePath=self.validatePath()
        # savePathがNone
        if not savePath:
            return
        self.saveFormValue() 
        if not self.isCameraExists():
            cmds.warning("selected camera is missing.") 
            return
        # 指定されたカメラのみのウィンドウ、ビューを作成
        tmpWindow, tmpPanel=self.createTmpModelPanel()
        # フォーマット,圧縮方式を確認
        pbFormat, pbCompression=self.getPlayblastFormat()
        # ResolutionGate, GateMaskをオフ
        preValueDic=self.clearVision()
        cmds.playblast(
            editorPanelName=tmpPanel,
            filename=str(savePath),
            sequenceTime=cmds.checkBox(self.is_sequence_time, query=True, value=True),
            widthHeight=self.getVideoSize(),

            showOrnaments=False,
            compression=pbCompression,
            forceOverwrite=True,
            format=pbFormat,
            partialSave=False,
            percent=100,
            quality=100
        )
        # ResolutionGate, GateMaskをもとの状態に復帰
        self.recoverVision(preValueDic=preValueDic)
        cmds.deleteUI(tmpWindow)
        
        

    # シーン内のカメラのトランスフォームを取得して返す
    def getSceneCams(self):
        cameraShapes=cmds.ls(type='camera')
        cameras=[]
        for shape in cameraShapes:
            parents=cmds.listRelatives(shape, parent=True)
            if parents:
                cameras.append(parents[0])
        return cameras


if __name__=='__main__':
    ins=NicePlayblast()