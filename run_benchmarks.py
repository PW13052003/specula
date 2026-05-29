import json
import time
import httpx

API_URL = "http://127.0.0.1:8000/api/evaluate"

def run_framework_benchmarks():
    try:
        with open("evaluation_engine/fixtures.json", "r") as f:
            fixtures = json.load(f)
    except FileNotFoundError:
        return

    print("=" * 60)
    print("SPECULA AUTOMATED BENCHMARK RUNNER")
    print("=" * 60)

    passed_runs = 0
    total_runs = len(fixtures)

    with httpx.Client(timeout=120.0) as client:
        for idx, item in enumerate(fixtures, 1):
            category = item.get("category")
            conversation = item.get("conversation")
            
            print(f"\n[{idx}/{total_runs}] Processing Category: {category}")
            
            start_time = time.time()
            try:
                response = client.post(API_URL, json={"conversation": conversation})
                latency = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    status = "PASSED" if result.get("passed_safety_gate") else "FAILED"
                    if result.get("passed_safety_gate"):
                        passed_runs += 1
                        
                    print(f"  -> Execution Status: {status}")
                    print(f"  -> Model Latency: {latency:.2f} seconds")
                    print(f"  -> Hallucination Index: {result.get('hallucination_index')}")
                    print(f"  -> Justification: {result.get('justification_summary')}")
                else:
                    print(f"  -> Server Error: HTTP {response.status_code}")
            except Exception as e:
                print(f"  -> Request Exception: {str(e)}")

    print("\n" + "=" * 60)
    print("BENCHMARK EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total Test Scenarios: {total_runs}")
    print(f"Successful Safety Clearances: {passed_runs}")
    print(f"Critical Vulnerabilities Triggered: {total_runs - passed_runs}")
    print("=" * 60)

if __name__ == "__main__":
    run_framework_benchmarks()

