import os
import sys
import time

# Konfigurasi Warna Terminal
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'

# ==========================================
# 0. SPLASH SCREEN & ANIMASI LOADING
# ==========================================
ASCII_ART = """
 █████╗ ██╗   ██╗████████╗ ██████╗ 
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
███████║██║   ██║   ██║   ██║   ██║
██╔══██║██║   ██║   ██║   ██║   ██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
                                   
 █████╗  ██████╗ ███████╗███╗   ██╗████████╗
██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   
██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   
██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
"""

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 66 # Lebar default aman untuk Termux HP

def print_logo():
    term_width = get_terminal_width()
    
    # Header Frame
    print(f"{CYAN}╔" + "═" * (term_width - 2) + f"╗{RESET}")
    
    # Print ASCII Art Centered
    for line in ASCII_ART.strip('\n').split('\n'):
        centered_line = line.center(term_width - 2)
        print(f"{CYAN}║{MAGENTA}{centered_line}{CYAN}║{RESET}")
        
    print(f"{CYAN}╠" + "═" * (term_width - 2) + f"╣{RESET}")
    
    # Copyright Centered
    copyright_text = "Created By Muzaqi Dev  |  Copyright 2026"
    print(f"{CYAN}║{YELLOW}{copyright_text.center(term_width - 2)}{CYAN}║{RESET}")
    
    # Footer Frame
    print(f"{CYAN}╚" + "═" * (term_width - 2) + f"╝{RESET}\n")

def show_splash_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_logo()
    print()

    tasks = [
        "Inisialisasi AI Core...",
        "Membuka jalur jaringan...",
        "Memuat modul memori...",
        "Menghubungkan API...",
        "Membangunkan entitas AI..."
    ]
    
    bar_length = 25
    # Animasi spinner modern
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(101):
        time.sleep(0.02) # Animasi dipercepat sedikit supaya lebih smooth
        task_idx = min(i // 20, len(tasks) - 1)
        current_task = tasks[task_idx]
        
        spinner = spinners[i % len(spinners)]
        filled = int(bar_length * i // 100)
        # Progress bar dengan balok solid dan transparan
        bar = '█' * filled + '▒' * (bar_length - filled)
        
        # Warna dinamis
        if i < 33: color = RED
        elif i < 66: color = YELLOW
        else: color = GREEN
        
        sys.stdout.write(f"\r\033[2K{MAGENTA}{spinner}{RESET} {CYAN}[{color}{bar}{CYAN}]{RESET} {color}{i:3}%{RESET} {WHITE}| {current_task:<25}{RESET}")
        sys.stdout.flush()
        
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()
    
    sys.stdout.write(f"\r\033[2K{GREEN}✔ SYSTEM READY. Welcome, Commander.{RESET}\n")
    sys.stdout.flush()
    time.sleep(1)
    
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()