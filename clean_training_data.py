#!/usr/bin/env python3
"""
Enhanced script to clean and improve the training data for better model performance.
"""

import json
import re
from pathlib import Path
from collections import Counter

def clean_training_data(input_file, output_file):
    """Clean the training data by removing problematic samples."""
    print(f"Cleaning training data from {input_file}...")
    
    cleaned_samples = []
    removed_samples = []
    duplicate_count = 0
    
    # Track patterns to identify repetitive content
    input_patterns = Counter()
    output_patterns = Counter()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                obj = json.loads(line)
                
                # Validate required fields
                if 'input' not in obj or 'output' not in obj:
                    removed_samples.append(f"Line {line_num}: Missing required fields")
                    continue
                
                input_text = obj['input'].strip()
                output_text = obj['output'].strip()
                
                # Check for empty content
                if not input_text or not output_text:
                    removed_samples.append(f"Line {line_num}: Empty input or output")
                    continue
                
                # Check for extremely short outputs
                if len(output_text) < 200:
                    removed_samples.append(f"Line {line_num}: Output too short ({len(output_text)} chars)")
                    continue
                
                # Check for extremely long outputs (likely corrupted)
                if len(output_text) > 10000:
                    removed_samples.append(f"Line {line_num}: Output too long ({len(output_text)} chars)")
                    continue
                
                # Check for sufficient test cases (at least 3 pm.test statements)
                test_case_count = output_text.count('pm.test')
                if test_case_count < 3:
                    removed_samples.append(f"Line {line_num}: Insufficient test cases ({test_case_count})")
                    continue
                
                # Check for incomplete JavaScript (missing closing braces)
                if not has_complete_js_structure(output_text):
                    removed_samples.append(f"Line {line_num}: Incomplete JavaScript structure")
                    continue
                
                # Check for repetitive patterns
                # if has_repetitive_patterns(output_text):
                #     removed_samples.append(f"Line {line_num}: Contains repetitive patterns")
                #     continue
                
                # Check for poor JavaScript structure
                if not has_proper_js_structure(output_text):
                    removed_samples.append(f"Line {line_num}: Poor JavaScript structure")
                    continue
                
                # Check for malformed outputs (like the ones in training log)
                if has_malformed_output(output_text):
                    removed_samples.append(f"Line {line_num}: Malformed output")
                    continue
                
                # Check for duplicate content
                input_hash = hash(input_text)
                output_hash = hash(output_text)
                
                if (input_hash, output_hash) in [(s.get('input_hash'), s.get('output_hash')) for s in cleaned_samples]:
                    duplicate_count += 1
                    removed_samples.append(f"Line {line_num}: Duplicate content")
                    continue
                
                # Track patterns for analysis
                input_patterns[input_text[:100]] += 1
                output_patterns[output_text[:200]] += 1
                
                # Clean up the output text
                cleaned_output = clean_output_text(output_text)
                
                # Create cleaned sample
                cleaned_sample = {
                    'input': input_text,
                    'output': cleaned_output,
                    'input_hash': input_hash,
                    'output_hash': output_hash
                }
                
                cleaned_samples.append(cleaned_sample)
                
            except Exception as e:
                removed_samples.append(f"Line {line_num}: JSON parsing error - {e}")
    
    # Remove samples with too many similar patterns
    final_samples = remove_similar_samples(cleaned_samples)
    
    # Save cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in final_samples:
            # Remove hash fields before saving
            clean_sample = {
                'input': sample['input'],
                'output': sample['output']
            }
            f.write(json.dumps(clean_sample, ensure_ascii=False) + '\n')
    
    print(f"✅ Cleaning completed!")
    print(f"📊 Original samples: {len(cleaned_samples) + len(removed_samples)}")
    print(f"✅ Cleaned samples: {len(final_samples)}")
    print(f"❌ Removed samples: {len(removed_samples)}")
    print(f"🔄 Duplicates removed: {duplicate_count}")
    print(f"📈 Similar samples removed: {len(cleaned_samples) - len(final_samples)}")
    
    if removed_samples:
        print(f"\n📋 Removed samples summary:")
        for i, reason in enumerate(removed_samples[:10]):
            print(f"  {reason}")
        if len(removed_samples) > 10:
            print(f"  ... and {len(removed_samples) - 10} more")
    
    return len(final_samples), len(removed_samples)

def has_complete_js_structure(text):
    """Check if text has complete JavaScript structure."""
    # Count opening and closing braces
    open_braces = text.count('{')
    close_braces = text.count('}')
    open_parens = text.count('(')
    close_parens = text.count(')')
    
    # Check for balanced braces and parentheses
    if abs(open_braces - close_braces) > 2:
        return False
    
    if abs(open_parens - close_parens) > 2:
        return False
    
    # Should end with proper closing
    if not text.strip().endswith(('}', '});', ');')):
        return False
    
    return True

def has_malformed_output(text):
    """Check for malformed outputs like those in the training log."""
    # Check for incomplete patterns like the ones in training log
    malformed_patterns = [
        r'\{payagent-url\}\}/.*?\{.*?\}\}',
        r'\{.*?\}\}.*?\{.*?\}\}',
        r'payagentUrl.*?\{.*?\}',
        r'Validate.*?\{.*?\}',
        r'Tip.*?\{.*?\}',
        r'No.*?\{.*?\}'
    ]
    
    for pattern in malformed_patterns:
        if re.search(pattern, text):
            return True
    
    # Check for incomplete sentences
    if re.search(r'[A-Z][a-z]+.*?\{.*?\}\}', text):
        return True
    
    return False

def has_repetitive_patterns(text):
    """Check if text contains repetitive patterns."""
    # Check for repeated phrases
    words = text.split()
    if len(words) < 10:
        return False
    
    # Check for excessive repetition of short phrases (be less strict)
    for i in range(len(words) - 4):
        phrase = ' '.join(words[i:i+4])
        if text.count(phrase) > 5:  # Increased threshold
            return True
    
    # Check for repeated test names (be less strict)
    test_names = re.findall(r'pm\.test\("([^"]+)"', text)
    if len(test_names) > 10 and len(test_names) != len(set(test_names)):
        # Only flag if there are many tests and some are duplicates
        return True
    
    # Check for excessive repetition of specific patterns
    patterns_to_check = [
        r'pm\.expect\([^)]+\)\.to\.have\.property\([^)]+\)',
        r'pm\.expect\([^)]+\)\.to\.be\.a\([^)]+\)',
        r'pm\.expect\([^)]+\)\.to\.not\.equal\([^)]+\)'
    ]
    
    for pattern in patterns_to_check:
        matches = re.findall(pattern, text)
        if len(matches) > 8:  # Allow more repetitions
            return True
    
    return False

def has_proper_js_structure(text):
    """Check if text has proper JavaScript structure."""
    # Should contain basic Postman test structure
    required_elements = [
        'pm.test',
        'pm.response',
        'pm.expect'
    ]
    
    for element in required_elements:
        if element not in text:
            return False
    
    # Should have proper function structure
    if 'function () {' not in text:
        return False
    
    # Should have proper test structure
    if not re.search(r'pm\.test\("[^"]+",\s*function\s*\(\)\s*\{', text):
        return False
    
    return True

def remove_similar_samples(samples, similarity_threshold=0.8):
    """Remove samples that are too similar to each other."""
    if len(samples) <= 1:
        return samples
    
    # Sort by output length (prefer longer, more complete samples)
    samples.sort(key=lambda x: len(x['output']), reverse=True)
    
    unique_samples = []
    for sample in samples:
        is_similar = False
        for unique_sample in unique_samples:
            similarity = calculate_similarity(sample['output'], unique_sample['output'])
            if similarity > similarity_threshold:
                is_similar = True
                break
        
        if not is_similar:
            unique_samples.append(sample)
    
    return unique_samples

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts."""
    # Simple word-based similarity
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def clean_output_text(text):
    """Clean up the output text."""
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Ensure proper spacing around pm.test
    text = re.sub(r'pm\.test\s*\(', 'pm.test(', text)
    
    # Fix common spacing issues
    text = re.sub(r'\)\s*{', ') {', text)
    text = re.sub(r'}\s*;', '};', text)
    
    # Fix common typos
    text = re.sub(r'etnryMode', 'entryMode', text)
    text = re.sub(r'contactlessChip', 'contactless', text)
    
    # Remove trailing whitespace
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    return text.strip()

def main():
    """Main function to clean training data."""
    input_file = "augmented_postman_tests_for_training.merged_cleaned.jsonl"
    output_file = "augmented_postman_tests_for_training.cleaned_improved.jsonl"
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    cleaned_count, removed_count = clean_training_data(input_file, output_file)
    
    if cleaned_count > 0:
        print(f"\n🎉 Successfully created cleaned training data: {output_file}")
        print(f"📈 Quality improvement: {removed_count} problematic samples removed")
        print(f"✅ Ready for training with {cleaned_count} high-quality samples")
        
        # Provide recommendations
        print(f"\n💡 Recommendations for better training:")
        print(f"  1. Consider increasing the minimum test case count if model still generates incomplete outputs")
        print(f"  2. Add more diverse input patterns to reduce overfitting")
        print(f"  3. Consider using a larger model or longer training time")
        print(f"  4. Implement early stopping based on validation loss")
    else:
        print(f"\n❌ No valid samples found. Please check your training data.")

if __name__ == "__main__":
    main() 