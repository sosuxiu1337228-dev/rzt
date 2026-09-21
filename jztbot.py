import telebot
import re

# Твой токен уже здесь, кавычки на месте
BOT_TOKEN = "8755448925:AAHGkuOO26LEKd6DPu4KUId7W23J0MYHbM0"

bot = telebot.TeleBot(BOT_TOKEN)

def calculate_score(nums):
    """
    x1, x2, x3, x4 - первые четыре критерия
    x5 - Атмосфера / Вайб
    Формула: round((x1+x2+x3+x4) * (42+3*x5) / 32)
    """
    x1, x2, x3, x4, x5 = nums
    result = (x1 + x2 + x3 + x4) * (42 + 3 * x5) / 32
    return round(result)

@bot.message_handler(commands=['start', 'calc'])
def start(message):
    text = (
        "👋 Привет! Я считаю итоговый балл по системе RISA.\n\n"
        "Отправь мне 5 оценок (от 1 до 10) одним сообщением для критериев:\n"
        "1. Рифмы / Образы\n"
        "2. Структура / Ритмика\n"
        "3. Реализация стиля\n"
        "4. Индивидуальность / Харизма\n"
        "5. Атмосфера / Вайб\n\n"
        "💡 *Пример ввода (в строчку или столбик):*\n"
        "`8 7 9 10 5`"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_input(message):
    # Ищем все числа в сообщении (разделитель пробел, запятая или перенос строки)
    # Заменяем запятые на точки для дробных чисел, если они будут
    finds = re.findall(r"[-+]?\d*\.\d+|\d+", message.text.replace(",", "."))
    
    try:
        # Превращаем найденное в список чисел
        nums = [float(x) for x in finds]
        
        # Проверяем, что чисел ровно 5
        if len(nums) != 5:
            bot.reply_to(message, f"❌ Нужно 5 чисел (по числу критериев), а я нашёл {len(nums)}.\nОтправь оценки ещё раз.")
            return

        # Проверяем, чтобы все были в диапазоне от 1 до 10
        for n in nums:
            if not (1 <= n <= 10):
                bot.reply_to(message, f"❌ Оценка `{n}` не подходит. Все числа должны быть от 1 до 10.")
                return

        # Считаем результат
        score = calculate_score(nums)
        
        res_text = (
            f"✅ *Расчёт выполнен!*\n\n"
            f"Рифмы / Образы: `{nums[0]}`\n"
            f"Структура / Ритмика: `{nums[1]}`\n"
            f"Реализация стиля: `{nums[2]}`\n"
            f"Индивидуальность / Харизма: `{nums[3]}`\n"
            f"Атмосфера / Вайб: `{nums[4]}`\n\n"
            f"🎯 *Итоговый балл: {score}*"
        )
        bot.send_message(message.chat.id, res_text, parse_mode="Markdown")
        
    except Exception:
        bot.reply_to(message, "❌ Ошибка! Пришли, пожалуйста, только цифры (5 оценок).")

# Запуск
print("🤖 Бот запущен и ждет список оценок!")
bot.polling()
