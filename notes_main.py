# 1. подключение PyQt5

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
 
import json

###############################################################
# 2. Создание виджетов

app = QApplication([]) # приложение
 
'''Интерфейс приложения'''
#параметры окна приложения
notes_win = QWidget() # главное окно
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)
 
#виджеты окна приложения
list_notes = QListWidget() # список элементов
list_notes_label = QLabel('Список заметок')

# создание необходимых кнопок
button_note_create = QPushButton('Создать заметку') #появляется окно с полем "Введите имя заметки"
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
 
field_tag = QLineEdit('') # поле для ввода текста в одну строку
field_tag.setPlaceholderText('Введите тег...') # временная надпись
field_text = QTextEdit() # поле для ввода текста в несколько строк
list_tags = QListWidget() # виджет списка элементов
list_tags_label = QLabel('Список тегов')

##########################################################
#расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()

col_1 = QVBoxLayout() # левая колонка
col_1.addWidget(field_text)

# создание, сохранение, удаление и список заметок
col_2 = QVBoxLayout() # вертикальная линия
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout() # горизонтальная линия
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addLayout(row_1)
col_2.addWidget(button_note_save)

# создание, удаление и поиск по тегам
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag) # поле для ввода тегов
row_2 = QHBoxLayout() # горизонтальная линия
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)
col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)

notes_win.setLayout(layout_notes)

### функциональный блок

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удалния не выбрана!")

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)

       
notes_win.show()
with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)
app.exec()


######################## ПАМЯТКА

# 1. PyQt5
### Импортирование, виджеты, направляющие линии (верстка), функциональный блок, обработка событий, запуск приложения

### разделение функционала
# PyQt умеет сам:
# 1. создавать приложение и окно (app = Apllication([]))
# 2. создавать направляющие линии (line = QVBoxLayout())
# 3. размещать виджеты на линиях (line.addWidget(button))
# 4. размещать линии на линиях (line.addLayout(row))
# 5. закреплять линию в окне (window.setLayout(line))
# 6. реагировать на события (button.clicked.connect(function))
# 7. показывать окна и запускать приложения (window.show(), app.exec())

# PyQt делать не умеет (должны сделать мы):
# 1. показывание заметки, когда нажимаем на заметку в списке 
# 2. создавать новую пустую заметку
# 3. удалять выбранную заметку
# 4. сохранять написанную заметку


# 2. Работа с файлами
### Открытие файлов в 3 разных режимах ('r', 'w', 'a')
### Конструкция with open() as file - сессия работы с файлом
# with open('notes.txt', 'a') as file:
#     file.write('\nКак дела?')


# 3. Текстовый формат json
### json - словарь словарей в python
### Словари, ключи, значения, вложенность
# {
#     "название_заметки":{
#         "текст":"какой-то текст",
#         "теги":["какой-то тег 1", "какой-то тег 2"]
#     }
# }
