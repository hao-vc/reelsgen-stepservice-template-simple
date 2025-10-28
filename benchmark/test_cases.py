"""
Benchmark test cases configuration for FastAPI microservice.
"""
from typing import List, Dict, Any


def get_test_cases() -> List[Dict[str, Any]]:
    """Get all benchmark test cases."""
    return [
        # Health Check Tests
        {
            "name": "Health Check",
            "endpoint": "/health",
            "method": "GET",
            "headers": {},
            "expected_status": 200,
            "description": "Test basic health check endpoint"
        },
        
        # Operations Tests
        {
            "name": "Operations Process - Basic",
            "endpoint": "/operations/process",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook_url": "https://test.example.com/webhook",
                "data": {
                    "input": "test data"
                }
            },
            "expected_status": 202,
            "description": "Test basic operation processing"
        },
        
        {
            "name": "Operations Process - Complex Data",
            "endpoint": "/operations/process",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook_url": "https://test.example.com/webhook",
                "data": {
                    "input": "complex test data with special characters: !@#$%^&*()",
                    "metadata": {
                        "source": "benchmark",
                        "timestamp": "2024-01-15T10:30:00Z"
                    }
                }
            },
            "expected_status": 202,
            "description": "Test operation processing with complex data"
        },
        
        # Step Call Tests
        {
            "name": "Step Call - Video Processing",
            "endpoint": "/step/call",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "step": {
                    "id": "550e8400-e29b-41d4-a716-446655440000"
                },
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "video_url": "https://example.com/video.mp4",
                        "duration": 120,
                        "quality": "1080p",
                        "format": "mp4"
                    }
                },
                "variables": {
                    "timeout": 300,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test step call for video processing"
        },
        
        {
            "name": "Step Call - Audio Processing",
            "endpoint": "/step/call",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "step": {
                    "id": "550e8400-e29b-41d4-a716-446655440001"
                },
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "audio_url": "https://example.com/audio.mp3",
                        "duration": 60,
                        "quality": "high",
                        "format": "mp3"
                    }
                },
                "variables": {
                    "bitrate": 320,
                    "sample_rate": 44100
                }
            },
            "expected_status": 202,
            "description": "Test step call for audio processing"
        },
        
        # Example Endpoint Tests
        {
            "name": "Example Process Text - Uppercase",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "hello world",
                        "operation": "uppercase",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 30,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test text processing - uppercase operation"
        },
        
        {
            "name": "Example Process Text - Lowercase",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "HELLO WORLD",
                        "operation": "lowercase",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 30,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test text processing - lowercase operation"
        },
        
        {
            "name": "Example Process Text - Reverse",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "Hello World",
                        "operation": "reverse",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 30,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test text processing - reverse operation"
        },
        
        {
            "name": "Example Process Text - Complex",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "This is a complex text with multiple words and special characters: !@#$%^&*()",
                        "operation": "uppercase",
                        "language": "en",
                        "format": "plain",
                        "encoding": "utf-8",
                        "max_length": 1000,
                        "preserve_spaces": True,
                        "remove_punctuation": False,
                        "add_timestamp": True,
                        "custom_delimiter": " ",
                        "metadata": {
                            "source": "benchmark",
                            "version": "1.0",
                            "user_id": "benchmark-user"
                        }
                    }
                },
                "variables": {
                    "timeout": 60,
                    "retry_count": 5
                }
            },
            "expected_status": 202,
            "description": "Test text processing with all optional parameters"
        },
        
        # Error Cases
        {
            "name": "Operations Process - No Auth",
            "endpoint": "/operations/process",
            "method": "POST",
            "headers": {},
            "body": {
                "webhook_url": "https://test.example.com/webhook",
                "data": {
                    "input": "test data"
                }
            },
            "expected_status": 401,
            "description": "Test operation processing without authentication"
        },
        
        {
            "name": "Operations Process - Invalid Auth",
            "endpoint": "/operations/process",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer invalid-token"
            },
            "body": {
                "webhook_url": "https://test.example.com/webhook",
                "data": {
                    "input": "test data"
                }
            },
            "expected_status": 401,
            "description": "Test operation processing with invalid authentication"
        },
        
        {
            "name": "Operations Process - Missing Webhook",
            "endpoint": "/operations/process",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "data": {
                    "input": "test data"
                }
            },
            "expected_status": 422,
            "description": "Test operation processing without webhook URL"
        },
        
        {
            "name": "Example Process Text - Missing Text",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "operation": "uppercase"
                    }
                }
            },
            "expected_status": 422,
            "description": "Test text processing without text input"
        },
        
        {
            "name": "Non-existent Endpoint",
            "endpoint": "/non-existent",
            "method": "GET",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "expected_status": 404,
            "description": "Test non-existent endpoint"
        }
    ]


def get_custom_test_cases() -> List[Dict[str, Any]]:
    """Get custom test cases for specific scenarios."""
    return [
        # Performance Tests
        {
            "name": "Performance Test - Large Text",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "Lorem ipsum " * 1000,  # Large text
                        "operation": "uppercase",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 60,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test performance with large text input"
        },
        
        # Edge Cases
        {
            "name": "Edge Case - Empty Text",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "",
                        "operation": "uppercase",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 30,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test edge case with empty text"
        },
        
        {
            "name": "Edge Case - Special Characters Only",
            "endpoint": "/example/process-text",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "webhook": {
                    "url": "https://test.example.com/webhook"
                },
                "initial": {
                    "input": {
                        "text": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
                        "operation": "uppercase",
                        "language": "en",
                        "format": "plain"
                    }
                },
                "variables": {
                    "timeout": 30,
                    "retry_count": 3
                }
            },
            "expected_status": 202,
            "description": "Test edge case with special characters only"
        }
    ]


def get_all_test_cases() -> List[Dict[str, Any]]:
    """Get all test cases including custom ones."""
    return get_test_cases() + get_custom_test_cases()


def get_test_cases_by_category(category: str) -> List[Dict[str, Any]]:
    """Get test cases by category."""
    all_cases = get_all_test_cases()
    
    if category == "health":
        return [case for case in all_cases if "health" in case["name"].lower()]
    elif category == "operations":
        return [case for case in all_cases if "operations" in case["name"].lower()]
    elif category == "step":
        return [case for case in all_cases if "step" in case["name"].lower()]
    elif category == "example":
        return [case for case in all_cases if "example" in case["name"].lower()]
    elif category == "errors":
        return [case for case in all_cases if case["expected_status"] >= 400]
    elif category == "performance":
        return [case for case in all_cases if "performance" in case["name"].lower()]
    elif category == "edge":
        return [case for case in all_cases if "edge" in case["name"].lower()]
    else:
        return all_cases


if __name__ == "__main__":
    # Example usage
    cases = get_all_test_cases()
    print(f"Total test cases: {len(cases)}")
    
    # Print categories
    categories = ["health", "operations", "step", "example", "errors", "performance", "edge"]
    for category in categories:
        category_cases = get_test_cases_by_category(category)
        print(f"{category.capitalize()} tests: {len(category_cases)}")
