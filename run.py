import os
import subprocess
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
\033[1;36m======================================================================
     _  _                         ___      _            _   _          
    | \| |_____ _  _ _  _ ___    | _ \ ___| |_ ___ _ _ | |_(_)___ _ _  
    | .` / -_) \ / || | (_-<     |   // -_)  _/ -_) ' \|  _| / _ \ ' \ 
    |_|\_\___/_\_\\\\_,_/ /__/     |_|_\\\\___|\\__\\___|_||_|\\__|_\\___/_||_|
                                                                       
        🎯 EdTech SaaS Churn Risk & Agentic Retention Platform
======================================================================\033[0m
"""
    print(banner)

def run_command(command, description, wait_for_exit=True):
    print(f"\n\033[1;33m[*] {description}...\033[0m")
    print(f"\033[90mExecuting: {command}\033[0m")
    
    # Run the subprocess
    if wait_for_exit:
        try:
            result = subprocess.run(command, shell=True, check=True)
            if result.returncode == 0:
                print(f"\033[1;32m[✓] Completed successfully.\033[0m")
                return True
        except subprocess.CalledProcessError as err:
            print(f"\033[1;31m[✗] Error occurred: {err}\033[0m")
            return False
    else:
        # Long running processes like Streamlit or FastAPI
        try:
            process = subprocess.Popen(command, shell=True)
            print(f"\033[1;32m[✓] Process started in background (PID: {process.pid}).\033[0m")
            return process
        except Exception as err:
            print(f"\033[1;31m[✗] Failed to launch: {err}\033[0m")
            return None

def main():
    while True:
        clear_screen()
        print_banner()
        print("\033[1;35mSelect a pipeline operation to execute:\033[0m\n")
        print("  \033[1;32m[1]\033[0m Run Classic Batch Pipeline")
        print("      \033[90m(Generates baseline data -> Trains XGBoost -> Launches Classic Dashboard)\033[0m\n")
        print("  \033[1;32m[2]\033[0m Run Advanced MAARS Pipeline")
        print("      \033[90m(Generates telemetry DB -> Trains advanced XGBoost -> Launches Command Center)\033[0m\n")
        print("  \033[1;32m[3]\033[0m Launch Live Streaming RAG Simulator")
        print("      \033[90m(Launches interactive event streaming dashboard)\033[0m\n")
        print("  \033[1;32m[4]\033[0m Launch FastAPI Event Ingestion Server")
        print("      \033[90m(Launches real-time inference API endpoint on port 8000)\033[0m\n")
        print("  \033[1;31m[5]\033[0m Exit")
        
        choice = input("\n\033[1;36mEnter choice (1-5): \033[0m").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            print("\033[1;34m--- Running Classic Batch Pipeline ---\033[0m")
            if run_command("python data_generation/generate_users.py", "1. Generating synthetic users"):
                if run_command("python data_generation/generate_usage_events.py", "2. Generating daily usage event logs"):
                    if run_command("python src/models/train_xgboost.py", "3. Training classic XGBoost classifier & SHAP explainer"):
                        run_command("streamlit run app.py", "4. Launching Streamlit Executive Dashboard", wait_for_exit=False)
                        time.sleep(3)
            input("\nPress Enter to return to main menu...")
            
        elif choice == '2':
            clear_screen()
            print_banner()
            print("\033[1;34m--- Running Advanced MAARS Pipeline ---\033[0m")
            if run_command("python src/data/generate_telemetry.py", "1. Generating advanced event-level telemetry database"):
                if run_command("python src/models/train_advanced_xgboost.py", "2. Training advanced XGBoost with behavior velocity & SHAP"):
                    run_command("streamlit run src/app/main.py", "3. Launching MAARS Command Center Dashboard", wait_for_exit=False)
                    time.sleep(3)
            input("\nPress Enter to return to main menu...")
            
        elif choice == '3':
            clear_screen()
            print_banner()
            print("\033[1;34m--- Launching Live Streaming RAG Simulator ---\033[0m")
            run_command("streamlit run src/app/live_dashboard.py", "Launching Streaming Intervention Dashboard", wait_for_exit=False)
            time.sleep(3)
            input("\nPress Enter to return to main menu...")
            
        elif choice == '4':
            clear_screen()
            print_banner()
            print("\033[1;34m--- Launching FastAPI Event Ingestion Server ---\033[0m")
            run_command("python src/api/server.py", "Launching FastAPI Server on http://localhost:8000", wait_for_exit=False)
            time.sleep(3)
            input("\nPress Enter to return to main menu...")
            
        elif choice == '5':
            print("\n\033[1;32mThank you for using Nexus Retention Intelligence. Good luck with your interviews!\033[0m")
            break
        else:
            print("\n\033[1;31m[!] Invalid choice. Please select between 1 and 5.\033[0m")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
