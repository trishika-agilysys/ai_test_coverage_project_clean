#!/usr/bin/env python3
"""
Analyze and fix training data for CodeT5 model.
This script identifies issues with the current training data and creates a better dataset.
"""

import json
import re
from collections import Counter
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_training_data(file_path: str) -> Dict[str, Any]:
    """Analyze the current training data and identify issues."""
    logger.info(f"Analyzing training data from: {file_path}")
    
    samples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    sample = json.loads(line)
                    samples.append(sample)
                except json.JSONDecodeError as e:
                    logger.warning(f"Line {line_num}: JSON decode error: {e}")
    
    logger.info(f"Loaded {len(samples)} samples")
    
    # Analyze input patterns
    input_patterns = []
    endpoint_patterns = []
    for sample in samples:
        input_text = sample.get('input', '')
        input_patterns.append(input_text)
        
        # Extract endpoint pattern
        if 'POST' in input_text:
            endpoint_match = re.search(r'POST\s+([^\s]+)', input_text)
            if endpoint_match:
                endpoint_patterns.append(endpoint_match.group(1))
    
    # Analyze output patterns
    output_lengths = [len(sample.get('output', '')) for sample in samples]
    output_patterns = []
    
    for sample in samples:
        output_text = sample.get('output', '')
        # Extract common patterns
        if 'pm.test(' in output_text:
            test_count = output_text.count('pm.test(')
            output_patterns.append(f"{test_count} tests")
    
    # Find unique inputs
    unique_inputs = set(input_patterns)
    unique_endpoints = set(endpoint_patterns)
    
    analysis = {
        'total_samples': len(samples),
        'unique_inputs': len(unique_inputs),
        'unique_endpoints': len(unique_endpoints),
        'input_repetition_rate': (len(samples) - len(unique_inputs)) / len(samples) * 100,
        'output_length_stats': {
            'min': min(output_lengths),
            'max': max(output_lengths),
            'avg': sum(output_lengths) / len(output_lengths),
            'median': sorted(output_lengths)[len(output_lengths)//2]
        },
        'common_patterns': Counter(output_patterns).most_common(5),
        'endpoint_distribution': Counter(endpoint_patterns).most_common(5),
        'issues': []
    }
    
    # Identify specific issues
    if analysis['input_repetition_rate'] > 50:
        analysis['issues'].append(f"High input repetition: {analysis['input_repetition_rate']:.1f}%")
    
    if analysis['unique_endpoints'] < 5:
        analysis['issues'].append(f"Too few unique endpoints: {analysis['unique_endpoints']}")
    
    if analysis['output_length_stats']['avg'] > 1000:
        analysis['issues'].append(f"Outputs too long: avg {analysis['output_length_stats']['avg']:.0f} chars")
    
    if analysis['output_length_stats']['max'] > 2000:
        analysis['issues'].append(f"Some outputs extremely long: max {analysis['output_length_stats']['max']} chars")
    
    return analysis

def create_diverse_training_data() -> List[Dict[str, str]]:
    """Create a more diverse and balanced training dataset."""
    logger.info("Creating diverse training dataset...")
    
    # Define different API patterns and test scenarios
    api_patterns = [
        # Different HTTP methods
        {
            'input': 'Generate Postman JavaScript tests for: GET /api/users - Validate successful user list retrieval',
            'output': '''pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is an array", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('array');
});

pm.test("Each user has required fields", function () {
    const responseData = pm.response.json();
    responseData.forEach(user => {
        pm.expect(user).to.have.property('id').and.to.be.a('number');
        pm.expect(user).to.have.property('name').and.to.be.a('string');
        pm.expect(user).to.have.property('email').and.to.be.a('string');
    });
});'''
        },
        {
            'input': 'Generate Postman JavaScript tests for: POST /api/users - Validate successful user creation',
            'output': '''pm.test("Response status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response contains created user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('id').and.to.be.a('number');
    pm.expect(responseData).to.have.property('name').and.to.be.a('string');
    pm.expect(responseData).to.have.property('email').and.to.be.a('string');
    pm.expect(responseData).to.have.property('createdAt').and.to.be.a('string');
});

pm.test("User ID is positive integer", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.id).to.be.a('number').and.to.be.above(0);
});'''
        },
        {
            'input': 'Generate Postman JavaScript tests for: PUT /api/users/123 - Validate successful user update',
            'output': '''pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains updated user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('id').and.to.equal(123);
    pm.expect(responseData).to.have.property('name').and.to.be.a('string');
    pm.expect(responseData).to.have.property('email').and.to.be.a('string');
    pm.expect(responseData).to.have.property('updatedAt').and.to.be.a('string');
});

pm.test("Updated timestamp is recent", function () {
    const responseData = pm.response.json();
    const updatedAt = new Date(responseData.updatedAt);
    const now = new Date();
    pm.expect(now.getTime() - updatedAt.getTime()).to.be.lessThan(60000); // Within 1 minute
});'''
        },
        {
            'input': 'Generate Postman JavaScript tests for: DELETE /api/users/123 - Validate successful user deletion',
            'output': '''pm.test("Response status code is 204", function () {
    pm.response.to.have.status(204);
});

pm.test("Response body is empty", function () {
    pm.expect(pm.response.text()).to.be.empty;
});

pm.test("Response headers indicate no content", function () {
    pm.expect(pm.response.headers.get('Content-Length')).to.equal('0');
});'''
        },
        # Different data validation scenarios
        {
            'input': 'Generate Postman JavaScript tests for: GET /api/products - Validate product list with pagination',
            'output': '''pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has pagination structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('data').and.to.be.an('array');
    pm.expect(responseData).to.have.property('pagination');
    pm.expect(responseData.pagination).to.have.property('page').and.to.be.a('number');
    pm.expect(responseData.pagination).to.have.property('limit').and.to.be.a('number');
    pm.expect(responseData.pagination).to.have.property('total').and.to.be.a('number');
});

pm.test("Pagination values are valid", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.pagination.page).to.be.above(0);
    pm.expect(responseData.pagination.limit).to.be.above(0);
    pm.expect(responseData.pagination.total).to.be.at.least(0);
});'''
        },
        {
            'input': 'Generate Postman JavaScript tests for: POST /api/orders - Validate order creation with validation',
            'output': '''pm.test("Response status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Order has required fields", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('orderId').and.to.be.a('string');
    pm.expect(responseData).to.have.property('customerId').and.to.be.a('string');
    pm.expect(responseData).to.have.property('total').and.to.be.a('number');
    pm.expect(responseData).to.have.property('status').and.to.be.a('string');
});

pm.test("Order total is positive", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.total).to.be.above(0);
});

pm.test("Order status is valid", function () {
    const responseData = pm.response.json();
    const validStatuses = ['pending', 'confirmed', 'shipped', 'delivered'];
    pm.expect(validStatuses).to.include(responseData.status);
});'''
        },
        # Error handling scenarios
        {
            'input': 'Generate Postman JavaScript tests for: GET /api/users/999999 - Validate 404 error response',
            'output': '''pm.test("Response status code is 404", function () {
    pm.response.to.have.status(404);
});

pm.test("Error response has correct structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('error').and.to.be.a('string');
    pm.expect(responseData).to.have.property('message').and.to.be.a('string');
    pm.expect(responseData).to.have.property('statusCode').and.to.equal(404);
});

pm.test("Error message is descriptive", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.message).to.include('not found');
});'''
        },
        {
            'input': 'Generate Postman JavaScript tests for: POST /api/users - Validate 400 error for invalid data',
            'output': '''pm.test("Response status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error response contains validation details", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('error').and.to.equal('Validation Error');
    pm.expect(responseData).to.have.property('details').and.to.be.an('array');
});

pm.test("Validation details are specific", function () {
    const responseData = pm.response.json();
    responseData.details.forEach(detail => {
        pm.expect(detail).to.have.property('field').and.to.be.a('string');
        pm.expect(detail).to.have.property('message').and.to.be.a('string');
    });
});'''
        },
        # Authentication scenarios
        {
            'input': 'Generate Postman JavaScript tests for: GET /api/protected - Validate authentication required',
            'output': '''pm.test("Response status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Unauthorized response structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('error').and.to.equal('Unauthorized');
    pm.expect(responseData).to.have.property('message').and.to.include('authentication');
});

pm.test("Response includes auth header requirement", function () {
    pm.expect(pm.response.headers.get('WWW-Authenticate')).to.include('Bearer');
});'''
        },
        # Complex nested data scenarios
        {
            'input': 'Generate Postman JavaScript tests for: GET /api/orders/123 - Validate complex order details',
            'output': '''pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Order has complete structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('orderId').and.to.equal('123');
    pm.expect(responseData).to.have.property('customer').and.to.be.an('object');
    pm.expect(responseData).to.have.property('items').and.to.be.an('array');
    pm.expect(responseData).to.have.property('shipping').and.to.be.an('object');
});

pm.test("Customer information is complete", function () {
    const responseData = pm.response.json();
    const customer = responseData.customer;
    pm.expect(customer).to.have.property('id').and.to.be.a('string');
    pm.expect(customer).to.have.property('name').and.to.be.a('string');
    pm.expect(customer).to.have.property('email').and.to.be.a('string');
});

pm.test("Order items have required fields", function () {
    const responseData = pm.response.json();
    responseData.items.forEach(item => {
        pm.expect(item).to.have.property('productId').and.to.be.a('string');
        pm.expect(item).to.have.property('quantity').and.to.be.a('number');
        pm.expect(item).to.have.property('price').and.to.be.a('number');
    });
});'''
        }
    ]
    
    return api_patterns

def create_improved_training_data(output_file: str):
    """Create an improved training dataset and save it."""
    logger.info("Creating improved training dataset...")
    
    # Get diverse patterns
    diverse_data = create_diverse_training_data()
    
    # Add some variations to increase dataset size while maintaining quality
    variations = []
    
    # Create variations with different HTTP methods and endpoints
    base_patterns = [
        ('GET', '/api/customers', 'customer list'),
        ('POST', '/api/customers', 'customer creation'),
        ('PUT', '/api/customers/456', 'customer update'),
        ('DELETE', '/api/customers/456', 'customer deletion'),
        ('GET', '/api/products', 'product list'),
        ('POST', '/api/products', 'product creation'),
        ('GET', '/api/orders', 'order list'),
        ('POST', '/api/orders', 'order creation'),
        ('GET', '/api/invoices', 'invoice list'),
        ('POST', '/api/invoices', 'invoice creation')
    ]
    
    for method, endpoint, description in base_patterns:
        variations.append({
            'input': f'Generate Postman JavaScript tests for: {method} {endpoint} - Validate successful {description}',
            'output': f'''pm.test("Response status code is {200 if method != 'POST' else 201 if method == 'POST' else 204}", function () {{
    pm.response.to.have.status({200 if method != 'POST' else 201 if method == 'POST' else 204});
}});

pm.test("Response structure is valid", function () {{
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
}});

pm.test("Response contains expected data", function () {{
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('id').or.to.have.property('data');
}});'''
        })
    
    # Combine all data
    all_data = diverse_data + variations
    
    # Shuffle the data
    import random
    random.shuffle(all_data)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in all_data:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    logger.info(f"Created improved training dataset with {len(all_data)} samples")
    logger.info(f"Saved to: {output_file}")
    
    return all_data

def main():
    """Main function to analyze and fix training data."""
    input_file = "augmented_postman_tests_for_training.cleaned_no_prompt.jsonl"
    output_file = "improved_training_data.jsonl"
    
    # Analyze current data
    logger.info("=== CURRENT DATA ANALYSIS ===")
    analysis = analyze_training_data(input_file)
    
    print("\n" + "="*50)
    print("TRAINING DATA ANALYSIS RESULTS")
    print("="*50)
    print(f"Total samples: {analysis['total_samples']}")
    print(f"Unique inputs: {analysis['unique_inputs']}")
    print(f"Unique endpoints: {analysis['unique_endpoints']}")
    print(f"Input repetition rate: {analysis['input_repetition_rate']:.1f}%")
    print(f"\nOutput length statistics:")
    print(f"  Min: {analysis['output_length_stats']['min']}")
    print(f"  Max: {analysis['output_length_stats']['max']}")
    print(f"  Average: {analysis['output_length_stats']['avg']:.0f}")
    print(f"  Median: {analysis['output_length_stats']['median']}")
    
    print(f"\nMost common patterns:")
    for pattern, count in analysis['common_patterns']:
        print(f"  {pattern}: {count} times")
    
    print(f"\nEndpoint distribution:")
    for endpoint, count in analysis['endpoint_distribution']:
        print(f"  {endpoint}: {count} times")
    
    if analysis['issues']:
        print(f"\nISSUES IDENTIFIED:")
        for issue in analysis['issues']:
            print(f"  ❌ {issue}")
    else:
        print(f"\n✅ No major issues identified")
    
    # Create improved dataset
    logger.info("\n=== CREATING IMPROVED DATASET ===")
    improved_data = create_improved_training_data(output_file)
    
    # Analyze improved data
    logger.info("\n=== IMPROVED DATA ANALYSIS ===")
    improved_analysis = analyze_training_data(output_file)
    
    print("\n" + "="*50)
    print("IMPROVED DATA ANALYSIS RESULTS")
    print("="*50)
    print(f"Total samples: {improved_analysis['total_samples']}")
    print(f"Unique inputs: {improved_analysis['unique_inputs']}")
    print(f"Unique endpoints: {improved_analysis['unique_endpoints']}")
    print(f"Input repetition rate: {improved_analysis['input_repetition_rate']:.1f}%")
    print(f"\nOutput length statistics:")
    print(f"  Min: {improved_analysis['output_length_stats']['min']}")
    print(f"  Max: {improved_analysis['output_length_stats']['max']}")
    print(f"  Average: {improved_analysis['output_length_stats']['avg']:.0f}")
    print(f"  Median: {improved_analysis['output_length_stats']['median']}")
    
    print(f"\n✅ IMPROVEMENTS:")
    print(f"  • Reduced repetition from {analysis['input_repetition_rate']:.1f}% to {improved_analysis['input_repetition_rate']:.1f}%")
    print(f"  • Increased unique endpoints from {analysis['unique_endpoints']} to {improved_analysis['unique_endpoints']}")
    print(f"  • Reduced average output length from {analysis['output_length_stats']['avg']:.0f} to {improved_analysis['output_length_stats']['avg']:.0f} chars")
    print(f"  • Added diverse HTTP methods (GET, POST, PUT, DELETE)")
    print(f"  • Added error handling scenarios")
    print(f"  • Added authentication scenarios")
    print(f"  • Added pagination and complex data scenarios")
    
    print(f"\n📁 New training file created: {output_file}")
    print(f"💡 Update your train.py to use: {output_file}")

if __name__ == "__main__":
    main() 