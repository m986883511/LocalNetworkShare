# coding=utf-8
import os
import sys
import logging
import traceback
from wsgiref import simple_server

import pecan
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import utils
from copypaste import app

utils.copy_py_as_pyc(os.path.join(os.path.dirname(__file__), 'config.py'))
import config

LOG = logging.getLogger()


class MyThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    my_signal = pyqtSignal(str)

    def __init__(self):
        super(MyThread, self).__init__()
        self.end_flag = False

    def run(self):
        try:
            local_host_ip = utils.get_local_host_ip()
            port = config.server['port']
            port = int(port) if isinstance(port, str) else port
            LOG.info('pecan service will start on http://{}:{}'.format(local_host_ip, port))
            config_dict = pecan.configuration.conf_from_file(config.current_file_path)
            service = simple_server.make_server(local_host_ip, port, app.setup_app(config_dict))
            success_msg = 'web共享服务启动成功，http://{}:{}'.format(local_host_ip, port)
            LOG.info(success_msg)
            self.my_signal.emit(success_msg + '\n' + config.help_string)
            service.serve_forever()
        except:
            err_msg = 'web服务器启动故障，err={}'.format(traceback.format_exc())
            self.my_signal.emit(err_msg)
        self.end_flag = True


class ShareView(QDialog):

    def __init__(self):
        super(ShareView, self).__init__()
        self.setGeometry(300, 300, 400, 400)
        self.setMaximumHeight(600)
        self.setMaximumWidth(600)
        self.setWindowTitle("局域网文本共享")
        self.setWindowIcon(QIcon('share.ico'))

        btn = QPushButton(self)
        btn.setText("设置文本区为共享内容")
        btn.clicked.connect(self.set_share_value)
        self.text_edit = QTextEdit()

        btn1 = QPushButton(self)
        btn1.setText("清空文本区")
        btn1.clicked.connect(self.clear_text)
        btn2 = QPushButton(self)
        btn2.setText("获取共享内容")
        btn2.clicked.connect(self.update_text)
        btn3 = QPushButton(self)
        btn3.setText("复制文本区")
        btn3.clicked.connect(self.copy_text)

        local_ip, local_port = utils.get_local_host_ip(), config.server['port']
        self.link_url = 'http://{}:{}'.format(local_ip, local_port)
        link_button = QPushButton('其他局域网设备访问: {}'.format(self.link_url))
        link_button.clicked.connect(self.open_web)

        layout = QGridLayout()
        layout.addWidget(btn, 0, 0, 1, 3)
        layout.addWidget(self.text_edit, 1, 0, 1, 3)
        layout.addWidget(btn1, 2, 0, 1, 1)
        layout.addWidget(btn2, 2, 1, 1, 1)
        layout.addWidget(btn3, 2, 2, 1, 1)
        layout.addWidget(link_button, 3, 0, 1, 3)
        self.setLayout(layout)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.update_text_edit)

        self.web_thread = MyThread()
        self.web_thread.my_signal.connect(self.set_text_edit)
        self.web_thread.start()

    def event(self, event):
        if event.type() == QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_edit.setText(config.help_string)
        return QDialog.event(self, event)

    def clear_text(self):
        self.text_edit.setText('')

    def update_text_edit(self):
        self.text_edit.setText(self.clipboard.text())
        print('update_text_edit')

    def copy_text(self):
        value = self.clipboard.text()
        text_value = self.text_edit.toPlainText()
        if text_value != value:
            self.clipboard.setText(text_value)
            print('copy content={}'.format(text_value))

    def set_text_edit(self, str1):
        self.text_edit.setText(str1)

    def update_text(self):
        try:
            from copypaste.controllers import root
            self.text_edit.setText(root.Share.value)
        except Exception as e:
            err = '设置文本错误，报错={}'.format(e)
            self.text_edit.setText(err)

    def set_share_value(self):
        try:
            from copypaste.controllers import root
            root.Share.value = self.text_edit.toPlainText()
            # import requests
            # requests.post(self.link_url+'/share_value',json={'value':self.text_edit.toPlainText()})
        except Exception as e:
            err = '设置文本错误，报错={}'.format(e)
            self.text_edit.setText(err)

    def open_web(self):
        try:
            from PyQt5.QtCore import QUrl
            from PyQt5.QtGui import QDesktopServices
            QDesktopServices.openUrl(QUrl(self.link_url))
        except Exception as e:
            err = '打开电脑默认浏览器错误，报错={};\n\n请手动打开此地址:\n{}'.format(e, self.link_url)
            self.text_edit.setText(err)


if __name__ == "__main__":
    import cgitb

    cgitb.enable()
    qt_app = QtWidgets.QApplication(sys.argv)
    my = ShareView()
    my.show()
    sys.exit(qt_app.exec_())
