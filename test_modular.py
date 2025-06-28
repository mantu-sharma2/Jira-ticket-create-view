#!/usr/bin/env python3
"""
Test script for modular Jira Ticket Manager
Verifies that all modules can be imported and basic functionality works
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported successfully"""
    logger.info("Testing module imports...")
    
    try:
        # Test core modules
        import helpers
        logger.info("✓ helpers module imported successfully")
        
        import validation
        logger.info("✓ validation module imported successfully")
        
        import jira_service
        logger.info("✓ jira_service module imported successfully")
        
        import controllers
        logger.info("✓ controllers module imported successfully")
        
        import routes
        logger.info("✓ routes module imported successfully")
        
        import app
        logger.info("✓ app module imported successfully")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error during import: {e}")
        return False

def test_helpers():
    """Test helper functions"""
    logger.info("Testing helper functions...")
    
    try:
        from helpers import (
            generate_preview_id, generate_operation_id,
            validate_file_extension, format_timestamp,
            create_success_response, create_error_response
        )
        
        # Test ID generation
        preview_id = generate_preview_id()
        operation_id = generate_operation_id()
        assert len(preview_id) > 0
        assert len(operation_id) > 0
        logger.info("✓ ID generation works")
        
        # Test file extension validation
        assert validate_file_extension("test.xlsx") == True
        assert validate_file_extension("test.xls") == True
        assert validate_file_extension("test.txt") == False
        logger.info("✓ File extension validation works")
        
        # Test response formatting
        success_resp = create_success_response({"test": "data"})
        error_resp = create_error_response("Test error")
        
        assert success_resp["success"] == True
        assert error_resp["success"] == False
        logger.info("✓ Response formatting works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Helper functions test failed: {e}")
        return False

def test_validation():
    """Test validation functions"""
    logger.info("Testing validation functions...")
    
    try:
        from validation import (
            validate_filename, validate_project_key,
            validate_assignee, validate_labels
        )
        
        # Test filename validation
        assert validate_filename("test.xlsx")[0] == True
        assert validate_filename("")[0] == False
        logger.info("✓ Filename validation works")
        
        # Test project key validation
        assert validate_project_key("PROJ")[0] == True
        assert validate_project_key("P")[0] == False  # Too short
        logger.info("✓ Project key validation works")
        
        # Test assignee validation
        assert validate_assignee("john.doe")[0] == True
        assert validate_assignee("")[0] == True  # Optional field
        logger.info("✓ Assignee validation works")
        
        # Test labels validation
        assert validate_labels("frontend,urgent")[0] == True
        assert validate_labels("")[0] == True  # Optional field
        logger.info("✓ Labels validation works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Validation functions test failed: {e}")
        return False

def test_controllers():
    """Test controller initialization"""
    logger.info("Testing controller initialization...")
    
    try:
        from controllers import (
            get_file_upload_controller,
            get_ticket_creation_controller,
            get_ticket_search_controller
        )
        
        # Test controller instantiation
        file_controller = get_file_upload_controller()
        ticket_controller = get_ticket_creation_controller()
        search_controller = get_ticket_search_controller()
        
        assert file_controller is not None
        assert ticket_controller is not None
        assert search_controller is not None
        logger.info("✓ Controllers initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Controller initialization test failed: {e}")
        return False

def test_jira_service():
    """Test Jira service initialization"""
    logger.info("Testing Jira service initialization...")
    
    try:
        from jira_service import get_jira_service, validate_jira_config
        
        # Test service initialization (may fail if config is not set)
        service = get_jira_service()
        if service is None:
            logger.warning("⚠ Jira service not initialized (config not set)")
        else:
            logger.info("✓ Jira service initialized successfully")
        
        # Test config validation
        is_valid, message = validate_jira_config()
        logger.info(f"Config validation: {is_valid} - {message}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Jira service test failed: {e}")
        return False

def test_app_creation():
    """Test Flask app creation"""
    logger.info("Testing Flask app creation...")
    
    try:
        from app import create_app
        
        # Test app creation
        app = create_app()
        assert app is not None
        logger.info("✓ Flask app created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Flask app creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting modular architecture tests...")
    logger.info("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Helper Functions", test_helpers),
        ("Validation Functions", test_validation),
        ("Controller Initialization", test_controllers),
        ("Jira Service", test_jira_service),
        ("Flask App Creation", test_app_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name} test...")
        try:
            if test_func():
                passed += 1
                logger.info(f"✓ {test_name} test PASSED")
            else:
                logger.error(f"✗ {test_name} test FAILED")
        except Exception as e:
            logger.error(f"✗ {test_name} test FAILED with exception: {e}")
    
    logger.info("=" * 50)
    logger.info(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Modular architecture is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 