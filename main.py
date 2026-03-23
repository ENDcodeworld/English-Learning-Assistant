from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.clock import Clock
import random
import json
from datetime import datetime


class EnglishLearningApp(App):
    """英语学习助手APP"""
    
    # 单词库
    WORDS = {
        'CET4': [
            {'word': 'abandon', 'meaning': 'v. 放弃，抛弃', 'example': 'He abandoned his car in the snow.'},
            {'word': 'ability', 'meaning': 'n. 能力，才能', 'example': 'She has the ability to speak four languages.'},
            {'word': 'absence', 'meaning': 'n. 缺席，缺乏', 'example': 'His absence was noticed by everyone.'},
            {'word': 'absolute', 'meaning': 'adj. 绝对的，完全的', 'example': 'I have absolute confidence in you.'},
            {'word': 'absorb', 'meaning': 'v. 吸收，吸引', 'example': 'The sponge absorbs water quickly.'},
        ],
        'CET6': [
            {'word': 'ambiguous', 'meaning': 'adj. 模糊的，模棱两可的', 'example': 'His answer was ambiguous.'},
            {'word': 'apparent', 'meaning': 'adj. 明显的，表面的', 'example': 'It was apparent that he was lying.'},
            {'word': 'appropriate', 'meaning': 'adj. 适当的，恰当的', 'example': 'Please wear appropriate clothing.'},
            {'word': 'assume', 'meaning': 'v. 假设，承担', 'example': 'I assume you have heard the news.'},
            {'word': 'available', 'meaning': 'adj. 可用的，有空的', 'example': 'The book is available online.'},
        ],
        'IELTS': [
            {'word': 'accelerate', 'meaning': 'v. 加速，促进', 'example': 'The car accelerated rapidly.'},
            {'word': 'accommodate', 'meaning': 'v. 容纳，适应', 'example': 'The hotel can accommodate 500 guests.'},
            {'word': 'accumulate', 'meaning': 'v. 积累，积聚', 'example': 'Dust accumulated on the furniture.'},
            {'word': 'accurate', 'meaning': 'adj. 精确的，准确的', 'example': 'The weather forecast was accurate.'},
            {'word': 'acknowledge', 'meaning': 'v. 承认，致谢', 'example': 'He acknowledged his mistake.'},
        ]
    }
    
    # 常用句子
    SENTENCES = [
        {'en': 'How are you doing today?', 'cn': '你今天怎么样？', 'scene': '日常问候'},
        {'en': 'Could you help me with this?', 'cn': '你能帮我一下吗？', 'scene': '请求帮助'},
        {'en': 'I\'m looking forward to meeting you.', 'cn': '我期待见到你。', 'scene': '表达期待'},
        {'en': 'That sounds great!', 'cn': '听起来很棒！', 'scene': '表达赞同'},
        {'en': 'What do you think about it?', 'cn': '你觉得怎么样？', 'scene': '征求意见'},
        {'en': 'Let me think about it.', 'cn': '让我考虑一下。', 'scene': '需要时间'},
        {'en': 'I\'m not sure about that.', 'cn': '我不太确定。', 'scene': '表达不确定'},
        {'en': 'Can you repeat that, please?', 'cn': '你能重复一遍吗？', 'scene': '请求重复'},
    ]
    
    # 语法要点
    GRAMMAR = [
        {
            'title': '一般现在时',
            'rule': '表示经常性、习惯性的动作或状态',
            'structure': '主语 +动词原形/第三人称单数',
            'example': 'She goes to school every day.'
        },
        {
            'title': '现在进行时',
            'rule': '表示正在进行的动作',
            'structure': '主语 + am/is/are + doing',
            'example': 'They are playing basketball now.'
        },
        {
            'title': '一般过去时',
            'rule': '表示过去发生的动作',
            'structure': '主语 + 动词过去式',
            'example': 'I visited Beijing last year.'
        },
        {
            'title': '现在完成时',
            'rule': '表示过去发生对现在有影响的动作',
            'structure': '主语 + have/has + done',
            'example': 'I have finished my homework.'
        },
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_word = None
        self.study_count = 0
        self.correct_count = 0
    
    def build(self):
        self.title = '英语学习助手'
        Window.clearcolor = get_color_from_hex('#E8F5E9')
        
        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 标题
        title = Label(
            text='🇬🇧 英语学习助手',
            font_size=dp(26),
            color=get_color_from_hex('#1B5E20'),
            size_hint_y=None,
            height=dp(50),
            bold=True
        )
        self.root.add_widget(title)
        
        # 功能按钮区
        func_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        funcs = [
            ('📚 背单词', self.show_words),
            ('💬 学句子', self.show_sentences),
            ('📖 语法', self.show_grammar),
            ('🎮 测试', self.show_quiz),
        ]
        
        for text, callback in funcs:
            btn = Button(
                text=text,
                font_size=dp(14),
                background_color=get_color_from_hex('#4CAF50'),
                color=get_color_from_hex('#FFFFFF')
            )
            btn.bind(on_press=callback)
            func_box.add_widget(btn)
        
        self.root.add_widget(func_box)
        
        # 内容显示区
        self.content_box = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # 默认显示单词学习
        self.show_words(None)
        
        self.root.add_widget(self.content_box)
        
        # 统计信息
        self.stats_label = Label(
            text=f'今日学习: {self.study_count} 个单词 | 正确率: 0%',
            font_size=dp(12),
            color=get_color_from_hex('#666666'),
            size_hint_y=None,
            height=dp(30)
        )
        self.root.add_widget(self.stats_label)
        
        return self.root
    
    def clear_content(self):
        """清空内容区"""
        self.content_box.clear_widgets()
    
    def show_words(self, instance):
        """显示单词学习"""
        self.clear_content()
        
        # 级别选择
        level_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.level = 'CET4'
        for level in ['CET4', 'CET6', 'IELTS']:
            btn = ToggleButton(
                text=level,
                group='level',
                state='down' if level == 'CET4' else 'normal',
                background_color=get_color_from_hex('#81C784')
            )
            btn.bind(on_press=lambda x, l=level: self.change_level(l))
            level_box.add_widget(btn)
        
        self.content_box.add_widget(level_box)
        
        # 单词显示卡片
        self.word_card = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        with self.word_card.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.word_card.rect = Rectangle(size=self.word_card.size, pos=self.word_card.pos)
        self.word_card.bind(size=self._update_rect, pos=self._update_rect)
        
        self.word_label = Label(
            text='点击"下一个"开始学习',
            font_size=dp(32),
            color=get_color_from_hex('#1B5E20'),
            bold=True
        )
        self.word_card.add_widget(self.word_label)
        
        self.meaning_label = Label(
            text='',
            font_size=dp(18),
            color=get_color_from_hex('#424242'),
            markup=True
        )
        self.word_card.add_widget(self.meaning_label)
        
        self.example_label = Label(
            text='',
            font_size=dp(14),
            color=get_color_from_hex('#757575'),
            italic=True
        )
        self.word_card.add_widget(self.example_label)
        
        self.content_box.add_widget(self.word_card)
        
        # 控制按钮
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        show_btn = Button(
            text='👁️ 显示意思',
            background_color=get_color_from_hex('#FF9800'),
            color=get_color_from_hex('#FFFFFF')
        )
        show_btn.bind(on_press=self.show_meaning)
        btn_box.add_widget(show_btn)
        
        next_btn = Button(
            text='➡️ 下一个',
            background_color=get_color_from_hex('#2196F3'),
            color=get_color_from_hex('#FFFFFF')
        )
        next_btn.bind(on_press=self.next_word)
        btn_box.add_widget(next_btn)
        
        self.content_box.add_widget(btn_box)
        
        # 加载第一个单词
        self.next_word(None)
    
    def _update_rect(self, instance, value):
        """更新背景矩形"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def change_level(self, level):
        """切换级别"""
        self.level = level
        self.next_word(None)
    
    def next_word(self, instance):
        """下一个单词"""
        words = self.WORDS.get(self.level, self.WORDS['CET4'])
        self.current_word = random.choice(words)
        
        self.word_label.text = self.current_word['word']
        self.meaning_label.text = ''
        self.example_label.text = ''
        
        self.study_count += 1
        self.update_stats()
    
    def show_meaning(self, instance):
        """显示意思"""
        if self.current_word:
            self.meaning_label.text = f"[b]{self.current_word['meaning']}[/b]"
            self.example_label.text = f"例句: {self.current_word['example']}"
    
    def show_sentences(self, instance):
        """显示常用句子"""
        self.clear_content()
        
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        box.bind(minimum_height=box.setter('height'))
        
        for sent in self.SENTENCES:
            card = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5), size_hint_y=None, height=dp(120))
            with card.canvas.before:
                Color(*get_color_from_hex('#FFFFFF'))
                card.rect = Rectangle(size=card.size, pos=card.pos)
            card.bind(size=self._update_rect, pos=self._update_rect)
            
            card.add_widget(Label(
                text=f"[b]{sent['en']}[/b]",
                markup=True,
                font_size=dp(16),
                color=get_color_from_hex('#1B5E20'),
                halign='left'
            ))
            card.add_widget(Label(
                text=sent['cn'],
                font_size=dp(14),
                color=get_color_from_hex('#424242'),
                halign='left'
            ))
            card.add_widget(Label(
                text=f"场景: {sent['scene']}",
                font_size=dp(12),
                color=get_color_from_hex('#757575'),
                halign='left'
            ))
            
            box.add_widget(card)
        
        scroll.add_widget(box)
        self.content_box.add_widget(scroll)
    
    def show_grammar(self, instance):
        """显示语法学习"""
        self.clear_content()
        
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        box.bind(minimum_height=box.setter('height'))
        
        for gram in self.GRAMMAR:
            card = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5), size_hint_y=None, height=dp(150))
            with card.canvas.before:
                Color(*get_color_from_hex('#FFFFFF'))
                card.rect = Rectangle(size=card.size, pos=card.pos)
            card.bind(size=self._update_rect, pos=self._update_rect)
            
            card.add_widget(Label(
                text=f"[b]{gram['title']}[/b]",
                markup=True,
                font_size=dp(18),
                color=get_color_from_hex('#E91E63'),
                halign='left'
            ))
            card.add_widget(Label(
                text=f"用法: {gram['rule']}",
                font_size=dp(13),
                color=get_color_from_hex('#424242'),
                halign='left'
            ))
            card.add_widget(Label(
                text=f"结构: {gram['structure']}",
                font_size=dp(13),
                color=get_color_from_hex('#2196F3'),
                halign='left'
            ))
            card.add_widget(Label(
                text=f"例句: {gram['example']}",
                font_size=dp(12),
                color=get_color_from_hex('#757575'),
                halign='left'
            ))
            
            box.add_widget(card)
        
        scroll.add_widget(box)
        self.content_box.add_widget(scroll)
    
    def show_quiz(self, instance):
        """显示测试"""
        self.clear_content()
        
        # 随机选一道题
        words = self.WORDS['CET4']
        correct = random.choice(words)
        wrong_options = random.sample([w for w in words if w != correct], 3)
        
        options = [correct] + wrong_options
        random.shuffle(options)
        
        self.quiz_answer = correct['meaning']
        
        # 题目
        q_label = Label(
            text=f'"{correct["word"]}" 是什么意思？',
            font_size=dp(20),
            color=get_color_from_hex('#1B5E20'),
            size_hint_y=None,
            height=dp(80)
        )
        self.content_box.add_widget(q_label)
        
        # 选项
        for opt in options:
            btn = Button(
                text=opt['meaning'],
                font_size=dp(14),
                background_color=get_color_from_hex('#E3F2FD'),
                color=get_color_from_hex('#1565C0'),
                size_hint_y=None,
                height=dp(60)
            )
            btn.bind(on_press=lambda x, ans=opt['meaning']: self.check_answer(ans))
            self.content_box.add_widget(btn)
        
        # 结果显示
        self.quiz_result = Label(
            text='',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50)
        )
        self.content_box.add_widget(self.quiz_result)
        
        # 下一题按钮
        next_btn = Button(
            text='下一题',
            font_size=dp(16),
            background_color=get_color_from_hex('#4CAF50'),
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=None,
            height=dp(50)
        )
        next_btn.bind(on_press=self.show_quiz)
        self.content_box.add_widget(next_btn)
    
    def check_answer(self, answer):
        """检查答案"""
        if answer == self.quiz_answer:
            self.quiz_result.text = '[color=#4CAF50]✅ 回答正确！[/color]'
            self.quiz_result.markup = True
            self.correct_count += 1
        else:
            self.quiz_result.text = f'[color=#F44336]❌ 错误！正确答案是: {self.quiz_answer}[/color]'
            self.quiz_result.markup = True
        
        self.update_stats()
    
    def update_stats(self):
        """更新统计"""
        accuracy = int(self.correct_count / max(self.study_count, 1) * 100)
        self.stats_label.text = f'今日学习: {self.study_count} 个单词 | 正确率: {accuracy}%'


if __name__ == '__main__':
    EnglishLearningApp().run()
