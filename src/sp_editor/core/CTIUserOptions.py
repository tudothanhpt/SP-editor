class UserOptions:
    def __init__(self):
        # 0-Investigation Mode; 1-Design Mode (Run Option in Project left panel | Run Options)
        self.run_option = 0
        # Unit System 0-English; 1-Metric Units (Unit system in Project left panel | General)
        self.unit_system = 0
        # Design Code 0-ACI 318-02; 1-CSA A23.3-94; 2-ACI 318-05; 3-CSA A23.3-04; 4-ACI 318-08; 5-ACI 318-11; 6-ACI
        # 318-14; 7-CSA A23.3-14; 8-ACI 318-19; 9-CSA A23.3-19 (Design Code in Project left panel | General)
        self.design_code = 8
        # Run Axis 0-X Axis Run; 1-Y Axis Run; 2-Biaxial Run (Run Axis in Project left panel | Run Options)
        self.run_axis = 2
        # Reserved. Do not edit
        self.reserved1 = 0
        # Slenderness Consideration 0-Not considered; 1-Considered (Consider Slenderness in Project left panel | Run
        # Options)
        self.slenderness_consideration = 0
        # Bar Selection 0-Design for minimum number of bars; 1-Design for minimum area of reinforcement (Bar
        # selection in Definitions dialog | Properties | Design Criteria | Reinforcement Bars)
        self.bar_selection = 0
        # Reserved. Do not edit
        self.reserved2 = 0
        # Column Section Shape 0-Rectangular Column Section; 1-Circular Column Section; 2-Irregular Column Section (
        # Section left panel)
        self.column_section_shape = 2
        # Reinforcing Bar Layout 0-Rectangular reinforcing bar layout; 1-Circular reinforcing bar layout (Layout in
        # Section left panel | Rect. Or Cir. | Bar Arrangement - when Type is All Sides Equal)
        self.reinforcing_bar_layout = 0
        # Column Type 0-Structural Column Section; 1-Architectural Column Section; 2-User Defined Column Section (
        # Column Type in Definitions dialog | Properties | Design Criteria)
        self.column_type = 0
        # Confinement Type 0-Tied Confinement; 1-Spiral Confinement; 2-Other Confinement (Confinement in Definitions
        # dialog | Properties | Reduction Factors | Confinement)
        self.confinement_type = 0
        # Load Type for Inspection Mode 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        self.load_type_inspection = 0
        # Load Type for Design Mode 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        self.load_type_design = 0
        # Reinforcement Layout for Inspection Mode 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular
        # Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        self.reinforcement_layout_inspection = 3
        # Reinforcement Layout for Design Mode 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular
        # Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        self.reinforcement_layout_design = 0
        # Reserved. Do not edit for regular bars. No of bars for irregular bars
        self.reserved3 = 0
        # Number of Factored Loads (Factored Loads in Loads dialog | Loads)
        self.num_factored_loads = 0
        # Number of Service Loads (Service Loads in Loads dialog | Loads)
        self.num_service_loads = 0
        # Number of Points on Exterior Column Section If there is only one exterior column section then Number of
        # points on exterior column section. If there are more than one exterior column sections then 0
        self.num_exterior_points = 0
        # Number of Points on Interior Section Opening If there is only one interior section opening then Number of
        # points on the interior section opening. If there are more than one interior section openings then 0
        self.num_interior_points = 9
        # Reserved. Do not edit
        self.reserved4 = 0
        # Reserved. Do not edit
        self.reserved5 = 0
        # Cover Type for investigation mode 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section
        # left panel | Rect. Or Cir. | Cover Type)
        self.cover_type_investion_mode = 0
        # Cover Type for Design Mode 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section left panel
        # | Rect. Or Cir. | Cover Type)
        self.cover_type_design_mode = 0
        # Number of Load Combinations (Load combinations in Definitions dialog | Load Case/Combo)
        self.num_load_combinations = 13
        # Section Capacity Method 0-Moment capacity method; 1-Critical Capacity method (Section capacity in Project
        # left panel | General)
        self.section_capacity_method = 1

    def set_user_options_CTIformat(self):
        options = [
            self.run_option,
            self.unit_system,
            self.design_code,
            self.run_axis,
            self.reserved1,
            self.slenderness_consideration,
            self.bar_selection,
            self.reserved2,
            self.column_section_shape,
            self.reinforcing_bar_layout,
            self.column_type,
            self.confinement_type,
            self.load_type_inspection,
            self.load_type_design,
            self.reinforcement_layout_inspection,
            self.reinforcement_layout_design,
            self.reserved3,
            self.num_factored_loads,
            self.num_service_loads,
            self.num_exterior_points,
            self.num_interior_points,
            self.reserved4,
            self.reserved5,
            self.cover_type_investion_mode,
            self.cover_type_design_mode,
            self.num_load_combinations,
            self.section_capacity_method,
        ]
        return ",".join(map(str, options))
