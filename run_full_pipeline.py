import os
from modules.phase1_divertor_rhea import run_phase1_screening
from modules.phase2_structure_v4cr4ti import run_phase2_screening
from modules.phase3_breeder_pb17li import run_phase3_screening
from modules.phase4_magnets_rebco import run_phase4_screening
from modules.phase5_multiphysics_yield import run_phase5_multiphysics

def main():
    print("==========================================================")
    print(" NEXTGEN TOKAMAK MATERIALS SUITE - FULL SIMULATION RUN   ")
    print("==========================================================")
    
    reports_dir = "./reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    run_phase1_screening(reports_dir)
    run_phase2_screening(reports_dir)
    run_phase3_screening(reports_dir)
    run_phase4_screening(reports_dir)
    run_phase5_multiphysics(reports_dir)
    
    print("\n==========================================================")
    print(f"[+] All 5 Modules executed successfully!")
    print(f"[+] Artifacts and reports archived in: '{reports_dir}/'")
    print("==========================================================")

if __name__ == "__main__":
    main()
