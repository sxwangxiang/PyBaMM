#
# Base class for lithium plating models.
#
import pybamm
from ..base_interface import BaseInterface


class BasePlating(BaseInterface):
    """Base class for lithium plating models.
    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    options : dict, optional
        A dictionary of options to be passed to the model.

    References
    ----------
    .. [1] SEJ O'Kane, ID Campbell, MWJ Marzook, GJ Offer and M Marinescu. "Physical
           Origin of the Differential Voltage Minimum Associated with Li Plating in
           Lithium-Ion Batteries". Journal of The Electrochemical Society,
           167:090540, 2019

    **Extends:** :class:`pybamm.interface.BaseInterface`
    """

    def __init__(self, param, options=None):
        reaction = "lithium plating"
        domain = "Negative"
        super().__init__(param, domain, reaction, options=options)

    def get_coupled_variables(self, variables):
        # Update some common variables
        zero_av = pybamm.PrimaryBroadcast(0, "current collector")
        zero = pybamm.FullBroadcast(0, "positive electrode", "current collector")

        variables.update(
            {
                "X-averaged negative electrode lithium plating interfacial current "
                "density": variables[
                    "X-averaged lithium plating interfacial current density"
                ],
                "X-averaged positive electrode lithium plating interfacial current "
                "density": zero_av,
                "Negative electrode lithium plating interfacial current "
                "density": variables["Lithium plating interfacial current density"],
                "Positive electrode lithium plating interfacial current density": zero,
            }
        )
        variables.update(
            self._get_standard_whole_cell_interfacial_current_variables(variables)
        )

        return variables

    def _get_standard_concentration_variables(self, c_plated_Li):
        """
        A private function to obtain the standard variables which
        can be derived from the local plated lithium concentration.
        Parameters
        ----------
        c_plated_Li : :class:`pybamm.Symbol`
            The plated lithium concentration.
        Returns
        -------
        variables : dict
            The variables which can be derived from the plated lithium thickness.
        """
        param = self.param

        # Set scales to one for the "no plating" model so that they are not required
        # by parameter values in general
        if isinstance(self, pybamm.lithium_plating.NoPlating):
            c_scale = 1
            L_scale = 1
        else:
            c_scale = param.c_Li_typ
            L_scale = param.V_bar_plated_Li * c_scale / param.a_n_typ

        c_plated_Li_av = pybamm.x_average(c_plated_Li)
        L_plated_Li = c_plated_Li  # plated Li thickness
        L_plated_Li_av = pybamm.x_average(L_plated_Li)
        Q_plated_Li = c_plated_Li_av * param.L_n * param.L_y * param.L_z

        variables = {
            "Lithium plating concentration": c_plated_Li,
            "Lithium plating concentration [mol.m-3]": c_plated_Li * c_scale,
            "X-averaged lithium plating concentration": c_plated_Li_av,
            "X-averaged lithium plating concentration"
            " [mol.m-3]": c_plated_Li_av * c_scale,
            "Lithium plating thickness": L_plated_Li,
            "Lithium plating thickness [m]": L_plated_Li * L_scale,
            "X-averaged lithium plating thickness [m]": L_plated_Li_av * L_scale,
            "Loss of lithium to lithium plating [mol]": Q_plated_Li * c_scale,
            "Loss of capacity to lithium plating [A.h]": Q_plated_Li
            * c_scale
            * param.F
            / 3600,
        }

        return variables

    def _get_standard_reaction_variables(self, j_stripping):
        """
        A private function to obtain the standard variables which
        can be derived from the lithum stripping interfacial reaction current
        Parameters
        ----------
        j_stripping : :class:`pybamm.Symbol`
            The net lithium stripping interfacial reaction current.
        Returns
        -------
        variables : dict
            The variables which can be derived from the plated lithium thickness.
        """
        # Set scales to one for the "no plating" model so that they are not required
        # by parameter values in general
        param = self.param
        j_scale = param.j_scale_n
        j_stripping_av = pybamm.x_average(j_stripping)

        variables = {
            "Lithium plating interfacial current density": j_stripping,
            "Lithium plating interfacial current density [A.m-2]": j_stripping
            * j_scale,
            "X-averaged lithium plating interfacial current density": j_stripping_av,
            "X-averaged lithium plating "
            "interfacial current density [A.m-2]": j_stripping_av * j_scale,
        }

        return variables
