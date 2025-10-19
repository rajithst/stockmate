import pytest
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase

from app.util.map_model import map_model


class TestMapModel:
    """Test suite for map_model utility function."""

    class Base(DeclarativeBase):
        pass

    class MockSQLAlchemyModel(Base):
        """Mock SQLAlchemy model for testing."""

        __tablename__ = "mock_table"

        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        price = Column(Float)
        description = Column(String(200))

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = "Original Name"
            self.price = 100.0
            self.description = "Original Description"

    @pytest.fixture
    def target_model(self):
        """Fixture providing a fresh SQLAlchemy model instance."""
        return self.MockSQLAlchemyModel()

    def test_map_model_basic_mapping(self, target_model):
        """Test basic field mapping functionality."""

        # Arrange
        class SourceModel(BaseModel):
            name: str = "New Name"
            price: float = 150.0

        source = SourceModel()

        # Act
        result = map_model(target_model, source)

        # Assert
        assert result.name == "New Name"
        assert result.price == 150.0
        assert result.description == "Original Description"  # Unchanged

    def test_map_model_only_existing_attributes(self, target_model):
        """Test that only existing attributes on target are updated."""

        # Arrange
        class SourceWithExtraFields(BaseModel):
            name: str = "Updated Name"
            price: float = 200.0
            nonexistent_field: str = "Should not map"
            another_extra: int = 999

        source = SourceWithExtraFields()

        # Act
        result = map_model(target_model, source)

        # Assert
        assert result.name == "Updated Name"
        assert result.price == 200.0
        assert not hasattr(result, "nonexistent_field")
        assert not hasattr(result, "another_extra")

    def test_map_model_with_none_values(self, target_model):
        """Test mapping with None values."""

        # Arrange
        class SourceWithNone(BaseModel):
            name: str | None = None
            price: float | None = None

        source = SourceWithNone()

        # Act
        result = map_model(target_model, source)

        # Assert
        assert result.name is None
        assert result.price is None
        assert result.description == "Original Description"

    def test_map_model_partial_update(self, target_model):
        """Test updating only some fields."""

        # Arrange
        class PartialSource(BaseModel):
            name: str = "Only Name Updated"

        source = PartialSource()

        # Act
        result = map_model(target_model, source)

        # Assert
        assert result.name == "Only Name Updated"
        assert result.price == 100.0  # Original value
        assert result.description == "Original Description"  # Original value

    def test_map_model_type_conversion(self, target_model):
        """Test mapping with type conversion."""

        # Arrange
        class SourceWithDifferentTypes(BaseModel):
            price: str = "299.99"  # String instead of float

        source = SourceWithDifferentTypes()
        result = map_model(target_model, source)

        # Assert
        assert isinstance(result.price, str)  # Value is mapped as string
        assert result.price == "299.99"
        # Original fields remain unchanged
        assert result.name == "Original Name"
        assert result.description == "Original Description"

    def test_map_model_invalid_target(self):
        """Test mapping with invalid target model."""

        # Arrange
        class NotASQLAlchemyModel:
            def __init__(self):
                self.name = "test"

        class SimpleSource(BaseModel):
            name: str = "test"

        target = NotASQLAlchemyModel()
        source = SimpleSource()

        # Act & Assert
        with pytest.raises(TypeError) as exc_info:
            map_model(target, source)

        assert str(exc_info.value) == "Target must be a SQLAlchemy model instance"
