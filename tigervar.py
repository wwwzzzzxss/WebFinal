import tkinter as tk
import random
import time

# 定义老虎机的水果图标
fruits = ["🍒", "🍋", "🍊", "🍇", "🍎"]

# 初始化Tkinter窗口
window = tk.Tk()
window.title("老虎机游戏")

# 创建画布用于显示老虎机轮盘
canvas = tk.Canvas(window, width=200, height=100)
canvas.pack()

# 创建一个标签用于显示结果
result_label = tk.Label(window, text="", font=("Helvetica", 20))
result_label.pack()

# 旋转老虎机轮盘
def spin_wheel():
    result = [random.choice(fruits) for _ in range(3)]
    return result

# 处理按钮点击事件
def play():
    spin_button.config(state=tk.DISABLED)
    for _ in range(10):  # 旋转10次以模拟动画效果
        result = spin_wheel()
        result_label.config(text=" ".join(result))
        window.update()
        time.sleep(0.2)
    spin_button.config(state=tk.NORMAL)
    payout = calculate_payout(result)
    result_label.config(text=f"奖金: ${payout * bet.get()}")

# 计算奖金
def calculate_payout(result):
    if len(set(result)) == 1:
        return 10
    elif len(set(result)) == 2:
        return 3
    else:
        return 0

# 创建一个变量来存储下注金额
bet = tk.IntVar()
bet.set(1)

# 创建下注输入框
bet_entry = tk.Entry(window, textvariable=bet)
bet_entry.pack()

# 创建旋转按钮
spin_button = tk.Button(window, text="旋转", command=play)
spin_button.pack()

# 运行Tkinter应用程序
window.mainloop()
