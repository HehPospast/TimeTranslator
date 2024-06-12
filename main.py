import os
import tkinter as tk
from tkinter import messagebox
import requests
import subprocess

# Constants
REPO_OWNER = "HehPospast"
REPO_NAME = "TimeTranslator"
BRANCH_NAME = "main"
FILE_PATH = "main.py"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={FILE_PATH}"


def fetch_latest_commit():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        commits = response.json()
        if commits:
            return commits[0]['sha']
        return None
    except requests.RequestException as e:
        print(f"Error fetching commits: {e}")
        return None


def check_for_updates():
    latest_commit = fetch_latest_commit()
    if not latest_commit:
        return False

    if not os.path.exists(".commit"):
        return True

    with open(".commit", "r") as file:
        local_commit = file.read().strip()

    return local_commit != latest_commit

# def delete_commit_file():
#     try:
#         if os.path.exists(".commit"):
#             os.remove(".commit")
#             print(".commit file deleted")
#     except Exception as e:
#         print(f"Error deleting .commit file: {e}")

def update_script():
    try:
        response = requests.get(f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH_NAME}/{FILE_PATH}")
        response.raise_for_status()

        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(response.text)

        latest_commit = fetch_latest_commit()
        if latest_commit:
            with open(".commit", "w", encoding="utf-8") as file:
                file.write(latest_commit)

        # delete_commit_file()
        messagebox.showinfo("Успех", "Скрипт обновлён. Пожалуйста, перезапустите программу.")
        root.quit()
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось обновить скрипт: {e}")

def prompt_update():
    if check_for_updates():
        if messagebox.askyesno("Обновление доступно", "Доступно новое обновление. Обновить сейчас?"):
            update_script()

# Список ролей и их названия, сгруппированные по отделам
departments = {
    "Командование": {
        "JobHeadOfPersonnel": "Глава Персонала",
        "JobCaptain": "Капитан",
        "JobNanotrasenRepresentive": "Представитель NanoTrasen",
        "JobHeadOfSecurity": "Глава Службы Безопасности",
        "JobChiefMedicalOfficer": "Главный врач",
        "JobQuartermaster": "Квартирмейстер",
        "JobResearchDirector": "Научный Руководитель",
        "JobChiefEngineer": "Старший Инженер",
        "JobMagistrat": "Магистрат",
        "JobBlueshield": "Офицер 'Синий Щит'"
    },
    "Служба безопасности": {
        "JobHeadOfSecurity": "Глава Службы Безопасности",
        "JobBrigmedic": "Бригмедик",
        "JobDetective": "Детектив",
        "JobSeniorOfficer": "Инструктор СБ",
        "JobSecurityCadet": "Кадет СБ",
        "JobSecurityOfficer": "Офицер СБ",
        "JobInvestigator": "Следователь",
        "JobWarden": "Смотритель"
    },
    "Инженерный отдел": {
        "JobChiefEngineer": "Старший Инженер",
        "JobAtmosphericTechnician": "Атмосферный техник",
        "JobSeniorEngineer": "Ведущий инженер",
        "JobStationEngineer": "Инженер",
        "JobTechnicalAssistant": "Технический Ассистент"
    },
    "Медицинский отдел": {
        "JobChiefMedicalOfficer": "Главный врач",
        "JobSeniorPhysician": "Ведущий врач",
        "JobMedicalDoctor": "Врач",
        "JobMedicalIntern": "Интерн",
        "JobParamedic": "Парамедик",
        "JobBrigmedic": "Патологоанатом",
        "JobPsychologist": "Психолог",
        "JobChemist": "Химик"
    },
    "Отдел снабжения": {
        "JobQuartermaster": "Квартирмейстер",
        "JobCargoTechnician": "Грузчик",
        "JobSalvageSpecialist": "Утилизатор"
    },
    "Научный отдел": {
        "JobResearchDirector": "Научный Руководитель",
        "JobSeniorResearcher": "Ведущий учёный",
        "JobScientist": "Учёный",
        "JobResearchAssistant": "Научный ассистент"
    },
    "Юридический отдел":{
        "JobIAA": "Агент внутренних дел",
        "JobLawyer": "Юрист",
    },
    "Сервисный отдел": {
        "JobBartender": "Бармен",
        "JobBotanist": "Ботаник",
        "JobChef": "Шеф-повар",
        "JobClown": "Клоун",
        "JobChaplain": "Священник",
        "JobJanitor": "Уборщик",
        "JobLibrarian": "Библиотекарь",
        "JobMime": "Мим",
        "JobMusician": "Музыкант",
        "JobPassenger": "Пассажир",
        "JobReporter": "Репортёр",
        "JobBoxer": "Боксёр",
        "JobZookeeper": "Зоотехник",
        "JobServiceWorker": "Сервисный работник"
    },
    "ОБР": {
        "JobERTEngineer": "Инженер ОБР",
        "JobERTJanitor": "Уборщик ОБР",
        "JobERTLeader": "Лидер ОБР",
        "JobERTMedical": "Медик ОБР",
        "JobERTSecurity": "Офицер безопасности ОБР"
    },
    "Центральное Командование": {
        "JobCentralCommandPCK": "Представитель Центком",
        "JobCentralCommandHOCK": "Начальник Штаба Центкома",
        "JobCentralCommandIntern": "Ассистент Центкома",
        "JobCentralCommandOperator": "Оператор Центкома",
        "JobCentralCommandSecurity": "Офицер Специальной Службы Безопасности (ОССБ)"
    },
}


# Функция для конвертации времени в минуты
def convert_time_to_minutes(hours, minutes):
    return int(hours) * 60 + int(minutes)


# Функция для конвертации минут в часы и минуты
def convert_minutes_to_time(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return hours, minutes


# Функция для сохранения данных в файл
def save_data():
    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showwarning("Предупреждение", "Введите ник.")
        return

    unique_entries = {}

    for dept_key, dept_roles in departments.items():
        for role_key, role_name in dept_roles.items():
            hours = role_entries[role_key]['hours'].get()
            minutes = role_entries[role_key]['minutes'].get()

            # Проверка, что поля не пустые и содержат числовые значения
            if hours.isdigit() and minutes.isdigit():
                total_minutes = convert_time_to_minutes(hours, minutes)
                if role_key not in unique_entries:
                    unique_entries[role_key] = total_minutes

    with open(f"roles_times_{nickname}.txt", "w", encoding="utf-8") as file:
        for role_key, total_minutes in unique_entries.items():
            file.write(f"playtime_addrole {nickname} {role_key} {total_minutes}\n")

    messagebox.showinfo("Успех", "Данные успешно сохранены в файл.")


def open_file():
    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showerror("Ошибка", "Укажите ник.")
        return
    try:
        os.startfile(f"roles_times_{nickname}.txt")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

# Функция для загрузки данных из файла
def load_data():
    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showwarning("Предупреждение", "Введите ник.")
        return

    # Очищение всех полей перед загрузкой данных
    for entries in role_entries.values():
        entries['hours'].delete(0, tk.END)
        entries['minutes'].delete(0, tk.END)

    try:
        with open(f"roles_times_{nickname}.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 4 and parts[0] == "playtime_addrole":
                    role_key = parts[2]
                    total_minutes = int(parts[3])
                    hours, minutes = convert_minutes_to_time(total_minutes)

                    if role_key in role_entries:
                        role_entries[role_key]['hours'].delete(0, tk.END)
                        role_entries[role_key]['hours'].insert(0, str(hours))
                        role_entries[role_key]['minutes'].delete(0, tk.END)
                        role_entries[role_key]['minutes'].insert(0, str(minutes))

        messagebox.showinfo("Успех", "Данные успешно загружены из файла.")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл roles_times_{nickname}.txt не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")


# Создание главного окна
root = tk.Tk()
root.title("Учет времени ролей")


# Автоапдейт
# fixme OFF FOR DEBUG
prompt_update()


# Поле для ввода ника
frame_nickname = tk.Frame(root)
frame_nickname.pack(pady=10)
tk.Label(frame_nickname, text="Ник:").pack(side=tk.LEFT)
entry_nickname = tk.Entry(frame_nickname)
entry_nickname.pack(side=tk.LEFT)

# Создание canvas и scrollbar для прокрутки
canvas = tk.Canvas(root, borderwidth=0)
frame_roles = tk.Frame(canvas)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4, 4), window=frame_roles, anchor="nw")

frame_roles.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))


# Функция для обновления области прокрутки
def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


role_entries = {}

# Создание полей ввода для каждой роли
for dept_key, dept_roles in departments.items():
    # Добавление заголовка отдела
    tk.Label(frame_roles, text=dept_key, font=("Helvetica", 14, "bold")).pack(fill=tk.X, pady=5)

    for role_key, role_name in dept_roles.items():
        frame_role = tk.Frame(frame_roles)
        frame_role.pack(fill=tk.X, pady=2)

        tk.Label(frame_role, text=role_name, width=30, anchor=tk.W).pack(side=tk.LEFT)
        entry_hours = tk.Entry(frame_role, width=5)
        entry_hours.pack(side=tk.LEFT)
        tk.Label(frame_role, text="ч").pack(side=tk.LEFT)
        entry_minutes = tk.Entry(frame_role, width=5)
        entry_minutes.pack(side=tk.LEFT)
        tk.Label(frame_role, text="мин").pack(side=tk.LEFT)

        role_entries[role_key] = {'hours': entry_hours, 'minutes': entry_minutes}

# Кнопка для сохранения данных
btn_save = tk.Button(root, text="Сохранить", command=save_data)
btn_save.pack(pady=10)

# Кнопка для загрузки данных из файла
btn_load = tk.Button(root, text="Загрузить из файла", command=load_data)
btn_load.pack(pady=10)

# Кнопка для открытия файла
btn_open = tk.Button(root, text="Открыть файл с командами", command=open_file)
btn_open.pack(pady=10)

root.mainloop()