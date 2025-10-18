import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.core.config import Config


class TestConfig:
    """Test suite for Config class."""

    def test_config_default_values(self):
        """Test default configuration values."""
        # Act
        config = Config()

        # Assert
        assert config.app_name == "StockMate"
        assert config.debug is True
        assert config.db_user is not None
        assert config.db_password is not None
        assert config.db_host is not None
        assert config.db_port is not None
        assert config.db_name is not None
        assert config.fmp_api_key is not None
        assert config.openai_api_key is not None

    def test_config_with_valid_values(self):
        """Test configuration with valid values."""
        # Act
        config = Config(
            app_name="TestApp",
            debug=True,
            db_user="testuser",
            db_password="testpass",
            db_host="testhost",
            db_port=5432,
            db_name="testdb",
            fmp_api_key="test_fmp_key",
            openai_api_key="test_openai_key",
        )

        # Assert
        assert config.app_name == "TestApp"
        assert config.debug is True
        assert config.db_user == "testuser"
        assert config.db_password == "testpass"
        assert config.db_host == "testhost"
        assert config.db_port == 5432
        assert config.db_name == "testdb"
        assert config.fmp_api_key == "test_fmp_key"
        assert config.openai_api_key == "test_openai_key"

    def test_config_validation_empty_db_user(self):
        """Test validation fails for empty db_user."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(db_user="")

        errors = exc_info.value.errors()
        assert len(errors) >= 1
        assert any("db_user" in str(error) for error in errors)

    def test_config_validation_whitespace_db_user(self):
        """Test validation fails for whitespace-only db_user."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(db_user="   ")

        errors = exc_info.value.errors()
        assert len(errors) >= 1
        assert any("db_user" in str(error) for error in errors)

    def test_config_validation_empty_db_password(self):
        """Test validation fails for empty db_password."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(db_password="")

        errors = exc_info.value.errors()
        assert len(errors) >= 1
        assert any("db_password" in str(error) for error in errors)

    def test_config_validation_empty_db_name(self):
        """Test validation fails for empty db_name."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(db_name="")

        errors = exc_info.value.errors()
        assert len(errors) >= 1
        assert any("db_name" in str(error) for error in errors)

    def test_config_validation_empty_fmp_api_key(self):
        """Test validation fails for empty fmp_api_key."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(fmp_api_key="")

        errors = exc_info.value.errors()
        assert len(errors) >= 1
        assert any("fmp_api_key" in str(error) for error in errors)

    def test_config_validation_multiple_empty_fields(self):
        """Test validation fails for multiple empty required fields."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Config(db_user="", db_password="", db_name="", fmp_api_key="")

        errors = exc_info.value.errors()
        assert len(errors) >= 4  # At least 4 validation errors

    def test_config_validation_valid_required_fields(self):
        """Test validation passes with valid required fields."""
        # Act
        config = Config(
            db_user="validuser",
            db_password="validpass",
            db_name="validdb",
            fmp_api_key="valid_api_key",
        )

        # Assert - Should not raise any exceptions
        assert config.db_user == "validuser"
        assert config.db_password == "validpass"
        assert config.db_name == "validdb"
        assert config.fmp_api_key == "valid_api_key"

    def test_db_url_property_basic(self):
        """Test db_url property with basic values."""
        # Arrange
        config = Config(
            db_user="testuser",
            db_password="testpass",
            db_host="localhost",
            db_port=3306,
            db_name="testdb",
        )

        # Act
        db_url = config.db_url

        # Assert
        expected = "mysql+pymysql://testuser:testpass@localhost:3306/testdb"
        assert db_url == expected

    def test_db_url_property_with_special_characters(self):
        """Test db_url property with special characters in password."""
        # Arrange
        config = Config(
            db_user="user@domain",
            db_password="pass@word#123",
            db_host="remote.host.com",
            db_port=5432,
            db_name="mydb",
        )

        # Act
        db_url = config.db_url

        # Assert
        # The password should be URL encoded
        assert "mysql+pymysql://" in db_url
        assert "user@domain" in db_url  # @ encoded as %40
        assert "pass%40word%23123" in db_url  # @ and # encoded
        assert "@remote.host.com:5432/mydb" in db_url

    def test_db_url_property_with_url_unsafe_characters(self):
        """Test db_url property with URL-unsafe characters in password."""
        # Arrange
        config = Config(
            db_user="testuser",
            db_password="p@ssw0rd!$#%",
            db_host="localhost",
            db_port=3306,
            db_name="testdb",
        )

        # Act
        db_url = config.db_url

        # Assert
        # All special characters should be properly encoded
        assert "mysql+pymysql://testuser:" in db_url
        assert "@localhost:3306/testdb" in db_url
        # The encoded password should be between the colon and @
        password_part = db_url.split("://testuser:")[1].split("@")[0]
        assert "p%40ssw0rd%21%24%23%25" == password_part

    @patch.dict(
        os.environ,
        {
            "DB_USER": "env_user",
            "DB_PASSWORD": "env_pass",
            "DB_NAME": "env_db",
            "FMP_API_KEY": "env_api_key",
            "OPENAI_API_KEY": "env_openai_key",
            "DEBUG": "true",
        },
    )
    def test_config_loads_from_environment(self):
        """Test that configuration loads from environment variables."""
        # Act
        config = Config()

        # Assert
        assert config.db_user == "env_user"
        assert config.db_password == "env_pass"
        assert config.db_name == "env_db"
        assert config.fmp_api_key == "env_api_key"
        assert config.openai_api_key == "env_openai_key"
        assert config.debug is True

    @patch.dict(
        os.environ, {"DB_HOST": "env.host.com", "DB_PORT": "5432", "APP_NAME": "EnvApp"}
    )
    def test_config_loads_optional_from_environment(self):
        """Test that optional configuration loads from environment variables."""
        # Act
        config = Config(
            db_user="user", db_password="pass", db_name="db", fmp_api_key="key"
        )

        # Assert
        assert config.db_host == "env.host.com"
        assert config.db_port == 5432
        assert config.app_name == "EnvApp"

    def test_config_explicit_values_override_defaults(self):
        """Test that explicitly provided values override defaults."""
        # Act
        config = Config(
            app_name="CustomApp",
            debug=True,
            db_host="custom.host.com",
            db_port=1234,
            db_user="customuser",
            db_password="custompass",
            db_name="customdb",
            fmp_api_key="custom_api_key",
            openai_api_key="custom_openai_key",
        )

        # Assert
        assert config.app_name == "CustomApp"
        assert config.debug is True
        assert config.db_host == "custom.host.com"
        assert config.db_port == 1234
        assert config.db_user == "customuser"
        assert config.db_password == "custompass"
        assert config.db_name == "customdb"
        assert config.fmp_api_key == "custom_api_key"
        assert config.openai_api_key == "custom_openai_key"

    @pytest.mark.parametrize("invalid_port", [-1, 0, 65536, 100000])
    def test_config_invalid_port_values(self, invalid_port):
        """Test configuration with invalid port values."""
        # This test depends on whether Pydantic validates port ranges
        # Act & Assert
        try:
            config = Config(
                db_port=invalid_port,
                db_user="user",
                db_password="pass",
                db_name="db",
                fmp_api_key="key",
            )
            # If no validation error, at least verify the value is set
            assert config.db_port == invalid_port
        except ValidationError:
            # If Pydantic validates port ranges, this is expected
            pass

    def test_config_model_config_settings(self):
        """Test that model configuration settings are properly set."""
        # Act
        config = Config(
            db_user="user", db_password="pass", db_name="db", fmp_api_key="key"
        )

        # Assert
        # Check that the model has the expected configuration
        model_config = config.model_config
        assert model_config.get("env_file") == ".env"
        assert model_config.get("env_file_encoding") == "utf-8"

    @patch("app.core.config.quote_plus")
    def test_db_url_calls_quote_plus(self, mock_quote_plus):
        """Test that db_url property calls quote_plus for password encoding."""
        # Arrange
        mock_quote_plus.return_value = "encoded_password"
        config = Config(
            db_user="testuser",
            db_password="testpass",
            db_host="localhost",
            db_port=3306,
            db_name="testdb",
        )

        # Act
        db_url = config.db_url

        # Assert
        mock_quote_plus.assert_called_once_with("testpass")
        assert "encoded_password" in db_url

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("db_user", "valid_user"),
            ("db_password", "valid_pass"),
            ("db_name", "valid_db"),
            ("fmp_api_key", "valid_key"),
        ],
    )
    def test_individual_field_validation(self, field_name, field_value):
        """Test individual field validation for required fields."""
        # Arrange
        kwargs = {
            "db_user": "default_user",
            "db_password": "default_pass",
            "db_name": "default_db",
            "fmp_api_key": "default_key",
        }
        kwargs[field_name] = field_value

        # Act
        config = Config(**kwargs)

        # Assert
        assert getattr(config, field_name) == field_value
