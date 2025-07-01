import subprocess
import os
import sys
import json
import pandas as pd
from collections import defaultdict

def deduplicate_prioritized_tests(prioritized_file="ai_model/data/prioritized_tests.json"):
    """Remove duplicates from prioritized tests and keep the highest risk score for each unique endpoint"""
    print("Deduplicating prioritized tests...")
    
    if not os.path.exists(prioritized_file):
        print("WARNING: Prioritized tests file not found, skipping deduplication")
        return
    
    # Load the prioritized tests
    with open(prioritized_file, 'r', encoding='utf-8') as f:
        tests = json.load(f)
    
    print(f"Original prioritized tests: {len(tests)}")
    
    # Create a dictionary to store unique endpoints with highest risk scores
    unique_tests = {}
    
    for test in tests:
        # Create a unique key based on method and URL
        key = f"{test['method']}_{test['url']}"
        
        # Keep the test with the highest risk score
        if key not in unique_tests or test['risk_score'] > unique_tests[key]['risk_score']:
            unique_tests[key] = test
    
    # Convert back to list
    deduplicated_tests = list(unique_tests.values())
    
    # Sort by risk score (highest first)
    deduplicated_tests.sort(key=lambda x: x['risk_score'], reverse=True)
    
    print(f"Deduplicated tests: {len(deduplicated_tests)} (removed {len(tests) - len(deduplicated_tests)} duplicates)")
    
    # Save the deduplicated tests
    with open(prioritized_file, 'w', encoding='utf-8') as f:
        json.dump(deduplicated_tests, f, indent=2)
    
    return deduplicated_tests

def run_command_with_error_handling(command, description):
    """Run a command with proper error handling"""
    try:
        print(f"Running: {description}...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError as e:
        print(f"ERROR: {description} failed - file not found: {e}")
        return False

def main():
    print("[START] Starting COMPREHENSIVE AI Test Coverage Pipeline")
    print("=" * 70)
    
    NUM_CYCLES = 1  # Number of full pipeline cycles
    
    for cycle in range(NUM_CYCLES):
        print(f"\n=== Pipeline Cycle {cycle+1} ===")
        
        # Step 1: Generate COMPREHENSIVE English test cases from Swagger
        print("\n[STEP1] Step 1: Generating COMPREHENSIVE English test cases from Swagger...")
        if not run_command_with_error_handling(
            [sys.executable, "comprehensive_test_generator.py"],
            "Comprehensive English test case generation"
        ):
            print("WARNING: Trying basic English test generation as fallback...")
            run_command_with_error_handling(
                [sys.executable, "generate_english_tests.py"],
                "Basic English test case generation"
            )
        
        # Step 2: Deduplicate prioritized tests
        print("\n[STEP2] Step 2: Deduplicating prioritized tests...")
        deduplicated_tests = deduplicate_prioritized_tests()
        
        # Step 3: Generate test cases using AI Test Generator
        print("\n[STEP3] Step 3: Generating AI test cases...")
        prioritized_path = "ai_model/data/prioritized_tests.json"
        if os.path.exists(prioritized_path) and deduplicated_tests:
            print(f"Using {len(deduplicated_tests)} deduplicated prioritized tests...")
            if not run_command_with_error_handling(
                [sys.executable, "-m", "ai_test_generator.run_ai_generator", "--prioritized"],
                "Prioritized test case generation"
            ):
                print("WARNING: Trying full test generation instead...")
                run_command_with_error_handling(
                    [sys.executable, "-m", "ai_test_generator.run_ai_generator"],
                    "Full test case generation"
                )
        else:
            print("No prioritized tests found, generating all test cases...")
            run_command_with_error_handling(
                [sys.executable, "-m", "ai_test_generator.run_ai_generator"],
                "Full test case generation"
            )
        
        # Step 4: Run the generated test cases
        print("\n[STEP4] Step 4: Running test cases...")
        if not run_command_with_error_handling(
            [sys.executable, "test_case_generator/run_tests.py"],
            "Test execution"
        ):
            print("WARNING: Test execution failed, but continuing with pipeline")
        
        # Step 5: Analyze test execution logs
        print("\n[STEP5] Step 5: Analyzing test execution logs...")
        if not run_command_with_error_handling(
            [sys.executable, "ai_model/analyze_logs.py"],
            "Log analysis"
        ):
            print("WARNING: Log analysis failed, but continuing with pipeline")
        
        # Step 6: Prepare training data for CodeT5 fine-tuning
        print("\n[STEP6] Step 6: Preparing training data for CodeT5...")
        if not run_command_with_error_handling(
            [sys.executable, "src/data/prepare_training_data.py"],
            "Training data preparation"
        ):
            print("WARNING: Training data preparation failed, but continuing with pipeline")
        
        # Step 7: Fine-tune CodeT5 model
        print("\n[STEP7] Step 7: Fine-tuning CodeT5 model...")
        if not run_command_with_error_handling(
            [sys.executable, "ai_model/fine_tune_codet5.py"],
            "CodeT5 fine-tuning"
        ):
            print("WARNING: CodeT5 fine-tuning failed, but continuing with pipeline")
        
        # Step 8: Generate COMPREHENSIVE Python tests from English descriptions
        print("\n[STEP8] Step 8: Generating COMPREHENSIVE Python tests from English descriptions...")
        if not run_command_with_error_handling(
            [sys.executable, "comprehensive_python_test_generator.py"],
            "Comprehensive Python test generation from English"
        ):
            print("WARNING: Trying basic Python test generation as fallback...")
            run_command_with_error_handling(
                [sys.executable, "generate_improved_python_tests.py"],
                "Basic Python test generation from English"
            )
        
        # Step 9: Train XGBoost model for test prioritization
        print("\n[STEP9] Step 9: Training XGBoost model for test prioritization...")
        if not run_command_with_error_handling(
            [sys.executable, "ai_model/train_model.py"],
            "XGBoost model training"
        ):
            print("WARNING: XGBoost training failed, but continuing with pipeline")
        
        # Step 10: Generate comprehensive test report
        print("\n[STEP10] Step 10: Generating comprehensive test report...")
        generate_comprehensive_test_report()
    
    print("\n[SUCCESS] COMPREHENSIVE PIPELINE COMPLETE!")
    print("Check the following directories for outputs:")
    print("  [FILE] data/processed/comprehensive_test_cases.json (Comprehensive English test descriptions)")
    print("  [FILE] data/processed/english_test_cases.json (Basic English test descriptions)")
    print("  [PYTHON] comprehensive_python_tests/ (Comprehensive Python test files)")
    print("  [PYTHON] improved_python_tests/ (Basic Python test files)")
    print("  [AI] src/tests/generated/ (AI-generated test files)")
    print("  [PRIORITY] ai_model/data/prioritized_tests.json (Deduplicated prioritized tests)")

def generate_comprehensive_test_report():
    """Generate a comprehensive test report including both basic and comprehensive test data"""
    try:
        report = {
            "pipeline_summary": {
                "timestamp": pd.Timestamp.now().isoformat(),
                "total_endpoints_processed": 0,
                "comprehensive_test_scenarios_generated": 0,
                "basic_english_test_cases_generated": 0,
                "comprehensive_python_test_files_generated": 0,
                "basic_python_test_files_generated": 0,
                "prioritized_tests_count": 0
            },
            "file_locations": {
                "comprehensive_english_test_cases": "data/processed/comprehensive_test_cases.json",
                "basic_english_test_cases": "data/processed/english_test_cases.json",
                "comprehensive_python_tests": "comprehensive_python_tests/",
                "basic_python_tests": "improved_python_tests/",
                "ai_generated_tests": "src/tests/generated/",
                "prioritized_tests": "ai_model/data/prioritized_tests.json"
            },
            "test_coverage_analysis": {
                "scenario_types": [],
                "security_tests": 0,
                "performance_tests": 0,
                "parameter_tests": 0
            }
        }
        
        # Count comprehensive test cases
        if os.path.exists("data/processed/comprehensive_test_cases.json"):
            with open("data/processed/comprehensive_test_cases.json", 'r') as f:
                comprehensive_data = json.load(f)
                report["pipeline_summary"]["total_endpoints_processed"] = len(comprehensive_data)
                
                total_scenarios = 0
                scenario_types = set()
                security_tests = 0
                performance_tests = 0
                parameter_tests = 0
                
                for endpoint, data in comprehensive_data.items():
                    scenarios = data.get('test_cases', [])
                    total_scenarios += len(scenarios)
                    
                    for scenario in scenarios:
                        scenario_type = scenario.get('scenario_type', 'unknown')
                        scenario_types.add(scenario_type)
                        
                        if 'security' in scenario_type or scenario.get('security_test'):
                            security_tests += 1
                        elif 'performance' in scenario_type or scenario.get('performance_test'):
                            performance_tests += 1
                        elif 'parameter' in scenario_type or scenario.get('params'):
                            parameter_tests += 1
                
                report["pipeline_summary"]["comprehensive_test_scenarios_generated"] = total_scenarios
                report["test_coverage_analysis"]["scenario_types"] = list(scenario_types)
                report["test_coverage_analysis"]["security_tests"] = security_tests
                report["test_coverage_analysis"]["performance_tests"] = performance_tests
                report["test_coverage_analysis"]["parameter_tests"] = parameter_tests
        
        # Count basic English test cases (fallback)
        if os.path.exists("data/processed/english_test_cases.json"):
            with open("data/processed/english_test_cases.json", 'r') as f:
                basic_data = json.load(f)
                report["pipeline_summary"]["basic_english_test_cases_generated"] = sum(
                    len(data['test_cases']) for data in basic_data.values()
                )
        
        # Count comprehensive Python test files
        if os.path.exists("comprehensive_python_tests"):
            comprehensive_python_files = [f for f in os.listdir("comprehensive_python_tests") if f.endswith('.py')]
            report["pipeline_summary"]["comprehensive_python_test_files_generated"] = len(comprehensive_python_files)
        
        # Count basic Python test files
        if os.path.exists("improved_python_tests"):
            basic_python_files = [f for f in os.listdir("improved_python_tests") if f.endswith('.py')]
            report["pipeline_summary"]["basic_python_test_files_generated"] = len(basic_python_files)
        
        # Count prioritized tests
        if os.path.exists("ai_model/data/prioritized_tests.json"):
            with open("ai_model/data/prioritized_tests.json", 'r') as f:
                prioritized_data = json.load(f)
                report["pipeline_summary"]["prioritized_tests_count"] = len(prioritized_data)
        
        # Save report
        with open("comprehensive_pipeline_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("[SUCCESS] SUCCESS: Comprehensive test report generated: comprehensive_pipeline_report.json")
        
        # Print summary
        print(f"\n[STATS] COMPREHENSIVE TEST GENERATION SUMMARY:")
        print(f"   • Total Endpoints: {report['pipeline_summary']['total_endpoints_processed']}")
        print(f"   • Comprehensive Test Scenarios: {report['pipeline_summary']['comprehensive_test_scenarios_generated']}")
        print(f"   • Security Tests: {report['test_coverage_analysis']['security_tests']}")
        print(f"   • Performance Tests: {report['test_coverage_analysis']['performance_tests']}")
        print(f"   • Parameter Tests: {report['test_coverage_analysis']['parameter_tests']}")
        print(f"   • Comprehensive Python Files: {report['pipeline_summary']['comprehensive_python_test_files_generated']}")
        print(f"   • Scenario Types: {', '.join(report['test_coverage_analysis']['scenario_types'][:5])}...")
        
    except Exception as e:
        print(f"[WARNING] WARNING: Failed to generate comprehensive test report: {e}")

if __name__ == "__main__":
    main() 