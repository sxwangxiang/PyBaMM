#
# Test leading stefan maxwell electrolyte conductivity submodel
#

import pybamm
import tests
import unittest


class TestLeadingOrder(unittest.TestCase):
    def test_public_functions(self):
        param = pybamm.standard_parameters_lithium_ion
        a = pybamm.Scalar(0)
        variables = {
            "Current collector current density": a,
            "Average negative electrode potential": a,
            "Average negative electrode open circuit potential": a,
            "Average negative electrode reaction overpotential": a,
        }
        submodel = pybamm.electrolyte.stefan_maxwell.conductivity.LeadingOrder(param)
        std_tests = tests.StandardSubModelTests(submodel, variables)
        std_tests.test_all()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()
