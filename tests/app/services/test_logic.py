from src.app.services.pricing import PricingService

def test_pricing_calculation():
    # 1. Arrange
    service = PricingService(base_rate=2.0)

    # 2. Act
    cost = service.calculate_cost(minutes=10)

    # 3. Assert
    assert cost == 20.0

def test_negative_minutes():
    # 1. Arrange
    service = PricingService(base_rate=2.0)

    # 2. Act
    cost = service.calculate_cost(minutes=-5)

    # 3. Assert
    assert cost == 0.0  # Negative minutes should not result in negative cost