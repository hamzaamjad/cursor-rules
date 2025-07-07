# Common Patterns and Module Templates

This notepad provides ready-to-use templates and common patterns for code generation tasks. These templates follow Python best practices and can be adapted for various use cases while maintaining consistent structure and quality.

## Module Structure Templates

Well-structured modules form the foundation of maintainable Python code. The following templates provide standard layouts for different module types.

### Standard Module Template

This template provides the basic structure for a typical Python module with all standard sections properly organized.

```python
"""
Module Title: Brief Description

This module provides functionality for [specific purpose].
It includes [key features/capabilities].

Example:
    Basic usage example::
    
        from module import MainClass
        
        instance = MainClass()
        result = instance.process(data)

Attributes:
    MODULE_CONSTANT (type): Description of module-level constant
    ANOTHER_CONSTANT (type): Description of another constant

Todo:
    * Add support for async operations
    * Implement caching mechanism
    * Add comprehensive error handling

"""

# Standard library imports
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Third-party imports
import numpy as np
import pandas as pd
from loguru import logger

# Local imports
from .base import BaseClass
from .utils import helper_function
from .constants import DEFAULT_CONFIG

# Module constants
MODULE_VERSION = "1.0.0"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Module-level logger configuration
logger.add("module.log", rotation="10 MB")


class MainClass(BaseClass):
    """
    Main class implementing core functionality.
    
    This class provides [specific functionality description].
    It inherits from BaseClass and extends it with [extensions].
    
    Attributes:
        config (Dict): Configuration parameters
        state (str): Current processing state
        results (List): Accumulated results
    
    Example:
        >>> instance = MainClass(config={'debug': True})
        >>> instance.process([1, 2, 3])
        [2, 4, 6]
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize MainClass with configuration.
        
        Args:
            config: Optional configuration dictionary.
                    Defaults to DEFAULT_CONFIG if not provided.
        
        Raises:
            ValueError: If config contains invalid parameters
        """
        super().__init__()
        self.config = config or DEFAULT_CONFIG.copy()
        self.state = "initialized"
        self.results = []
        self._validate_config()
        
        logger.info(f"MainClass initialized with config: {self.config}")
    
    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        required_keys = ['timeout', 'retry_count']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")
    
    def process(self, data: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        Process input data through the pipeline.
        
        Args:
            data: List of numeric values to process
            
        Returns:
            List of processed values
            
        Raises:
            TypeError: If data contains non-numeric values
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Cannot process empty data")
        
        self.state = "processing"
        try:
            # Processing logic
            self.results = [self._transform(item) for item in data]
            self.state = "completed"
            return self.results
        except Exception as e:
            self.state = "error"
            logger.error(f"Processing failed: {e}")
            raise
    
    def _transform(self, item: Union[int, float]) -> Union[int, float]:
        """Transform single data item."""
        return item * 2


def standalone_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Standalone utility function.
    
    Args:
        param1: String parameter description
        param2: Integer parameter with default value
        
    Returns:
        Dictionary containing processed results
        
    Example:
        >>> standalone_function("test", 20)
        {'input': 'test', 'count': 20, 'processed': True}
    """
    return {
        'input': param1,
        'count': param2,
        'processed': True
    }


def main():
    """Entry point for module execution."""
    parser = argparse.ArgumentParser(description="Module description")
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', default='output.json', help='Output file path')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.level = "DEBUG"
    
    try:
        # Main execution logic
        processor = MainClass()
        with open(args.input, 'r') as f:
            data = json.load(f)
        
        results = processor.process(data)
        
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Processing complete. Results written to {args.output}")
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Data Processing Module Template

Specialized template for modules focused on data processing and analysis tasks.

```python
"""
Data Processing Module

Provides functionality for processing and analyzing structured data
with support for multiple formats and transformation pipelines.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging
from datetime import datetime

# Configure module logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Process structured data through configurable pipelines.
    
    Supports CSV, JSON, and Parquet formats with automatic
    format detection and optimized processing strategies.
    """
    
    SUPPORTED_FORMATS = {'.csv', '.json', '.parquet', '.xlsx'}
    
    def __init__(self, chunk_size: int = 10000):
        """
        Initialize processor with configuration.
        
        Args:
            chunk_size: Number of rows to process at once
        """
        self.chunk_size = chunk_size
        self.metrics = {
            'rows_processed': 0,
            'errors_encountered': 0,
            'processing_time': 0
        }
    
    def load_data(self, filepath: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from file with automatic format detection.
        
        Args:
            filepath: Path to data file
            
        Returns:
            Loaded dataframe
            
        Raises:
            ValueError: If file format not supported
            FileNotFoundError: If file doesn't exist
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {suffix}")
        
        logger.info(f"Loading data from {filepath}")
        
        if suffix == '.csv':
            return pd.read_csv(filepath)
        elif suffix == '.json':
            return pd.read_json(filepath)
        elif suffix == '.parquet':
            return pd.read_parquet(filepath)
        elif suffix == '.xlsx':
            return pd.read_excel(filepath)
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process dataframe through standard pipeline.
        
        Pipeline stages:
        1. Validate data structure
        2. Clean and standardize
        3. Apply transformations
        4. Generate derived features
        
        Args:
            df: Input dataframe
            
        Returns:
            Processed dataframe
        """
        start_time = datetime.now()
        
        # Stage 1: Validation
        self._validate_data(df)
        
        # Stage 2: Cleaning
        df_clean = self._clean_data(df)
        
        # Stage 3: Transformation
        df_transformed = self._transform_data(df_clean)
        
        # Stage 4: Feature engineering
        df_final = self._engineer_features(df_transformed)
        
        # Update metrics
        self.metrics['rows_processed'] += len(df)
        self.metrics['processing_time'] = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Processed {len(df)} rows in {self.metrics['processing_time']:.2f}s")
        
        return df_final
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """Validate data meets requirements."""
        if df.empty:
            raise ValueError("Empty dataframe")
        
        required_columns = ['id', 'timestamp', 'value']
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize data."""
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Handle missing values
        df_clean['value'] = df_clean['value'].fillna(0)
        
        # Standardize timestamps
        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
        
        return df_clean
    
    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply business transformations."""
        df_transformed = df.copy()
        
        # Example transformations
        df_transformed['value_squared'] = df_transformed['value'] ** 2
        df_transformed['value_log'] = np.log1p(df_transformed['value'].abs())
        
        return df_transformed
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate derived features."""
        df_features = df.copy()
        
        # Time-based features
        df_features['hour'] = df_features['timestamp'].dt.hour
        df_features['day_of_week'] = df_features['timestamp'].dt.dayofweek
        df_features['is_weekend'] = df_features['day_of_week'].isin([5, 6])
        
        # Rolling statistics
        df_features['value_rolling_mean'] = (
            df_features['value']
            .rolling(window=7, min_periods=1)
            .mean()
        )
        
        return df_features
    
    def save_results(self, df: pd.DataFrame, filepath: Union[str, Path],
                    format: str = 'parquet') -> None:
        """
        Save processed data to file.
        
        Args:
            df: Dataframe to save
            filepath: Output file path
            format: Output format (csv, json, parquet)
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            df.to_csv(path, index=False)
        elif format == 'json':
            df.to_json(path, orient='records', indent=2)
        elif format == 'parquet':
            df.to_parquet(path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {format}")
        
        logger.info(f"Results saved to {filepath}")
    
    def get_metrics(self) -> Dict[str, Union[int, float]]:
        """Return processing metrics."""
        return self.metrics.copy()


# Utility functions
def validate_schema(df: pd.DataFrame, schema: Dict[str, type]) -> bool:
    """
    Validate dataframe against expected schema.
    
    Args:
        df: Dataframe to validate
        schema: Expected column names and types
        
    Returns:
        True if valid, False otherwise
    """
    for col, expected_type in schema.items():
        if col not in df.columns:
            return False
        if not df[col].dtype == expected_type:
            return False
    return True


def generate_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics.
    
    Args:
        df: Input dataframe
        
    Returns:
        Summary statistics dataframe
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    summary = pd.DataFrame({
        'count': df[numeric_cols].count(),
        'mean': df[numeric_cols].mean(),
        'std': df[numeric_cols].std(),
        'min': df[numeric_cols].min(),
        '25%': df[numeric_cols].quantile(0.25),
        '50%': df[numeric_cols].quantile(0.50),
        '75%': df[numeric_cols].quantile(0.75),
        'max': df[numeric_cols].max(),
        'null_count': df[numeric_cols].isnull().sum(),
        'unique_count': df[numeric_cols].nunique()
    })
    
    return summary.T


if __name__ == "__main__":
    # Example usage
    processor = DataProcessor()
    
    # Load and process data
    data = processor.load_data("input_data.csv")
    processed = processor.process_data(data)
    
    # Generate summary
    summary = generate_summary_statistics(processed)
    print(summary)
    
    # Save results
    processor.save_results(processed, "output_data.parquet")
    print(f"Metrics: {processor.get_metrics()}")
```

### Test Module Template

Comprehensive template for test modules using pytest framework.

```python
"""
Test Module for [Component Name]

Comprehensive test suite covering unit tests, integration tests,
and edge cases for the [component] module.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
import tempfile
import json

# Import modules to test
from mypackage.processor import DataProcessor, ValidationError
from mypackage.utils import calculate_metrics, format_output


class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return pd.DataFrame({
            'id': range(100),
            'value': np.random.randn(100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='H')
        })
    
    @pytest.fixture
    def processor(self):
        """Provide configured processor instance."""
        return DataProcessor(chunk_size=50)
    
    def test_initialization(self):
        """Test processor initialization."""
        processor = DataProcessor()
        assert processor.chunk_size == 10000
        assert processor.metrics['rows_processed'] == 0
        
        custom_processor = DataProcessor(chunk_size=5000)
        assert custom_processor.chunk_size == 5000
    
    def test_load_data_csv(self, tmp_path, sample_data):
        """Test loading CSV files."""
        # Create temporary CSV file
        csv_path = tmp_path / "test_data.csv"
        sample_data.to_csv(csv_path, index=False)
        
        processor = DataProcessor()
        loaded_data = processor.load_data(csv_path)
        
        assert len(loaded_data) == len(sample_data)
        assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_load_data_unsupported_format(self, processor, tmp_path):
        """Test error handling for unsupported formats."""
        invalid_path = tmp_path / "test.txt"
        invalid_path.write_text("invalid data")
        
        with pytest.raises(ValueError, match="Unsupported format"):
            processor.load_data(invalid_path)
    
    def test_load_data_missing_file(self, processor):
        """Test error handling for missing files."""
        with pytest.raises(FileNotFoundError):
            processor.load_data("nonexistent_file.csv")
    
    @pytest.mark.parametrize("null_percentage", [0.1, 0.5, 0.9])
    def test_process_data_with_nulls(self, processor, sample_data, null_percentage):
        """Test processing data with various null percentages."""
        # Introduce nulls
        null_mask = np.random.random(len(sample_data)) < null_percentage
        sample_data.loc[null_mask, 'value'] = np.nan
        
        processed = processor.process_data(sample_data)
        
        # Verify nulls were handled
        assert processed['value'].isnull().sum() == 0
        assert len(processed) == len(sample_data)
    
    def test_process_empty_dataframe(self, processor):
        """Test error handling for empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError, match="Empty dataframe"):
            processor.process_data(empty_df)
    
    def test_process_missing_columns(self, processor):
        """Test error handling for missing required columns."""
        invalid_df = pd.DataFrame({'wrong_column': [1, 2, 3]})
        
        with pytest.raises(ValueError, match="Missing required columns"):
            processor.process_data(invalid_df)
    
    @patch('mypackage.processor.logger')
    def test_logging(self, mock_logger, processor, sample_data):
        """Test logging functionality."""
        processor.process_data(sample_data)
        
        # Verify logging calls
        assert mock_logger.info.called
        log_messages = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("Processed" in msg for msg in log_messages)
    
    def test_metrics_tracking(self, processor, sample_data):
        """Test metrics are tracked correctly."""
        initial_metrics = processor.get_metrics()
        assert initial_metrics['rows_processed'] == 0
        
        processor.process_data(sample_data)
        updated_metrics = processor.get_metrics()
        
        assert updated_metrics['rows_processed'] == len(sample_data)
        assert updated_metrics['processing_time'] > 0
    
    def test_concurrent_processing(self, processor, sample_data):
        """Test thread safety of processor."""
        import threading
        import queue
        
        results = queue.Queue()
        errors = queue.Queue()
        
        def process_chunk(data, index):
            try:
                result = processor.process_data(data)
                results.put((index, len(result)))
            except Exception as e:
                errors.put((index, str(e)))
        
        # Create threads
        threads = []
        chunk_size = 25
        for i in range(0, len(sample_data), chunk_size):
            chunk = sample_data.iloc[i:i+chunk_size]
            thread = threading.Thread(
                target=process_chunk,
                args=(chunk, i)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Verify results
        assert errors.empty()
        total_processed = sum(r[1] for r in list(results.queue))
        assert total_processed == len(sample_data)


@pytest.mark.integration
class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_end_to_end_processing(self, tmp_path):
        """Test complete processing pipeline."""
        # Generate test data
        test_data = pd.DataFrame({
            'id': range(1000),
            'value': np.random.randn(1000),
            'timestamp': pd.date_range('2024-01-01', periods=1000, freq='T')
        })
        
        # Save to file
        input_path = tmp_path / "input.csv"
        test_data.to_csv(input_path, index=False)
        
        # Process data
        processor = DataProcessor()
        loaded = processor.load_data(input_path)
        processed = processor.process_data(loaded)
        
        # Save results
        output_path = tmp_path / "output.parquet"
        processor.save_results(processed, output_path)
        
        # Verify output
        assert output_path.exists()
        result = pd.read_parquet(output_path)
        assert len(result) == len(test_data)
        assert 'value_squared' in result.columns
        assert 'hour' in result.columns


@pytest.mark.performance
class TestPerformance:
    """Performance tests for scalability verification."""
    
    @pytest.mark.parametrize("size", [1000, 10000, 100000])
    def test_processing_speed(self, size):
        """Test processing speed scales linearly."""
        import time
        
        # Generate data
        data = pd.DataFrame({
            'id': range(size),
            'value': np.random.randn(size),
            'timestamp': pd.date_range('2024-01-01', periods=size, freq='S')
        })
        
        processor = DataProcessor()
        
        start_time = time.time()
        processor.process_data(data)
        elapsed = time.time() - start_time
        
        # Verify reasonable performance
        rows_per_second = size / elapsed
        assert rows_per_second > 1000, f"Processing too slow: {rows_per_second} rows/s"
    
    def test_memory_usage(self):
        """Test memory usage remains reasonable."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process large dataset
        large_data = pd.DataFrame({
            'id': range(1000000),
            'value': np.random.randn(1000000),
            'timestamp': pd.date_range('2024-01-01', periods=1000000, freq='S')
        })
        
        processor = DataProcessor(chunk_size=10000)
        processor.process_data(large_data)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 500, f"Excessive memory usage: {memory_increase}MB"


# Fixtures for cross-test usage
@pytest.fixture(scope="session")
def test_database():
    """Provide test database connection."""
    # Setup test database
    db = create_test_database()
    yield db
    # Teardown
    db.close()


@pytest.fixture
def mock_api_client():
    """Provide mocked API client."""
    client = Mock()
    client.get.return_value = {'status': 'success', 'data': []}
    client.post.return_value = {'id': '123', 'created': True}
    return client


# Helper functions for tests
def assert_dataframe_equal(df1, df2, check_dtype=True):
    """Assert two dataframes are equal."""
    pd.testing.assert_frame_equal(
        df1, df2, 
        check_dtype=check_dtype,
        check_index_type=False
    )


def create_test_file(path, content):
    """Create test file with content."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([__file__, '-v', '--cov=mypackage', '--cov-report=html'])
```

## Configuration File Templates

Configuration files provide essential settings for applications while maintaining flexibility and clarity.

### Application Configuration (config.py)

```python
"""
Application Configuration Module

Centralized configuration management with environment-specific settings
and validation.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import json
import yaml
from functools import lru_cache


@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str = "user"
    password: str = ""
    pool_size: int = 10
    echo: bool = False
    
    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        return (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


@dataclass
class APIConfig:
    """External API configuration."""
    base_url: str = "https://api.example.com"
    api_key: str = ""
    timeout: int = 30
    retry_count: int = 3
    rate_limit: int = 100  # requests per minute


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = "logs/app.log"
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5
    enable_console: bool = True


@dataclass
class ApplicationConfig:
    """Main application configuration."""
    app_name: str = "MyApplication"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Sub-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Application-specific settings
    data_directory: str = "./data"
    temp_directory: str = "./temp"
    max_upload_size: int = 104857600  # 100MB
    allowed_extensions: List[str] = field(
        default_factory=lambda: ['.csv', '.json', '.xlsx']
    )
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        Path(self.data_directory).mkdir(exist_ok=True)
        Path(self.temp_directory).mkdir(exist_ok=True)
        if self.logging.file_path:
            Path(self.logging.file_path).parent.mkdir(exist_ok=True)


class ConfigurationManager:
    """Manage application configuration with multiple sources."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self._config: Optional[ApplicationConfig] = None
    
    @property
    def config(self) -> ApplicationConfig:
        """Get configuration instance."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> ApplicationConfig:
        """
        Load configuration from multiple sources.
        
        Priority order:
        1. Environment variables
        2. Configuration file
        3. Default values
        """
        config_dict = {}
        
        # Load from file if provided
        if self.config_file and Path(self.config_file).exists():
            config_dict = self._load_from_file(self.config_file)
        
        # Override with environment variables
        config_dict = self._apply_env_overrides(config_dict)
        
        # Create configuration object
        return self._create_config_object(config_dict)
    
    def _load_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        path = Path(file_path)
        
        if path.suffix == '.json':
            with open(path) as f:
                return json.load(f)
        elif path.suffix in ['.yml', '.yaml']:
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
    
    def _apply_env_overrides(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides."""
        # Database settings
        if db_host := os.getenv('DB_HOST'):
            config_dict.setdefault('database', {})['host'] = db_host
        if db_port := os.getenv('DB_PORT'):
            config_dict.setdefault('database', {})['port'] = int(db_port)
        if db_name := os.getenv('DB_NAME'):
            config_dict.setdefault('database', {})['database'] = db_name
        if db_user := os.getenv('DB_USER'):
            config_dict.setdefault('database', {})['username'] = db_user
        if db_pass := os.getenv('DB_PASSWORD'):
            config_dict.setdefault('database', {})['password'] = db_pass
        
        # API settings
        if api_key := os.getenv('API_KEY'):
            config_dict.setdefault('api', {})['api_key'] = api_key
        if api_url := os.getenv('API_BASE_URL'):
            config_dict.setdefault('api', {})['base_url'] = api_url
        
        # Application settings
        if debug := os.getenv('DEBUG'):
            config_dict['debug'] = debug.lower() in ['true', '1', 'yes']
        if env := os.getenv('ENVIRONMENT'):
            config_dict['environment'] = env
        
        return config_dict
    
    def _create_config_object(self, config_dict: Dict[str, Any]) -> ApplicationConfig:
        """Create configuration object from dictionary."""
        # Extract sub-configurations
        db_config = DatabaseConfig(**config_dict.pop('database', {}))
        api_config = APIConfig(**config_dict.pop('api', {}))
        log_config = LoggingConfig(**config_dict.pop('logging', {}))
        
        # Create main configuration
        return ApplicationConfig(
            database=db_config,
            api=api_config,
            logging=log_config,
            **config_dict
        )
    
    def save_config(self, file_path: str, format: str = 'yaml'):
        """Save current configuration to file."""
        config_dict = self._config_to_dict(self.config)
        
        path = Path(file_path)
        path.parent.mkdir(exist_ok=True)
        
        if format == 'json':
            with open(path, 'w') as f:
                json.dump(config_dict, f, indent=2)
        elif format == 'yaml':
            with open(path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
    
    def _config_to_dict(self, config: ApplicationConfig) -> Dict[str, Any]:
        """Convert configuration object to dictionary."""
        return {
            'app_name': config.app_name,
            'version': config.version,
            'debug': config.debug,
            'environment': config.environment,
            'database': {
                'host': config.database.host,
                'port': config.database.port,
                'database': config.database.database,
                'username': config.database.username,
                'pool_size': config.database.pool_size,
                'echo': config.database.echo
            },
            'api': {
                'base_url': config.api.base_url,
                'timeout': config.api.timeout,
                'retry_count': config.api.retry_count,
                'rate_limit': config.api.rate_limit
            },
            'logging': {
                'level': config.logging.level,
                'format': config.logging.format,
                'file_path': config.logging.file_path,
                'max_bytes': config.logging.max_bytes,
                'backup_count': config.logging.backup_count,
                'enable_console': config.logging.enable_console
            },
            'data_directory': config.data_directory,
            'temp_directory': config.temp_directory,
            'max_upload_size': config.max_upload_size,
            'allowed_extensions': config.allowed_extensions
        }


# Singleton instance
_config_manager: Optional[ConfigurationManager] = None


@lru_cache()
def get_config() -> ApplicationConfig:
    """Get application configuration."""
    global _config_manager
    if _config_manager is None:
        config_file = os.getenv('CONFIG_FILE', 'config/default.yaml')
        _config_manager = ConfigurationManager(config_file)
    return _config_manager.config


# Environment-specific configurations
CONFIGS = {
    'development': {
        'debug': True,
        'database': {'echo': True},
        'logging': {'level': 'DEBUG'}
    },
    'testing': {
        'debug': True,
        'database': {'database': 'myapp_test'},
        'logging': {'level': 'DEBUG', 'file_path': None}
    },
    'production': {
        'debug': False,
        'database': {'echo': False, 'pool_size': 20},
        'logging': {'level': 'INFO'}
    }
}


if __name__ == "__main__":
    # Example usage
    config = get_config()
    print(f"Application: {config.app_name} v{config.version}")
    print(f"Environment: {config.environment}")
    print(f"Database: {config.database.connection_string}")
    
    # Save example configuration
    manager = ConfigurationManager()
    manager.save_config("config/example.yaml")
```

These templates provide comprehensive starting points for various module types, demonstrating best practices in structure, documentation, error handling, and testing. Each template can be customized for specific use cases while maintaining consistency and quality standards.