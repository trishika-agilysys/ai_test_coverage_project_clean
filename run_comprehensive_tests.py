#!/usr/bin/env python3
"""
Comprehensive Test Generation Script
===================================

This script runs the comprehensive test generation pipeline:
1. Generate comprehensive English test cases from Swagger
2. Generate comprehensive Python test files
3. Generate a detailed report

Usage:
    python run_comprehensive_tests.py [--swagger path/to/swagger.json]
"""

import subprocess
import sys
import os
import json
import argparse

def run_step(command, description):
    """Run a command and handle errors gracefully."""
    try:
        print(f"[RUN] Running: {description}...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed with error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"[ERROR] {description} failed with unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run comprehensive test generation pipeline')
    parser.add_argument('--swagger', default='data/raw/swagger_fixed.json',
                      help='Path to the Swagger specification file')
    args = parser.parse_args()

    print("=" * 60)
    print("COMPREHENSIVE TEST GENERATION PIPELINE")
    print("=" * 60)
    print(f"[LOAD] Using Swagger file: {args.swagger}")

    # Step 1: Generate comprehensive English test cases
    print(f"\n[STEP1] Step 1: Generating comprehensive English test cases...")
    success = run_step(
        f'python comprehensive_test_generator.py --swagger "{args.swagger}"',
        "Comprehensive English test case generation"
    )
    
    if not success:
        print("[FAIL] Comprehensive test generation failed. Exiting.")
        return

    # Step 2: Generate summary report
    print(f"\n[STEP2] Step 2: Generating summary report...")
    run_step(
        'python generate_summary_report.py',
        "Summary report generation"
    )

    print(f"\n[SUCCESS] COMPREHENSIVE TEST GENERATION COMPLETE!")
    print("=" * 60)
    
    # Show final summary
    print(f"\n[INFO] Generated files:")
    print(f"  • data/processed/comprehensive_test_cases.json")
    print(f"  • comprehensive_test_summary.md")
    
    print(f"\n[STATS] QUICK STATS:")
    try:
        with open('data/processed/comprehensive_test_cases.json', 'r') as f:
            data = json.load(f)
            total_endpoints = len(data)
            total_scenarios = sum(len(endpoint_data.get('test_cases', [])) for endpoint_data in data.values())
            print(f"  • Total Endpoints: {total_endpoints}")
            print(f"  • Total Test Scenarios: {total_scenarios}")
            print(f"  • Average Scenarios per Endpoint: {total_scenarios/total_endpoints:.1f}")
    except Exception as e:
        print(f"  [ERROR] Could not load statistics: {e}")
    
    print("\n[INFO] Next steps:")
    print("  1. Review generated test cases in data/processed/comprehensive_test_cases.json")
    print("  2. Run individual test scenarios as needed")
    print("  3. Use the summary report for analysis")

if __name__ == "__main__":
    main()
    sys.exit(0) 