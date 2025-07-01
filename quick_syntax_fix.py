#!/usr/bin/env python3
"""
Quick fix for the remaining 3 syntax errors.
"""

import os

def fix_syntax_error():
    """Fix the remaining syntax errors."""
    
    # Fix 1: transaction_capture_transaction_transactionId.py - line 309
    file1 = 'generated_python_tests/test_POST _transaction_capture_transaction_transactionId.py'
    if os.path.exists(file1):
        with open(file1, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the 4-quote issue
        content = content.replace('"""Verify whether the capture transaction is successful when authorization process ends with "Bearer Token""""', 
                                '"""Verify whether the capture transaction is successful when authorization process ends with "Bearer Token"""')
        
        with open(file1, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed transaction_capture_transaction_transactionId.py")
    
    # Fix 2: transaction_refund_transaction_transactionId.py - line 214
    file2 = 'generated_python_tests/test_POST _transaction_refund_transaction_transactionId.py'
    if os.path.exists(file2):
        with open(file2, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the problematic line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '"""Verify whether the refund is successful when request was sent with API key' in line and line.count('"') > 6:
                lines[i] = line.replace('""""', '"""')
                break
        
        content = '\n'.join(lines)
        with open(file2, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed transaction_refund_transaction_transactionId.py")
    
    # Fix 3: transaction_void_transaction_transactionId.py - line 138
    file3 = 'generated_python_tests/test_POST _transaction_void_transaction_transactionId.py'
    if os.path.exists(file3):
        with open(file3, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the problematic line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '"""Verify whether the void is successful when request was sent with API key' in line and line.count('"') > 6:
                lines[i] = line.replace('""""', '"""')
                break
        
        content = '\n'.join(lines)
        with open(file3, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed transaction_void_transaction_transactionId.py")

if __name__ == "__main__":
    print("🔧 Quick fixing remaining syntax errors...")
    fix_syntax_error()
    print("✅ All syntax errors fixed!") 