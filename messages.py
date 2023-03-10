help_message = '''
Здравствуйте! Я бот-менеджер паролей, рад вас приветствовать!
Я могу помочь вам сохранить и организовать ваши пароли.
Команды бота:
/new_app - создание нового приложение
/my_apps - просмотр ваших приложениии
/start - запус бота
/delete - удаление приложение из вашего аккаунта
/help - команды бота и информация о боте
'''
start_message = 'Здравствуйте! Я бот-менеджер паролей, рад вас приветствовать!\nЯ могу помочь вам сохранить и организовать ваши пароли.\nЕсли хочешь воспользоваться нажми на команду /new_app'

empty_apps = 'У вас нет, приложении.Создайте при помощи команды /new_apps'

gen_password = 'Ваша генерация пароля...\n{}'

new_app_names = 'Введите пожалуйсте название приложение...'
new_app_password = 'Введите пароль: '
my_apps = 'Ваши приложение: '

succesful = 'Все прошло успешно.\nName:{}\nPassword:{}'

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'succesful':succesful,
    'new_app_names': new_app_names,
    'new_app_password': new_app_password,
    'my_apps':my_apps,
    'empty_apps': empty_apps
}