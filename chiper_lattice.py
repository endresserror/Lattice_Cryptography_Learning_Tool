import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, colorchooser, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import time
import random
from scipy.spatial import ConvexHull
import io
from PIL import Image, ImageTk
import os

# set the theme and language
DARK_MODE = False
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#333333",
        "accent": "#3498db",
        "secondary": "#e74c3c",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "button_bg": "#3498db",
        "button_fg": "white",
        "header_bg": "#2c3e50",
        "header_fg": "white",
        "plot_bg": "#ffffff",
        "grid": "#cccccc",
        "neon_accent": "#00ffff",
        "neon_secondary": "#ff00ff"
    },
    "dark": {
        "bg": "#1a1a2e",
        "fg": "#e6e6ff",
        "accent": "#4d7cff",
        "secondary": "#ff5555",
        "success": "#50fa7b",
        "warning": "#ffb86c", 
        "button_bg": "#4d7cff",
        "button_fg": "white",
        "header_bg": "#0f0f23",
        "header_fg": "#e6e6ff",
        "plot_bg": "#16213e",
        "grid": "#304b6a",
        "neon_accent": "#00ffff",
        "neon_secondary": "#ff00ff"
    }
}

# laguage settings
LANGUAGES = {
    "en": {
        "app_title": "Advanced Lattice Cryptography Learning System",
        "overview_tab": "Overview",
        "2d_lattice_tab": "2D Lattice",
        "3d_lattice_tab": "3D Lattice",
        "lll_tab": "LLL Algorithm",
        "svp_tab": "SVP",
        "cvp_tab": "CVP",
        "ntru_tab": "NTRU Encryption",
        "attack_tab": "Lattice Attacks",
        "file_menu": "File",
        "save_results": "Save Results",
        "load_settings": "Load Settings",
        "exit": "Exit",
        "settings_menu": "Settings",
        "toggle_theme": "Toggle Theme",
        "language": "Language",
        "help_menu": "Help",
        "documentation": "Documentation",
        "about": "About",
        "dark_mode": "🌙 Dark Mode",
        "light_mode": "☀️ Light Mode",
        "lattice_overview_title": "Lattice-Based Cryptography",
        "input_error": "Input Error",
        "numeric_values_error": "Please enter numeric values for basis vectors.",
        "plot_lattice": "Plot Lattice",
        "run_lll": "Run LLL",
        "solve_svp": "Solve SVP",
        "solve_cvp": "Solve CVP",
        "run_ntru_demo": "Run NTRU Demo",
        "simulate_attack": "Simulate Attack",
        "original_lattice": "Original Lattice",
        "reduced_lattice": "Reduced Lattice",
        "lattice_properties": "Lattice Properties",
        "original_det": "Original Det",
        "reduced_det": "Reduced Det",
        "vector_lengths": "Vector Lengths",
        "orthogonality_defect": "Orthogonality Defect",
        "shortest_vectors": "Shortest Vectors in Lattice",
        "closest_vectors": "Closest Vectors in Lattice",
        "dimension": "Dimension",
        "rotate": "Rotate",
        "reset_view": "Reset View",
        "message": "Message",
        "encryption_step1": "Step 1: Key Generation",
        "encryption_step2": "Step 2: Message Preparation",
        "encryption_step3": "Step 3: Encryption",
        "encryption_step4": "Step 4: Decryption",
        "decryption_success": "✓ Decryption successful!",
        "decryption_fail": "✗ Decryption failed!",
        "lattice_overview_text": "Lattice-based cryptography is one of the post-quantum cryptographic methods that are believed to be secure against quantum computer attacks. It uses mathematical structures called lattices to achieve security different from RSA and elliptic curve cryptography.\n\nA lattice is defined as the set of all integer linear combinations of linearly independent vectors. Once a basis is given, the entire lattice is determined.\n\nLattice Reduction (LLL Algorithm) is a technique for transforming basis vectors to shorter, more orthogonal ones to reveal the structure of the lattice.\n\nHard Problems in Lattice Cryptography include the Shortest Vector Problem (SVP) and the Closest Vector Problem (CVP).\n\nNTRU Encryption is one of the earliest and most practical lattice-based encryption schemes, using polynomial operations in quotient rings for efficient encryption and decryption.",
        "ctf_challenge_tab": "Lattice CTF Challenge",
        "ctf_basis_input": "Enter lattice basis (one vector per line, space separated):",
        "ctf_decode": "Solve Challenge",
        "ctf_result": "Challenge Result:",
        "ctf_error": "Error solving challenge:"
    },
    "ja": {
        "app_title": "高度格子暗号学習システム",
        "overview_tab": "概要",
        "2d_lattice_tab": "2次元格子",
        "3d_lattice_tab": "3次元格子",
        "lll_tab": "LLLアルゴリズム",
        "svp_tab": "最短ベクトル問題",
        "cvp_tab": "最近ベクトル問題",
        "ntru_tab": "NTRU暗号",
        "attack_tab": "格子攻撃",
        "file_menu": "ファイル",
        "save_results": "結果を保存",
        "load_settings": "設定を読み込む",
        "exit": "終了",
        "settings_menu": "設定",
        "toggle_theme": "テーマ切替",
        "language": "言語",
        "help_menu": "ヘルプ",
        "documentation": "ドキュメント",
        "about": "このアプリについて",
        "dark_mode": "🌙 ダークモード",
        "light_mode": "☀️ ライトモード",
        "lattice_overview_title": "格子ベース暗号",
        "input_error": "入力エラー",
        "numeric_values_error": "基底ベクトルには数値を入力してください。",
        "plot_lattice": "格子を描画",
        "run_lll": "LLLを実行",
        "solve_svp": "SVPを解く",
        "solve_cvp": "CVPを解く",
        "run_ntru_demo": "NTRUデモ実行",
        "simulate_attack": "攻撃シミュレーション",
        "original_lattice": "元の格子",
        "reduced_lattice": "縮小された格子",
        "lattice_properties": "格子の特性",
        "original_det": "元の行列式",
        "reduced_det": "縮小後の行列式",
        "vector_lengths": "ベクトル長",
        "orthogonality_defect": "直交欠陥",
        "shortest_vectors": "格子内の最短ベクトル",
        "closest_vectors": "最も近いベクトル",
        "dimension": "次元",
        "rotate": "回転",
        "reset_view": "表示リセット",
        "message": "メッセージ",
        "encryption_step1": "ステップ1: 鍵生成",
        "encryption_step2": "ステップ2: メッセージ準備",
        "encryption_step3": "ステップ3: 暗号化",
        "encryption_step4": "ステップ4: 復号化",
        "decryption_success": "✓ 復号化成功！",
        "decryption_fail": "✗ 復号化失敗！",
        "lattice_overview_text": "格子ベース暗号は、量子コンピュータ攻撃に対しても安全と考えられている耐量子暗号手法の一つです。RSAや楕円曲線暗号とは異なるセキュリティを実現するために、格子と呼ばれる数学的構造を使用しています。\n\n格子は、線形独立なベクトルの整数線形結合の集合として定義されます。基底が与えられると、格子全体が決定されます。\n\n格子縮小（LLLアルゴリズム）は、基底ベクトルをより短く、より直交に変換して格子の構造を明らかにする技術です。\n\n格子暗号における困難な問題には、最短ベクトル問題（SVP）と最近ベクトル問題（CVP）があります。\n\nNTRU暗号は、最も初期の実用的な格子ベース暗号方式の一つで、商環における多項式演算を用いて効率的な暗号化と復号化を実現しています。",
        "ctf_challenge_tab": "格子CTF",
        "ctf_basis_input": "格子基底を入力してください（各行が1つのベクトル、空白区切り）：",
        "ctf_decode": "解く",
        "ctf_result": "結果：",
        "ctf_error": "エラーが発生しました："
    },
    "zh": {
        "app_title": "高级格子密码学学习系统",
        "overview_tab": "概述",
        "2d_lattice_tab": "二维格子",
        "3d_lattice_tab": "三维格子",
        "lll_tab": "LLL算法",
        "svp_tab": "最短向量问题",
        "cvp_tab": "最近向量问题",
        "ntru_tab": "NTRU加密",
        "attack_tab": "格子攻击",
        "file_menu": "文件",
        "save_results": "保存结果",
        "load_settings": "加载设置",
        "exit": "退出",
        "settings_menu": "设置",
        "toggle_theme": "切换主题",
        "language": "语言",
        "help_menu": "帮助",
        "documentation": "文档",
        "about": "关于",
        "dark_mode": "🌙 暗黑模式",
        "light_mode": "☀️ 亮色模式",
        "lattice_overview_title": "基于格子的密码学",
        "input_error": "输入错误",
        "numeric_values_error": "请为基底向量输入数值。",
        "plot_lattice": "绘制格子",
        "run_lll": "运行LLL",
        "solve_svp": "求解SVP",
        "solve_cvp": "求解CVP",
        "run_ntru_demo": "运行NTRU演示",
        "simulate_attack": "模拟攻击",
        "original_lattice": "原始格子",
        "reduced_lattice": "缩减后格子",
        "lattice_properties": "格子属性",
        "original_det": "原始行列式",
        "reduced_det": "缩减后行列式",
        "vector_lengths": "向量长度",
        "orthogonality_defect": "正交缺陷",
        "shortest_vectors": "格子中最短向量",
        "closest_vectors": "最接近的向量",
        "dimension": "维数",
        "rotate": "旋转",
        "reset_view": "重置视图",
        "message": "消息",
        "encryption_step1": "步骤1：密钥生成",
        "encryption_step2": "步骤2：准备消息",
        "encryption_step3": "步骤3：加密",
        "encryption_step4": "步骤4：解密",
        "decryption_success": "✓ 解密成功！",
        "decryption_fail": "✗ 解密失败！",
        "lattice_overview_text": "基于格子的密码学是一种被认为能够抵抗量子计算机攻击的耐量子密码方法。它利用称为‘格子’的数学结构，来实现与RSA及椭圆曲线密码不同的安全性。\n\n格子定义为由一组线性无关向量的所有整数线性组合构成的集合。一旦给定基底，整个格子即确定。\n\nLLL算法是一种将基底向量转换为更短、更正交的向量，揭示格子结构的技术。\n\n在格子密码学中，难题包括最短向量问题（SVP）和最近向量问题（CVP）。\n\nNTRU加密是最早且最实用的基于格子的加密方案之一，它利用商环中多项式运算实现高效的加密与解密。",
        "ctf_challenge_tab": "格子CTF挑战",
        "ctf_basis_input": "请输入格子基底（每行一个向量，以空格分隔）：",
        "ctf_decode": "解题",
        "ctf_result": "挑战结果：",
        "ctf_error": "解题错误："
    }
}

# default settings
current_theme = THEMES["light"] if not DARK_MODE else THEMES["dark"]
current_language = "en"  # default language

# get text from language settings
def get_text(key):
    return LANGUAGES[current_language].get(key, key)

# set the style
def apply_style():
    style = ttk.Style()
    if DARK_MODE:
        style.theme_use('alt')  # dark theme
    else:
        style.theme_use('clam')  # light theme
    
    # tab style
    style.configure('TNotebook', background=current_theme["bg"])
    style.configure('TNotebook.Tab', background=current_theme["bg"], 
                   foreground=current_theme["fg"], padding=[10, 2])
    style.map('TNotebook.Tab', background=[('selected', current_theme["accent"])],
              foreground=[('selected', current_theme["button_fg"])])
    
    # button style
    style.configure('TButton', background=current_theme["button_bg"], 
                   foreground=current_theme["button_fg"], padding=5,
                   font=('Helvetica', 10, 'bold'))
    style.map('TButton', background=[('active', current_theme["accent"])])
    
    # neon button style
    style.configure('Neon.TButton', 
                   background=current_theme["neon_accent"],
                   foreground='black',
                   padding=5,
                   font=('Helvetica', 10, 'bold'))
    style.map('Neon.TButton', 
             background=[('active', current_theme["neon_secondary"])])
    
    # label style
    style.configure('TLabel', background=current_theme["bg"], 
                   foreground=current_theme["fg"], font=('Helvetica', 10))
    
    # frame style
    style.configure('TFrame', background=current_theme["bg"])
    style.configure('Header.TFrame', background=current_theme["header_bg"])
    
    # entry style
    style.configure('TEntry', fieldbackground=current_theme["bg"], 
                   foreground=current_theme["fg"])
    
    # accent label style
    style.configure('Accent.TLabel', foreground=current_theme["accent"],
                   font=('Helvetica', 12, 'bold'))
    style.configure('Warning.TLabel', foreground=current_theme["warning"],
                   font=('Helvetica', 10, 'bold'))
    style.configure('Success.TButton', background=current_theme["success"],
                   foreground=current_theme["button_fg"])
    style.configure('Warning.TButton', background=current_theme["warning"],
                   foreground=current_theme["button_fg"])
    style.configure('Secondary.TButton', background=current_theme["secondary"],
                   foreground=current_theme["button_fg"])

# animated lattice plot
def plot_lattice_animated():
    try:
        # get input values and validate
        b1x = float(vis_b1x_entry.get())
        b1y = float(vis_b1y_entry.get())
        b2x = float(vis_b2x_entry.get())
        b2y = float(vis_b2y_entry.get())
    except ValueError:
        messagebox.showerror(get_text("input_error"), get_text("numeric_values_error"))
        return

    b1 = np.array([b1x, b1y])
    b2 = np.array([b2x, b2y])
    
    # clear the plot frame
    for widget in vis_plot_frame.winfo_children():
        widget.destroy()
    
    # make a new 2D plot (neon style)
    fig = plt.figure(figsize=(5,5), facecolor=current_theme["plot_bg"])
    ax = fig.add_subplot(111)
    ax.set_facecolor(current_theme["plot_bg"])
    ax.grid(True, color=current_theme["grid"], linestyle='--', alpha=0.7)
    ax.set_title("2D Lattice Visualization", color=current_theme["fg"], fontsize=14, fontweight='bold')
    ax.set_xlabel("x", color=current_theme["fg"])
    ax.set_ylabel("y", color=current_theme["fg"])
    ax.tick_params(colors=current_theme["fg"])
    
    # show the origin with neon effect
    ax.scatter([0], [0], color=current_theme["neon_accent"], s=100, zorder=10, edgecolor='white', linewidth=1)
    ax.text(0.1, 0.1, "O", color=current_theme["fg"], fontsize=12, fontweight='bold')
    
    # generate lattice points (small range)
    points = []
    for m in range(-10, 11):
        for n in range(-10, 11):
            point = m * b1 + n * b2
            points.append(point)
    points = np.array(points)
    
    # show basis vectors with neon effect
    arrow_props = dict(
        head_width=0.3, 
        head_length=0.3, 
        length_includes_head=True, 
        zorder=10, 
        animated=True
    )
    glow_size = 5
    
    # basis 1 with neon effect
    for i in range(glow_size):
        alpha = 0.1 - (i * 0.02)
        width = (glow_size - i) * 0.1
        ax.arrow(0, 0, b1[0], b1[1], fc=current_theme["neon_accent"], ec=current_theme["neon_accent"], 
                width=width, alpha=alpha, **arrow_props)
    
    arrow_b1 = ax.arrow(0, 0, b1[0], b1[1], fc=current_theme["accent"], ec=current_theme["accent"], 
                        **arrow_props)
    
    # basis 2 with neon effect
    for i in range(glow_size):
        alpha = 0.1 - (i * 0.02)
        width = (glow_size - i) * 0.1
        ax.arrow(0, 0, b2[0], b2[1], fc=current_theme["neon_secondary"], ec=current_theme["neon_secondary"], 
                width=width, alpha=alpha, **arrow_props)
    
    arrow_b2 = ax.arrow(0, 0, b2[0], b2[1], fc=current_theme["secondary"], ec=current_theme["secondary"], 
                        **arrow_props)
    
    text_b1 = ax.text(b1[0], b1[1], " b₁", color=current_theme["accent"], 
                      fontsize=12, fontweight='bold', animated=True)
    text_b2 = ax.text(b2[0], b2[1], " b₂", color=current_theme["secondary"], 
                      fontsize=12, fontweight='bold', animated=True)
    
    # reset view button
    scatter = ax.scatter([], [], s=15, c=current_theme["neon_accent"], alpha=0.7, animated=True,
                        edgecolor='white', linewidth=0.5)
    
    # parallelogram representing the lattice
    parallelogram = plt.Polygon([
        [0, 0],
        b1,
        b1 + b2,
        b2
    ], closed=True, alpha=0.2, color=current_theme["accent"], animated=True)
    ax.add_patch(parallelogram)
    
    # animation settings
    total_steps = 60
    
    # update function for animation
    def update(frame):
        if frame <= total_steps:
            # lattice points animation (gradual appearance)
            step_size = max(1, len(points) // total_steps)
            idx = min(len(points), frame * step_size)
            subset = points[:idx]
            if len(subset) > 0:
                scatter.set_offsets(subset)
                
            # parallelogram animation (gradual appearance)
            if frame <= total_steps // 3:
                parallelogram.set_alpha(0.2 * frame / (total_steps // 3))
            
            #   basis vectors animation (gradual appearance)
            if frame <= total_steps // 2:
                progress = frame / (total_steps // 2)
                arrow_b1.set_data(x=0, y=0, dx=b1[0] * progress, dy=b1[1] * progress)
                arrow_b2.set_data(x=0, y=0, dx=b2[0] * progress, dy=b2[1] * progress)
                text_b1.set_position((b1[0] * progress, b1[1] * progress))
                text_b2.set_position((b2[0] * progress, b2[1] * progress))
                
        # change the size of the scatter points
        if frame > total_steps:
            cycle_pos = (frame - total_steps) % 20
            size_factor = 1.0 + 0.2 * np.sin(cycle_pos * np.pi / 10)
            scatter.set_sizes([15 * size_factor])
                
        return scatter, arrow_b1, arrow_b2, text_b1, text_b2, parallelogram
    
    # make the animation
    ani = animation.FuncAnimation(fig, update, frames=total_steps+40, 
                                 interval=50, blit=True)
    
    # embed the animation in tkinter canvas
    ax.set_aspect('equal')
    ax.autoscale_view()
    max_val = max(np.max(np.abs(points)), 1)
    ax.set_xlim(-max_val*1.2, max_val*1.2)
    ax.set_ylim(-max_val*1.2, max_val*1.2)
    
    # Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=vis_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Toolbar
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    toolbar = NavigationToolbar2Tk(canvas, vis_plot_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# 3D lattice plot
def plot_3d_lattice():
    try:
        # get input values and validate
        b1x = float(vis3d_b1x_entry.get())
        b1y = float(vis3d_b1y_entry.get())
        b1z = float(vis3d_b1z_entry.get())
        b2x = float(vis3d_b2x_entry.get())
        b2y = float(vis3d_b2y_entry.get())
        b2z = float(vis3d_b2z_entry.get())
        b3x = float(vis3d_b3x_entry.get())
        b3y = float(vis3d_b3y_entry.get())
        b3z = float(vis3d_b3z_entry.get())
    except ValueError:
        messagebox.showerror(get_text("input_error"), get_text("numeric_values_error"))
        return
    
    b1 = np.array([b1x, b1y, b1z])
    b2 = np.array([b2x, b2y, b2z])
    b3 = np.array([b3x, b3y, b3z])
    
    # clear the plot frame
    for widget in vis3d_plot_frame.winfo_children():
        widget.destroy()
    
    # make new 3D plot (neon style)
    fig = plt.figure(figsize=(6,6), facecolor=current_theme["plot_bg"])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(current_theme["plot_bg"])
    ax.grid(True, color=current_theme["grid"], linestyle='--', alpha=0.7)
    ax.set_title("3D Lattice Visualization", color=current_theme["fg"], fontsize=14, fontweight='bold')
    ax.set_xlabel("x", color=current_theme["fg"])
    ax.set_ylabel("y", color=current_theme["fg"])
    ax.set_zlabel("z", color=current_theme["fg"])
    ax.tick_params(colors=current_theme["fg"])
    
    # show the origin with neon effect
    ax.scatter([0], [0], [0], color=current_theme["neon_accent"], s=100, edgecolor='white', linewidth=1)
    
    # make lattice points (small range)
    points = []
    for m in range(-3, 4):
        for n in range(-3, 4):
            for l in range(-3, 4):
                point = m * b1 + n * b2 + l * b3
                points.append(point)
    points = np.array(points)
    
    # show basis vectors with neon effect
    # red for b1, green for b2, blue for b3
    ax.quiver(0, 0, 0, b1[0], b1[1], b1[2], color=current_theme["neon_accent"], 
             arrow_length_ratio=0.1, linewidth=2)
    
    # green for b2
    ax.quiver(0, 0, 0, b2[0], b2[1], b2[2], color=current_theme["neon_secondary"], 
             arrow_length_ratio=0.1, linewidth=2)
    
    # blue for b3
    ax.quiver(0, 0, 0, b3[0], b3[1], b3[2], color=current_theme["success"], 
             arrow_length_ratio=0.1, linewidth=2)
    
    # label the basis vectors
    ax.text(b1[0], b1[1], b1[2], "  b₁", color=current_theme["accent"], fontsize=10, fontweight='bold')
    ax.text(b2[0], b2[1], b2[2], "  b₂", color=current_theme["secondary"], fontsize=10, fontweight='bold')
    ax.text(b3[0], b3[1], b3[2], "  b₃", color=current_theme["success"], fontsize=10, fontweight='bold')
    
    # plot the lattice points
    scatter = ax.scatter(points[:,0], points[:,1], points[:,2], 
                        c=current_theme["neon_accent"], alpha=0.8, s=30, 
                        edgecolor='white', linewidth=0.5)
    
    # show the parallelepiped representing the lattice
    vertices = np.array([
        [0, 0, 0],
        b1, b2, b3,
        b1 + b2, b1 + b3, b2 + b3,
        b1 + b2 + b3
    ])
    hull = ConvexHull(vertices)
    
    # show the lattice faces
    for simplex in hull.simplices:
        face = vertices[simplex]
        face_center = np.mean(face, axis=0)
        # make gradient color based on distance from origin
        dist = np.linalg.norm(face_center)
        ax.plot3D(vertices[simplex, 0], vertices[simplex, 1], vertices[simplex, 2], 
                 color=current_theme["warning"], alpha=0.3, linewidth=1.5)
        
        vtx = np.array([vertices[s] for s in simplex])
        tri = ax.plot_trisurf(vtx[:,0], vtx[:,1], vtx[:,2], 
                             color=current_theme["warning"], alpha=0.1, shade=True)
    
    #show the lattice edges
    ax.plot([0, max_val*1.2], [0, 0], [0, 0], color=current_theme["accent"], alpha=0.5, linestyle='--')
    ax.plot([0, 0], [0, max_val*1.2], [0, 0], color=current_theme["secondary"], alpha=0.5, linestyle='--')
    ax.plot([0, 0], [0, 0], [0, max_val*1.2], color=current_theme["success"], alpha=0.5, linestyle='--')
    
    # set the view limits
    max_val = np.max(np.abs(points))
    ax.set_xlim(-max_val*1.2, max_val*1.2)
    ax.set_ylim(-max_val*1.2, max_val*1.2)
    ax.set_zlim(-max_val*1.2, max_val*1.2)
    
    
    canvas = FigureCanvasTkAgg(fig, master=vis3d_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # add toolbar
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    toolbar = NavigationToolbar2Tk(canvas, vis3d_plot_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # animation functions
    def rotate(angle):
        ax.view_init(elev=30, azim=angle)
        canvas.draw()
    
    # auto-rotate function
    def auto_rotate():
        for angle in range(0, 360, 5):
            ax.view_init(elev=30, azim=angle)
            canvas.draw()
            
            vis3d_plot_frame.update()
            time.sleep(0.05)
    
    # add rotation buttons
    rotation_frame = ttk.Frame(vis3d_plot_frame)
    rotation_frame.pack(pady=5)
    
    ttk.Button(rotation_frame, text=get_text("rotate"), style='Neon.TButton',
              command=lambda: threading.Thread(target=auto_rotate, daemon=True).start()).pack(side=tk.LEFT, padx=5)
    ttk.Button(rotation_frame, text=get_text("reset_view"), style='Secondary.TButton',
              command=lambda: rotate(30)).pack(side=tk.LEFT, padx=5)

# change the current language
def set_language(lang):
    global current_language
    current_language = lang

    # change the text of all widgets
    root.title(get_text("app_title"))
    
    # refresh the text of all widgets
    notebook.tab(tab_overview, text=get_text("overview_tab"))
    notebook.tab(tab_visual, text=get_text("2d_lattice_tab"))
    notebook.tab(tab_3d_visual, text=get_text("3d_lattice_tab"))
    notebook.tab(tab_lll, text=get_text("lll_tab"))
    notebook.tab(tab_svp, text=get_text("svp_tab"))
    notebook.tab(tab_ntru, text=get_text("ntru_tab"))
    notebook.tab(tab_ctf, text=get_text("ctf_challenge_tab"))
    
    # renew the menu items
    file_menu.entryconfigure(0, label=get_text("save_results"))
    file_menu.entryconfigure(1, label=get_text("load_settings"))
    file_menu.entryconfigure(3, label=get_text("exit"))
    settings_menu.entryconfigure(0, label=get_text("toggle_theme"))
    help_menu.entryconfigure(0, label=get_text("documentation"))
    help_menu.entryconfigure(1, label=get_text("about"))
    
    # renew the text of all widgets
    header_label.config(text=get_text("lattice_overview_title"))
    overview_text.config(state='normal')
    overview_text.delete("1.0", tk.END)
    overview_text.insert(tk.END, get_text("lattice_overview_text"))
    overview_text.config(state='disabled')
    
    # refresh the text of all buttons
    vis_plot_button.config(text=get_text("plot_lattice"))
    vis3d_plot_button.config(text=get_text("plot_lattice"))
    lll_button.config(text=get_text("run_lll"))
    svp_button.config(text=get_text("solve_svp"))
    ntru_button.config(text=get_text("run_ntru_demo"))
    ctf_header_label.config(text=get_text("ctf_challenge_tab"))
    ctf_basis_input_label.config(text=get_text("ctf_basis_input"))
    ctf_solve_button.config(text=get_text("ctf_decode"))
    ctf_result_label.config(text=get_text("ctf_result"))
    
    # renew the text of the theme button
    theme_button.config(text=get_text("dark_mode") if not DARK_MODE else get_text("light_mode"))

# change the current theme
def toggle_theme():
    global DARK_MODE, current_theme
    DARK_MODE = not DARK_MODE
    current_theme = THEMES["dark"] if DARK_MODE else THEMES["light"]
    apply_style()
    
    # renew lavels and buttons
    theme_button.config(text=get_text("light_mode") if DARK_MODE else get_text("dark_mode"))
    
    # change the background color of the root window
    root.configure(bg=current_theme["bg"])
    
    # change the background color of all tabs
    for tab in [tab_overview, tab_visual, tab_3d_visual, tab_lll, tab_svp, tab_cvp, tab_ntru, tab_ctf]:
        tab.configure(style='TFrame')
    
    # change the background color of all text widgets
    for text_widget in [overview_text, result_text, svp_result_text, cvp_result_text, ntru_output, ctf_basis_input_text, ctf_output_text]:
        text_widget.configure(
            bg=current_theme["bg"],
            fg=current_theme["fg"],
            insertbackground=current_theme["fg"]
        )

# extended LLL reduction algorithm
def lll_reduction(basis, delta=0.75):
    """
    LLL (Lenstra-Lenstra-Lovász) 格子基底縮小アルゴリズム
    任意次元の格子基底に対応
    """
    basis = np.array(basis, dtype=float)
    n, m = basis.shape  # n: vector dimension, m: number of vectors
    
    
    ortho = np.zeros_like(basis, dtype=float)
    # gram-schmidt orthogonalization
    mu = np.zeros((n, n), dtype=float)
    
    # action of the Gram-Schmidt process
    def gram_schmidt():
        for i in range(n):
            ortho[i] = basis[i].copy()
            for j in range(i):
                mu[i,j] = np.dot(basis[i], ortho[j]) / np.dot(ortho[j], ortho[j])
                ortho[i] = ortho[i] - mu[i,j] * ortho[j]
    
    
    gram_schmidt()
    
    
    k = 1
    while k < n:
        
        for j in range(k-1, -1, -1):
            if abs(mu[k,j]) > 0.5:
                
                r = round(mu[k,j])
                basis[k] = basis[k] - r * basis[j]
                
                for i in range(j+1):
                    mu[k,i] = mu[k,i] - r * mu[j,i]
        
        
        if np.dot(ortho[k], ortho[k]) >= (delta - mu[k,k-1]**2) * np.dot(ortho[k-1], ortho[k-1]):
            k = k + 1
        else:
            basis[[k, k-1]] = basis[[k-1, k]]
            gram_schmidt()
            k = max(1, k-1)
    
    return basis

def run_lll_advanced():
    try:
        dimension = int(lll_dimension_var.get())
        
        basis = []
        
        if dimension == 2:
            b1 = [float(lll_b1x_entry.get()), float(lll_b1y_entry.get())]
            b2 = [float(lll_b2x_entry.get()), float(lll_b2y_entry.get())]
            basis = [b1, b2]
        elif dimension == 3:
            b1 = [float(lll_3d_b1x_entry.get()), float(lll_3d_b1y_entry.get()), float(lll_3d_b1z_entry.get())]
            b2 = [float(lll_3d_b2x_entry.get()), float(lll_3d_b2y_entry.get()), float(lll_3d_b2z_entry.get())]
            b3 = [float(lll_3d_b3x_entry.get()), float(lll_3d_b3y_entry.get()), float(lll_3d_b3z_entry.get())]
            basis = [b1, b2, b3]
        else:
            text_input = lll_matrix_input.get("1.0", tk.END)
            lines = text_input.strip().split('\n')
            for line in lines:
                vector = [float(x) for x in line.split()]
                if len(vector) != dimension:
                    raise ValueError(f"Vector dimension does not match: expected {dimension}, got {len(vector)}")
                basis.append(vector)
            if len(basis) != dimension:
                raise ValueError(f"Expected {dimension} vectors, got {len(basis)}")
    
    except ValueError as e:
        messagebox.showerror(get_text("input_error"), f"Invalid input: {str(e)}")
        return
    
    # actual LLL reduction
    orig_basis = np.array(basis)
    reduced_basis = lll_reduction(orig_basis.copy())
    
    # show the results
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"【{get_text('original_lattice')}】\n")
    for i, vec in enumerate(orig_basis):
        vec_str = ", ".join([f"{x:.4f}" for x in vec])
        result_text.insert(tk.END, f"b{i+1} = ({vec_str})\n")
    
    result_text.insert(tk.END, f"\n【{get_text('reduced_lattice')}】\n")
    for i, vec in enumerate(reduced_basis):
        vec_str = ", ".join([f"{x:.4f}" for x in vec])
        result_text.insert(tk.END, f"b{i+1}' = ({vec_str})\n")
    
    result_text.insert(tk.END, f"\n【{get_text('lattice_properties')}】\n")
    
    det_orig = np.linalg.det(orig_basis)
    det_red = np.linalg.det(reduced_basis)
    
    result_text.insert(tk.END, f"{get_text('original_det')}: {abs(det_orig):.4f}\n")
    result_text.insert(tk.END, f"{get_text('reduced_det')}: {abs(det_red):.4f}\n")
    
    orig_lengths = [np.linalg.norm(v) for v in orig_basis]
    red_lengths = [np.linalg.norm(v) for v in reduced_basis]
    
    result_text.insert(tk.END, f"\n{get_text('vector_lengths')}:\n")
    for i, (ol, rl) in enumerate(zip(orig_lengths, red_lengths)):
        result_text.insert(tk.END, f"b{i+1}: {ol:.4f} -> b{i+1}': {rl:.4f} ({100*(ol-rl)/ol:.1f}% reduction)\n")
    
    def orthogonality_defect(basis):
        prod_lengths = np.prod([np.linalg.norm(v) for v in basis])
        vol = abs(np.linalg.det(basis))
        return prod_lengths / vol
    
    orig_orth = orthogonality_defect(orig_basis)
    red_orth = orthogonality_defect(reduced_basis)
    
    result_text.insert(tk.END, f"\n{get_text('orthogonality_defect')}:\n")
    result_text.insert(tk.END, f"{get_text('original_lattice')}: {orig_orth:.4f}\n")
    result_text.insert(tk.END, f"{get_text('reduced_lattice')}: {red_orth:.4f}\n")
    
    if dimension == 2:
        fig1 = plt.figure(figsize=(4,4), facecolor=current_theme["plot_bg"])
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor(current_theme["plot_bg"])
        ax1.grid(True, color=current_theme["grid"], linestyle='--', alpha=0.7)
        ax1.set_title(get_text("original_lattice"), color=current_theme["fg"], fontsize=14)
        
        # generate lattice points
        points_orig = []
        for m in range(-10, 11):
            for n in range(-10, 11):
                point = m * orig_basis[0] + n * orig_basis[1]
                points_orig.append(point)
        points_orig = np.array(points_orig)
        
        # show the lattice points with neon effect
        ax1.scatter(points_orig[:,0], points_orig[:,1], s=15, 
                   color=current_theme["neon_accent"], alpha=0.8, 
                   edgecolor='white', linewidth=0.5)
        glow_size = 3
        for i in range(glow_size):
            alpha = 0.1 - (i * 0.03)
            width = (glow_size - i) * 0.1
            ax1.arrow(0, 0, orig_basis[0][0], orig_basis[0][1], 
                     fc=current_theme["neon_accent"], ec=current_theme["neon_accent"],
                     width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                     length_includes_head=True)
            ax1.arrow(0, 0, orig_basis[1][0], orig_basis[1][1], 
                     fc=current_theme["neon_secondary"], ec=current_theme["neon_secondary"],
                     width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                     length_includes_head=True)
        
        ax1.arrow(0, 0, orig_basis[0][0], orig_basis[0][1], head_width=0.3, head_length=0.3, 
                 fc=current_theme["accent"], ec=current_theme["accent"], length_includes_head=True)
        ax1.arrow(0, 0, orig_basis[1][0], orig_basis[1][1], head_width=0.3, head_length=0.3, 
                 fc=current_theme["secondary"], ec=current_theme["secondary"], length_includes_head=True)
        
        parallelogram = plt.Polygon([
            [0, 0],
            orig_basis[0],
            orig_basis[0] + orig_basis[1],
            orig_basis[1]
        ], closed=True, alpha=0.2, color=current_theme["accent"])
        ax1.add_patch(parallelogram)
        
        ax1.set_xlabel("x", color=current_theme["fg"])
        ax1.set_ylabel("y", color=current_theme["fg"])
        ax1.tick_params(colors=current_theme["fg"])
        ax1.set_aspect('equal')
        
        plt.tight_layout()
        plt.show(block=False)

        fig2 = plt.figure(figsize=(4,4), facecolor=current_theme["plot_bg"])
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor(current_theme["plot_bg"])
        ax2.grid(True, color=current_theme["grid"], linestyle='--', alpha=0.7)
        ax2.set_title(get_text("reduced_lattice"), color=current_theme["fg"], fontsize=14)
        
        points_red = []
        for m in range(-10, 11):
            for n in range(-10, 11):
                point = m * reduced_basis[0] + n * reduced_basis[1]
                points_red.append(point)
        points_red = np.array(points_red)
        
        ax2.scatter(points_red[:,0], points_red[:,1], s=15, 
                   color=current_theme["neon_accent"], alpha=0.8, 
                   edgecolor='white', linewidth=0.5)
        
        for i in range(glow_size):
            alpha = 0.1 - (i * 0.03)
            width = (glow_size - i) * 0.1
            ax2.arrow(0, 0, reduced_basis[0][0], reduced_basis[0][1], 
                     fc=current_theme["neon_accent"], ec=current_theme["neon_accent"],
                     width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                     length_includes_head=True)
            ax2.arrow(0, 0, reduced_basis[1][0], reduced_basis[1][1], 
                     fc=current_theme["neon_secondary"], ec=current_theme["neon_secondary"],
                     width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                     length_includes_head=True)
        
        ax2.arrow(0, 0, reduced_basis[0][0], reduced_basis[0][1], head_width=0.3, head_length=0.3, 
                 fc=current_theme["accent"], ec=current_theme["accent"], length_includes_head=True)
        ax2.arrow(0, 0, reduced_basis[1][0], reduced_basis[1][1], head_width=0.3, head_length=0.3, 
                 fc=current_theme["secondary"], ec=current_theme["secondary"], length_includes_head=True)
        
        parallelogram = plt.Polygon([
            [0, 0],
            reduced_basis[0],
            reduced_basis[0] + reduced_basis[1],
            reduced_basis[1]
        ], closed=True, alpha=0.2, color=current_theme["success"])
        ax2.add_patch(parallelogram)
        
        ax2.set_xlabel("x", color=current_theme["fg"])
        ax2.set_ylabel("y", color=current_theme["fg"])
        ax2.tick_params(colors=current_theme["fg"])
        ax2.set_aspect('equal')
        
        plt.tight_layout()
        plt.show(block=False)
    
    elif dimension == 3:
        fig1 = plt.figure(figsize=(5,5), facecolor=current_theme["plot_bg"])
        ax1 = fig1.add_subplot(111, projection='3d')
        ax1.set_facecolor(current_theme["plot_bg"])
        ax1.set_title(get_text("original_lattice"), color=current_theme["fg"], fontsize=14)

        points_orig = []
        for m in range(-3, 4):
            for n in range(-3, 4):
                for l in range(-3, 4):
                    point = m * orig_basis[0] + n * orig_basis[1] + l * orig_basis[2]
                    points_orig.append(point)
        points_orig = np.array(points_orig)
        
        ax1.scatter(points_orig[:,0], points_orig[:,1], points_orig[:,2], 
                   s=30, color=current_theme["neon_accent"], alpha=0.8, 
                   edgecolor='white', linewidth=0.5)
        
        ax1.quiver(0, 0, 0, orig_basis[0][0], orig_basis[0][1], orig_basis[0][2], 
                  color=current_theme["neon_accent"], arrow_length_ratio=0.1, linewidth=2)
        ax1.quiver(0, 0, 0, orig_basis[1][0], orig_basis[1][1], orig_basis[1][2], 
                  color=current_theme["neon_secondary"], arrow_length_ratio=0.1, linewidth=2)
        ax1.quiver(0, 0, 0, orig_basis[2][0], orig_basis[2][1], orig_basis[2][2], 
                  color=current_theme["success"], arrow_length_ratio=0.1, linewidth=2)
        
        vertices = np.array([
            [0, 0, 0],
            orig_basis[0], orig_basis[1], orig_basis[2],
            orig_basis[0] + orig_basis[1], orig_basis[0] + orig_basis[2], 
            orig_basis[1] + orig_basis[2],
            orig_basis[0] + orig_basis[1] + orig_basis[2]
        ])
        hull = ConvexHull(vertices)

        for simplex in hull.simplices:
            ax1.plot3D(vertices[simplex, 0], vertices[simplex, 1], vertices[simplex, 2], 
                     color=current_theme["warning"], alpha=0.3, linewidth=1.5)
            vtx = np.array([vertices[s] for s in simplex])
            tri = ax1.plot_trisurf(vtx[:,0], vtx[:,1], vtx[:,2], 
                                 color=current_theme["warning"], alpha=0.1, shade=True)
        
        ax1.set_xlabel("x", color=current_theme["fg"])
        ax1.set_ylabel("y", color=current_theme["fg"])
        ax1.set_zlabel("z", color=current_theme["fg"])
        ax1.tick_params(colors=current_theme["fg"])
        
        plt.tight_layout()
        plt.show(block=False)
        
        fig2 = plt.figure(figsize=(5,5), facecolor=current_theme["plot_bg"])
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.set_facecolor(current_theme["plot_bg"])
        ax2.set_title(get_text("reduced_lattice"), color=current_theme["fg"], fontsize=14)
        
        # generate lattice points (limited range)
        points_red = []
        for m in range(-3, 4):
            for n in range(-3, 4):
                for l in range(-3, 4):
                    point = m * reduced_basis[0] + n * reduced_basis[1] + l * reduced_basis[2]
                    points_red.append(point)
        points_red = np.array(points_red)
        
        ax2.scatter(points_red[:,0], points_red[:,1], points_red[:,2], 
                   s=30, color=current_theme["neon_accent"], alpha=0.8, 
                   edgecolor='white', linewidth=0.5)
        
        ax2.quiver(0, 0, 0, reduced_basis[0][0], reduced_basis[0][1], reduced_basis[0][2], 
                  color=current_theme["neon_accent"], arrow_length_ratio=0.1, linewidth=2)
        ax2.quiver(0, 0, 0, reduced_basis[1][0], reduced_basis[1][1], reduced_basis[1][2], 
                  color=current_theme["neon_secondary"], arrow_length_ratio=0.1, linewidth=2)
        ax2.quiver(0, 0, 0, reduced_basis[2][0], reduced_basis[2][1], reduced_basis[2][2], 
                  color=current_theme["success"], arrow_length_ratio=0.1, linewidth=2)
        
        vertices = np.array([
            [0, 0, 0],
            reduced_basis[0], reduced_basis[1], reduced_basis[2],
            reduced_basis[0] + reduced_basis[1], reduced_basis[0] + reduced_basis[2], 
            reduced_basis[1] + reduced_basis[2],
            reduced_basis[0] + reduced_basis[1] + reduced_basis[2]
        ])
        hull = ConvexHull(vertices)
        
        for simplex in hull.simplices:
            ax2.plot3D(vertices[simplex, 0], vertices[simplex, 1], vertices[simplex, 2], 
                     color=current_theme["warning"], alpha=0.3, linewidth=1.5)
            vtx = np.array([vertices[s] for s in simplex])
            tri = ax2.plot_trisurf(vtx[:,0], vtx[:,1], vtx[:,2], 
                                 color=current_theme["warning"], alpha=0.1, shade=True)
        
        ax2.set_xlabel("x", color=current_theme["fg"])
        ax2.set_ylabel("y", color=current_theme["fg"])
        ax2.set_zlabel("z", color=current_theme["fg"])
        ax2.tick_params(colors=current_theme["fg"])
        
        plt.tight_layout()
        plt.show(block=False)

def shortest_vector_problem():
    try:
        dimension = int(svp_dimension_var.get())

        basis = []
        
        if dimension == 2:
            b1 = [float(svp_b1x_entry.get()), float(svp_b1y_entry.get())]
            b2 = [float(svp_b2x_entry.get()), float(svp_b2y_entry.get())]
            basis = [b1, b2]
        else:
            text_input = svp_matrix_input.get("1.0", tk.END)
            lines = text_input.strip().split('\n')
            for line in lines:
                vector = [float(x) for x in line.split()]
                if len(vector) != dimension:
                    raise ValueError(f"Vector dimension does not match: expected {dimension}, got {len(vector)}")
                basis.append(vector)
            if len(basis) != dimension:
                raise ValueError(f"Expected {dimension} vectors, got {len(basis)}")
        
        basis = np.array(basis)
        
        max_range = 10 if dimension == 2 else 3
        lattice_points = []
        vectors = []
        
        for coeffs in np.ndindex(*[2*max_range+1]*dimension):
            coeffs = np.array(coeffs) - max_range
            if np.any(coeffs != 0):
                point = np.zeros(dimension)
                for i, coeff in enumerate(coeffs):
                    point += coeff * basis[i]
                lattice_points.append(point)
                vectors.append(coeffs)
        
        distances = [np.linalg.norm(point) for point in lattice_points]
        sorted_indices = np.argsort(distances)
        
        svp_result_text.delete("1.0", tk.END)
        svp_result_text.insert(tk.END, f"【{get_text('shortest_vectors')}】\n\n")
        
        for i, idx in enumerate(sorted_indices[:10]):
            point = lattice_points[idx]
            vector = vectors[idx]
            distance = distances[idx]
            
            vector_str = " + ".join([f"{v}b{j+1}" for j, v in enumerate(vector) if v != 0])
            if not vector_str:
                vector_str = "0"
            
            point_str = ", ".join([f"{x:.4f}" for x in point])
            svp_result_text.insert(tk.END, f"{i+1}. Vector: {vector_str}\n")
            svp_result_text.insert(tk.END, f"   Coordinates: ({point_str})\n")
            svp_result_text.insert(tk.END, f"   Length: {distance:.4f}\n\n")
        
        if dimension == 2:
            fig = plt.figure(figsize=(6, 6), facecolor=current_theme["plot_bg"])
            ax = fig.add_subplot(111)
            ax.set_facecolor(current_theme["plot_bg"])
            ax.grid(True, color=current_theme["grid"], linestyle='--', alpha=0.7)
            ax.set_title(get_text("shortest_vectors"), color=current_theme["fg"], fontsize=14, fontweight='bold')

            points_array = np.array(lattice_points)
            ax.scatter(points_array[:,0], points_array[:,1], s=15, 
                      color=current_theme["neon_accent"], alpha=0.8, 
                      edgecolor='white', linewidth=0.5)
            glow_size = 3
            for i in range(glow_size):
                alpha = 0.1 - (i * 0.03)
                width = (glow_size - i) * 0.1
                ax.arrow(0, 0, basis[0][0], basis[0][1], 
                         fc=current_theme["neon_accent"], ec=current_theme["neon_accent"],
                         width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                         length_includes_head=True)
                ax.arrow(0, 0, basis[1][0], basis[1][1], 
                         fc=current_theme["neon_secondary"], ec=current_theme["neon_secondary"],
                         width=width, alpha=alpha, head_width=0.3, head_length=0.3, 
                         length_includes_head=True)
            
            ax.arrow(0, 0, basis[0][0], basis[0][1], head_width=0.3, head_length=0.3, 
                     fc=current_theme["accent"], ec=current_theme["accent"], length_includes_head=True)
            ax.arrow(0, 0, basis[1][0], basis[1][1], head_width=0.3, head_length=0.3, 
                     fc=current_theme["secondary"], ec=current_theme["secondary"], length_includes_head=True)
            
            shortest_idx = sorted_indices[0]
            shortest_point = lattice_points[shortest_idx]
            ax.arrow(0, 0, shortest_point[0], shortest_point[1], head_width=0.3, head_length=0.3, 
                    fc=current_theme["success"], ec=current_theme["success"], 
                    length_includes_head=True, linewidth=2, zorder=10)
            ax.text(shortest_point[0]/2, shortest_point[1]/2, "Shortest", 
                   color=current_theme["success"], fontweight='bold')
            
            for i, idx in enumerate(sorted_indices[1:5]):
                point = lattice_points[idx]
                ax.arrow(0, 0, point[0], point[1], head_width=0.2, head_length=0.2, 
                        fc=current_theme["warning"], ec=current_theme["warning"], 
                        length_includes_head=True, alpha=0.7, zorder=9-i)
            
            ax.set_xlabel("x", color=current_theme["fg"])
            ax.set_ylabel("y", color=current_theme["fg"])
            ax.tick_params(colors=current_theme["fg"])
            ax.set_aspect('equal')
            
            plt.tight_layout()
            plt.show(block=False)
    
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        return

class NTRUCipher:
    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q
        self.public_key = None
        self.private_key_f = None
        self.private_key_g = None
    
    def generate_keys(self):
        """鍵生成: ランダムな多項式f, gからh = p*f^-1 * g mod qを計算"""
        while True:
            try:
                # make random coefficients for f and g
                f_coeffs = [random.choice([-1, 0, 1]) for _ in range(self.N)]
                g_coeffs = [random.choice([-1, 0, 1]) for _ in range(self.N)]
                
                f_inv_p = self._invert_poly_mod(f_coeffs, self.p, self.N)
                f_inv_q = self._invert_poly_mod(f_coeffs, self.q, self.N)
                
                h_coeffs = self._multiply_poly_mod(
                    self._multiply_scalar(f_inv_q, self.p),
                    g_coeffs,
                    self.q,
                    self.N
                )
                
                self.public_key = h_coeffs
                self.private_key_f = f_coeffs
                self.private_key_g = g_coeffs
                
                return (h_coeffs, (f_coeffs, g_coeffs))
            
            except ValueError:
                continue
    
    def encrypt(self, message, r=None):
        """暗号化: e = r*h + m mod q"""
        if not self.public_key:
            raise ValueError("Public key not generated")
        
        if isinstance(message, str):
            m_coeffs = [ord(c) % self.p for c in message]
            m_coeffs.extend([0] * (self.N - len(m_coeffs)))
            m_coeffs = m_coeffs[:self.N]
        else:
            m_coeffs = message
        
        if r is None:
            r_coeffs = [random.choice([-1, 0, 1]) for _ in range(self.N)]
        else:
            r_coeffs = r
        
        # e = r*h + m mod q
        e_coeffs = self._add_poly_mod(
            self._multiply_poly_mod(r_coeffs, self.public_key, self.q, self.N),
            m_coeffs,
            self.q
        )
        
        return e_coeffs
    
    def decrypt(self, ciphertext):
        """復号: m = f*e mod p を、中心リフトと丸め込みで正しく計算する"""
        if not self.private_key_f:
            raise ValueError("Private key not generated")
        
        a_coeffs = self._multiply_poly_mod(
            self.private_key_f,
            ciphertext,
            self.q,
            self.N
        )
        
        a_coeffs = [int(round(self._centered_mod(a, self.q))) for a in a_coeffs]
        
        m_coeffs = [a % self.p for a in a_coeffs]
        return m_coeffs
    
    def _centered_mod(self, a, mod):
        """中心化された剰余を返す（-mod/2からmod/2の範囲）"""
        a = a % mod
        if a > mod // 2:
            a -= mod
        return a
    
    def _poly_mod_xn_minus_1(self, poly, n):
        """多項式をx^n - 1で割った余り（係数リストを返す）"""
        result = [0] * n
        for i, coef in enumerate(poly):
            result[i % n] = (result[i % n] + coef)
        return result
    
    def _add_poly_mod(self, poly1, poly2, mod):
        """多項式の加算（mod適用）"""
        return [(a + b) % mod for a, b in zip(poly1, poly2)]
    
    def _multiply_scalar(self, poly, scalar):
        """多項式のスカラー倍"""
        return [coef * scalar for coef in poly]
    
    def _multiply_poly_mod(self, poly1, poly2, mod, n):
        """多項式の乗算（mod適用、x^n - 1での剰余計算）"""
        result = [0] * (2 * n)
        
        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i + j] = (result[i + j] + poly1[i] * poly2[j]) % mod
        
        return self._poly_mod_xn_minus_1(result, n)
    
    def _invert_poly_mod(self, poly, mod, n):
        """拡張ユークリッドアルゴリズムを用いた多項式の逆元計算"""

        s = [0] * (2 * n)
        t = [0] * (2 * n)
        s[0] = 1
        mod_poly = [0] * (n + 1)
        mod_poly[0] = -1
        mod_poly[n] = 1
        
        a = poly.copy() + [0] * n
        b = mod_poly.copy()
        
        while True:
            deg_a = next((i for i in range(len(a) - 1, -1, -1) if a[i] != 0), -1)
            deg_b = next((i for i in range(len(b) - 1, -1, -1) if b[i] != 0), -1)
            
            if deg_b == -1:
                raise ValueError("Polynomial not invertible")
            
            if deg_b == 0:
                if b[0] == 0:
                    raise ValueError("Polynomial not invertible")

                b_inv = pow(b[0], -1, mod)
                return [(s[i] * b_inv) % mod for i in range(n)]
            
            if deg_a < deg_b:
                a, b = b, a
                s, t = t, s
                continue
            
            if a[deg_a] == 0 or b[deg_b] == 0:
                continue
                
            factor = (a[deg_a] * pow(b[deg_b], -1, mod)) % mod
            power = deg_a - deg_b
            
            for i in range(deg_b + 1):
                a[i + power] = (a[i + power] - factor * b[i]) % mod
            
            # renew s, t
            for i in range(n):
                s[i + power] = (s[i + power] - factor * t[i]) % mod

# action: NTRU cipher demo
def run_ntru_demo():
    try:
        # get parameters
        N = int(ntru_N_entry.get())
        p = int(ntru_p_entry.get())
        q = int(ntru_q_entry.get())
        
        # get message
        message = ntru_message_entry.get()
        
        # clear output
        ntru_output.delete("1.0", tk.END)
        
        # reset random seed
        ntru = NTRUCipher(N, p, q)
        
        # show parameters
        ntru_output.insert(tk.END, f"NTRU Encryption Demo (N={N}, p={p}, q={q})\n")
        ntru_output.insert(tk.END, "=" * 50 + "\n\n")
        
        # make keys
        ntru_output.insert(tk.END, f"{get_text('encryption_step1')}\n\n")
        public_key, private_key = ntru.generate_keys()
        
        ntru_output.insert(tk.END, f"Public key h(x): {public_key}\n\n")
        ntru_output.insert(tk.END, f"Private key f(x): {private_key[0]}\n")
        ntru_output.insert(tk.END, f"Private key g(x): {private_key[1]}\n\n")
        
        ntru_output.insert(tk.END, f"{get_text('encryption_step2')}\n\n")
        ntru_output.insert(tk.END, f"Original message: {message}\n")
        
        # change message to polynomial
        m_coeffs = [ord(c) % p for c in message]
        m_coeffs.extend([0] * (N - len(m_coeffs)))
        m_coeffs = m_coeffs[:N]
        
        ntru_output.insert(tk.END, f"Message polynomial m(x): {m_coeffs}\n\n")
        
        # encrypt
        ntru_output.insert(tk.END, f"{get_text('encryption_step3')}\n\n")
        
        # role of r(x)
        r_coeffs = [random.choice([-1, 0, 1]) for _ in range(N)]
        ntru_output.insert(tk.END, f"Random polynomial r(x): {r_coeffs}\n")
        
        # encrypt
        ciphertext = ntru.encrypt(m_coeffs, r_coeffs)
        ntru_output.insert(tk.END, f"Ciphertext e(x): {ciphertext}\n\n")
        
        # decrypt
        ntru_output.insert(tk.END, f"{get_text('encryption_step4')}\n\n")
        decrypted = ntru.decrypt(ciphertext)
        ntru_output.insert(tk.END, f"Decrypted polynomial: {decrypted}\n")
        
        decrypted_message = ""
        for coef in decrypted:
            if coef != 0:
                decrypted_message += chr(coef)
        
        ntru_output.insert(tk.END, f"Decrypted message: {decrypted_message}\n\n")
        
        is_correct = decrypted[:len(message)] == m_coeffs[:len(message)]
        if is_correct:
            ntru_output.insert(tk.END, f"{get_text('decryption_success')}\n")
        else:
            ntru_output.insert(tk.END, f"{get_text('decryption_fail')}\n")
    
    except Exception as e:
        ntru_output.insert(tk.END, f"Error: {str(e)}\n")

def solve_lattice_ctf():
    try:
        text = ctf_basis_input_text.get("1.0", tk.END).strip()
        if not text:
            raise ValueError(get_text("ctf_error") + "No input provided.")
        lines = text.splitlines()
        basis = []
        for line in lines:
            vector = [float(x) for x in line.split()]
            basis.append(vector)
        basis = np.array(basis)
        if basis.ndim != 2:
            raise ValueError(get_text("ctf_error") + "Invalid matrix format.")
        
        # action: LLL reduction
        reduced = lll_reduction(basis.copy())
        # choice: shortest vector
        lengths = [np.linalg.norm(v) for v in reduced]
        min_index = np.argmin(lengths)
        short_vec = reduced[min_index]
        
        msg = ""
        convertable = all(32 <= int(round(x)) <= 126 for x in short_vec)
        if convertable:
            for val in short_vec:
                msg += chr(int(round(val)))
        else:
            msg = "Short vector: " + ", ".join([f"{x:.4f}" for x in short_vec])
        return msg
    except Exception as e:
        return get_text("ctf_error") + " " + str(e)

# application GUI
root = tk.Tk()
root.title(get_text("app_title"))
root.geometry("1000x700")
root.configure(bg=current_theme["bg"])

# Setting up the menu
menubar = tk.Menu(root)
root.config(menu=menubar)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_text("file_menu"), menu=file_menu)
file_menu.add_command(label=get_text("save_results"), command=lambda: messagebox.showinfo("Info", "Save functionality will be implemented here"))
file_menu.add_command(label=get_text("load_settings"), command=lambda: messagebox.showinfo("Info", "Load functionality will be implemented here"))
file_menu.add_separator()
file_menu.add_command(label=get_text("exit"), command=root.quit)

# Settings menu 
settings_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_text("settings_menu"), menu=settings_menu)
settings_menu.add_command(label=get_text("toggle_theme"), command=toggle_theme)

# Set language
language_menu = tk.Menu(settings_menu, tearoff=0)
settings_menu.add_cascade(label=get_text("language"), menu=language_menu)
language_menu.add_command(label="日本語", command=lambda: set_language("ja"))
language_menu.add_command(label="中分", command=lambda: set_language("zh"))
language_menu.add_command(label="English", command=lambda: set_language("en"))


# Help menu
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label=get_text("help_menu"), menu=help_menu)
help_menu.add_command(label=get_text("documentation"), command=lambda: messagebox.showinfo("Documentation", "Documentation will be shown here"))
help_menu.add_command(label=get_text("about"), command=lambda: messagebox.showinfo("About", "Advanced Lattice Cryptography Learning System\nVersion 2.0"))

# Toolbar
toolbar = ttk.Frame(root, style='Header.TFrame')
toolbar.pack(side=tk.TOP, fill=tk.X)

# change theme button
theme_button = ttk.Button(toolbar, text=get_text("dark_mode"), command=toggle_theme)
theme_button.pack(side=tk.RIGHT, padx=5, pady=5)

# control variables
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ===============================
# tab1 
# ===============================
tab_overview = ttk.Frame(notebook)
notebook.add(tab_overview, text=get_text("overview_tab"))

# hedd frame
header_frame = ttk.Frame(tab_overview, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text=get_text("lattice_overview_title"), 
                         style='Accent.TLabel', font=('Helvetica', 16, 'bold'))
header_label.pack(pady=10)

# text about lattice
overview_text = scrolledtext.ScrolledText(tab_overview, wrap=tk.WORD, width=80, height=30, 
                                         font=("Helvetica", 12), bg=current_theme["bg"], 
                                         fg=current_theme["fg"])
overview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
intro_text = get_text("lattice_overview_text")
overview_text.insert(tk.END, intro_text)
overview_text.configure(state='disabled')

# ===============================
# tab2: viusalization
# ===============================
tab_visual = ttk.Frame(notebook)
notebook.add(tab_visual, text=get_text("2d_lattice_tab"))

# hedd frame
header_frame = ttk.Frame(tab_visual, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text="2D Lattice Visualization", 
                         style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
header_label.pack(pady=10)

# input frame
vis_input_frame = ttk.Frame(tab_visual)
vis_input_frame.pack(pady=10)

ttk.Label(vis_input_frame, text="b₁ = (").grid(row=0, column=0)
vis_b1x_entry = ttk.Entry(vis_input_frame, width=8)
vis_b1x_entry.grid(row=0, column=1)
ttk.Label(vis_input_frame, text=",").grid(row=0, column=2)
vis_b1y_entry = ttk.Entry(vis_input_frame, width=8)
vis_b1y_entry.grid(row=0, column=3)
ttk.Label(vis_input_frame, text=")").grid(row=0, column=4, padx=(0,20))

ttk.Label(vis_input_frame, text="b₂ = (").grid(row=0, column=5)
vis_b2x_entry = ttk.Entry(vis_input_frame, width=8)
vis_b2x_entry.grid(row=0, column=6)
ttk.Label(vis_input_frame, text=",").grid(row=0, column=7)
vis_b2y_entry = ttk.Entry(vis_input_frame, width=8)
vis_b2y_entry.grid(row=0, column=8)
ttk.Label(vis_input_frame, text=")").grid(row=0, column=9)

# setteing default values
vis_b1x_entry.insert(0, "3")
vis_b1y_entry.insert(0, "0")
vis_b2x_entry.insert(0, "1")
vis_b2y_entry.insert(0, "2")

# プplot setting button
button_frame = ttk.Frame(tab_visual)
button_frame.pack(pady=10)
vis_plot_button = ttk.Button(button_frame, text=get_text("plot_lattice"), style='TButton', 
                            command=plot_lattice_animated)
vis_plot_button.pack(side=tk.LEFT, padx=5)

# figure frame
vis_plot_frame = ttk.Frame(tab_visual)
vis_plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ===============================
# tab3: 3D lattice visualization
# ===============================
tab_3d_visual = ttk.Frame(notebook)
notebook.add(tab_3d_visual, text=get_text("3d_lattice_tab"))

# header
header_frame = ttk.Frame(tab_3d_visual, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text="3D Lattice Visualization", 
                         style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
header_label.pack(pady=10)

# input frame
vis3d_input_frame = ttk.Frame(tab_3d_visual)
vis3d_input_frame.pack(pady=10)

# vector inputs
ttk.Label(vis3d_input_frame, text="b₁ = (").grid(row=0, column=0)
vis3d_b1x_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b1x_entry.grid(row=0, column=1)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=2)
vis3d_b1y_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b1y_entry.grid(row=0, column=3)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=4)
vis3d_b1z_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b1z_entry.grid(row=0, column=5)
ttk.Label(vis3d_input_frame, text=")").grid(row=0, column=6, padx=(0,10))

ttk.Label(vis3d_input_frame, text="b₂ = (").grid(row=0, column=7)
vis3d_b2x_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b2x_entry.grid(row=0, column=8)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=9)
vis3d_b2y_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b2y_entry.grid(row=0, column=10)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=11)
vis3d_b2z_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b2z_entry.grid(row=0, column=12)
ttk.Label(vis3d_input_frame, text=")").grid(row=0, column=13, padx=(0,10))

ttk.Label(vis3d_input_frame, text="b₃ = (").grid(row=0, column=14)
vis3d_b3x_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b3x_entry.grid(row=0, column=15)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=16)
vis3d_b3y_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b3y_entry.grid(row=0, column=17)
ttk.Label(vis3d_input_frame, text=",").grid(row=0, column=18)
vis3d_b3z_entry = ttk.Entry(vis3d_input_frame, width=6)
vis3d_b3z_entry.grid(row=0, column=19)
ttk.Label(vis3d_input_frame, text=")").grid(row=0, column=20)

# setting default values
vis3d_b1x_entry.insert(0, "1")
vis3d_b1y_entry.insert(0, "0")
vis3d_b1z_entry.insert(0, "0")
vis3d_b2x_entry.insert(0, "0")
vis3d_b2y_entry.insert(0, "1")
vis3d_b2z_entry.insert(0, "0")
vis3d_b3x_entry.insert(0, "0")
vis3d_b3y_entry.insert(0, "0")
vis3d_b3z_entry.insert(0, "1")

# protto button
button_frame = ttk.Frame(tab_3d_visual)
button_frame.pack(pady=10)
vis3d_plot_button = ttk.Button(button_frame, text=get_text("plot_lattice"), style='TButton', 
                              command=plot_3d_lattice)
vis3d_plot_button.pack(side=tk.LEFT, padx=5)

# frame for the plot
vis3d_plot_frame = ttk.Frame(tab_3d_visual)
vis3d_plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ===============================
# タブ4: LLL algorithm
# ===============================
tab_lll = ttk.Frame(notebook)
notebook.add(tab_lll, text=get_text("lll_tab"))

# Heddader
header_frame = ttk.Frame(tab_lll, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text="LLL Algorithm", 
                         style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
header_label.pack(pady=10)

# choice of dimension
dimension_frame = ttk.Frame(tab_lll)
dimension_frame.pack(pady=10)
ttk.Label(dimension_frame, text=get_text("dimension")).pack(side=tk.LEFT)
lll_dimension_var = tk.StringVar(value="2")
dimension_menu = ttk.OptionMenu(dimension_frame, lll_dimension_var, "2", "2", "3", "4", "5")
dimension_menu.pack(side=tk.LEFT, padx=5)

# 2D input frame
lll_2d_frame = ttk.Frame(tab_lll)
lll_2d_frame.pack(pady=10)

ttk.Label(lll_2d_frame, text="b₁ = (").grid(row=0, column=0)
lll_b1x_entry = ttk.Entry(lll_2d_frame, width=8)
lll_b1x_entry.grid(row=0, column=1)
ttk.Label(lll_2d_frame, text=",").grid(row=0, column=2)
lll_b1y_entry = ttk.Entry(lll_2d_frame, width=8)
lll_b1y_entry.grid(row=0, column=3)
ttk.Label(lll_2d_frame, text=")").grid(row=0, column=4, padx=(0,20))

ttk.Label(lll_2d_frame, text="b₂ = (").grid(row=0, column=5)
lll_b2x_entry = ttk.Entry(lll_2d_frame, width=8)
lll_b2x_entry.grid(row=0, column=6)
ttk.Label(lll_2d_frame, text=",").grid(row=0, column=7)
lll_b2y_entry = ttk.Entry(lll_2d_frame, width=8)
lll_b2y_entry.grid(row=0, column=8)
ttk.Label(lll_2d_frame, text=")").grid(row=0, column=9)

# 3D input frame
lll_3d_frame = ttk.Frame(tab_lll)
lll_3d_frame.pack(pady=10)

ttk.Label(lll_3d_frame, text="b₁ = (").grid(row=0, column=0)
lll_3d_b1x_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b1x_entry.grid(row=0, column=1)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=2)
lll_3d_b1y_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b1y_entry.grid(row=0, column=3)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=4)
lll_3d_b1z_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b1z_entry.grid(row=0, column=5)
ttk.Label(lll_3d_frame, text=")").grid(row=0, column=6, padx=(0,10))

ttk.Label(lll_3d_frame, text="b₂ = (").grid(row=0, column=7)
lll_3d_b2x_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b2x_entry.grid(row=0, column=8)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=9)
lll_3d_b2y_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b2y_entry.grid(row=0, column=10)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=11)
lll_3d_b2z_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b2z_entry.grid(row=0, column=12)
ttk.Label(lll_3d_frame, text=")").grid(row=0, column=13, padx=(0,10))

ttk.Label(lll_3d_frame, text="b₃ = (").grid(row=0, column=14)
lll_3d_b3x_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b3x_entry.grid(row=0, column=15)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=16)
lll_3d_b3y_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b3y_entry.grid(row=0, column=17)
ttk.Label(lll_3d_frame, text=",").grid(row=0, column=18)
lll_3d_b3z_entry = ttk.Entry(lll_3d_frame, width=6)
lll_3d_b3z_entry.grid(row=0, column=19)
ttk.Label(lll_3d_frame, text=")").grid(row=0, column=20)

# matrix input frame
lll_matrix_frame = ttk.Frame(tab_lll)
lll_matrix_frame.pack(pady=10)
ttk.Label(lll_matrix_frame, text="Enter basis vectors (one per line):").pack()
lll_matrix_input = scrolledtext.ScrolledText(lll_matrix_frame, wrap=tk.WORD, width=60, height=10, 
                                            font=("Helvetica", 12), bg=current_theme["bg"], 
                                            fg=current_theme["fg"])
lll_matrix_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Set default values
lll_b1x_entry.insert(0, "3")
lll_b1y_entry.insert(0, "0")
lll_b2x_entry.insert(0, "1")
lll_b2y_entry.insert(0, "2")

lll_3d_b1x_entry.insert(0, "1")
lll_3d_b1y_entry.insert(0, "0")
lll_3d_b1z_entry.insert(0, "0")
lll_3d_b2x_entry.insert(0, "0")
lll_3d_b2y_entry.insert(0, "1")
lll_3d_b2z_entry.insert(0, "0")
lll_3d_b3x_entry.insert(0, "0")
lll_3d_b3y_entry.insert(0, "0")
lll_3d_b3z_entry.insert(0, "1")

# action button
button_frame = ttk.Frame(tab_lll)
button_frame.pack(pady=10)
lll_button = ttk.Button(button_frame, text=get_text("run_lll"), style='TButton', 
                       command=run_lll_advanced)
lll_button.pack(side=tk.LEFT, padx=5)

# show result
result_text = scrolledtext.ScrolledText(tab_lll, wrap=tk.WORD, width=80, height=10, 
                                       font=("Helvetica", 12), bg=current_theme["bg"], 
                                       fg=current_theme["fg"])
result_text.pack(pady=10, fill=tk.BOTH, expand=True)

# ===============================
# tab5: SVP
# ===============================
tab_svp = ttk.Frame(notebook)
notebook.add(tab_svp, text=get_text("svp_tab"))

# header
header_frame = ttk.Frame(tab_svp, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text="Shortest Vector Problem (SVP)", 
                         style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
header_label.pack(pady=10)

# choice of dimension
dimension_frame = ttk.Frame(tab_svp)
dimension_frame.pack(pady=10)
ttk.Label(dimension_frame, text=get_text("dimension")).pack(side=tk.LEFT)
svp_dimension_var = tk.StringVar(value="2")
dimension_menu = ttk.OptionMenu(dimension_frame, svp_dimension_var, "2", "2", "3", "4", "5")
dimension_menu.pack(side=tk.LEFT, padx=5)

# input frame
svp_2d_frame = ttk.Frame(tab_svp)
svp_2d_frame.pack(pady=10)

ttk.Label(svp_2d_frame, text="b₁ = (").grid(row=0, column=0)
svp_b1x_entry = ttk.Entry(svp_2d_frame, width=8)
svp_b1x_entry.grid(row=0, column=1)
ttk.Label(svp_2d_frame, text=",").grid(row=0, column=2)
svp_b1y_entry = ttk.Entry(svp_2d_frame, width=8)
svp_b1y_entry.grid(row=0, column=3)
ttk.Label(svp_2d_frame, text=")").grid(row=0, column=4, padx=(0,20))

ttk.Label(svp_2d_frame, text="b₂ = (").grid(row=0, column=5)
svp_b2x_entry = ttk.Entry(svp_2d_frame, width=8)
svp_b2x_entry.grid(row=0, column=6)
ttk.Label(svp_2d_frame, text=",").grid(row=0, column=7)
svp_b2y_entry = ttk.Entry(svp_2d_frame, width=8)
svp_b2y_entry.grid(row=0, column=8)
ttk.Label(svp_2d_frame, text=")").grid(row=0, column=9)

# input frame for matrix
svp_matrix_frame = ttk.Frame(tab_svp)
svp_matrix_frame.pack(pady=10)
ttk.Label(svp_matrix_frame, text="Enter basis vectors (one per line):").pack()
svp_matrix_input = scrolledtext.ScrolledText(svp_matrix_frame, wrap=tk.WORD, width=60, height=10, 
                                            font=("Helvetica", 12), bg=current_theme["bg"], 
                                            fg=current_theme["fg"])
svp_matrix_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# set default values
svp_b1x_entry.insert(0, "3")
svp_b1y_entry.insert(0, "0")
svp_b2x_entry.insert(0, "1")
svp_b2y_entry.insert(0, "2")

# action button
button_frame = ttk.Frame(tab_svp)
button_frame.pack(pady=10)
svp_button = ttk.Button(button_frame, text=get_text("solve_svp"), style='TButton', 
                       command=shortest_vector_problem)
svp_button.pack(side=tk.LEFT, padx=5)

# show result
svp_result_text = scrolledtext.ScrolledText(tab_svp, wrap=tk.WORD, width=80, height=10, 
                                           font=("Helvetica", 12), bg=current_theme["bg"], 
                                           fg=current_theme["fg"])
svp_result_text.pack(pady=10, fill=tk.BOTH, expand=True)

# ===============================
#   tab6: NTRU cryptosystem
# ===============================
tab_ntru = ttk.Frame(notebook)
notebook.add(tab_ntru, text=get_text("ntru_tab"))

# header
header_frame = ttk.Frame(tab_ntru, style='Header.TFrame')
header_frame.pack(fill=tk.X, pady=10)
header_label = ttk.Label(header_frame, text="NTRU Encryption", 
                         style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
header_label.pack(pady=10)

# input parameters
ntru_param_frame = ttk.Frame(tab_ntru)
ntru_param_frame.pack(pady=10)

ttk.Label(ntru_param_frame, text="N:").grid(row=0, column=0)
ntru_N_entry = ttk.Entry(ntru_param_frame, width=8)
ntru_N_entry.grid(row=0, column=1, padx=(0,20))

ttk.Label(ntru_param_frame, text="p:").grid(row=0, column=2)
ntru_p_entry = ttk.Entry(ntru_param_frame, width=8)
ntru_p_entry.grid(row=0, column=3, padx=(0,20))

ttk.Label(ntru_param_frame, text="q:").grid(row=0, column=4)
ntru_q_entry = ttk.Entry(ntru_param_frame, width=8)
ntru_q_entry.grid(row=0, column=5)

# set default values
ntru_N_entry.insert(0, "11")
ntru_p_entry.insert(0, "3")
ntru_q_entry.insert(0, "32")

# input message
ntru_message_frame = ttk.Frame(tab_ntru)
ntru_message_frame.pack(pady=10)
ttk.Label(ntru_message_frame, text=get_text("message")).pack(side=tk.LEFT)
ntru_message_entry = ttk.Entry(ntru_message_frame, width=40)
ntru_message_entry.pack(side=tk.LEFT, padx=5)

# action NTRU button
button_frame = ttk.Frame(tab_ntru)
button_frame.pack(pady=10)
ntru_button = ttk.Button(button_frame, text=get_text("run_ntru_demo"), style='TButton', 
                        command=run_ntru_demo)
ntru_button.pack(side=tk.LEFT, padx=5)

# show text output
ntru_output = scrolledtext.ScrolledText(tab_ntru, wrap=tk.WORD, width=80, height=10, 
                                       font=("Helvetica", 12), bg=current_theme["bg"], 
                                       fg=current_theme["fg"])
ntru_output.pack(pady=10, fill=tk.BOTH, expand=True)

# ===============================
# tab7: CTF
# ===============================
tab_ctf = ttk.Frame(notebook)
notebook.add(tab_ctf, text=get_text("ctf_challenge_tab"))

# header
ctf_header_frame = ttk.Frame(tab_ctf, style='Header.TFrame')
ctf_header_frame.pack(fill=tk.X, pady=10)
ctf_header_label = ttk.Label(ctf_header_frame, text=get_text("ctf_challenge_tab"),
                             style='Accent.TLabel', font=('Helvetica', 14, 'bold'))
ctf_header_label.pack(pady=10)

# input frame
ctf_input_frame = ttk.Frame(tab_ctf)
ctf_input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
ctf_basis_input_label = ttk.Label(ctf_input_frame, text=get_text("ctf_basis_input"))
ctf_basis_input_label.pack(anchor=tk.W)

ctf_basis_input_text = scrolledtext.ScrolledText(ctf_input_frame, wrap=tk.WORD, width=80, height=10,
                                                 font=("Helvetica", 12), bg=current_theme["bg"],
                                                 fg=current_theme["fg"])
ctf_basis_input_text.pack(fill=tk.BOTH, expand=True, pady=5)

# answer button
ctf_button_frame = ttk.Frame(tab_ctf)
ctf_button_frame.pack(pady=5)
ctf_solve_button = ttk.Button(ctf_button_frame, text=get_text("ctf_decode"), style='Neon.TButton',
                              command=lambda: ctf_output_text.config(state='normal') or ctf_output_text.delete("1.0", tk.END) or ctf_output_text.insert(tk.END, solve_lattice_ctf()) or ctf_output_text.config(state='disabled'))
ctf_solve_button.pack(pady=5)

# show result
ctf_output_frame = ttk.Frame(tab_ctf)
ctf_output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
ctf_result_label = ttk.Label(ctf_output_frame, text=get_text("ctf_result"))
ctf_result_label.pack(anchor=tk.W)
ctf_output_text = scrolledtext.ScrolledText(ctf_output_frame, wrap=tk.WORD, width=80, height=8,
                                            font=("Helvetica", 12), bg=current_theme["bg"],
                                            fg=current_theme["fg"])
ctf_output_text.pack(fill=tk.BOTH, expand=True)
ctf_output_text.config(state='disabled')

# -------------------------------
# main loop
# -------------------------------
apply_style()
root.mainloop()
