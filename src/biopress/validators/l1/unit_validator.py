"""L1 Unit Validator for unit consistency checking."""



class UnitValidator:
    """Validates units and performs unit conversions."""

    CONVERSION_FACTORS = {
        "length": {
            "m": 1.0,
            "cm": 0.01,
            "mm": 0.001,
            "km": 1000.0,
            "inch": 0.0254,
            "ft": 0.3048,
            "mile": 1609.344,
        },
        "mass": {
            "kg": 1.0,
            "g": 0.001,
            "mg": 0.000001,
            "tonne": 1000.0,
            "lb": 0.453592,
            "oz": 0.0283495,
        },
        "time": {
            "s": 1.0,
            "ms": 0.001,
            "min": 60.0,
            "h": 3600.0,
            "day": 86400.0,
        },
        "velocity": {
            "m/s": 1.0,
            "km/h": 0.277778,
            "cm/s": 0.01,
            "km/s": 1000.0,
            "mph": 0.44704,
            "ft/s": 0.3048,
        },
        "acceleration": {
            "m/s^2": 1.0,
            "cm/s^2": 0.01,
            "km/h^2": 0.0000771605,
            "g": 9.80665,
        },
        "force": {
            "N": 1.0,
            "kN": 1000.0,
            "dyn": 0.00001,
            "lbf": 4.44822,
            "kgf": 9.80665,
        },
        "energy": {
            "J": 1.0,
            "kJ": 1000.0,
            "cal": 4.184,
            "kcal": 4184.0,
            "eV": 1.60218e-19,
            "Wh": 3600.0,
            "kWh": 3600000.0,
        },
        "power": {
            "W": 1.0,
            "kW": 1000.0,
            "MW": 1000000.0,
            "hp": 745.7,
        },
        "pressure": {
            "Pa": 1.0,
            "kPa": 1000.0,
            "atm": 101325.0,
            "bar": 100000.0,
            "mmHg": 133.322,
            "psi": 6894.76,
        },
        "temperature": {
            "K": 1.0,
            "C": 1.0,
            "F": 0.555556,
        },
    }

    SI_BASE_UNITS = {
        "m": {"L": 1},
        "kg": {"M": 1},
        "s": {"T": 1},
        "A": {"I": 1},
        "K": {"theta": 1},
        "mol": {"N": 1},
        "cd": {"J": 1},
    }

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert value from one unit to another within the same dimension.

        Args:
            value: The numerical value to convert
            from_unit: Source unit (e.g., 'km/h')
            to_unit: Target unit (e.g., 'm/s')

        Returns:
            Converted value

        Raises:
            ValueError: If units are incompatible or unknown
        """
        for dimension, units in self.CONVERSION_FACTORS.items():
            if from_unit in units and to_unit in units:
                base_value = value * units[from_unit]
                return base_value / units[to_unit]

        raise ValueError(
            f"Cannot convert from '{from_unit}' to '{to_unit}': "
            f"units are from different dimensions or unknown"
        )

    def check_unit_consistency(self, quantity: str, unit: str) -> bool:
        """
        Check if unit is consistent with the physical quantity.

        Args:
            quantity: Physical quantity name
            unit: Unit to check

        Returns:
            True if unit is consistent, False otherwise
        """
        quantity_lower = quantity.lower()
        unit_lower = unit.lower()

        valid_units = {
            "velocity": ["m/s", "km/h", "cm/s", "mm/s", "km/s", "mph"],
            "acceleration": ["m/s^2", "cm/s^2", "km/h^2", "g"],
            "force": ["n", "kn", "dyn", "lbf", "kgf"],
            "energy": ["j", "kj", "cal", "kcal", "ev", "wh", "kwh"],
            "power": ["w", "kw", "mw", "hp"],
            "pressure": ["pa", "kpa", "atm", "bar", "mmhg", "psi"],
            "mass": ["kg", "g", "mg", "tonne", "lb", "oz"],
            "length": ["m", "cm", "mm", "km", "inch", "ft", "mile"],
            "time": ["s", "ms", "min", "h", "day"],
            "temperature": ["k", "c", "f"],
        }

        if quantity_lower in valid_units:
            return unit_lower in valid_units[quantity_lower]

        return False

    def get_base_units(self, unit: str) -> dict[str, int]:
        """
        Get the SI base unit representation for a derived unit.

        Args:
            unit: The unit to decompose (e.g., 'm/s', 'N', 'J')

        Returns:
            Dictionary of base units with their powers
        """
        return self._parse_to_base_units(unit)

    def _parse_to_base_units(self, unit: str) -> dict[str, int]:
        """Parse a unit to its SI base components."""
        unit_lower = unit.lower().replace("^", "**")

        base_unit_map = {
            "m": {"L": 1},
            "s": {"T": -1},
            "kg": {"M": 1},
            "g": {"M": 1},
            "n": {"M": 1, "L": 1, "T": -2},
            "j": {"M": 1, "L": 2, "T": -2},
            "w": {"M": 1, "L": 2, "T": -3},
            "pa": {"M": 1, "L": -1, "T": -2},
            "hz": {"T": -1},
        }

        for base, dimensions in base_unit_map.items():
            if unit_lower.startswith(base) or unit_lower == base:
                return dimensions

        return {}

    def validate_unit_conversion(
        self, value: float, from_unit: str, to_unit: str, expected_result: float, tolerance: float = 1e-6
    ) -> tuple[bool, str]:
        """
        Validate that a unit conversion produces the expected result.

        Args:
            value: Original value
            from_unit: Source unit
            to_unit: Target unit
            expected_result: Expected converted value
            tolerance: Allowed difference

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            result = self.convert_units(value, from_unit, to_unit)
            diff = abs(result - expected_result)
            if diff <= tolerance:
                return True, f"Conversion correct: {value} {from_unit} = {result} {to_unit}"
            return False, f"Conversion incorrect: expected {expected_result}, got {result}"
        except ValueError as e:
            return False, str(e)


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from one unit to another."""
    validator = UnitValidator()
    return validator.convert_units(value, from_unit, to_unit)


def check_unit_consistency(quantity: str, unit: str) -> bool:
    """Check if unit is consistent with quantity."""
    validator = UnitValidator()
    return validator.check_unit_consistency(quantity, unit)


def get_base_units(unit: str) -> dict[str, int]:
    """Get SI base units for a unit."""
    validator = UnitValidator()
    return validator.get_base_units(unit)