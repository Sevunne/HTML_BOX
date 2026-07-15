import json
import shutil
import time
import zipfile
import re
import traceback
from win11toast import notify
import webbrowser
from datetime import datetime
import os
import sys
#from html_dom_parser import html_to_node_tree, node_tree_to_html


from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QTextEdit, QSplitter, QToolBar,
                               QFileDialog, QMessageBox, QLabel,
                               QStatusBar, QFrame, QDialog, QDialogButtonBox,
                               QFormLayout, QComboBox, QSpinBox, QFontDialog,
                               QCheckBox, QTabWidget, QGroupBox, QProgressDialog,
                               QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
                               QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QDockWidget, QScrollArea, QSizePolicy,
                               QMenu)
from PySide6.QtGui import (QIcon, QFont, QPalette, QColor, QKeySequence,
                           QTextCharFormat, QSyntaxHighlighter, QFontMetrics,
                           QDrag, QPixmap, QBrush, QPen, QAction, QShortcut)
from PySide6.QtCore import Qt, QSize, QTimer, QSettings, QThread, Signal, QRegularExpression, QMimeData
from PySide6.QtWebEngineWidgets import QWebEngineView


# ===================== 原有完整类（无任何删减，原样保留） =====================
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_count = 0  # 点击计数器
        self.init_ui()
        # 删除问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    def init_ui(self):
        self.setWindowTitle("关于 HTML BOX")
        self.setGeometry(300, 300, 400, 400)
        # 设置深色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QGroupBox {
                color: #569cd6;
                font-weight: bold;
                border: 1px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        # 标题
        title_label = QLabel("HTML BOX")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #569cd6;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        # 简介
        desc_label = QLabel(
            "一款基于 PyQt5 开发的深色主题 HTML 编辑器\n\n"
            "✨ 功能特色：\n"
            "• 实时预览\n"
            "• 语法高亮\n"
            "• 代码导出\n"
            "• 深色主题\n"
            "• 全新积木节点编辑模式\n\n"
            "👨‍💻 制作人员：布丁"
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("padding: 10px; line-height: 1.5;")
        layout.addWidget(desc_label)
        # 版本信息
        version_group = QGroupBox("版本历史")
        version_layout = QVBoxLayout(version_group)
        # 显示最近几个版本
        recent_versions = [
            "v2.0.0 - 新增积木节点模式、.htbx工程文件",
            "v1.3.0 - 新增关于窗口",
            "v1.2.0 - 添加语法高亮功能",
            "v1.1.0 - 新增导出功能",
            "v1.0.0 - 基础编辑器功能"
        ]
        for version in recent_versions:
            version_label = QLabel(version)
            version_label.setStyleSheet("padding: 2px;")
            version_layout.addWidget(version_label)
        # 全部版本按钮
        self.full_version_btn = QPushButton("查看全部版本")
        self.full_version_btn.clicked.connect(self.show_full_versions)
        version_layout.addWidget(self.full_version_btn)
        layout.addWidget(version_group)
        # 彩蛋按钮区域
        egg_layout = QHBoxLayout()
        egg_layout.addStretch()
        # 彩蛋按钮 - 看起来像个普通按钮
        self.egg_button = QPushButton("🤔")
        self.egg_button.setToolTip("这是什么？")
        self.egg_button.setFixedSize(40, 40)
        self.egg_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: #808080;
                border: 1px dashed #606060;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #505050;
                border: 1px dashed #808080;
            }
        """)
        self.egg_button.clicked.connect(self.on_egg_button_clicked)
        egg_layout.addWidget(self.egg_button)
        egg_layout.addStretch()
        layout.addLayout(egg_layout)
        # 关闭按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
    def on_egg_button_clicked(self):
        """彩蛋按钮点击事件"""
        self.click_count += 1
        # 根据点击次数显示不同提示
        if self.click_count == 1:
            self.egg_button.setText("🤨")
            self.egg_button.setToolTip("你点我干嘛？")
        elif self.click_count == 2:
            self.egg_button.setText("😒")
            self.egg_button.setToolTip("别点了，没什么好看的")
        elif self.click_count == 3:
            self.egg_button.setText("😠")
            self.egg_button.setToolTip("再点我要生气了！")
        elif self.click_count == 4:
            self.egg_button.setText("💢")
            self.egg_button.setToolTip("最后一次警告！")
        elif self.click_count == 5:
            self.trigger_easter_egg()
            self.click_count = 0  # 重置计数器
            self.egg_button.setText("🤔")
            self.egg_button.setToolTip("这是什么？")
        # 添加点击动画效果
        self.animate_button()
    def animate_button(self):
        """按钮点击动画"""
        original_style = self.egg_button.styleSheet()
        self.egg_button.setStyleSheet(original_style + """
            QPushButton {
                background-color: #569cd6;
            }
        """)
        # 0.2秒后恢复原样式
        QTimer.singleShot(200, lambda: self.egg_button.setStyleSheet(original_style))
    def trigger_easter_egg(self):
        """触发彩蛋"""
        # 创建彩蛋对话框
        egg_dialog = QDialog(self)
        egg_dialog.setWindowTitle("🎉 发现彩蛋！")
        egg_dialog.setGeometry(350, 350, 500, 400)
        egg_dialog.setWindowFlags(egg_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        egg_dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #ff6b6b, stop:0.5 #4ecdc4, stop:1 #45b7d1);
                color: white;
                font-family: "Microsoft YaHei";
            }
            QLabel {
                color: white;
                background-color: transparent;
                font-size: 14px;
            }
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.7);
                color: #00ff00;
                border: 2px solid #ffff00;
                border-radius: 10px;
                font-family: "Consolas", monospace;
                font-size: 12px;
            }
            QPushButton {
                background-color: #ff4757;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff3742;
            }
        """)
        layout = QVBoxLayout(egg_dialog)
        # 彩蛋标题
        title_label = QLabel("🎊 恭喜发现隐藏彩蛋！ 🎊")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffff00;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        # 彩蛋内容
        content_label = QLabel("这是给你的特别奖励：")
        content_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(content_label)
        # 特殊代码
        code_text = QTextEdit()
        code_text.setPlainText("""<!-- 隐藏的魔法代码 -->
<div class="easter-egg">
    <h1>✨ 布丁的祝福 ✨</h1>
    <p>愿你的代码永无bug！</p>
    <style>
        .easter-egg {
            animation: rainbow 2s infinite;
            text-align: center;
        }
        @keyframes rainbow {
            0% { color: #ff6b6b; }
            25% { color: #4ecdc4; }
            50% { color: #45b7d1; }
            75% { color: #96ceb4; }
            100% { color: #ff6b6b; }
        }
    </style>
</div>
<!-- 复制这段代码到编辑器中看看吧！ -->""")
        code_text.setReadOnly(True)
        layout.addWidget(code_text)
        # 按钮布局
        button_layout = QHBoxLayout()
        # 复制代码按钮
        copy_btn = QPushButton("📋 复制魔法代码")
        copy_btn.clicked.connect(lambda: self.copy_easter_egg_code(egg_dialog))
        # 关闭按钮
        close_btn = QPushButton("🎁 一个礼物")
        close_btn.clicked.connect(self.gifts)
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        notify(
            title="我是彩蛋！",
            body="""哈哈，没想到你点进来了，我是彩蛋！\n能点个关注吗QAQ""",
            image={
                "src": "",
                "placement": "hero",
            },
            buttons=[
                {
                    "activationType": "protocol",
                    "arguments": "https://space.bilibili.com/3546811608336574",
                    "content": "关注一下我吧！",
                },
            ],
        )
        egg_dialog.exec()
    def gifts(self):
        webbrowser.open('https://www.bilibili.com/video/BV1ucGzzuEhw/?spm_id_from=333.337.search-card.all.click&vd_source=d49d3d94217437a309f0b9b049a911d7')
    def copy_easter_egg_code(self, dialog):
        """复制彩蛋代码到编辑器"""
        magic_code = """<!-- 隐藏的魔法代码 -->
<div class="easter-egg">
    <h1>✨ 布丁的祝福 ✨</h1>
    <p>愿你的代码永无bug！</p>
    <style>
        .easter-egg {
            animation: rainbow 2s infinite;
            text-align: center;
            padding: 50px;
            font-family: Arial, sans-serif;
        }
        @keyframes rainbow {
            0% { color: #ff6b6b; }
            25% { color: #4ecdc4; }
            50% { color: #45b7d1; }
            75% { color: #96ceb4; }
            100% { color: #ff6b6b; }
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.5em;
        }
    </style>
</div>"""
        if hasattr(self.parent(), 'editor'):
            self.parent().editor.insertPlainText(magic_code)
            QMessageBox.information(dialog, "成功", "魔法代码已插入到编辑器！\n快去预览看看吧！🎉")
        else:
            QMessageBox.information(dialog, "提示", "代码已准备好，请手动复制使用！")
    def show_full_versions(self):
        """显示完整版本历史"""
        full_versions = [
            "v2.0.0 - 新增积木节点模式、.htbx工程文件、双向代码同步",
            "v1.9.0 - 解决堆栈溢出问题",
            "v1.7.0 - 改bug",
            "v1.4.0 - 全面改用pyside6制作",
            "v1.3.0 - 新增关于窗口和彩蛋功能",
            "v1.2.1 - 修复设置对话框崩溃问题",
            "v1.2.0 - 添加语法高亮功能",
            "v1.1.2 - 优化导出性能",
            "v1.1.1 - 修复导出对话框样式",
            "v1.1.0 - 新增导出功能",
            "v1.0.2 - 修复实时预览延迟",
            "v1.0.1 - 优化界面布局",
            "v1.0.0 - 基础编辑器功能发布",
            "v0.9.0 - Beta测试版本",
            "v0.8.0 - Alpha测试版本",
            "v0.1.0 - 项目初始版本"
        ]
        # 创建显示完整版本的对话框
        version_dialog = QDialog(self)
        version_dialog.setWindowTitle("全部版本历史")
        version_dialog.setGeometry(350, 350, 500, 400)
        version_dialog.setWindowFlags(version_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        version_dialog.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
                font-family: Consolas, monospace;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
        """)
        layout = QVBoxLayout(version_dialog)
        # 版本列表
        version_text = QTextEdit()
        version_text.setReadOnly(True)
        version_text.setPlainText("\n".join(full_versions))
        layout.addWidget(version_text)
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(version_dialog.accept)
        layout.addWidget(close_btn)
        version_dialog.exec()

class HTMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6"))  # 蓝色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "\\bhtml\\b", "\\bhead\\b", "\\bbody\\b", "\\btitle\\b", "\\bmeta\\b",
            "\\blink\\b", "\\bscript\\b", "\\bstyle\\b", "\\bdiv\\b", "\\bspan\\b",
            "\\bp\\b", "\\bh1\\b", "\\bh2\\b", "\\bh3\\b", "\\bh4\\b", "\\bh5\\b", "\\bh6\\b",
            "\\ba\\b", "\\bimg\\b", "\\bbr\\b", "\\bhr\\b", "\\binput\\b", "\\bbutton\\b",
            "\\bform\\b", "\\blabel\\b", "\\bselect\\b", "\\boption\\b", "\\btextarea\\b",
            "\\btable\\b", "\\btr\\b", "\\btd\\b", "\\bth\\b", "\\bul\\b", "\\bol\\b", "\\bli\\b",
            "\\bheader\\b", "\\bfooter\\b", "\\bnav\\b", "\\bsection\\b", "\\barticle\\b",
            "\\baside\\b", "\\bmain\\b", "\\bfigure\\b", "\\bfigcaption\\b"
        ]
        for pattern in keywords:
            self.highlighting_rules.append((QRegularExpression(pattern), keyword_format))
        # 属性格式
        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("#9cdcfe"))  # 浅蓝色
        attributes = [
            "\\bclass\\b", "\\bid\\b", "\\bsrc\\b", "\\bhref\\b", "\\balt\\b", "\\btitle\\b",
            "\\bwidth\\b", "\\bheight\\b", "\\bstyle\\b", "\\btype\\b", "\\brel\\b",
            "\\bname\\b", "\\bvalue\\b", "\\bplaceholder\\b", "\\brequired\\b", "\\bdisabled\\b",
            "\\bchecked\\b", "\\bselected\\b", "\\brows\\b", "\\bcols\\b", "\\bmaxlength\\b"
        ]
        for pattern in attributes:
            self.highlighting_rules.append((QRegularExpression(pattern), attribute_format))
        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178"))  # 橙色
        self.highlighting_rules.append((QRegularExpression("\"[^\"]*\""), string_format))
        self.highlighting_rules.append((QRegularExpression("'[^']*'"), string_format))
        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955"))  # 绿色
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression("<!--[^-]*-*>"), comment_format))
        self.highlighting_rules.append((QRegularExpression("//[^\n]*"), comment_format))
        # 标签符号格式
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#808080"))  # 灰色
        self.highlighting_rules.append((QRegularExpression("[<>]"), tag_format))
        # CSS 格式
        css_format = QTextCharFormat()
        css_format.setForeground(QColor("#d7ba7d"))  # 黄色
        css_properties = [
            "\\bcolor\\b", "\\bbackground\\b", "\\bfont\\b", "\\bmargin\\b", "\\bpadding\\b",
            "\\bwidth\\b", "\\bheight\\b", "\\bdisplay\\b", "\\bposition\\b", "\\bfloat\\b",
            "\\bborder\\b", "\\btext-align\\b", "\\bvertical-align\\b", "\\bopacity\\b"
        ]
        for pattern in css_properties:
            self.highlighting_rules.append((QRegularExpression(pattern), css_format))
        # 数字格式
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8"))  # 浅绿色
        self.highlighting_rules.append((QRegularExpression("\\b\\d+\\b"), number_format))
        # DOCTYPE 格式
        doctype_format = QTextCharFormat()
        doctype_format.setForeground(QColor("#569cd6"))  # 蓝色
        doctype_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression("<!DOCTYPE[^>]*>"), doctype_format))
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                index = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(index, length, format)
                match = expression.match(text, index + length)
        self.setCurrentBlockState(0)

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_editor()
        # 新增撤销栈内存回收定时器
        self.gc_timer = QTimer(self)
        self.gc_timer.setInterval(8000)
        self.document().setMaximumBlockCount(0)  # 这个是文本块上限，不是撤销
        # Qt6 下 QTextDocument 依然没有撤销栈接口
        self.gc_timer.timeout.connect(self.clean_undo_stack)
        self.gc_timer.start()
    def setup_editor(self):
        # 设置等宽字体
        font = QFont("Consolas", 11)
        self.setFont(font)
        # 设置行高
        self.document().setDocumentMargin(10)
        # 设置制表符宽度
        self.setTabStopDistance(40)
        # 设置语法高亮
        self.highlighter = HTMLHighlighter(self.document())
    def clean_undo_stack(self):
        """撤销栈内存回收，防止高频编辑堆栈溢出"""
        doc = self.document()


class ExportWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    def __init__(self, html_content, export_path, export_type):
        super().__init__()
        self.html_content = html_content
        self.export_path = export_path
        self.export_type = export_type
    def run(self):
        try:
            if self.export_type == "single_html":
                self.export_single_html()
            elif self.export_type == "project_zip":
                self.export_project_zip()
            elif self.export_type == "minified":
                self.export_minified()
            self.finished.emit(self.export_path)
        except Exception as e:
            err_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.error.emit(err_msg)
    def export_single_html(self):
        self.progress.emit(50)
        with open(self.export_path, 'w', encoding='utf-8') as f:
            f.write(self.html_content)
        self.progress.emit(100)
    def export_project_zip(self):
        self.progress.emit(20)
        # 创建临时目录结构
        temp_dir = os.path.join(os.path.dirname(self.export_path), "temp_export")
        os.makedirs(temp_dir, exist_ok=True)
        # 创建标准项目结构
        with open(os.path.join(temp_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(self.html_content)
        self.progress.emit(40)
        # 创建 CSS 目录和默认样式
        css_dir = os.path.join(temp_dir, "css")
        os.makedirs(css_dir, exist_ok=True)
        with open(os.path.join(css_dir, "style.css"), 'w', encoding='utf-8') as f:
            f.write("/* 你的样式文件 */\nbody { margin: 0; padding: 20px; }")
        self.progress.emit(60)
        # 创建 JS 目录
        js_dir = os.path.join(temp_dir, "js")
        os.makedirs(js_dir, exist_ok=True)
        with open(os.path.join(js_dir, "script.js"), 'w', encoding='utf-8') as f:
            f.write("// 你的 JavaScript 文件\nconsole.log('Hello World!');")
        self.progress.emit(80)
        # 创建 README
        with open(os.path.join(temp_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(f"# HTML 项目\n\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # 压缩为 ZIP
        with zipfile.ZipFile(self.export_path, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        # 清理临时文件
        shutil.rmtree(temp_dir)
        self.progress.emit(100)
    def export_minified(self):
        self.progress.emit(30)
        # 简单的 HTML 压缩
        minified_html = self.html_content
        # 移除多余空白
        minified_html = ' '.join(minified_html.split())
        # 移除注释（简单实现）
        minified_html = minified_html.replace('<!--', '').replace('-->', '')
        self.progress.emit(70)
        with open(self.export_path, 'w', encoding='utf-8') as f:
            f.write(minified_html)
        self.progress.emit(100)

class ExportDialog(QDialog):
    def __init__(self, parent=None, html_content=""):
        super().__init__(parent)
        self.html_content = html_content
        self.setup_ui()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    def setup_ui(self):
        self.setWindowTitle("导出")
        self.setFixedSize(450, 200)
        # 简单深色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QComboBox, QLineEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        # 导出类型
        type_layout = QHBoxLayout()
        type_label = QLabel("导出类型:")
        self.export_type = QComboBox()
        self.export_type.addItems(["单个HTML文件", "完整项目(ZIP)", "压缩版HTML"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.export_type)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        # 导出路径
        path_layout = QHBoxLayout()
        path_label = QLabel("保存路径:")
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("点击浏览选择路径...")
        self.browse_btn = QPushButton("浏览")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)
        layout.addSpacing(10)
        # 按钮
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("导出")
        self.export_btn.clicked.connect(self.do_export)
        self.export_btn.setStyleSheet("background-color: #569cd6;")
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
    def browse_path(self):
        export_type = self.export_type.currentIndex()
        if export_type == 1:  # ZIP
            path, _ = QFileDialog.getSaveFileName(self, "保存项目", "", "ZIP文件 (*.zip)")
        else:  # HTML
            path, _ = QFileDialog.getSaveFileName(self, "保存HTML", "", "HTML文件 (*.html)")
        if path:
            self.path_edit.setText(path)
    def do_export(self):
        path = self.path_edit.text()
        if not path:
            QMessageBox.warning(self, "警告", "请选择保存路径")
            return
        try:
            if self.export_type.currentIndex() == 0:  # 单个HTML
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.html_content)
            elif self.export_type.currentIndex() == 1:  # 项目ZIP
                with zipfile.ZipFile(path, 'w') as zipf:
                    zipf.writestr("index.html", self.html_content)
                    zipf.writestr("css/style.css", "/* CSS文件 */\nbody { margin: 0; }")
                    zipf.writestr("js/script.js", "// JS文件\nconsole.log('hello');")
            else:  # 压缩版
                compressed = ' '.join(self.html_content.split())
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(compressed)
            QMessageBox.information(self, "成功", f"导出完成!\n{path}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

class HTMLPreview(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setup_preview()
        # 缓存渲染优化
    def setup_preview(self):
        self.setHtml("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #569cd6;
                }
            </style>
        </head>
        <body>
            <h1>HTML 预览</h1>
            <p>开始编写 HTML 代码以查看预览...</p>
        </body>
        </html>
        """)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setFixedSize(400, 340)
        # 简单深色主题
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QGroupBox {
                color: #569cd6;
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QComboBox, QSpinBox {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QCheckBox {
                color: #e0e0e0;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #569cd6;
                border: 1px solid #569cd6;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        # 字体设置
        font_group = QGroupBox("编辑器设置")
        font_layout = QFormLayout(font_group)
        font_layout.setVerticalSpacing(10)
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Consolas", "Courier New", "Monaco"])
        font_layout.addRow("字体:", self.font_combo)
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(11)
        font_layout.addRow("字体大小:", self.font_size)
        self.syntax_highlight = QCheckBox("启用语法高亮")
        self.syntax_highlight.setChecked(True)
        font_layout.addRow(self.syntax_highlight)
        layout.addWidget(font_group)
        # 预览设置
        preview_group = QGroupBox("预览设置")
        preview_layout = QFormLayout(preview_group)
        preview_layout.setVerticalSpacing(10)
        self.preview_delay = QSpinBox()
        self.preview_delay.setRange(100, 3000)
        self.preview_delay.setValue(500)
        self.preview_delay.setSuffix(" ms")
        preview_layout.addRow("预览延迟:", self.preview_delay)
        self.auto_preview = QCheckBox("自动实时预览")
        self.auto_preview.setChecked(True)
        preview_layout.addRow(self.auto_preview)
        layout.addWidget(preview_group)
        # 积木模式设置
        block_group = QGroupBox("积木节点设置")
        block_layout = QFormLayout(block_group)
        self.auto_sync = QCheckBox("代码/节点双向自动同步")
        self.auto_sync.setChecked(True)
        block_layout.addRow(self.auto_sync)
        layout.addWidget(block_group)
        layout.addStretch()
        # 按钮
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("应用")
        self.apply_btn.clicked.connect(self.apply_settings)
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept_and_apply)
        self.ok_btn.setStyleSheet("background-color: #569cd6;")
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.load_settings()
    def load_settings(self):
        settings = QSettings("HTMLBOX", "Editor")
        self.font_combo.setCurrentText(settings.value("editor/font", "Consolas"))
        self.font_size.setValue(int(settings.value("editor/font_size", 11)))
        self.syntax_highlight.setChecked(settings.value("editor/syntax_highlight", True, type=bool))
        self.preview_delay.setValue(int(settings.value("preview/delay", 500)))
        self.auto_preview.setChecked(settings.value("preview/auto", True, type=bool))
        self.auto_sync.setChecked(settings.value("block/auto_sync", True, type=bool))
    def save_settings(self):
        settings = QSettings("HTMLBOX", "Editor")
        settings.setValue("editor/font", self.font_combo.currentText())
        settings.setValue("editor/font_size", self.font_size.value())
        settings.setValue("editor/syntax_highlight", self.syntax_highlight.isChecked())
        settings.setValue("preview/delay", self.preview_delay.value())
        settings.setValue("preview/auto", self.auto_preview.isChecked())
        settings.setValue("block/auto_sync", self.auto_sync.isChecked())
    def apply_settings(self):
        self.save_settings()
        if self.parent:
            self.parent.apply_settings()
        QMessageBox.information(self, "提示", "设置已应用")
    def accept_and_apply(self):
        self.save_settings()
        if self.parent:
            self.parent.apply_settings()
        self.accept()

# ===================== 全新新增：积木节点整套模块 =====================
class BlockNodeItem(QTreeWidgetItem):
    """节点树单项，存储组件数据"""
    def __init__(self, tag_name, attrs=None, inner_text="", child_nodes=None):
        super().__init__()
        self.tag = tag_name
        self.attrs = attrs if attrs else {}
        self.inner_text = inner_text
        self.child_nodes = child_nodes if child_nodes else []
        self.setText(0, tag_name)
        self.setIcon(0, QIcon())
        self.setData(0, Qt.UserRole, self.serialize())
    def serialize(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "inner_text": self.inner_text,
            "children": [child.serialize() for child in self.child_nodes]
        }
    def deserialize(self, data):
        self.tag = data["tag"]
        self.attrs = data["attrs"]
        self.inner_text = data["inner_text"]
        self.child_nodes = []
        self.setText(0, self.tag)
        for child_data in data["children"]:
            child_item = BlockNodeItem("div")
            child_item.deserialize(child_data)
            self.addChild(child_item)
            self.child_nodes.append(child_item)
        self.setData(0, Qt.UserRole, self.serialize())
    def to_html(self):
        attr_str = " ".join([f'{k}="{v}"' for k, v in self.attrs.items()])
        children_html = "".join([c.to_html() for c in self.child_nodes])
        if self.tag in ["br", "hr", "img"]:
            return f"<{self.tag} {attr_str}/>"
        return f"<{self.tag} {attr_str}>{self.inner_text}{children_html}</{self.tag}>"

class BlockLibraryList(QListWidget):
    """左侧积木素材库，支持拖拽"""
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #444;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """)
        self.load_library()
    def load_library(self):
        lib_groups = {
            "容器": ["div", "section", "header", "footer", "nav", "article"],
            "文本": ["p", "h1", "h2", "h3", "span", "a"],
            "媒体": ["img", "br", "hr"],
            "表单": ["button", "input", "label", "textarea"],
            "列表": ["ul", "ol", "li"],
            "表格": ["table", "tr", "td", "th"]
        }
        for group, tags in lib_groups.items():
            group_item = QListWidgetItem(f"==== {group} ====")
            group_item.setFlags(Qt.NoItemFlags)
            group_item.setForeground(QColor("#569cd6"))
            self.addItem(group_item)
            for tag in tags:
                item = QListWidgetItem(tag)
                item.setData(Qt.UserRole, tag)
                self.addItem(item)
    def startDrag(self, actions):
        drag = QDrag(self)
        mime = QMimeData()
        current = self.currentItem()
        tag = current.data(Qt.UserRole)
        mime.setText(tag)
        drag.setMimeData(mime)
        drag.exec(actions)

class BlockTreeWidget(QTreeWidget):
    """中间节点层级树，接收拖拽"""
    nodeChanged = Signal()
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setHeaderLabel("页面节点树")
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #444;
            }
            QTreeWidget::item:selected {
                background-color: #255577;
                border: 1px solid #569cd6;
            }
        """)
        self.root = BlockNodeItem("html", {"lang":"zh-CN"})
        head_node = BlockNodeItem("head")
        body_node = BlockNodeItem("body")
        self.root.addChild(head_node)
        self.root.addChild(body_node)
        self.addTopLevelItem(self.root)
        self.expandAll()
        self.itemChanged.connect(self.on_item_modify)
    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            super().dragEnterEvent(e)
    def dropEvent(self, e):
        target = self.itemAt(e.position().toPoint())
        tag = e.mimeData().text()
        if target and tag and not tag.startswith("===="):
            new_node = BlockNodeItem(tag)
            target.addChild(new_node)
            self.expandItem(target)
            self.nodeChanged.emit()
        super().dropEvent(e)
    def on_item_modify(self):
        self.nodeChanged.emit()
    def clear_all(self):
        self.clear()
        self.root = BlockNodeItem("html", {"lang":"zh-CN"})
        head_node = BlockNodeItem("head")
        body_node = BlockNodeItem("body")
        self.root.addChild(head_node)
        self.root.addChild(body_node)
        self.addTopLevelItem(self.root)
        self.expandAll()
        self.nodeChanged.emit()
    def generate_full_html(self):
        doctype = "<!DOCTYPE html>\n"
        html = self.root.to_html()
        return doctype + html
    def load_from_serial(self, root_data):
        self.clear()
        self.root = BlockNodeItem("html")
        self.root.deserialize(root_data)
        self.addTopLevelItem(self.root)
        self.expandAll()
        self.nodeChanged.emit()

class BlockPropertyPanel(QWidget):
    """右侧节点属性编辑面板"""
    propChange = Signal()
    def __init__(self, tree_widget):
        super().__init__()
        self.tree = tree_widget
        self.current_node = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10,10,10,10)
        self.setStyleSheet("background:#252525;color:#eee;")
        # 标签
        self.info_label = QLabel("选中节点编辑属性")
        layout.addWidget(self.info_label)
        # 文本内容
        self.text_group = QGroupBox("内部文本")
        text_layout = QVBoxLayout(self.text_group)
        self.text_edit = QLineEdit()
        self.text_edit.textChanged.connect(self.on_text_change)
        text_layout.addWidget(self.text_edit)
        layout.addWidget(self.text_group)
        # 属性编辑
        self.attr_group = QGroupBox("标签属性")
        attr_layout = QFormLayout(self.attr_group)
        self.attr_key = QLineEdit()
        self.attr_val = QLineEdit()
        add_attr_btn = QPushButton("添加属性")
        add_attr_btn.clicked.connect(self.add_attr)
        attr_layout.addRow("属性名", self.attr_key)
        attr_layout.addRow("属性值", self.attr_val)
        attr_layout.addRow("", add_attr_btn)
        layout.addWidget(self.attr_group)
        # 节点操作按钮
        btn_layout = QHBoxLayout()
        self.copy_btn = QPushButton("复制节点")
        self.del_btn = QPushButton("删除节点")
        self.copy_btn.clicked.connect(self.copy_node)
        self.del_btn.clicked.connect(self.del_node)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)
        layout.addStretch()
    def set_target_node(self, node):
        self.current_node = node
        if not node:
            self.info_label.setText("未选中节点")
            self.text_edit.clear()
            return
        self.info_label.setText(f"当前标签：<{node.tag}>")
        self.text_edit.setText(node.inner_text)
    def on_text_change(self):
        if not self.current_node:
            return
        self.current_node.inner_text = self.text_edit.text()
        self.current_node.setData(0, Qt.UserRole, self.current_node.serialize())
        self.propChange.emit()
    def add_attr(self):
        if not self.current_node:
            return
        k = self.attr_key.text().strip()
        v = self.attr_val.text().strip()
        if k:
            self.current_node.attrs[k] = v
            self.current_node.setData(0, Qt.UserRole, self.current_node.serialize())
            self.propChange.emit()
    def copy_node(self):
        if not self.current_node:
            return
        parent = self.current_node.parent()
        copy_node = BlockNodeItem(self.current_node.tag, self.current_node.attrs.copy(), self.current_node.inner_text)
        parent.addChild(copy_node)
        self.tree.expandItem(parent)
        self.tree.nodeChanged.emit()
    def del_node(self):
        if not self.current_node or self.current_node.tag in ["html", "head", "body"]:
            return
        parent = self.current_node.parent()
        parent.removeChild(self.current_node)
        self.tree.nodeChanged.emit()

class BlockEditorWidget(QWidget):
    """完整积木编辑面板（素材库+节点树+属性面板）"""
    htmlUpdateSignal = Signal(str)
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0,0,0,0)
        # 1.左侧素材库
        self.lib_list = BlockLibraryList()
        self.lib_list.setFixedWidth(160)
        # 2.中间节点树
        self.tree_widget = BlockTreeWidget()
        self.tree_widget.nodeChanged.connect(self.on_tree_modified)
        self.tree_widget.itemSelectionChanged.connect(self.on_select_node)
        # 3.右侧属性面板
        self.prop_panel = BlockPropertyPanel(self.tree_widget)
        self.prop_panel.setFixedWidth(220)
        self.prop_panel.propChange.connect(self.on_tree_modified)
        # 分割器
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.lib_list)
        splitter1.addWidget(self.tree_widget)
        splitter1.addWidget(self.prop_panel)
        splitter1.setSizes([160, 400, 220])
        main_layout.addWidget(splitter1)
    def on_select_node(self):
        selected = self.tree_widget.currentItem()
        self.prop_panel.set_target_node(selected)
    def on_tree_modified(self):
        html = self.tree_widget.generate_full_html()
        self.htmlUpdateSignal.emit(html)

    def load_html_to_tree(self, html_str):
        """外部传入HTML文本，自动解析并渲染到积木树"""
        from html_dom_parser import html_to_node_tree

        root_model = html_to_node_tree(html_str)
        if not root_model:
            return

        # 把解析出来的通用节点 → 转为 BlockNodeItem
        def model_to_item(node):
            item = BlockNodeItem(node.tag_name, node.attrs, node.inner_text)
            for child_model in node.children:
                child_item = model_to_item(child_model)
                item.addChild(child_item)
                item.child_nodes.append(child_item)
            return item

        new_root = model_to_item(root_model)
        serial_data = new_root.serialize()
        self.tree_widget.load_from_serial(serial_data)

    def get_serialized_nodes(self):
        return self.tree_widget.root.serialize()
    def load_serialized_nodes(self, data):
        self.tree_widget.load_from_serial(data)

# ===================== 新增 .htbx 工程文件读写工具 =====================
class HTBXProject:
    @staticmethod
    def save_project(file_path, html_code, node_tree_data):
        data = {
            "version": "2.0.0",
            "html": html_code,
            "nodes": node_tree_data,
            "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    @staticmethod
    def load_project(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

# ===================== 主窗口（整合双模式、全部原有逻辑） =====================
class DarkThemeHTMLIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("HTMLBOX", "Editor")
        # 全局变量
        self.edit_mode = "code"  # code / block
        self.current_htbx_path = ""
        self.current_html_path = ""
        self.auto_sync = True
        # 防抖预览定时器重构
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.update_preview)
        # 初始化UI
        # 设置启动窗口宽、高，推荐适中尺寸，你可以自由修改数字
        self.resize(1100, 720)

        # 窗口启动自动在屏幕中间（非常好用，加上！）
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.init_ui()
        # 全局异常捕获
        sys.excepthook = self.global_exception_handler
    def global_exception_handler(self, exc_type, exc_val, exc_tb):
        err = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
        QMessageBox.critical(self, "程序异常", f"操作发生错误：\n{err[:1000]}")
    def init_ui(self):
        self.setWindowTitle("HTML BOX - 专业代码模式")
        self.setGeometry(100, 100, 1300, 800)
        self.apply_dark_theme()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # 工具栏
        self.create_toolbar()
        # 模式切换顶部栏

        # 主分割区域（左侧编辑器/积木 + 右侧预览）
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        # 左侧容器（代码编辑器/积木编辑器切换）
        self.left_stack = QWidget()
        self.left_stack_layout = QVBoxLayout(self.left_stack)
        self.left_stack_layout.setContentsMargins(5,5,5,5)
        # 1.原版代码编辑器
        self.code_frame = QFrame()
        code_layout = QVBoxLayout(self.code_frame)
        code_label = QLabel("HTML 代码编辑器")
        code_label.setStyleSheet("color: #569cd6; font-weight:bold; font-size:14px;")
        self.editor = CodeEditor()
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        code_layout.addWidget(code_label)
        code_layout.addWidget(self.editor)
        # 2.全新积木编辑器
        self.block_editor = BlockEditorWidget()
        self.block_editor.htmlUpdateSignal.connect(self.on_block_html_changed)
        # 默认加载代码模式
        self.left_stack_layout.addWidget(self.code_frame)
        # 右侧预览面板
        preview_frame = QFrame()
        preview_layout = QVBoxLayout(preview_frame)
        self.preview = HTMLPreview()
        preview_layout.addWidget(self.preview)
        # 加入分割器
        self.main_splitter.addWidget(self.left_stack)
        self.main_splitter.addWidget(preview_frame)
        self.main_splitter.setSizes([650, 550])
        # 状态栏
        self.create_statusbar()
        # 信号绑定
        self.editor.textChanged.connect(self.on_text_changed)
        self.apply_settings()

    def create_mode_switch_bar(self):
        mode_bar = QWidget()
        bar_layout = QHBoxLayout(mode_bar)
        bar_layout.setContentsMargins(10, 2, 10, 2)  # 缩小上下边距，防止拉高
        mode_label = QLabel("编辑模式：")
        self.code_mode_btn = QPushButton("📝 专业代码模式")
        self.block_mode_btn = QPushButton("🧩 积木节点模式")
        self.code_mode_btn.clicked.connect(self.switch_code_mode)
        self.block_mode_btn.clicked.connect(self.switch_block_mode)
        bar_layout.addWidget(mode_label)
        bar_layout.addWidget(self.code_mode_btn)
        bar_layout.addWidget(self.block_mode_btn)
        bar_layout.addStretch()
        # 工程文件按钮
        self.save_htbx_btn = QPushButton("保存工程(.htbx)")
        self.load_htbx_btn = QPushButton("打开工程(.htbx)")
        self.save_htbx_btn.clicked.connect(self.save_htbx_project)
        self.load_htbx_btn.clicked.connect(self.load_htbx_project)
        bar_layout.addWidget(self.save_htbx_btn)
        bar_layout.addWidget(self.load_htbx_btn)
        return mode_bar  # 返回整块控件，交给工具栏摆放

    def switch_code_mode(self):
        if self.edit_mode == "code":
            return
        # 同步积木生成代码到编辑器
        #block_html = self.block_editor.tree_widget.generate_full_html()
        #self.editor.setPlainText(block_html)
        # 清空左侧布局，切换为代码面板
        self.clear_left_stack()
        self.left_stack_layout.addWidget(self.code_frame)
        self.edit_mode = "code"
        self.setWindowTitle("HTML BOX - 专业代码模式")
        self.status_label.setText("已切换：代码编辑模式")
    def switch_block_mode(self):
        if self.edit_mode == "block":
            return
        # 读取代码，生成积木（只读取，不改代码）
        code_html = self.editor.toPlainText()
        self.block_editor.load_html_to_tree(code_html)
        # 切换界面
        self.clear_left_stack()
        self.left_stack_layout.addWidget(self.block_editor)
        self.edit_mode = "block"
        self.setWindowTitle("HTML BOX - 积木节点模式")
        self.status_label.setText("已切换：积木节点模式")
    def clear_left_stack(self):
        while self.left_stack_layout.count():
            item = self.left_stack_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
    def on_block_html_changed(self, html):
        if self.auto_sync and self.edit_mode == "block":
            #self.editor.blockSignals(True)
            #self.editor.setPlainText(html)
            #self.editor.blockSignals(False)
            self.preview_timer.start(int(self.settings.value("preview/delay", 500)))
    def create_toolbar(self):
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        # 新建文件动作
        new_action = QAction("新建", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        # 打开文件动作
        open_action = QAction("打开", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        # 保存文件动作
        save_action = QAction("保存", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        # 运行/预览动作
        run_action = QAction("预览", self)
        run_action.setShortcut(Qt.CTRL | Qt.Key_R)
        run_action.triggered.connect(self.update_preview)
        toolbar.addAction(run_action)
        toolbar.addSeparator()
        # 导出动作
        export_action = QAction("导出", self)
        export_action.setShortcut(Qt.CTRL | Qt.Key_E)
        export_action.triggered.connect(self.export_file)
        toolbar.addAction(export_action)
        # 设置动作
        settings_action = QAction("设置", self)
        settings_action.setShortcut(Qt.CTRL | Qt.Key_Comma)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)
        # 关于动作
        about_action = QAction("关于", self)
        about_action.setShortcut(Qt.CTRL | Qt.Key_B)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        toolbar.addSeparator()
        mode_widget = self.create_mode_switch_bar()
        toolbar.addWidget(mode_widget)
    def create_statusbar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.status_label = QLabel("就绪 | 代码模式")
        status_bar.addWidget(self.status_label)
    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QToolBar {
                background-color: #3c3c3c;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: #505050;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QToolButton:hover {
                background-color: #606060;
            }
            QToolButton:pressed {
                background-color: #404040;
            }
            QSplitter::handle {
                background-color: #404040;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:vertical {
                height: 2px;
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: white;
            }
            QFrame {
                border-radius: 8px;
                background-color: #2d2d2d;
            }
            QPushButton {
                background:#444;color:#eee;padding:4px 10px;border-radius:3px;
            }
            QPushButton:hover {background:#555}
        """)
    def apply_settings(self):
        # 字体
        font_family = self.settings.value("editor/font", "Consolas")
        font_size = int(self.settings.value("editor/font_size", 11))
        font = QFont(font_family, font_size)
        self.editor.setFont(font)
        # 语法高亮
        syntax_highlight = self.settings.value("editor/syntax_highlight", True, type=bool)
        if syntax_highlight:
            if not hasattr(self.editor, 'highlighter') or self.editor.highlighter is None:
                self.editor.highlighter = HTMLHighlighter(self.editor.document())
        else:
            if hasattr(self.editor, 'highlighter') and self.editor.highlighter is not None:
                self.editor.highlighter.setDocument(None)
                self.editor.highlighter = None
        # 预览延迟
        delay = int(self.settings.value("preview/delay", 500))
        self.preview_timer.setInterval(delay)
        # 自动预览
        auto_preview = self.settings.value("preview/auto", True, type=bool)
        try:
            self.editor.textChanged.disconnect(self.on_text_changed)
        except RuntimeError:
            pass
        if auto_preview:
            self.editor.textChanged.connect(self.on_text_changed)
        # 双向同步开关
        self.auto_sync = self.settings.value("block/auto_sync", True, type=bool)
        self.status_label.setText("设置已应用")
    def on_text_changed(self):
        auto_preview = self.settings.value("preview/auto", True, type=bool)
        if auto_preview:
            self.preview_timer.start(int(self.settings.value("preview/delay", 500)))
    def update_preview(self):
        html_content = self.get_current_html()
        self.preview.setHtml(html_content)
        self.status_label.setText("预览已更新")
    def get_current_html(self):
        if self.edit_mode == "code":
            return self.editor.toPlainText()
        else:
            return self.block_editor.tree_widget.generate_full_html()
    # 原有文件操作（完全保留）
    def new_file(self):
        self.editor.clear()
        self.block_editor.tree_widget.clear_all()
        self.current_html_path = ""
        self.current_htbx_path = ""
        self.setWindowTitle("HTML BOX - 新文件")
        self.status_label.setText("已创建新文件")
        self.update_preview()
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开 HTML 文件", "", "HTML 文件 (*.html *.htm);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.setPlainText(content)
                    self.current_html_path = file_path
                    self.setWindowTitle(f"HTML BOX - {os.path.basename(file_path)}")
                    self.status_label.setText(f"已打开: {file_path}")
                    self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法打开文件: {str(e)}")
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存 HTML 文件", "", "HTML 文件 (*.html *.htm);;所有文件 (*)"
        )
        if file_path:
            try:
                html = self.get_current_html()
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(html)
                    self.current_html_path = file_path
                    self.setWindowTitle(f"HTML BOX - {os.path.basename(file_path)}")
                    self.status_label.setText(f"已保存: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件: {str(e)}")
    # 新增 .htbx 工程保存/加载
    def save_htbx_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存HTMLBOX工程", "", "HTBX工程 (*.htbx)")
        if not path:
            return
        html = self.get_current_html()
        node_data = self.block_editor.get_serialized_nodes()
        HTBXProject.save_project(path, html, node_data)
        self.current_htbx_path = path
        QMessageBox.information(self, "完成", f"工程已保存至：{path}")
        self.status_label.setText(f"工程已保存 {path}")
    def load_htbx_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开HTMLBOX工程", "", "HTBX工程 (*.htbx)")
        if not path:
            return
        proj_data = HTBXProject.load_project(path)
        html_code = proj_data["html"]
        node_data = proj_data["nodes"]
        # 加载代码
        self.editor.setPlainText(html_code)
        # 加载节点树
        self.block_editor.tree_widget.load_from_serial(node_data)
        self.current_htbx_path = path
        self.setWindowTitle(f"HTML BOX - {os.path.basename(path)}")
        self.update_preview()
        QMessageBox.information(self, "加载成功", "工程文件已载入，两种模式均可编辑")
    # 原有导出、设置、关于（完整保留）
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
    def export_file(self):
        html_content = self.get_current_html()
        dialog = ExportDialog(self, html_content)
        dialog.exec()
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ide = DarkThemeHTMLIDE()
    ide.show()
    sys.exit(app.exec())
