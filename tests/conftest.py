"""
Basic test configuration for the Secretaria El Cano application.
"""

import pytest
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def test_db_url():
    """Provide a test database URL."""
    return "sqlite:///:memory:"

@pytest.fixture
def sample_fallero_data():
    """Provide sample fallero data for testing."""
    return {
        "nombre": "Juan",
        "apellidos": "García López",
        "dni": "12345678A",
        "fecha_nacimiento": "1990-01-01"
    }

@pytest.fixture
def sample_usuario_data():
    """Provide sample usuario data for testing."""
    return {
        "nombre": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }