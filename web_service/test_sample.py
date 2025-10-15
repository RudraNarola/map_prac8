import pytest
import numpy as np


def test_feature_array_processing():
    features = [5.1, 3.5, 1.4, 0.2]
    features_array = np.array(features)
    features_reshaped = features_array.reshape(1, -1)

    assert features_reshaped.shape == (1, 4)
    np.testing.assert_array_equal(features_reshaped[0], [5.1, 3.5, 1.4, 0.2])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
