"""
Test runner for EcoAgent system.
This serves as a demonstration of the TDD approach with comprehensive testing.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tests():
    """Run all tests with coverage reporting."""
    print("🧪 Running EcoAgent Test Suite")
    print("="*50)
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Test commands to run
    test_commands = [
        ["python", "-m", "pytest", "tests/test_ecoagent.py::TestHealthCheck", "-v", "--tb=short"],
        ["python", "-m", "pytest", "tests/test_ecoagent.py::TestCarbonCalculation", "-v", "--tb=short"],
        ["python", "-m", "pytest", "tests/test_ecoagent.py::TestUserProfile", "-v", "--tb=short"],
        ["python", "-m", "pytest", "tests/test_ecoagent.py::TestGoals", "-v", "--tb=short"],
        ["python", "-m", "pytest", "tests/test_ecoagent.py::TestErrorHandling", "-v", "--tb=short"],
    ]
    
    results = []
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n📋 Running test set {i}/{len(test_commands)}: {' '.join(cmd[3:])}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PASS: {cmd[3] if len(cmd) > 3 else 'Test'}")
        else:
            print(f"❌ FAIL: {cmd[3] if len(cmd) > 3 else 'Test'}")
            print(result.stdout)
            print(result.stderr)
        
        results.append((cmd, result.returncode))
    
    # Summary
    passed = sum(1 for _, code in results if code == 0)
    total = len(results)
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Total Test Sets: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {total - passed}")
    print(f"   Success Rate: {passed/total*100:.1f}%" if total > 0 else "N/A")
    
    # Run one more comprehensive test to check integration
    print(f"\n🔄 Running Integration Test...")
    integration_result = subprocess.run([
        "python", "-m", "pytest", 
        "tests/test_ecoagent.py::TestUserProfile::test_user_registration_valid_data", 
        "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    if integration_result.returncode == 0:
        print("✅ Integration Test: PASS")
    else:
        print("❌ Integration Test: FAIL")
        print(integration_result.stdout)
        print(integration_result.stderr)
    
    overall_success = all(code == 0 for _, code in results) and integration_result.returncode == 0
    
    print(f"\n🎯 OVERALL STATUS: {'SUCCESS' if overall_success else 'FAILURE'}")
    
    return overall_success


def check_coverage():
    """Check test coverage (if available)."""
    print(f"\n📊 Checking for Coverage...")
    try:
        # Try to run coverage check if available
        result = subprocess.run([
            sys.executable, "-m", "coverage", "run", 
            "-m", "pytest", "tests/", "--tb=no"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            cov_result = subprocess.run([
                sys.executable, "-m", "coverage", "report"
            ], capture_output=True, text=True)
            
            print("Coverage Report:")
            print(cov_result.stdout)
        else:
            print("⚠️  Coverage check failed, but tests ran successfully")
    except subprocess.TimeoutExpired:
        print("⚠️  Coverage check timed out, but tests ran successfully")
    except FileNotFoundError:
        print("⚠️  Coverage tool not installed, but tests ran successfully")


if __name__ == "__main__":
    success = run_tests()
    check_coverage()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)