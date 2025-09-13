class PhysicalParameters:
    def __init__(
        self,
        x_inflow,
        incNS,
        uinf,
        rhoinf,
        re_deltaStar,
        Mainf,
        Pr,
        Tinf,
        Twall_dimensionless,
        gamma,
        adiabatic,
    ):
        self.x_inflow = x_inflow
        self.incNS = incNS
        self.uinf = uinf
        self.rhoinf = rhoinf
        self.re_deltaStar = re_deltaStar
        self.Mainf = Mainf
        self.Pr = Pr
        self.Tinf = Tinf
        self.Twall_dimensionless = Twall_dimensionless
        self.gamma = gamma
        self.adiabatic = adiabatic

        self.delta = 0
        self.deltaStar = 0
        self.theta = 0
        self.shapeFactor = 0

    def __repr__(self):
        return (
            "Boundary layer quantities (the formulas are valid for both incNS and comNS)\n"
            f"delta        = {self.delta} * x / sqrt(Re_x)\n"
            f"deltaStar    = {self.deltaStar} * x / sqrt(Re_x)\n"
            f"theta        = {self.theta} * x / sqrt(Re_x)\n"
            f"delta/delta* = {self.delta / self.deltaStar}\n"
            f"H            = {self.shapeFactor}\n"
        )


