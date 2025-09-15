"""
Validation utilities for the Secretaria El Cano application.

This module provides validation functions for common data types
used throughout the application.
"""

import re
from typing import List, Optional
from datetime import datetime, date
from constants.messages import Messages


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool = True, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str) -> None:
        """Add an error to the validation result."""
        self.errors.append(error)
        self.is_valid = False


class Validators:
    """Collection of validation functions."""
    
    @staticmethod
    def validate_dni(dni: str) -> ValidationResult:
        """
        Validate Spanish DNI format.
        
        Args:
            dni: DNI string to validate.
            
        Returns:
            ValidationResult with validation status and errors.
        """
        result = ValidationResult()
        
        if not dni or not dni.strip():
            result.add_error(Messages.VALIDATION_DNI_INVALID)
            return result
        
        dni = dni.strip().upper()
        
        # Check format: 8 digits + 1 letter
        if len(dni) != 9 or not dni[:8].isdigit() or not dni[8].isalpha():
            result.add_error(Messages.VALIDATION_DNI_INVALID)
            return result
        
        # Validate check letter
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        number = int(dni[:8])
        expected_letter = letters[number % 23]
        
        if dni[8] != expected_letter:
            result.add_error("El DNI no tiene la letra de control correcta.")
        
        return result
    
    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """
        Validate email format.
        
        Args:
            email: Email string to validate.
            
        Returns:
            ValidationResult with validation status and errors.
        """
        result = ValidationResult()
        
        if not email or not email.strip():
            result.add_error(Messages.VALIDATION_EMAIL_INVALID)
            return result
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            result.add_error(Messages.VALIDATION_EMAIL_INVALID)
        
        return result
    
    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> ValidationResult:
        """
        Validate password strength.
        
        Args:
            password: Password to validate.
            min_length: Minimum required length.
            
        Returns:
            ValidationResult with validation status and errors.
        """
        result = ValidationResult()
        
        if not password:
            result.add_error(Messages.VALIDATION_PASSWORD_MIN_LENGTH)
            return result
        
        if len(password) < min_length:
            result.add_error(f"La contraseña debe tener al menos {min_length} caracteres.")
        
        return result
    
    @staticmethod
    def validate_name(name: str, field_name: str = "nombre") -> ValidationResult:
        """
        Validate name field.
        
        Args:
            name: Name to validate.
            field_name: Name of the field being validated.
            
        Returns:
            ValidationResult with validation status and errors.
        """
        result = ValidationResult()
        
        if not name or not name.strip():
            if field_name == "nombre":
                result.add_error(Messages.VALIDATION_NAME_REQUIRED)
            elif field_name == "apellidos":
                result.add_error(Messages.VALIDATION_SURNAME_REQUIRED)
            else:
                result.add_error(f"El campo {field_name} es obligatorio.")
        
        return result
    
    @staticmethod
    def validate_birth_date(birth_date: date) -> ValidationResult:
        """
        Validate birth date.
        
        Args:
            birth_date: Date of birth to validate.
            
        Returns:
            ValidationResult with validation status and errors.
        """
        result = ValidationResult()
        
        if not birth_date:
            result.add_error("La fecha de nacimiento es obligatoria.")
            return result
        
        today = date.today()
        if birth_date > today:
            result.add_error("La fecha de nacimiento no puede ser futura.")
        
        # Check minimum age (e.g., 0 years)
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 0:
            result.add_error("La fecha de nacimiento no es válida.")
        
        # Check maximum age (e.g., 120 years)
        if age > 120:
            result.add_error("La fecha de nacimiento no es realista.")
        
        return result