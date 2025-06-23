import tkinter as tk


def query():
    # 这里写你要执行的逻辑
    print("按钮被点击，执行 query() 函数！")


# 创建主窗口
root = tk.Tk()
root.title("简单按钮示例")
root.geometry("500x500")  # 窗口大小：宽 300px，高 200px

# 创建一个按钮，command 参数指定点击后调用的函数
btn = tk.Button(root, text="RSA", command=query)
btn.pack(anchor="sw", padx=40, pady=200)

# 进入主事件循环
root.mainloop()
