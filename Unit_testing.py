
import pytest
from part1 import calculate_interest

class TestCalculateInterest:
    """Comprehensive unit tests for calculate_interest function"""

    # Test valid inputs for each tier
    def test_tier1_only(self):
        """Test deposits within first €1,000 tier"""
        # Exactly €500
        assert calculate_interest(500) == "15.00"  # 500 * 0.03
        # Exactly €1,000
        assert calculate_interest(1000) == "30.00"  # 1000 * 0.03

    def test_tier2_only(self):
        """Test deposits in second tier (€1,001 to €11,000)"""
        # €2,000 total
        assert calculate_interest(2000) == "65.00"  # (1000*0.03) + (1000*0.035)
        # €11,000 total
        assert calculate_interest(11000) == "380.00"  # (1000*0.03) + (10000*0.035)

    def test_tier3_only(self):
        """Test deposits in third tier (€11,001 to €100,000)"""
        # €50,000 total
        expected = (1000*0.03) + (10000*0.035) + (39000*0.04)
        assert calculate_interest(50000) == f"{expected:.2f}"
        # €100,000 total
        expected = (1000*0.03) + (10000*0.035) + (89000*0.04)
        assert calculate_interest(100000) == f"{expected:.2f}"

    def test_tier4_only(self):
        """Test deposits above €100,000"""
        # €150,000 total
        expected = (1000*0.03) + (10000*0.035) + (89000*0.04) + (50000*0.045)
        assert calculate_interest(150000) == f"{expected:.2f}"

    def test_zero_deposit(self):
        """Test zero deposit"""
        assert calculate_interest(0) == "0.00"

    def test_float_inputs(self):
        """Test floating point inputs"""
        # Small float
        assert calculate_interest(500.50) == "15.01"  # 500.50 * 0.03 = 15.015 (rounds to 15.01)
        # Float spanning tiers
        expected = (1000*0.03) + ((2000.75-1000)*0.035)  # 2000.75 total
        assert calculate_interest(2000.75) == f"{expected:.2f}"

    # Test input validation
    def test_negative_deposit(self):
        """Test negative deposit raises ValueError"""
        with pytest.raises(ValueError, match="Deposit cannot be negative"):
            calculate_interest(-100)

    def test_string_input(self):
        """Test string input raises ValueError"""
        with pytest.raises(ValueError, match="Deposit must not be a string"):
            calculate_interest("1000")

    def test_boolean_input(self):
        """Test boolean input raises ValueError"""
        with pytest.raises(ValueError, match="Deposit must not be a Boolean"):
            calculate_interest(True)

    def test_invalid_type(self):
        """Test invalid type input raises ValueError"""
        with pytest.raises(ValueError, match="Deposit must be a number"):
            calculate_interest([1000])

    def test_none_input(self):
        """Test None input raises ValueError"""
        with pytest.raises(ValueError, match="Deposit must be a number"):
            calculate_interest(None)

    # Test edge cases
    def test_boundary_tier1_to_tier2(self):
        """Test boundary between tier 1 and tier 2"""
        # Exactly €1,000.01
        expected = (1000*0.03) + (0.01*0.035)
        assert calculate_interest(1000.01) == f"{expected:.2f}"

    def test_boundary_tier2_to_tier3(self):
        """Test boundary between tier 2 and tier 3"""
        # Exactly €11,000.01
        expected = (1000*0.03) + (10000*0.035) + (0.01*0.04)
        assert calculate_interest(11000.01) == f"{expected:.2f}"

    def test_boundary_tier3_to_tier4(self):
        """Test boundary between tier 3 and tier 4"""
        # Exactly €100,000.01
        expected = (1000*0.03) + (10000*0.035) + (89000*0.04) + (0.01*0.045)
        assert calculate_interest(100000.01) == f"{expected:.2f}"

    def test_large_deposit(self):
        """Test very large deposit"""
        large_deposit = 1000000  # €1,000,000
        expected = (1000*0.03) + (10000*0.035) + (89000*0.04) + (900000*0.045)
        assert calculate_interest(large_deposit) == f"{expected:.2f}"

    def test_precision(self):
        """Test floating point precision"""
        # Test that results are properly rounded to 2 decimal places
        result = calculate_interest(1000.005)
        assert result == "30.00"  # Should round down
        assert len(result.split('.')[-1]) == 2  # Exactly 2 decimal places