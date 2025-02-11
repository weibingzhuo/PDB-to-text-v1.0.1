import re
import tkinter as tk
from tkinter import N, S, E, W
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import Style, Frame, LabelFrame


class PDBConverterApp:
    def __init__(self, root: object):
        self.root = root
        self.root.title("PDB-to-text v1.0.1")
        self.root.geometry("660x480")
        self.root.resizable(width=True, height=True)

        # 设置样式
        self.style = Style()
        self.style.theme_use("clam")  # 使用clam主题
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("Status.TLabel", font=("Arial", 10), foreground="gray")

        # 创建主框架
        self.main_frame = Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

        # 文件选择部分
        self.pdb_file_path = tk.StringVar()
        self.file_frame = LabelFrame(self.main_frame, text="Select PDB file", style="TFrame")
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(N, S, E, W))

        self.file_label = ttk.Label(self.file_frame, text="PDB File path:", style="TLabel")
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.pdb_file_path, width=50, style="TEntry")
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.browse_button = ttk.Button(self.file_frame, text="Select file", command=self.select_pdb_file, style="TButton")
        self.browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        # 转换按钮
        self.convert_button = ttk.Button(self.main_frame, text="Convert to text ", command=self.convert_pdb_to_text, style="TButton")
        self.convert_button.grid(row=1, column=0, padx=10, pady=10, sticky=(N, S, E, W))

        # 状态栏
        self.status_frame = Frame(self.main_frame, style="TFrame")
        self.status_frame.grid(row=2, column=0, padx=10, pady=10, sticky=(N, S, E, W))

        self.status_label = ttk.Label(self.status_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack()

    def select_pdb_file(self):
        """打开文件对话框，选择一个PDB文件"""
        file_path = filedialog.askopenfilename(
            title="Select PDB file",
            filetypes=(("PDB file", "*.pdb"), ("All files", "*.*"))
        )
        if file_path:
            self.pdb_file_path.set(file_path)
            self.status_label.config(text=f"Selected files：{file_path}")

    def convert_pdb_to_text(self):
        """将PDB文件解析为文本文件"""
        pdb_path = self.pdb_file_path.get()
        if not pdb_path:
            messagebox.showwarning("Warning", "Please select a PDB file.！")
            return

        # 解析PDB文件
        try:
            with open(pdb_path, 'r') as file:
                pdb_content = file.readlines()

            # 提取原子信息
            atoms = []
            atom_pattern = re.compile(r'^ATOM\s+(\d+)\s+([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s+(-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)')
            for line in pdb_content:
                if line.startswith('ATOM'):
                    match = atom_pattern.match(line)
                    if match:
                        atoms.append(match.groups())

            # 写入文本文件
            save_path = filedialog.asksaveasfilename(
                title="Save the text file",
                defaultextension=".txt",
                filetypes=(("text file", "*.txt"), ("所有文件", "*.*"))
            )
            if save_path:
                with open(save_path, 'w') as text_file:
                    text_file.write("Atom ID\tAtom Name\tResidue Name\tChain ID\tResidue ID\tX\tY\tZ\n")
                    for atom in atoms:
                        text_file.write("\t".join(atom) + "\n")
                messagebox.showinfo("Complete", f"The PDB file has been successfully converted into a text file：{save_path}")
                self.status_label.config(text=f"Conversion completed：{save_path}")
            else:
                self.status_label.config(text="Unsaved file")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while parsing the PDB file：{str(e)}")
            self.status_label.config(text="An error occurred")

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = PDBConverterApp(root)
    root.mainloop()