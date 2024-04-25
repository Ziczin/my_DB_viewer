from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import threading as th
import pickle

class Database:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            is_new_DB = True
            DB = {}
            
            if 'name' in kwargs:
                try:
                    with open(str(kwargs['name']) + ".db", "rb") as file:
                        DB = pickle.load(file)
                        is_new_DB = False
                              
                except:
                    with open(str(kwargs['name']) + ".db", "wb") as file:
                        DB = {}
            else:
                raise NameError("Database needs name!")

            if 'header' in kwargs and is_new_DB:
                if type(kwargs['header']) in (tuple, list):
                    cls.header = kwargs['header']
                else:
                    raise TypeError("Header must be list-like object")
            elif is_new_DB:
                    ValueError("Database needs header!")
            else:
                cls.header = DB['header']
                
            cls.instance = super(Database, cls).__new__(cls)
            cls.__data = DB['data'] if 'data' in DB else []
            cls.name = kwargs['name']
            
            return cls.instance
        
    def __init__(self, *args, **kwargs):
        for string in self.__data:
            if not len(string) == len(self.header):
                raise ValueError(f"{string} must match {self.header}")

    def save(self):
        with open(str(self.name) + ".db", "wb") as file:
            pickle.dump(
                {
                    'header': self.header,
                    'data': self.__data,
                    },
                file)
    def getIndex(self, target):
        if not target in self.header:
            raise IndexError(f"{target} not in {self.header}")
        return self.header.index(target)
        
    def getByID(self, ID):
        return self.__data[ID]

    def getByField(self, target, field):
        index = getIndex(field)
        for string in self.__data:
            if string[index] == target:
                return string

    def setByID(self, ID, *value):
        self.__data[ID] = value

    def append(self, *elements):
        if not len(elements) == len(self.header):
            raise ValueError(f"{elements} must match {self.header}")
        self.__data.append(elements)

    def deleteByID(self, ID):
        self.__data.pop(ID)

    def deleteByField(self, target, field, doAll=False):
        if not field in self.header:
            raise IndexError(f"{field} not in {self.header}")
        index = self.header.index(header)
        counter = 0
        while not counter == len(self.__data):
            if self.__data[counter][index] == target:
                self.__data.pop(counter)
                if not doAll: break
            else:
                counter += 1

    def modifyByID(self, ID, field, value):
        self.__data[ID][self.getIndex(field)] = value

    def getIdByData(self, *data):
        index = 0
        while not index == self.__data:
            if self.__data[index] == data:
                return index
            index += 1
        return None
        
    def get(self):
        return self.__data
    
    def __enter__(self):
        return self
                  
    def __exit__(self, type_, value, traceback):
        self.save()
        Database.delInstance()

    @classmethod
    def delInstance(cls):
        delattr(cls, 'instance')







 
class my_window:
    def __new__(cls, DB_name):
        if not hasattr(cls, 'instance'):
            cls.DB_name = DB_name
            cls.instance = super(my_window, cls).__new__(cls)
            return cls.instance


    #########################
    ### КОНФИГУРАЦИЯ ОКНА ###
    #########################
        
    def __init__(self, DB_name):
        th.Thread(target=self.init).start()

    def init(self):
        """
        Инициализация и функционирование происходят в потоке
        """
        self.reverse = False
        self.hovered_ID = 0
        self.hovered_string = []
        self.main_font = "Arial 12"
        self.main_BG_color = "#abcdef"

        ### ОБЛАСТЬ ОКНА ТОВАРОВ
        self.frames = {}
        self.articles = {}
        self.articles['vars'] = {}
        self.articles['labels'] = {}
        self.articles['buttons'] = {}
        self.articles['entries'] = {}

        ### СОЗДАНИЕ ПРИЛОЖЕНИЯ
        self.window=Tk()
        self.window.geometry("900x400")
        self.window.title("Мастер на все лапки")
        self.create_frames()
        self.update_tables()
        self.window.mainloop()


        
    #######################################
    ### ОСНОВНАЯ КОНФИГУРАЦИЯ ПРОГРАММЫ ###
    #######################################
        
    def articles_configure(self):
        """
        Определение элементов окна товаров
        """
        self.append_order = ['name', 'price', 'count']
        
        self.articles_table(
            300, 
            name = "Товар",
            price = "Цена",
            count = "Склад",
            )
        
        self.articles_vars(
            name = StringVar(),
            price = DoubleVar(),
            count = IntVar(),
            )
        
        self.articles_labels(
            name = "Наименование товара:",
            price = "Цена товара:",
            count = "Остаток на складе:",
            )
        
        self.articles_entries(
            'name', 'price', 'count',
            )
        
        self.articles_buttons(
            insert = {
                'name': "Добавить",
                'command': lambda: self.articles_append_to_table()},
            delete = {
                'name': "Удалить",
                'command': lambda: self.articles_remove_from_table()},
            update = {
                'name': "Записать\Обновить",
                'command': lambda: self.articles_update_in_table()},
            )
        
        self.articles_place()
        self.articles_binds()



    ############################
    ### РАЗМЕЩЕНИЕ НА ЭКРАНЕ ###
    ############################
        
    def articles_place(self):
        "Размещение в приложении всех элементов окна товара"
        self.articles['table'].place(x=10,y=10)
        
        self.articles['entries']['name'].place(x=350, y=60)
        self.articles['entries']['price'].place(x=350, y=140)
        self.articles['entries']['count'].place(x=350, y=220)
        
        self.articles['labels']['name'].place(x=350, y=20)
        self.articles['labels']['price'].place(x=350, y=100)
        self.articles['labels']['count'].place(x=350, y=180)
        
        self.articles['buttons']['insert'].place(x=600, y=60)
        self.articles['buttons']['delete'].place(x=600, y=100)
        self.articles['buttons']['update'].place(x=600, y=140)


        
    ########################
    ### СЛУЖЕБНЫЕ МЕТОДЫ ###
    ########################

    def clear_table(self): #
        "Очистка таблицы"
        for row in self.articles['table'].get_children():
            self.articles['table'].delete(row)

    def set_in_table(self, data): #
        "Подстановка значения в таблицу"
        self.articles['table'].insert(
            "", END, values=data)
        
    def update_tables(self): #
        "Обновить значения в таблицу"
        self.clear_table()
        with Database(name=self.DB_name) as DB:
            for row in DB.get():
                self.set_in_table(row)

    def select_articles(self, args): #
        "Выделить значение из таблицы и записать его в поля ввода"
        for row in self.articles['table'].selection():
            for index, elem in enumerate(args):
                elem.set(self.articles['table'].item(row)["values"][index])
        self.set_hovered_params()

    def get_data_by_entries(self):
        request = []
        for field in self.append_order:
            request.append(
                self.articles['vars'][field].get())
        return request
    
    def set_hovered_params(self):
        self.hovered_ID = DB.getIdByData(*self.get_data_by_entries())
        self.hovered_string = DB.getByID(self.hovered_ID)
        
    def sorted(self, target): #
        "Отсортировать таблицу по выбранному полю"
        self.reverse = not self.reverse
        self.clear_table()
        with Database(name=self.DB_name) as DB:
            for row in sorted(
                DB.get(),
                key=lambda x: x[DB.getIndex(target)],
                reverse=self.reverse):
                self.set_in_table(row)



    ###################
    ### ОПРЕДЕЛЕНИЯ ###
    ###################
    
    def articles_binds(self): #
        "Привязать к нажатию на строку метод её выделения"
        self.articles['table'].bind(
            "<<TreeviewSelect>>",
            lambda event: self.select_articles(
                self.articles['vars'].values()))
        


    #######################################
    ### АВТО-ОПРЕДЕЛЕНИЕ ЭЛЕМЕНТОВ ОКНА ###
    #######################################
        
    def create_frames(self):
        """
        Создание вкладок
        """
        self.notebook = Notebook()
        style = Style()
        style.configure("TFrame", background=self.main_BG_color)
        self.notebook.pack(expand=True, fill=BOTH)
        
        self.frames['articles'] = Frame(self.notebook)
        self.frames['buying'] = Frame(self.notebook)
        self.frames['selling'] = Frame(self.notebook)
        
        self.frames['articles'].pack(fill=BOTH, expand=True)
        self.frames['buying'].pack(fill=BOTH, expand=True)
        self.frames['selling'].pack(fill=BOTH, expand=True)
        
        self.notebook.add(self.frames['articles'], text="Товары")
        self.notebook.add(self.frames['buying'], text="Купить")
        self.notebook.add(self.frames['selling'], text="Продать")
        
        self.articles_configure()
        self.frame_buy()
        self.frame_sell()


    def clear_entries(self):
        for entry in self.articles['entries']:
            self.articles['entries'][entry].delete(0, END)
            
    def articles_append_to_table(self):
        with Database(name=self.DB_name) as DB:
            DB.append(*self.get_data_by_entries()) #####
        self.update_tables()
        self.clear_entries()
    
    def articles_remove_from_table(self):
        with Database(name=self.DB_name) as DB:
            DB.deleteByID(self.hovered_ID)
        self.update_tables()
        self.clear_entries()

    def articles_update_in_table(self):
        with Database(name=self.DB_name) as DB:
            DB.deleteByID(self.hovered_ID)
            DB.append(*self.get_data_by_entries())
        self.update_tables()
        self.clear_entries()

    def articles_table(self, width, **kwargs): #
        "Создание и определение столбцов таблицы окна товара"
        self.articles['table'] = Treeview(
            self.frames['articles'],
            columns=list(kwargs.keys()),
            show="headings")
        for key in kwargs:
            self.articles['table'].heading(
                key,
                text=kwargs[key],
                command=lambda col=key: self.sorted(col))
            self.articles['table'].column(key, width=width//len(kwargs), anchor="c")
        
    def articles_vars(self, **kwargs):
        """
        Создание переменных для хранения данных внутри
        Tkinter-элементов окна товара
        """
        for key in kwargs:
            self.articles['vars'][key] = kwargs[key]

    def articles_labels(self, **kwargs):
        "Создание текстовых меток окна товара"
        for key in kwargs:
            self.articles['labels'][key] = Label(
                self.frames['articles'],
                text=kwargs[key],
                font=self.main_font,
                background=self.main_BG_color)

    def articles_entries(self, *args):
        "Создание полей ввода окна товара"
        for arg in args:
            self.articles['entries'][arg] = Entry(
                self.frames['articles'],
                textvariable=self.articles['vars'][arg],
                font=self.main_font)

    def articles_buttons(self, **kwargs):
        "Создание кнопок окна товара"
        for key in kwargs:
            self.articles['buttons'][key] = Button(
                self.frames['articles'],
                text=kwargs[key]['name'],
                command=kwargs[key]['command'])
        
        

    
        
    def frame_buy(self): pass
    def frame_sell(self): pass

with Database(name="SHOP_DATABASE", header=['name', 'price', 'count']) as DB:
    pass
new_win = [my_window('SHOP_DATABASE') for i in range(10000)]


