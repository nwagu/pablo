# This Python file uses the following encoding: utf-8
#############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

"""
This file contains the exact signatures for all functions in module
PySide2.QtTest, except for defaults which are replaced by "...".
"""

# Module PySide2.QtTest
import shiboken2 as Shiboken
from PySide2.support.signature import typing
from PySide2.support.signature.mapping import (
    Virtual, Missing, Invalid, Default, Instance)

class Object(object): pass

Shiboken.Object = Object

import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtWidgets
import PySide2.QtTest


class QTest(Shiboken.Object):

    @staticmethod
    def addColumnInternal(id:int, name:str): ...
    @staticmethod
    def asciiToKey(ascii:typing.Union[str, int]) -> PySide2.QtCore.Qt.Key: ...
    @staticmethod
    def compare_ptr_helper(t1:int, t2:int, actual:str, expected:str, file:str, line:int) -> bool: ...
    @staticmethod
    def compare_string_helper(t1:str, t2:str, actual:str, expected:str, file:str, line:int) -> bool: ...
    @staticmethod
    def createTouchDevice(devType:PySide2.QtGui.QTouchDevice.DeviceType=...) -> PySide2.QtGui.QTouchDevice: ...
    @staticmethod
    def currentAppName() -> str: ...
    @staticmethod
    def currentDataTag() -> str: ...
    @staticmethod
    def currentTestFailed() -> bool: ...
    @staticmethod
    def currentTestFunction() -> str: ...
    @typing.overload
    @staticmethod
    def ignoreMessage(type:PySide2.QtCore.QtMsgType, message:str): ...
    @typing.overload
    @staticmethod
    def ignoreMessage(type:PySide2.QtCore.QtMsgType, messagePattern:PySide2.QtCore.QRegularExpression): ...
    @typing.overload
    @staticmethod
    def keyClick(widget:PySide2.QtWidgets.QWidget, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyClick(widget:PySide2.QtWidgets.QWidget, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyClick(window:PySide2.QtGui.QWindow, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyClick(window:PySide2.QtGui.QWindow, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @staticmethod
    def keyClicks(widget:PySide2.QtWidgets.QWidget, sequence:str, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyEvent(action:PySide2.QtTest.QTest.KeyAction, widget:PySide2.QtWidgets.QWidget, ascii:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyEvent(action:PySide2.QtTest.QTest.KeyAction, widget:PySide2.QtWidgets.QWidget, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyEvent(action:PySide2.QtTest.QTest.KeyAction, window:PySide2.QtGui.QWindow, ascii:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyEvent(action:PySide2.QtTest.QTest.KeyAction, window:PySide2.QtGui.QWindow, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyPress(widget:PySide2.QtWidgets.QWidget, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyPress(widget:PySide2.QtWidgets.QWidget, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyPress(window:PySide2.QtGui.QWindow, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyPress(window:PySide2.QtGui.QWindow, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyRelease(widget:PySide2.QtWidgets.QWidget, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyRelease(widget:PySide2.QtWidgets.QWidget, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyRelease(window:PySide2.QtGui.QWindow, key:PySide2.QtCore.Qt.Key, modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keyRelease(window:PySide2.QtGui.QWindow, key:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def keySequence(widget:PySide2.QtWidgets.QWidget, keySequence:PySide2.QtGui.QKeySequence): ...
    @typing.overload
    @staticmethod
    def keySequence(window:PySide2.QtGui.QWindow, keySequence:PySide2.QtGui.QKeySequence): ...
    @staticmethod
    def keyToAscii(key:PySide2.QtCore.Qt.Key) -> typing.Union[str, int]: ...
    @typing.overload
    @staticmethod
    def mouseClick(widget:PySide2.QtWidgets.QWidget, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseClick(window:PySide2.QtGui.QWindow, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseDClick(widget:PySide2.QtWidgets.QWidget, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseDClick(window:PySide2.QtGui.QWindow, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseEvent(action:PySide2.QtTest.QTest.MouseAction, widget:PySide2.QtWidgets.QWidget, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers, pos:PySide2.QtCore.QPoint, delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseEvent(action:PySide2.QtTest.QTest.MouseAction, window:PySide2.QtGui.QWindow, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers, pos:PySide2.QtCore.QPoint, delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseMove(widget:PySide2.QtWidgets.QWidget, pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseMove(window:PySide2.QtGui.QWindow, pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mousePress(widget:PySide2.QtWidgets.QWidget, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mousePress(window:PySide2.QtGui.QWindow, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseRelease(widget:PySide2.QtWidgets.QWidget, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @typing.overload
    @staticmethod
    def mouseRelease(window:PySide2.QtGui.QWindow, button:PySide2.QtCore.Qt.MouseButton, stateKey:PySide2.QtCore.Qt.KeyboardModifiers=..., pos:PySide2.QtCore.QPoint=..., delay:int=...): ...
    @staticmethod
    def qCleanup(): ...
    @staticmethod
    def qElementData(elementName:str, metaTypeId:int) -> int: ...
    @staticmethod
    def qExpectFail(dataIndex:str, comment:str, mode:PySide2.QtTest.QTest.TestFailMode, file:str, line:int) -> bool: ...
    @typing.overload
    @staticmethod
    def qFindTestData(basepath:str, file:str=..., line:int=..., builddir:str=...) -> str: ...
    @typing.overload
    @staticmethod
    def qFindTestData(basepath:str, file:str=..., line:int=..., builddir:str=...) -> str: ...
    @staticmethod
    def qGlobalData(tagName:str, typeId:int) -> int: ...
    @staticmethod
    def qRun() -> int: ...
    @staticmethod
    def qSkip(message:str, file:str, line:int): ...
    @staticmethod
    def qWaitForWindowActive(widget:PySide2.QtWidgets.QWidget, timeout:int=...) -> bool: ...
    @staticmethod
    def qWaitForWindowExposed(widget:PySide2.QtWidgets.QWidget, timeout:int=...) -> bool: ...
    @typing.overload
    @staticmethod
    def sendKeyEvent(action:PySide2.QtTest.QTest.KeyAction, widget:PySide2.QtWidgets.QWidget, code:PySide2.QtCore.Qt.Key, ascii:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers, delay:int=...): ...
    @typing.overload
    @staticmethod
    def sendKeyEvent(action:PySide2.QtTest.QTest.KeyAction, widget:PySide2.QtWidgets.QWidget, code:PySide2.QtCore.Qt.Key, text:str, modifier:PySide2.QtCore.Qt.KeyboardModifiers, delay:int=...): ...
    @typing.overload
    @staticmethod
    def sendKeyEvent(action:PySide2.QtTest.QTest.KeyAction, window:PySide2.QtGui.QWindow, code:PySide2.QtCore.Qt.Key, ascii:typing.Union[str, int], modifier:PySide2.QtCore.Qt.KeyboardModifiers, delay:int=...): ...
    @typing.overload
    @staticmethod
    def sendKeyEvent(action:PySide2.QtTest.QTest.KeyAction, window:PySide2.QtGui.QWindow, code:PySide2.QtCore.Qt.Key, text:str, modifier:PySide2.QtCore.Qt.KeyboardModifiers, delay:int=...): ...
    @staticmethod
    def setBenchmarkResult(result:float, metric:PySide2.QtTest.QTest.QBenchmarkMetric): ...
    @staticmethod
    def setMainSourcePath(file:str, builddir:str=...): ...
    @typing.overload
    @staticmethod
    def simulateEvent(widget:PySide2.QtWidgets.QWidget, press:bool, code:int, modifier:PySide2.QtCore.Qt.KeyboardModifiers, text:str, repeat:bool, delay:int=...): ...
    @typing.overload
    @staticmethod
    def simulateEvent(window:PySide2.QtGui.QWindow, press:bool, code:int, modifier:PySide2.QtCore.Qt.KeyboardModifiers, text:str, repeat:bool, delay:int=...): ...
    @staticmethod
    def testObject() -> PySide2.QtCore.QObject: ...
    @staticmethod
    def toPrettyCString(unicode:str, length:int) -> str: ...
    @typing.overload
    @staticmethod
    def touchEvent(widget:PySide2.QtWidgets.QWidget, device:PySide2.QtGui.QTouchDevice, autoCommit:bool=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
    @typing.overload
    @staticmethod
    def touchEvent(window:PySide2.QtGui.QWindow, device:PySide2.QtGui.QTouchDevice, autoCommit:bool=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...

    class QTouchEventSequence(Shiboken.Object):

        def commit(self, processEvents:bool=...): ...
        @typing.overload
        def move(self, touchId:int, pt:PySide2.QtCore.QPoint, widget:PySide2.QtWidgets.QWidget=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        @typing.overload
        def move(self, touchId:int, pt:PySide2.QtCore.QPoint, window:PySide2.QtGui.QWindow=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        @typing.overload
        def press(self, touchId:int, pt:PySide2.QtCore.QPoint, widget:PySide2.QtWidgets.QWidget=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        @typing.overload
        def press(self, touchId:int, pt:PySide2.QtCore.QPoint, window:PySide2.QtGui.QWindow=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        @typing.overload
        def release(self, touchId:int, pt:PySide2.QtCore.QPoint, widget:PySide2.QtWidgets.QWidget=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        @typing.overload
        def release(self, touchId:int, pt:PySide2.QtCore.QPoint, window:PySide2.QtGui.QWindow=...) -> PySide2.QtTest.QTest.QTouchEventSequence: ...
        def stationary(self, touchId:int) -> PySide2.QtTest.QTest.QTouchEventSequence: ...

# eof
