import json
import os
import argparse
from collections import defaultdict

def deduplicate_prioritized_tests(input_file="ai_model/data/prioritized_tests.json", 
                                 output_file=None,
                                 backup_original=True):
    """
    Remove duplicates from prioritized tests and keep the highest risk score for each unique endpoint
    
    Args:
        input_file (str): Path to the input prioritized tests file
        output_file (str): Path to save the deduplicated tests (defaults to input_file)
        backup_original (bool): Whether to create a backup of the original file
    """
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return None
    
    # Set output file to input file if not specified
    if output_file is None:
        output_file = input_file
    
    print(f"🔍 Deduplicating prioritized tests from: {input_file}")
    
    # Create backup if requested
    if backup_original and input_file == output_file:
        backup_file = f"{input_file}.backup"
        try:
            with open(input_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"💾 Backup created: {backup_file}")
        except Exception as e:
            print(f"⚠️  Failed to create backup: {e}")
    
    # Load the prioritized tests
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            tests = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in input file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading input file: {e}")
        return None
    
    print(f"📊 Original prioritized tests: {len(tests)}")
    
    # Analyze duplicates before deduplication
    endpoint_counts = defaultdict(int)
    for test in tests:
        key = f"{test['method']}_{test['url']}"
        endpoint_counts[key] += 1
    
    duplicate_endpoints = {k: v for k, v in endpoint_counts.items() if v > 1}
    total_duplicates = sum(v - 1 for v in duplicate_endpoints.values())
    
    print(f"🔍 Found {len(duplicate_endpoints)} endpoints with duplicates")
    print(f"📈 Total duplicate entries: {total_duplicates}")
    
    # Show top 5 most duplicated endpoints
    if duplicate_endpoints:
        print("\n🔝 Top 5 most duplicated endpoints:")
        sorted_duplicates = sorted(duplicate_endpoints.items(), key=lambda x: x[1], reverse=True)
        for i, (endpoint, count) in enumerate(sorted_duplicates[:5], 1):
            method, url = endpoint.split('_', 1)
            print(f"  {i}. {method} {url} ({count} occurrences)")
    
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
    
    print(f"\n✅ Deduplication results:")
    print(f"  - Original tests: {len(tests)}")
    print(f"  - Deduplicated tests: {len(deduplicated_tests)}")
    print(f"  - Duplicates removed: {len(tests) - len(deduplicated_tests)}")
    print(f"  - Reduction: {((len(tests) - len(deduplicated_tests)) / len(tests) * 100):.1f}%")
    
    # Show risk score distribution
    if deduplicated_tests:
        risk_scores = [test['risk_score'] for test in deduplicated_tests]
        print(f"\n📊 Risk score distribution:")
        print(f"  - Highest risk score: {max(risk_scores):.6f}")
        print(f"  - Lowest risk score: {min(risk_scores):.6f}")
        print(f"  - Average risk score: {sum(risk_scores) / len(risk_scores):.6f}")
    
    # Save the deduplicated tests
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(deduplicated_tests, f, indent=2)
        print(f"💾 Deduplicated tests saved to: {output_file}")
    except Exception as e:
        print(f"❌ Error saving output file: {e}")
        return None
    
    return deduplicated_tests

def analyze_test_distribution(tests):
    """Analyze the distribution of test methods and URL patterns"""
    if not tests:
        return
    
    print(f"\n📈 Test distribution analysis:")
    
    # Method distribution
    method_counts = defaultdict(int)
    for test in tests:
        method_counts[test['method']] += 1
    
    print(f"  HTTP Methods:")
    for method, count in sorted(method_counts.items()):
        percentage = (count / len(tests)) * 100
        print(f"    {method}: {count} ({percentage:.1f}%)")
    
    # URL pattern analysis
    url_patterns = defaultdict(int)
    for test in tests:
        # Extract base path (remove parameters)
        url = test['url']
        if '/v1.5/' in url:
            base_path = url.split('/v1.5/')[1].split('/')[0]
            url_patterns[base_path] += 1
    
    print(f"  Top URL patterns:")
    sorted_patterns = sorted(url_patterns.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_patterns[:10]:
        percentage = (count / len(tests)) * 100
        print(f"    {pattern}: {count} ({percentage:.1f}%)")

def main():
    parser = argparse.ArgumentParser(description='Deduplicate prioritized test cases')
    parser.add_argument('--input', '-i', 
                       default='ai_model/data/prioritized_tests.json',
                       help='Input file path (default: ai_model/data/prioritized_tests.json)')
    parser.add_argument('--output', '-o',
                       help='Output file path (default: overwrite input file)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backup of original file')
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='Analyze test distribution after deduplication')
    
    args = parser.parse_args()
    
    print("🚀 Prioritized Tests Deduplication Tool")
    print("=" * 50)
    
    # Run deduplication
    deduplicated_tests = deduplicate_prioritized_tests(
        input_file=args.input,
        output_file=args.output,
        backup_original=not args.no_backup
    )
    
    if deduplicated_tests and args.analyze:
        analyze_test_distribution(deduplicated_tests)
    
    print(f"\n🎉 Deduplication complete!")

if __name__ == "__main__":
    main() 