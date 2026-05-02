import os
import maya.mel as mel
import maya.cmds as cmds
from functools import partial
import importlib

from .ctrlData import curveData

importlib.reload(curveData)

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
iconDir = f'{dir_path}\ctrlData\icons'

curveList = [
    "_circle", "_square", "_blink", "_triangle", "_sunburst", "_pentagon",
    "_cube", "_sphere", "_pyramid", "_rhombic", "_cylinder",
    "_locator", "_arrow", "_plus", "_allMover3", "_allMover1",
    "_arrowCurve", "_arrow1", "_arrow2", "_arrow3",
]
# Color index and RGB mapping
colorData = [
    (1, (0, 0, 0)), (2, (0.75, 0.75, 0.75)), (3, (0.5, 0.5, 0.5)),
    (4, (0.8, 0, 0.2)), (5, (0, 0, .4)), (6, (0, 0, 1)),
    (7, (0, .3, 0)), (8, (0.2, 0, 0.3)), (9, (0.8, 0, 0.8)),
    (10, (0.6, 0.3, 0.2)), (11, (0.25, 0.13, 0.13)), (12, (0.7, 0.2, 0)),
    (13, (1, 0, 0)), (14, (0, 1, 0)), (15, (0, 0.3, 0.6)),
    (16, (1, 1, 1)), (17, (1, 1, 0)), (18, (0, 1, 1)),
    (19, (0, 1, 0.8)), (20, (1, 0.7, 0.7)), (21, (0.9, 0.7, 0.5)),
    (22, (1, 1, 0.4)), (23, (0, 0.7, 0.4)), (24, (0.6, 0.4, 0.2)),
    (25, (0.63, 0.63, 0.17)), (26, (0.4, 0.6, 0.2)), (27, (0.2, 0.63, 0.35)),
    (28, (0.18, 0.63, 0.63)), (29, (0.18, 0.4, 0.63)), (30, (0.43, 0.18, 0.63)),
    (31, (0.63, 0.18, 0.4))
]

def renameShapes(transformNode):
    # Rename shapes to match transform
    shapes = cmds.listRelatives(transformNode, shapes=True, fullPath=True) or []
    for i, shp in enumerate(shapes):
        newName = "{}Shape{}".format(transformNode, i + 1)
        cmds.rename(shp, newName)


def onTextCurve(*args):
    userText = cmds.textField("textCrvFld", text=True, q=True)
    uiOffsets = cmds.checkBoxGrp("addCcOffCheckGrp", q=True, v1=True)
    offsetSpace = cmds.intSliderGrp("createOffsetSlider", q=True, v=True)
    uiSuffix = cmds.textFieldGrp("suffixField", q=True, text=True)

    if not userText:
        cmds.warning("Enter text before creating a text curve.")
        return None

    try:
        textGroup = cmds.textCurves(ch=0, t=userText)[0]
    except Exception:
        return None

    allShapes = cmds.listRelatives(textGroup, ad=True, type="nurbsCurve") or []
    if not allShapes:
        if cmds.objExists(textGroup):
            cmds.delete(textGroup)
        return None

    seenTransforms = {}
    for shp in allShapes:
        parents = cmds.listRelatives(shp, p=True) or []
        if parents:
            seenTransforms[parents[0]] = True
    allTransforms = list(seenTransforms.keys())

    if allTransforms:
        cmds.parent(allTransforms, world=True)

    for tfm in allTransforms:
        cmds.makeIdentity(tfm, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.xform(tfm, ws=True, piv=[0, 0, 0])

    name = f'{userText}'
    grpTextCurve = cmds.group(empty=True, name=f'{name}_{uiSuffix}')
    cmds.parent(allShapes, grpTextCurve, r=True, s=True)

    nodesToDelete = [n for n in allTransforms + [textGroup] if cmds.objExists(n)]
    if nodesToDelete:
        cmds.delete(nodesToDelete)

    # Add offset logic for text curves
    finalNode = grpTextCurve
    if uiOffsets:
        lastParent = None
        for i in range(offsetSpace):
            grpName = f"{name}_off" if i == 0 else f"{name}_sdk{i}"
            currGrp = cmds.createNode('transform', name=grpName)
            if lastParent:
                cmds.parent(currGrp, lastParent)
            lastParent = currGrp
        cmds.parent(grpTextCurve, lastParent)
        finalNode = lastParent

    renameShapes(grpTextCurve)
    cmds.select(grpTextCurve, r=True)
    return finalNode

def onlineWidth(*args):
    # Set curve display thickness
    width = cmds.intSliderGrp("lineWidthInt", q=True, v=True)
    curves = cmds.ls(sl=True)
    if not curves:
        cmds.warning('Select Curve Only')
        return
    for cuv in curves:
        shapes = cmds.listRelatives(cuv, shapes=True) or []
        if not shapes:
            cmds.warning('Select Curve Only')
            return
        for shp in shapes:
            if cmds.nodeType(shp) != 'nurbsCurve':
                cmds.warning('Select Curve Only')
                return
            cmds.setAttr("{}.lineWidth".format(shp), width)


def onButtonChange(*args):
    # Swap control shapes with last selection
    sel = cmds.ls(sl=True)
    newCtrl = sel[-1]
    oldCtrls = sel[:-1]
    for oldCtrl in oldCtrls:
        dup = cmds.duplicate(newCtrl, rc=True)
        cmds.delete(cmds.parentConstraint(oldCtrl, dup))
        cmds.parent(dup, oldCtrl)
        cmds.makeIdentity(dup, apply=True)

        oldShapes = cmds.listRelatives(oldCtrl, type="shape")
        ctrlShapes = cmds.listRelatives(dup, type="shape")

        for oldShape in oldShapes:
            if cmds.getAttr(oldShape + ".overrideEnabled"):
                getColor = cmds.getAttr(oldShape + ".overrideColor")
                for i in ctrlShapes:
                    cmds.setAttr(i + ".overrideEnabled", 1)
                    cmds.setAttr(i + ".overrideColor", getColor)

        for ctrlShape in ctrlShapes:
            ren = cmds.rename(ctrlShape, oldCtrl + "Shape#")
            cmds.parent(ren, oldCtrl, relative=True, shape=True)

        cmds.delete(dup)
        cmds.delete(oldShapes)
    cmds.select(clear=True)


def onButtonClick(shapeName, *args):
    # Create new control with optional offset stack
    uiSuffix = cmds.textFieldGrp("suffixField", q=True, text=True)
    uiOffsets = cmds.checkBoxGrp("addCcOffCheckGrp", q=True, v1=True)
    offsetSpace = cmds.intSliderGrp("createOffsetSlider", q=True, v=True)
    shapeData = curveData.SHAPES.get(shapeName)

    if not shapeData:
        cmds.warning(f"Shape {shapeName} not found in curveData.py")
        return

    melCmd = shapeData[0]
    cleanName = shapeName.lstrip("_")
    finalMel = melCmd.format(name=f'{cleanName}_{uiSuffix}') if uiSuffix else melCmd.format(name=f'{cleanName}')

    try:
        crv = mel.eval(finalMel)
        renameShapes(crv)

        if uiOffsets:
            lastParent = None
            for i in range(offsetSpace):
                grpName = f"{cleanName}_off" if i == 0 else f"{cleanName}_sdk{i}"
                currGrp = cmds.createNode('transform', name=grpName)
                if lastParent:
                    cmds.parent(currGrp, lastParent)
                lastParent = currGrp
            cmds.parent(crv, lastParent)
        print(f"Successfully created: {cleanName}")
    except Exception as e:
        cmds.error(f"Failed to create curve: {e}")


def onButtonCombine(*args):
    # Merge selected shapes into one transform
    sel = cmds.ls(selection=True)
    if not sel:
        return None

    tokens = sel[0].split("_")
    newName = "_".join(tokens[:-1]) if len(tokens) > 1 else sel[0]
    allShapes = cmds.listRelatives(sel, ad=True, shapes=True) or []

    cmds.makeIdentity(sel, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.xform(sel, ws=True, piv=(0, 0, 0))
    newGrp = cmds.group(empty=True, name=newName)

    if allShapes:
        cmds.parent(allShapes, newGrp, r=True, s=True)

    for obj in sel:
        if cmds.objExists(obj):
            remaining = cmds.listRelatives(obj, children=True) or []
            if not remaining:
                cmds.delete(obj)

    renameShapes(newGrp)
    cmds.select(newGrp)
    return newGrp

### for color
def overrideDisabled(*args):
    # Disable color overrides
    sel = cmds.ls(sl=True)
    for i in sel:
        cmds.setAttr(i + ".overrideEnabled", 0)

def overrideEnabled(*args):
    # Enable color overrides
    sel = cmds.ls(sl=True)
    for i in sel:
        cmds.setAttr(i + ".overrideEnabled", 1)

def overrideColor(colorNumber, *args):
    # Set specific override color
    sel = cmds.ls(sl=True)
    overrideEnabled()
    for i in sel:
        cmds.setAttr((i + ".overrideColor"), colorNumber)


def toggleAddOffsetGrp(*args):
    state = cmds.checkBoxGrp("addCcOffCheckGrp", q=True, v1=True)
    cmds.intSliderGrp("createOffsetSlider", edit=True, enable=state)


def launchUI():
    # Build UI
    winName = "CtrlWin"
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)

    cmds.window(winName, title="cc", widthHeight=(500, 200))
    parentLayout = cmds.columnLayout(adj=True, rowSpacing=5, columnOffset=['both', 5])
    cmds.text(l="Create Controller", font="boldLabelFont", h=40)
    cmds.separator(h=5)

    cmds.textFieldGrp("suffixField", l="Suffix : ", text='ctrl', cw2=[80, 45])
    cmds.checkBoxGrp("addCcOffCheckGrp", l="Add offset : ", ncb=1, v1=True, cw2=[80, 100], cc=toggleAddOffsetGrp)
    cmds.intSliderGrp("createOffsetSlider", l='Offsets Group : ', field=True, min=1, max=11, v=1, cw3=[80, 25, 100],
                      en=True)
    cmds.separator(h=2)

    scroll = cmds.scrollLayout(h=60, childResizable=True)
    cmds.columnLayout(adjustableColumn=True, columnAlign='center')
    cmds.flowLayout(wrap=True, columnSpacing=2, h=120)

    for item in curveList:
        fullIconPath = os.path.join(iconDir, f"{item}.png")
        imagePath = fullIconPath if os.path.exists(fullIconPath) else ""
        cmds.iconTextButton(
            image=imagePath, style="iconOnly", bgc=[0.35, 0.35, 0.35],
            width=28, height=28, marginWidth=2, marginHeight=2,
            c=partial(onButtonClick, item), ann=item
        )

    cmds.setParent(parentLayout)
    cmds.separator(h=5)

    cmds.rowLayout(nc=3, ad3=2, cw3=[52, 50, 50], cl3=['left', 'center', 'right'])
    cmds.text(l="textCurve :")
    cmds.textField("textCrvFld", pht="textCurve...")
    cmds.button(l="Set", w=32, h=20, c=onTextCurve)
    cmds.setParent('..')

    cmds.separator(h=5)
    cmds.rowLayout(nc=2, adjustableColumn=1, columnWidth2=[50, 50], columnAlign2=['left', 'right'])
    cmds.intSliderGrp("lineWidthInt", l='lineWidth: ', field=True, min=1, max=11, v=1, cw3=[50, 20, 50], en=True)
    cmds.button(l="Set", w=30, h=20, c=onlineWidth)
    cmds.setParent('..')

    cmds.separator(h=5)
    # --- Color Buttons Section (Styled same as Curve buttons) ---
    cmds.scrollLayout(h=44, childResizable=True)
    cmds.columnLayout(adjustableColumn=True, columnAlign='center')
    cmds.flowLayout(wrap=True, columnSpacing=0, h=40)

    cmds.button(l="x", w=14.5, h=20, c=overrideDisabled, ann="Reset Color")
    for index, rgb in colorData:
        cmds.button(l="", bgc=rgb, w=14.5, h=20, c=partial(overrideColor, index), ann=f"Color Index: {index}")

    cmds.setParent("..")
    cmds.setParent('..')
    cmds.setParent(parentLayout)


    cmds.separator(h=5)
    form = cmds.formLayout(numberOfDivisions=100)
    btn1 = cmds.button(l="Change", c=onButtonChange, h=28, bgc=[0.1, 0.2, 0.3], ann='Select')
    btn2 = cmds.button(l="Combine", c=onButtonCombine, h=28, bgc=[0.1, 0.2, 0.3], ann='')
    cmds.formLayout(form, edit=True,
                    attachForm=[(btn1, 'left', 0), (btn1, 'top', 2), (btn2, 'right', 0), (btn2, 'top', 2)],
                    attachPosition=[(btn1, 'right', 1, 50), (btn2, 'left', 1, 50)])

    cmds.setParent('..')
    cmds.separator(h=5)
    cmds.showWindow(winName)