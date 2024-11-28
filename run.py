import os
from typing import List
from dotenv import load_dotenv
import openai

# Загрузка переменных из .env
load_dotenv()

# Установка API-ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Функция для чтения текста из файла
def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Функция для записи текста в файл
def write_file(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Функция для генерации резюме
def generate_summary(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используем более дешевую модель
            messages=[
                {"role": "user", "content": f"Summarize the following text:\n{text}"}
            ]
        )
        summary = response.choices[0].message.content
        usage = response.usage  # Получаем статистику по токенам
        print(f"Token usage: {usage}")
        return summary
    except openai.error.OpenAIError as e:
        return f"Error interacting with OpenAI API: {e}"

# Основной код
if __name__ == "__main__":
    try:
        # Создаем список файлов с частями транскрипта
        transcript_files = [f"transcript_{i}.txt" for i in range(1, 7)]

        # Генерация резюме для каждой части
        summaries = []
        for i, file_name in enumerate(transcript_files, start=1):
            print(f"Processing {file_name}...")
            chunk_text = read_file(file_name)
            summary = generate_summary(chunk_text)
            summaries.append(summary)
            write_file(f"summary_{i}.txt", summary)  # Сохраняем резюме в файл

        # Объединяем все резюме
        final_summary = "\n\n".join(summaries)

        # Сохраняем финальное резюме
        write_file("final_summary.txt", final_summary)

        # Вывод финального резюме
        print("Final Summary:")
        print(final_summary)

    except Exception as e:
        print(f"An error occurred: {e}")



