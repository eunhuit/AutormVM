import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading
import pygetwindow as gw

def run_macro(repeat_count, delay=0.001):
    for i in range(repeat_count):
        # Alt 키를 누른 상태에서 m 두 번, d 한 번 입력 후 Alt 해제
        pyautogui.keyDown('alt')
        time.sleep(0.0001)
        pyautogui.press('m')
        time.sleep(0.0001)
        pyautogui.press('m')
        time.sleep(0.0001)
        pyautogui.press('d')
        time.sleep(0.0001)
        pyautogui.keyUp('alt')
        time.sleep(0.0001)
        # Enter 키 입력
        pyautogui.press('enter')
        time.sleep(delay)

def finish_macro():
    # 프로그램 창을 맨 위로 올림
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    messagebox.showinfo("성공", "성공적으로 VM 삭제가 완료되었습니다!")

def start_macro():
    try:
        repeat_count = int(entry.get())
    except ValueError:
        messagebox.showerror("오류", "숫자를 입력해주세요.")
        return

    # 실행 전 샘플 VM이 없는지 확인 메시지
    result = messagebox.askokcancel("확인", "샘플 VM이 없는지 확인하세요.")
    if not result:
        return

    # VMware 프로그램 창 찾기 (창 제목에 "VMware" 포함)
    windows = gw.getWindowsWithTitle("VMware")
    if not windows:
        messagebox.showerror("오류", "VMware 프로그램을 찾을 수 없습니다.")
        return

    vmware_window = windows[0]
    try:
        vmware_window.activate()
    except Exception as e:
        messagebox.showerror("오류", f"VMware 창을 활성화하는데 실패했습니다:\n{e}")
        return

    # 별도 스레드에서 매크로 실행 (GUI 멈춤 방지)
    def macro_thread():
        run_macro(repeat_count)
        root.after(0, finish_macro)
    
    threading.Thread(target=macro_thread).start()

# GUI 구성
root = tk.Tk()
root.title("VM 삭제 매크로")
root.geometry("300x150")

label = tk.Label(root, text="VM의 갯수")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="실행", command=start_macro)
button.pack(pady=20)

root.mainloop()
