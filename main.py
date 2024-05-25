import os
import tkinter as tk
from tkinter import ttk, messagebox

# Список ролей и их названия
roles = {
    "JobMagistrat": "магистрат",
    "JobSeniorResearcher": 'ведущий учёный',
    "JobBorg": "киборг",
    "JobCentralCommandPCK": "Представитель Центком",
    "JobCentralCommandHOCK": "Начальник Штаба Центкома",
    "JobCentralCommandIntern": "Ассистент Центкома",
    "JobCentralCommandOperator": "Оператор Центкома",
    "JobCentralCommandSecurity": "Офицер Специальной Службы Безопасности (ОССБ)",
    "JobSeniorEngineer": "ведущий инженер",
    "JobSeniorPhysician": "ведущий врач",
    "JobSeniorOfficer": "инструктор СБ",
    "JobAtmosphericTechnician": "атмосферный техник",
    "JobBartender": "бармен",
    "JobBotanist": "ботаник",
    "JobCaptain": "капитан",
    "JobCargoTechnician": "грузчик",
    "JobChaplain": "священник",
    "JobChef": "шеф-повар",
    "JobChemist": "химик",
    "JobChiefEngineer": "старший инженер",
    "JobChiefMedicalOfficer": "главный врач",
    "JobClown": "клоун",
    "JobDetective": "детектив",
    "JobERTEngineer": "инженер ОБР",
    "JobBrigmedic": "бригмедик",
    "JobERTJanitor": "уборщик ОБР",
    "JobERTLeader": "лидер ОБР",
    "JobERTMedical": "медик ОБР",
    "JobERTSecurity": "офицер безопасности ОБР",
    "JobHeadOfPersonnel": "глава персонала",
    "JobHeadOfSecurity": "глава службы безопасности",
    "JobJanitor": "уборщик",
    "JobLawyer": "юрист",
    "JobLibrarian": "библиотекарь",
    "JobMedicalDoctor": "врач",
    "JobMedicalIntern": "интерн",
    "JobMime": "мим",
    "JobMusician": "музыкант",
    "JobPassenger": "пассажир",
    "JobParamedic": "парамедик",
    "JobPsychologist": "психолог",
    "JobQuartermaster": "квартирмейстер",
    "JobReporter": "репортёр",
    "JobBlueshield": "офицер Синий Щит",
    "JobResearchDirector": "научный руководитель",
    "JobResearchAssistant": "научный ассистент",
    "JobSalvageSpecialist": "утилизатор",
    "JobScientist": "учёный",
    "JobSecurityCadet": "кадет СБ",
    "JobSecurityOfficer": "офицер СБ",
    "JobServiceWorker": "сервисный работник",
    "JobStationEngineer": "инженер",
    "JobTechnicalAssistant": "технический ассистент",
    "JobWarden": "смотритель",
    "JobBoxer": "боксёр",
    "JobZookeeper": "зоотехник",
    "JobInvestigator": "следователь",
    "JobNanotrasenRepresentive": "представитель NanoTrasen",
    "JobIAA": "Агент внутренних дел"
}


# Функция для конвертации времени в минуты
def convert_time_to_minutes(hours, minutes):
    return int(hours) * 60 + int(minutes)


# Функция для сохранения данных в файл
def save_data():
    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showwarning("Предупреждение", "Введите ник.")
        return

    with open(f"roles_times_{nickname}.txt", "w", encoding="utf-8") as file:
        for role_key, role_name in roles.items():
            hours = role_entries[role_key]['hours'].get()
            minutes = role_entries[role_key]['minutes'].get()

            # Проверка, что поля не пустые и содержат числовые значения
            if hours.isdigit() and minutes.isdigit():
                total_minutes = convert_time_to_minutes(hours, minutes)
                file.write(f"playtime_addrole {nickname} {role_key} {total_minutes}\n")

    messagebox.showinfo("Успех", "Данные успешно сохранены в файл.")


def open_file():
    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showerror("Ошибка", f"Укажите ник.")
        return
    try:
        os.startfile(f"roles_times_{nickname}.txt")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")


# Создание главного окна
root = tk.Tk()
root.title("Учет времени ролей")

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
for role_key, role_name in roles.items():
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

# Кнопка для открытия файла
btn_open = tk.Button(root, text="Открыть файл с командами", command=open_file)
btn_open.pack(pady=10)

root.mainloop()
