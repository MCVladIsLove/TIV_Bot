from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from groq import Groq
import secret
import json
import re
#check pushing((
TELEGRAM_TOKEN = secret.tg
client_gpt = Groq(api_key=secret.gpt)
user_contexts = {}

json_format = '''{
    "commands": [ {"id" : ""} ],
    "response": ""
}'''

knowledge = """## База знаний для бота «Госуслуги»

### 1. Общая информация о портале «Госуслуги»
- **Портал «Госуслуги»** — это единая цифровая платформа, позволяющая гражданам Российской Федерации получать государственные, муниципальные и коммерческие услуги в электронном виде.
- Основная цель — **упростить взаимодействие** граждан с государственными органами (ФНС, МВД, ПФР, ФСС, Росреестр и др.), сократить очереди в МФЦ и снизить бюрократические издержки.
- Доступ к порталу возможен через:
  - Официальный сайт *gosuslugi.ru*.
  - Мобильное приложение «Госуслуги» для смартфонов и планшетов.
  - Региональные порталы (в некоторых субъектах РФ).

### 2. Регистрация, вход и учетная запись
- **Шаги регистрации**:
  1. Перейти на *gosuslugi.ru* или в мобильное приложение «Госуслуги».
  2. Ввести номер телефона и подтвердить его кодом из SMS.
  3. Указать свои персональные данные (ФИО, СНИЛС, дату рождения и др.).
  4. Пройти процедуру подтверждения личности (через банк, МФЦ или Почту России).
- **Уровни учётной записи**:
  - Упрощённая: базовые функции, не требующие подтверждения личности.
  - Стандартная: расширенные возможности после проверки СНИЛС и личности.
  - Подтверждённая: полный функционал, включая доступ к большинству государственных услуг и возможность подписывать документы ЭП (электронной подписью).
- **Восстановление доступа**:
  - По номеру телефона.
  - Через email.
  - С использованием резервных кодов (если были созданы заранее).

### 3. Популярные государственные услуги на портале
1. **Оформление документов**:
   - Заграничный паспорт (старого и нового образца).
   - Внутренний паспорт РФ (замена по достижению возраста или при смене фамилии).
   - Водительское удостоверение (получение, замена).
   - Свидетельство о рождении ребёнка.
2. **Учёт и регистрация**:
   - Регистрация по месту жительства или пребывания.
   - Постановка и снятие с воинского учёта.
   - Регистрация транспортных средств (приобретение, перерегистрация).
3. **Налоги и штрафы**:
   - Оплата налогов (транспортный, имущественный, НДФЛ).
   - Проверка и оплата штрафов ГИБДД.
   - Формирование справки о доходах (2-НДФЛ) и налоговый вычет.
4. **Социальные услуги и выплаты**:
   - Оформление пенсии (по старости, по инвалидности).
   - Пособие по уходу за ребёнком, декретные выплаты.
   - Получение сертификата на материнский капитал.
   - Оформление субсидий на оплату ЖКХ.
5. **Здоровье и медицина**:
   - Запись к врачу в государственные клиники.
   - Получение полиса ОМС.
   - Запрос и получение справок о прививках.

### 4. Дополнительные электронные сервисы
- **Цифровое образование и карьера**:
  - Поиск и подача заявлений в вузы и ссузы.
  - Запись на курсы повышения квалификации.
- **Бизнес-услуги**:
  - Регистрация ИП и ООО.
  - Получение выписки из ЕГРЮЛ/ЕГРИП.
  - Подача налоговой отчётности.
- **Прочие онлайн-сервисы**:
  - Проверка статуса документов (паспорта, прав и т.д.).
  - Электронная очередь в МФЦ (запись на приём).
  - Формирование и подача электронных обращений в государственные органы.

### 5. Вопросы безопасности и защиты персональных данных
- **Хранение данных**:
  - Все персональные данные хранятся в защищённых центрах обработки данных, соответствующих требованиям ФСТЭК и ФСБ.
- **Авторизация**:
  - Двухфакторная аутентификация (по желанию пользователя).
  - Использование электронной подписи для совершения юридически значимых действий.
- **Передача данных**:
  - Шифрованные каналы связи (HTTPS/TLS).
  - Безопасный обмен данными с органами власти и партнёрскими сервисами.
- **Советы по безопасности**:
  - Не передавать третьим лицам свой логин и пароль.
  - Использовать сложные пароли и регулярно их менять.
  - При потере телефона, где установлен аккаунт, срочно выходить из всех сеансов.

### 6. Программы лояльности и специальные предложения (необязательные для госуслуг, но возможны в интегрированных сервисах)
- **Кешбэк за оплату услуг**:
  - Некоторые банки могут предлагать повышенный кешбэк при оплате госпошлин через «Госуслуги».
- **Скидки на госуслуги**:
  - При подаче заявления на замену водительского удостоверения, выдачу паспорта или регистрацию автомобиля через портал можно получить скидку 30% на госпошлину (в некоторых случаях).
- **Партнёрские акции**:
  - Совместные программы с образовательными платформами, банками, страховыми компаниями — например, бесплатные вебинары или льготные тарифы при оформлении услуги через портал.

### 7. Политика обслуживания пользователей и поддержка
- **Каналы обратной связи**:
  - Горячая линия «Госуслуг»: единый номер 8-800-XXX-XX-XX (бесплатно по РФ).
  - Онлайн-чат в личном кабинете (при наличии подтверждённой учётной записи).
  - Официальные группы и чаты в мессенджерах и социальных сетях.
  - Раздел «Помощь» и «Частые вопросы» (FAQ) на сайте и в приложении.
- **Этика и стандарты обслуживания**:
  - Специалисты службы поддержки обязаны соблюдать принципы вежливости, конфиденциальности и оперативности.
  - Ответы на электронные обращения предоставляются в установленные законом сроки (обычно от 1 до 10 рабочих дней).
- **Решение споров и жалоб**:
  - При несогласии с решением госоргана пользователь может подать жалобу или написать обращение через портал.
  - В случае технических ошибок и недоступности сервиса можно оставить заявку в техподдержку для дальнейшего разбирательства.

### 8. Пошаговые инструкции и обучающие материалы
- **Пошаговые руководства (гайды)**:
  - Как оформить заграничный паспорт или заменить водительское удостоверение через «Госуслуги».
  - Как подать заявление на регистрацию брака или развод онлайн.
  - Как заполнить налоговую декларацию 3-НДФЛ и получить вычет.
- **Видеоинструкции и вебинары**:
  - Обзоры основных услуг портала и разъяснение законодательных изменений.
  - Вебинары с представителями госорганов и экспертов в области права, налогообложения и социальной защиты.
- **Шаблоны и бланки**:
  - Образцы заявлений и заявок, которые можно скачать и заполнить офлайн.
  - Рекомендации по правильному формату загружаемых документов и фотографий (например, требования к фото на паспорт).

### 9. Часто задаваемые вопросы (FAQ)
1. **Как узнать статус заявления?**
   - Перейти в раздел «Мои заявления» в личном кабинете. Статус будет отображаться рядом с названием услуги.
2. **Можно ли изменить личные данные?**
   - Да, данные (ФИО, адрес прописки и т.д.) можно обновить, но для этого может потребоваться повторное подтверждение личности или внесение изменений в документы.
3. **Что делать, если не приходит SMS с кодом подтверждения?**
   - Убедитесь, что номер телефона указан верно. Перезагрузите телефон или проверьте, не установлен ли блок на получение SMS от коротких номеров. При повторных сбоях свяжитесь с техподдержкой.
4. **Как получить скидку 30% при оплате госпошлины?**
   - Оформить соответствующую услугу полностью через портал «Госуслуги» и произвести оплату онлайн. Скидка автоматически учтётся в сумме платежа.
"""

initial_query = """Отвечай в формате JSON следующего вида:
{
    "commands": []
    "response": ""
}
Строго соблюдай эту структуру, не пиши вне фигурных скобок, не делай комментариев.
Результирующий ответ должен проходить парсер JSON без ошибок.
Вот список команд (Commands), которые можно предложить клиенту в чат-боте:\n\n    
    /start - Начать работу с ботом «Госуслуги»,
    /register - Узнать, как зарегистрироваться на портале,
    /login - Получить помощь при входе в личный кабинет,
    /services - Список популярных госуслуг,
    /status - Узнать статус поданных заявлений,
    /discount - Информация о скидках и льготах при оплате пошлин,
    /support - Связаться со службой поддержки,
    /faq - Часто задаваемые вопросы (FAQ),
    /security - Советы по безопасности и защите персональных данных,
    /logout - Выйти из учётной записи

В commands команды записывыай строго в формате "/command_name"

Ты бот, с который может общаться с клиентом и в случае просьбы пользователя выполнить перечисленные выше команды. Для этого ты возвращаешь их списком в формате JSON, а ответ отдельно. 
Ни в коем случае не говори пользователю названия самих команд. Если ты хочешь предложить команду, 
запиши её в commands. Не предлагай пользователю сразу все команды. Единовременно предлагай максимум
4 команды. Предлагай только те команды, о которых непосредственно просит пользователь или они могут
помочь пользователю.

Ты можешь неформально общаться с клиентом, немного выходя за рамки своей базы знаний. Но всегда старайся
сохранять диалог в рамках своей области знаний. И будь вежлив. Будь загадочен.

А также не пиши никогда ничего вне полей response и commands.
СТРОГО ЭТО ЗАПОМНИ.
"""

commands_dict = {
    "/start": "Начать работу с ботом «Госуслуги»",
    "/register": "Узнать, как зарегистрироваться на портале",
    "/login": "Получить помощь при входе в личный кабинет",
    "/services": "Список популярных госуслуг",
    "/status": "Узнать статус поданных заявлений",
    "/discount": "Информация о скидках и льготах при оплате пошлин",
    "/support": "Связаться со службой поддержки",
    "/faq": "Часто задаваемые вопросы (FAQ)",
    "/security": "Советы по безопасности и защите персональных данных",
    "/logout": "Выйти из учётной записи"
}

def log(message, level="INFO"):
    print(f"[{level}] {message}")

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_contexts[user_id] = []  
    await update.message.reply_text("Добро пожаловать!")

async def handle_text(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    context_history = user_contexts.get(user_id, [])
    
    try:
        gpt_prompt = generate_gpt_prompt(text, context_history)
        gpt_response = generate_gpt_response(gpt_prompt)

        if not gpt_response:
            await update.message.reply_text("GPT не вернул ответа. Попробуйте снова.", parse_mode="Markdown")
            return
        
        print(gpt_response)
        print("\n-----------\n" + re.findall(r'\{.*?\}', gpt_response, flags=re.DOTALL)[0])
        parsed_response = json.loads(re.findall(r'\{.*?\}', gpt_response, flags=re.DOTALL)[0])
       
        response_text = parsed_response.get("response", "")
        commands = parsed_response.get("commands", [])

        context_history.append({"user": text, "bot": response_text})
        user_contexts[user_id] = context_history
        
        if commands:
            buttons = [[InlineKeyboardButton(f"{commands_dict[cmd]}", callback_data=cmd)] for cmd in commands]
            reply_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(response_text, parse_mode="Markdown")

    except json.JSONDecodeError as e:
        log(f"Ошибка парсинга JSON ответа: {e}", level="ERROR")
        await update.message.reply_text("Ошибка формата ответа от GPT. Попробуйте позже.", parse_mode="Markdown")
    except Exception as e:
        log(f"Ошибка обработки текста: {e}", level="ERROR")
        await update.message.reply_text("Произошла ошибка при обработке текста. Попробуйте позже.", parse_mode="Markdown")

async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Вы выбрали услугу: {commands_dict[query.data]}")

def generate_gpt_prompt(user_input, context):
    return {
        "messages": [
            {"role": "system", "content": f"""Это твоя база знаний, бери все ответы оттуда: 
             {knowledge}
             {initial_query}"""},
            *[{"role": "user", "content": msg["user"]} for msg in context],
            {"role": "user", "content": user_input},
        ],
        "model": "llama-3.2-90b-vision-preview",
        "temperature": 0.9,
    }

def generate_gpt_response(prompt):
    try:
        response = client_gpt.chat.completions.create(**prompt)
        return response.choices[0].message.content.strip()
    except Exception as e:
        log(f"Ошибка при запросе к GPT: {e}", level="ERROR")
        return None

async def clear_context(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_contexts[user_id] = []
    await update.message.reply_text("Контекст очищен!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear_context))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_callback))

    log("Бот запущен!")
    app.run_polling()
