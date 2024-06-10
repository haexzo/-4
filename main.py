import tkinter as tk
from datetime import datetime

# 텍스트 파일 경로
text_file_path = 'student_data.txt'

# 학생 시간 저장용 사전
start_times = {}
stop_times = {}
study_duration = {}

# 함수: 바코드로 학생 정보 찾기
def find_student(barcode):
    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(',')
            if data[0] == barcode:
                return data[1], data[2] if len(data) > 2 else "0시간 0분 0초"
    return None, None

# 함수: 시간 문자열을 초로 변환
def time_to_seconds(time_str):
    parts = time_str.split()
    hours = float(parts[0].replace('시간', ''))
    minutes = float(parts[1].replace('분', ''))
    seconds = float(parts[2].replace('초', ''))
    return int(hours * 3600 + minutes * 60 + seconds)

# 함수: 초를 시간 문자열로 변환
def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours)}시간 {int(minutes)}분 {int(seconds)}초"

# 함수: 학생 정보 업데이트
def update_student_time(barcode, additional_time):
    updated_lines = []
    found = False
    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(',')
            if data[0] == barcode:
                existing_time_seconds = time_to_seconds(data[2]) if len(data) > 2 else 0
                total_seconds = existing_time_seconds + additional_time
                data[2] = seconds_to_time(total_seconds)
                found = True
            updated_lines.append(','.join(data))
    if not found:
        print(f"Barcode {barcode} not found in the file.")
    else:
        with open(text_file_path, 'w', encoding='utf-8') as file:
            for line in updated_lines:
                file.write(line + '\n')

# 함수: 학생 이름 및 버튼 표시
def show_student_info():
    global current_barcode, current_student_name, current_total_time
    barcode = barcode_entry.get()
    student_name, total_time = find_student(barcode)
    if student_name:
        current_barcode = barcode
        current_student_name = student_name
        current_total_time = total_time
        student_name_label.config(text=f"학생 이름: {student_name}")
        if barcode in start_times:
            start_time_label.config(text=f"시작 시간: {start_times[barcode].strftime('%H:%M:%S')}")
            start_button.pack_forget()
            stop_button.pack(pady=5)  # 종료 버튼 표시
        else:
            start_time_label.config(text="아직 시작 시간이 측정되지 않았습니다.")
            start_button.pack(pady=5)  # 시작 버튼 표시
            stop_button.pack_forget()

        if barcode in stop_times:
            stop_time_label.config(text=f"종료 시간: {stop_times[barcode].strftime('%H:%M:%S')}")
            if barcode in study_duration:
                today_total_study_time_label.config(text=f"이번 공부 시간: {study_duration[barcode]}")
            else:
                today_total_study_time_label.config(text=f"이번 공부 시간은 아직 측정되지 않았습니다.")
        else:
            stop_time_label.config(text="아직 종료 시간이 측정되지 않았습니다.")
        
        total_study_time_label.config(text=f"저장된 총 공부 시간: {total_time}")
    else:
        student_name_label.config(text="바코드를 찾을 수 없습니다.")
        start_button.pack_forget()
        stop_button.pack_forget()

# 함수: 시작 시간 표시
def show_start_time():
    barcode = barcode_entry.get()
    start_times[barcode] = datetime.now()
    start_time_label.config(text=f"시작 시간: {start_times[barcode].strftime('%H:%M:%S')}")
    start_button.pack_forget()
    stop_button.pack(pady=5)  # 종료 버튼 표시

# 함수: 종료 시간 표시 및 총 공부 시간 계산
def show_stop_time():
    barcode = barcode_entry.get()
    stop_times[barcode] = datetime.now()
    if barcode in start_times:
        stop_time_label.config(text=f"종료 시간: {stop_times[barcode].strftime('%H:%M:%S')}")
        study_duration[barcode] = stop_times[barcode] - start_times[barcode]
        duration_seconds = study_duration[barcode].total_seconds()
        today_total_study_time_label.config(text=f"이번 공부 시간: {seconds_to_time(duration_seconds)}")
        # 바코드와 총 공부 시간을 텍스트 파일에 기록
        update_student_time(barcode, duration_seconds)
        start_button.pack(pady=5)
        stop_button.pack_forget()
        show_student_info()
    else:
        stop_time_label.config(text="시작 시간을 먼저 입력하세요.")
        stop_button.pack_forget()

# 시간 초기화 확인 창
def reset_time_conform():
    conform_window = tk.Toplevel(root)
    conform_window.title("확인 창")
    conform_window.geometry('300x300')

    conform_label = tk.Label(conform_window, text="정말 초기화 하시겠습니까?", font=("Arial", 16))
    conform_label.pack(pady=10)
    conform_button = tk.Button(conform_window, text="확인", command=lambda: [reset_all_time(), quit(conform_window)])
    conform_button.pack(pady=10)

# 창 닫기
def quit(conform_window):
    conform_window.destroy()
    

# 모든 학생 시간 초기화 함수
def reset_all_time():
    updated_lines = []
    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(',')
            data[2] = "0시간 0분 0초"
            updated_lines.append(','.join(data))
    with open(text_file_path, 'w', encoding='utf-8') as file:
        for line in updated_lines:
            file.write(line + '\n')
    # 모든 레이블 초기화
    start_times.clear()
    stop_times.clear()
    study_duration.clear()
    student_name_label.config(text="")
    start_time_label.config(text="")
    stop_time_label.config(text="")
    today_total_study_time_label.config(text="")
    total_study_time_label.config(text="")
    barcode_entry.delete(0, tk.END)

# 순위 표시 함수
def show_ranking():
    students = []
    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(',')
            if len(data) > 2:
                total_time_seconds = time_to_seconds(data[2])
                students.append((data[1], total_time_seconds))

    # 총 공부 시간에 따라 정렬
    students.sort(key=lambda x: x[1], reverse=True)
    
    # 새로운 창에 순위 표시
    ranking_window = tk.Toplevel(root)
    ranking_window.title("학생 순위")
    ranking_window.geometry('300x300')

    rank_label = tk.Label(ranking_window, text="학생 순위", font=("Arial", 16))
    rank_label.pack(pady=10)

    for idx, (name, total_seconds) in enumerate(students):
        rank_text = f"{idx + 1}위: {name} - {seconds_to_time(total_seconds)}"
        student_rank_label = tk.Label(ranking_window, text=rank_text)
        student_rank_label.pack()

# 바코드 입력 시 자동 확인 함수
def on_barcode_entry_change(*args):
    barcode = barcode_var.get()
    if len(barcode) == 6:
        show_student_info()

# GUI 생성
root = tk.Tk()
root.title("시간측정 프로그램")
root.geometry('400x400')

# 바코드 입력 필드
barcode_label = tk.Label(root, text="바코드를 입력하세요:")
barcode_label.pack(pady=5)

barcode_var = tk.StringVar()
barcode_var.trace('w', on_barcode_entry_change)
barcode_entry = tk.Entry(root, width=40, textvariable=barcode_var)
barcode_entry.pack(pady=5)

# 학생 이름 표시 레이블
student_name_label = tk.Label(root, text="")
student_name_label.pack(pady=5)

# 시작 버튼 (처음에는 표시되지 않음)
start_button = tk.Button(root, text="시간 측정 시작", command=show_start_time)

# 종료 버튼 (처음에는 표시되지 않음)
stop_button = tk.Button(root, text="시간 측정 종료", command=show_stop_time)

# 입력 버튼
search_button = tk.Button(root, text="학생 정보 확인", command=show_student_info)
search_button.pack(pady=5)

# 시작 시간 표시 레이블
start_time_label = tk.Label(root, text="")
start_time_label.pack(pady=5)

# 종료 시간 표시 레이블
stop_time_label = tk.Label(root, text="")
stop_time_label.pack(pady=5)

# 이번 공부 시간 표시 레이블
today_total_study_time_label = tk.Label(root, text="")
today_total_study_time_label.pack(pady=5)

# 총 공부 시간 표시 레이블
total_study_time_label = tk.Label(root, text="")
total_study_time_label.pack(pady=5)

# 순위 보기 버튼
ranking_button = tk.Button(root, text="순위 보기", command=show_ranking)
ranking_button.pack(pady=5)

# 모든 학생 시간 초기화 버튼
reset_all_time_button = tk.Button(root, text="모든 학생 시간 초기화", command=reset_time_conform)
reset_all_time_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

# GUI 실행
root.mainloop()
