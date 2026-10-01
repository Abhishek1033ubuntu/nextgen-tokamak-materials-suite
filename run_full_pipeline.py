import os
import json
from modules.phase1_divertor_rhea import run_phase1_screening

def main():
    print("==========================================================")
    print(" SUBATOMIC TOKAMAK MATERIALS SUITE - EXECUTION PIPELINE   ")
    print("==========================================================")
    
    reports_dir = "./reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Run Modules
    p1_results = run_phase1_screening(reports_dir)
    
    print("\n[+] Full Pipeline Execution Completed!")
    print(f"[+] All reports successfully generated in '{reports_dir}/'")

if __name__ == "__main__":
    main()
