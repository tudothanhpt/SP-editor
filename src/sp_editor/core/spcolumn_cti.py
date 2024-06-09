import math
import read_acad
import connect_etabs
from core.CTIUserOptions import UserOptions


class CTIfile:
    """
    Represents a CTI (spColumn Text Input) file for managing column design and investigation data.

    Attributes:
        SpColumnVersion (str): Version of the spColumn software.
        ProjectName (str): Name of the project.
        ColumnID (str): Identifier for the column.
        Engineer (str): Name of the engineer.
        InvestigationRunFlag (int): Flag indicating if an investigation run is performed.
        DesignRunFlag (int): Flag indicating if a design run is performed.
        SlendernessFlag (int): Flag indicating if the column slenderness is considered.
        UserOptions (str): User-defined options.
        IrregularOptions (str): Options for irregular configurations.
        Ties (str): Information about ties.
        InvestigationReinforcement (str): Reinforcement data for investigation.
        DesignReinforcement (str): Reinforcement data for design.
        InvestigationSectionDimensions (str): Section dimensions for investigation.
        DesignSectionDimensions (str): Section dimensions for design.
        MaterialProperties (str): Properties of the materials used.
        ReductionFactors (str): Factors for reducing loads or capacities.
        DesignCriteria (str): Criteria used for design.
        ExternalPoints (str): Data about external points.
        InternalPoints (str): Data about internal points.
        ReinforcementBars (str): Details of the reinforcement bars.
        FactoredLoads (str): Factored loads applied to the column.
        SlendernessColumn (str): Information on column slenderness.
        SlendernessColumnAboveAndBelow (str): Slenderness data for columns above and below.
        SlendernessBeams (str): Slenderness data for beams.
        EI (str): Flexural rigidity data.
        SldOptFact (str): Slenderness optimization factor.
        PhiDelta (str): Phi delta value.
        CrackedI (str): Data on the cracked moment of inertia.
        ServiceLoads (str): Service load data.
        LoadCombinations (str): Combinations of different loads.
        BarGroupType (str): Type of bar group.
        UserDefinedBars (str): Data on user-defined bars.
        SustainedLoadFactors (str): Factors for sustained loads.
    """

    def __init__(self):
        self.__SpColumnVersion: str = "10.000"
        self.__ProjectName: str = ""
        self.__ColumnID: str = ""
        self.__Engineer: str = ""
        self.__InvestigationRunFlag: int = 15  # DEFAULT
        self.__DesignRunFlag: int = 0
        self.__SlendernessFlag: int = 31  # DEFAULT
        self.UserOptions: str = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        self.__IrregularOptions: str = ""
        self.__Ties: str = ""
        self.__InvestigationReinforcement: str = ""
        self.__DesignReinforcement: str = ""
        self.__InvestigationSectionDimensions: str = ""
        self.__DesignSectionDimensions: str = ""
        self.__MaterialProperties: str = ""
        self.__ReductionFactors: str = ""
        self.__DesignCriteria: str = ""
        self.__ExternalPoints: str = ""
        self.__InternalPoints: str = ""
        self.__ReinforcementBars: str = 0
        self.__FactoredLoads: str = ""
        self.__SlendernessColumn: str = ""
        self.__SlendernessColumnAboveAndBelow: str = ""
        self.__SlendernessBeams: str = ""
        self.__EI: str = ""
        self.__SldOptFact: str = ""
        self.__PhiDelta: str = ""
        self.__CrackedI: str = ""
        self.__ServiceLoads: str = ""
        self.__LoadCombinations: str = ""
        self.__BarGroupType: str = ""
        self.__UserDefinedBars: str = ""
        self.__SustainedLoadFactors: str = ""

    def set_column_id(self, spcolumn_filename: str) -> None:
        """
        Sets the column ID.

        Args:
            spcolumn_filename (str): The column ID to set.
        """
        self.__ColumnID = spcolumn_filename

    def set_project_name(self, name: str) -> None:
        """
        Sets the project name.

        Args:
            name (str): The project name to set.
        """
        self.__ProjectName = name

    def set_engineer(self, name: str) -> None:
        """
        Sets the name of the engineer.

        Args:
            name (str): The name of the engineer.
        """
        self.__Engineer = name

    def set_user_options1(self) -> None:
        """
        Sets the user options based on the provided number of force combinations.

        Args:
            numforceCombos (int): The number of force combinations.
        """
        # Option 1: 0-Investigation Mode; 1-Design Mode (Run Option in Project left panel | Run Options)
        option1 = 0
        # Option 2: 0-English Unit; 1-Metric Units (Unit system in Project left panel | General)
        option2 = 0
        # Option 3: 0-ACI 318-02; 1-CSA A23.3-94; 2-ACI 318-05; 3-CSA A23.3-04; 4-ACI 318-08; 5-ACI 318-11; 6-ACI 318-14; 7-CSA A23.3-14; 8-ACI 318-19; 9-CSA A23.3-19 (Design Code in Project left panel | General)
        option3 = 8
        # Option 4: 0-X Axis Run; 1-Y Axis Run; 2-Biaxial Run (Run Axis in Project left panel | Run Options)
        option4 = 2
        # Option 5: Reserved. Do not edit
        option5 = 0
        # Option 6: 0-Slenderness is not considered; 1-Slenderness in considered (Consider Slenderness in Project left panel | Run Options)
        option6 = 0
        # Option 7: 0-Design for minimum number of bars; 1-Design for minimum area of reinforcement (Bar selection in Definitions dialog | Properties | Design Criteria | Reinforcement Bars)
        option7 = 0
        # Option 8: Reserved. Do not edit
        option8 = 0
        # Option 9: 0-Rectangular Column Section; 1-Circular Column Section; 2-Irregular Column Section (Section left panel)
        option9 = 2
        # Option 10: 0-Rectangular reinforcing bar layout; 1-Circular reinforcing bar layout (Layout in Section left panel | Rect. Or Cir. | Bar Arrangement - when Type is All Sides Equal)
        option10 = 0
        # Option 11: 0-Structural Column Section; 1-Architectural Column Section; 2-User Defined Column Section (Column Type in Definitions dialog | Properties | Design Criteria)
        option11 = 0
        # Option 12: 0-Tied Confinement; 1-Spiral Confinement; 2-Other Confinement (Confinement in Definitions dialog | Properties | Reduction Factors | Confinement)
        option12 = 0
        # Option 13: Load type for investigation mode: 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        option13 = 0
        # Option 14: Load type for design mode: 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        option14 = 0
        # Option 15: Reinforcement layout for investigation mode: 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        option15 = 3
        # Option 16: Reinforcement layout for design mode: 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        option16 = 0
        # Option 17: Reserved. Do not edit for regular bars. No of bars for irregular bars
        option17 = 0
        # Option 18: Number of factored loads (Factored Loads in Loads dialog | Loads)
        option18 = 0
        # Option 19: Number of service loads (Service Loads in Loads dialog | Loads)
        option19 = 0
        # Option 20: If there is only one exterior column section then Number of points on exterior column section. If there are more than one exterior column sections then 0
        option20 = 0
        # Option 21: If there is only one interior section opening then Number of points on the interior section opening. If there are more than one interior section openings then 0
        option21 = 9
        # Option 22: Reserved. Do not edit
        option22 = 0
        # Option 23: Reserved. Do not edit
        option23 = 0
        # Option 24: Cover type for investigation mode: 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section left panel | Rect. Or Cir. | Cover Type)
        option24 = 0
        # Option 25: Cover type for design mode: 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section left panel | Rect. Or Cir. | Cover Type)
        option25 = 0
        # Option 26: Number of load combinations; (Load combinations in Definitions dialog | Load Case/Combo)
        option26 = 13
        # Option 27: Section capacity: 0-Moment capacity method; 1-Critical Capacity method (Section capacity in Project left panel | General)
        option27 = 1

        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
            option13,
            option14,
            option15,
            option16,
            option17,
            option18,
            option19,
            option20,
            option21,
            option22,
            option23,
            option24,
            option25,
            option26,
            option27,
        ]

        self.UserOptions = ",".join(map(str, options))

    def set_user_options2(self, numforceCombos: int) -> None:
        """
        Sets the user options based on the provided number of force combinations.

        Args:
            numforceCombos (int): The number of force combinations.
        """
        # Option 1: 0-Investigation Mode; 1-Design Mode (Run Option in Project left panel | Run Options)
        option1 = 0
        # Option 2: 0-English Unit; 1-Metric Units (Unit system in Project left panel | General)
        option2 = 0
        # Option 3: 0-ACI 318-02; 1-CSA A23.3-94; 2-ACI 318-05; 3-CSA A23.3-04; 4-ACI 318-08; 5-ACI 318-11; 6-ACI 318-14; 7-CSA A23.3-14; 8-ACI 318-19; 9-CSA A23.3-19 (Design Code in Project left panel | General)
        option3 = 8
        # Option 4: 0-X Axis Run; 1-Y Axis Run; 2-Biaxial Run (Run Axis in Project left panel | Run Options)
        option4 = 2
        # Option 5: Reserved. Do not edit
        option5 = 0
        # Option 6: 0-Slenderness is not considered; 1-Slenderness in considered (Consider Slenderness in Project left panel | Run Options)
        option6 = 0
        # Option 7: 0-Design for minimum number of bars; 1-Design for minimum area of reinforcement (Bar selection in Definitions dialog | Properties | Design Criteria | Reinforcement Bars)
        option7 = 0
        # Option 8: Reserved. Do not edit
        option8 = 0
        # Option 9: 0-Rectangular Column Section; 1-Circular Column Section; 2-Irregular Column Section (Section left panel)
        option9 = 2
        # Option 10: 0-Rectangular reinforcing bar layout; 1-Circular reinforcing bar layout (Layout in Section left panel | Rect. Or Cir. | Bar Arrangement - when Type is All Sides Equal)
        option10 = 0
        # Option 11: 0-Structural Column Section; 1-Architectural Column Section; 2-User Defined Column Section (Column Type in Definitions dialog | Properties | Design Criteria)
        option11 = 0
        # Option 12: 0-Tied Confinement; 1-Spiral Confinement; 2-Other Confinement (Confinement in Definitions dialog | Properties | Reduction Factors | Confinement)
        option12 = 0
        # Option 13: Load type for investigation mode: 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        option13 = 0
        # Option 14: Load type for design mode: 0-Factored; 1-Service; 2-Control Points; 3-Axial Loads (Loads dialog)
        option14 = 0
        # Option 15: Reinforcement layout for investigation mode: 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        option15 = 3
        # Option 16: Reinforcement layout for design mode: 0-All Side Equal; 1-Equal Spacing; 2-Sides Different; 3-Irregular Pattern (Layout in Section left panel | Rect. Or Cir. Bar Arrangement)
        option16 = 0
        # Option 17: Reserved. Do not edit for regular bars. No of bars for irregular bars
        option17 = 0
        # Option 18: Number of factored loads (Factored Loads in Loads dialog | Loads)
        option18 = int(numforceCombos)
        # Option 19: Number of service loads (Service Loads in Loads dialog | Loads)
        option19 = 0
        # Option 20: If there is only one exterior column section then Number of points on exterior column section. If there are more than one exterior column sections then 0
        option20 = 0
        # Option 21: If there is only one interior section opening then Number of points on the interior section opening. If there are more than one interior section openings then 0
        option21 = 9
        # Option 22: Reserved. Do not edit
        option22 = 0
        # Option 23: Reserved. Do not edit
        option23 = 0
        # Option 24: Cover type for investigation mode: 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section left panel | Rect. Or Cir. | Cover Type)
        option24 = 0
        # Option 25: Cover type for design mode: 0-To transverse bar; 1-To longitudinal bar (Clear cover to in Section left panel | Rect. Or Cir. | Cover Type)
        option25 = 0
        # Option 26: Number of load combinations; (Load combinations in Definitions dialog | Load Case/Combo)
        option26 = 13
        # Option 27: Section capacity: 0-Moment capacity method; 1-Critical Capacity method (Section capacity in Project left panel | General)
        option27 = 1

        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
            option13,
            option14,
            option15,
            option16,
            option17,
            option18,
            option19,
            option20,
            option21,
            option22,
            option23,
            option24,
            option25,
            option26,
            option27,
        ]

        self.UserOptions = ",".join(map(str, options))

    def set_irregular_options(self) -> None:
        """Set options related to irregular sections."""
        # Option 1: Reserved. Do not edit.
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        # Option 3: Reserved. Do not edit.
        option3 = 0
        # Option 4: Reserved. Do not edit.
        option4 = 0
        # Option 5: Area of reinforcing bar that is to be added through irregular section editor
        option5 = 0
        # Option 6: Maximum X value of drawing area of irregular section editor
        option6 = 0
        # Option 7:  Maximum Y value of drawing area of irregular section editor
        option7 = 0
        # Option 8: Minimum X value of drawing area of irregular section editor
        option8 = 0
        # Option 9: Minimum Y value of drawing area of irregular section editor
        option9 = 0
        # Option 10:  Grid step in X of irregular section editor
        option10 = 0
        # Option 11:  Grid step in Y of irregular section editor
        option11 = 0
        # Option 12:  Grid snap step in X of irregular section editor
        option12 = 0
        # Option 13: Grid snap step in Y of irregular section editor
        option13 = 0

        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
            option13,
        ]
        self.__IrregularOptions = ",".join(map(str, options))

    def set_ties(self) -> None:
        """Set options related to ties."""
        # Ties' options for Irregular options do not need to be cared, options are set to default. We do not use regular section for this API
        # If Irregular Pattern (Section left panel | Irregular) is selected: Reserved. Do not edit.
        # Option 1: Reserved. Do not edit.
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        # Option 3: Reserved. Do not edit.
        option3 = 0
        options = [option1, option2, option3]
        self.__Ties = ",".join(map(str, options))

    def set_investigation_reinforcement(self) -> None:
        # Investigation Reinforcement's options for Irregular options do not need to be cared, options are set to default. We do not use regular section for this API
        # Option 1: Reserved. Do not edit.
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        # Option 3: Reserved. Do not edit.
        option3 = 0
        # Option 4: Reserved. Do not edit.
        option4 = 0
        # Option 5: Reserved. Do not edit.
        option5 = 0
        # Option 6: Reserved. Do not edit.
        option6 = 0
        # Option 7: Reserved. Do not edit.
        option7 = 0
        # Option 8: Reserved. Do not edit.
        option8 = 0
        # Option 9: Reserved. Do not edit.
        option9 = 0
        # Option 10: Reserved. Do not edit.
        option10 = 0
        # Option 11: Reserved. Do not edit.
        option11 = 0
        # Option 12:  Reserved. Do not edit.
        option12 = 0

        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
        ]
        self.__InvestigationReinforcement = ",".join(map(str, options))

    def set_design_reinforcement(self) -> None:
        # This section applies to design mode only
        # DesignReinforcement's options are not applied for Irregular options, options are set to default. We do not use regular section for this API
        # Option 1: Reserved. Do not edit.
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        # Option 3: Reserved. Do not edit.
        option3 = 0
        # Option 4: Reserved. Do not edit.
        option4 = 0
        # Option 5: Reserved. Do not edit.
        option5 = 0
        # Option 6: Reserved. Do not edit.
        option6 = 0
        # Option 7: Reserved. Do not edit.
        option7 = 0
        # Option 8: Reserved. Do not edit.
        option8 = 0
        # Option 9: Reserved. Do not edit.
        option9 = 0
        # Option 10: Reserved. Do not edit.
        option10 = 0
        # Option 11: Reserved. Do not edit.
        option11 = 0
        # Option 12:  Reserved. Do not edit.
        option12 = 0

        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
        ]
        self.__DesignReinforcement = ",".join(map(str, options))

    def set_investigation_section_dimensions(self) -> None:
        # InvestigationSectionDimensions's options are not applied for Irregular options, options are set to default. We do not use regular section for this API'
        # Option 1: Reserved. Do not edit.
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        options = [option1, option2]
        self.__InvestigationSectionDimensions = ",".join(map(str, options))

    def set_design_section_dimensions(self) -> None:
        # This section applies to design mode only
        # DesignSectionDimensions's options are not applied for Irregular options, options are set to default. We do not use regular section for this API
        option1 = 0
        # Option 2: Reserved. Do not edit.
        option2 = 0
        # Option 3: Reserved. Do not edit.
        option3 = 0
        # Option 4: Reserved. Do not edit.
        option4 = 0
        # Option 5: Reserved. Do not edit.
        option5 = 0
        # Option 6: Reserved. Do not edit.
        option6 = 0

        options = [option1, option2, option3, option4, option5, option6]
        self.__DesignSectionDimensions = ",".join(map(str, options))

    def set_material_properties(self, fc, ec, fy, es) -> None:
        # Option 1: Concrete strength, f’c
        option1 = fc
        # Option 2: Concrete modulus of elasticity, Ec
        option2 = ec
        # Option 3: Concrete maximum stress, fc
        option3 = 8
        # Option 4: Beta (1) for concrete stress block
        option4 = 0.85
        # Option 5: Concrete ultimate strain
        option5 = 0
        # Option 6: Steel yield strength, fy
        option6 = fy
        # Option 7: Steel modulus of elasticity, Es
        option7 = es
        # Option 8: Precast material for concrete. Only applicable for CSA A23.3-14 and CSA A23.3-04. 0-non-precast; 1-Precast
        option8 = 0
        # Option 9: Standard material for concrete 0-Non-standard; 1-Standard
        option9 = 1
        # Option 10: Standard material for reinforcing steel 0-Non-standard; 1-Standard
        option10 = 1
        # Option 11: Compression-controlled strain limit
        option11 = 0.002069
        options = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
        ]
        self.__MaterialProperties = ",".join(map(str, options))

    def set_reduction_factors(self) -> None:
        """There are 5 values separated by commas in one line in this section. These values are described
        below in the order they appear from left to right. (Capacity Reduction Factors/Material Resistance
        Factors in Definitions dialog | Properties | Reduction Factors)"""
        # Option 1: Phi(a) for axial compression
        option1 = 0.8
        # Option 2: Phi(b) for tension-controlled failure
        option2 = 0.9
        # Option 3: Phi(c) for compression-controlled failure
        option3 = 0.650000
        # Option 4: Reserved. Do not edit
        option4 = 0.1
        # Option 5: Minimum dimension of tied irregular sections for CSA A23.3-14 and CSA A23.3-19; 0-for all other cases
        option5 = 0
        options = [option1, option2, option3, option4, option5]
        self.__ReductionFactors = ",".join(map(str, options))

    def set_design_criteria(self) -> None:
        """There are 4 values separated by commas in one line in this section. These values are described
        below in the order they appear from left to right. (Reinforcement Ratio, Reinforcement Bars and
        Capacity Ratio in Definitions dialog | Properties | Reduction Factors)"""
        # Option 1: Minimum reinforcement ratio
        option1 = 0.010000
        # Option 2: Maximum reinforcement ratio
        option2 = 0.080000
        # Option 3: Minimum clear spacing between bars
        option3 = 1.500000
        # Option 4: Allowable Capacity (Ratio)
        option4 = 1.000000
        options = [option1, option2, option3, option4]
        self.__DesignCriteria = ",".join(map(str, options))

    def set_external_points_etabs(self, lst_PierSDShape, pierIndex) -> None:
        self.__ExternalPoints = connect_etabs.SPcolumnPierPoint(
            lst_PierSDShape, pierIndex
        )

    def set_external_points_cad(self, acadPath: str) -> None:
        """
        Get external points from an AutoCAD file.

        Args:
        - filePath (str): The path to the AutoCAD file.

        Returns:
        - ExternalPoints: External points in SPcol format.
        """
        acaddoc = read_acad.open_autocad_file(acadPath)
        vertices = read_acad.getVerticesList_fromCAD(acaddoc)
        vertices_spColFormat = read_acad.format_vertices_for_spcolumn(vertices)
        self.__ExternalPoints = vertices_spColFormat

    def set_internal_points(self) -> None:
        self.__InternalPoints = "0"

    def set_reinforcement_bars_auto(
        self, lst_PierSDShape, pierIndex, offset_distance, spacing, rebarArea
    ) -> None:

        lst_PierSDShape = connect_etabs.get_sdshape_pierPolygon()

        def offset_polyline(lst_PierSDShape, pierIndex, offset_distance):
            """
            Input Pier's polyline list of control point from SPcolumnPierPoint
            Return Values:
            list_segments (list) : List of  segments forming the polyline

            """
            SPcolumnPierPoint = list(lst_PierSDShape[pierIndex].values()).pop()
            num_points = len(SPcolumnPierPoint)
            lst_offset_points = []
            for i in range(num_points):
                # Find the previous and next points
                prev_point = SPcolumnPierPoint[i - 1]
                curr_point = SPcolumnPierPoint[i]
                next_point = SPcolumnPierPoint[(i + 1) % num_points]

                # Calculate vectors
                v1 = (curr_point[0] - prev_point[0], curr_point[1] - prev_point[1])
                v2 = (next_point[0] - curr_point[0], next_point[1] - curr_point[1])

                # Calculate perpendicular vectors
                v1_perp = (-v1[1], v1[0])
                v2_perp = (-v2[1], v2[0])

                # Normalize the perpendicular vectors
                length_v1_perp = (v1_perp[0] ** 2 + v1_perp[1] ** 2) ** 0.5
                length_v2_perp = (v2_perp[0] ** 2 + v2_perp[1] ** 2) ** 0.5
                v1_perp_norm = (
                    v1_perp[0] / length_v1_perp,
                    v1_perp[1] / length_v1_perp,
                )
                v2_perp_norm = (
                    v2_perp[0] / length_v2_perp,
                    v2_perp[1] / length_v2_perp,
                )

                # Calculate the bisector vector
                bisector = (
                    (v1_perp_norm[0] + v2_perp_norm[0]) / 2,
                    (v1_perp_norm[1] + v2_perp_norm[1]) / 2,
                )

                # Scale the bisector vector by the offset distance
                offset_vector = (
                    offset_distance * bisector[0],
                    offset_distance * bisector[1],
                )

                # Calculate the offset point
                offset_point = (
                    curr_point[0] + offset_vector[0],
                    curr_point[1] + offset_vector[1],
                )

                lst_offset_points.append(offset_point)
            return lst_offset_points

        def extract_segments(polyline):
            """
            Input polyline to be extracted as list
            Return Values:
            list_segments (list) : List of  segments forming the polyline

            """
            segments = []
            num_points = len(polyline)
            for i in range(num_points - 1):
                segment = [polyline[i], polyline[i + 1]]
                segments.append(segment)
            return segments

        def calculate_rebarpoints_for_segments(lst_offsettedpolyline_points, spacing):
            """
            @lst_polyline: list of offsetted polyline (with cover and half rebar diameter)
            @spacing: rebar spacing (user defined)
            Return Values:
            list_rebarsPts (list) : List of rebars' coordinates based on polyline segments and user-specified spacing
            """
            # Break polyline into segments
            segments = extract_segments(lst_offsettedpolyline_points)
            temp_list_rebarsPts = []

            for segment in segments:
                start_point, end_point = segment
                # Calculate the control points for the current segment
                rounded_distance = math.sqrt(
                    (end_point[0] - start_point[0]) ** 2
                    + (end_point[1] - start_point[1]) ** 2
                )
                num_points = math.ceil(rounded_distance / spacing)
                num_points = max(num_points, 2)
                x_diff = (end_point[0] - start_point[0]) / (num_points - 1)
                y_diff = (end_point[1] - start_point[1]) / (num_points - 1)
                control_points = [
                    (
                        round(start_point[0] + i * x_diff, 5),
                        round(start_point[1] + i * y_diff, 5),
                    )
                    for i in range(num_points)
                ]

                # Append the calculated rebars point to the list of unique values
                temp_list_rebarsPts.append(control_points)

            # Remove duplicates from the list of rebars point
            list_rebarsPts = []

            for sublist in temp_list_rebarsPts:
                for lst_coordinates in sublist:
                    list_rebarsPts.append(lst_coordinates)
            return list_rebarsPts

        def SPcolumn_RebarFormat(lst_rebarCoordinates, rebarArea):
            """
            Converts a list of tuples into a multiline string format with a parameter added to each tuple.

            Args:
            - lst_rebarCoordiantes (list): The original list of tuples or lists of rebar coordiantes.
            - parameter: rebarArea.

            Returns:
            - str: The multiline string.
            """

            def add_parameter_to_tuples(lst, rebarArea):
                if isinstance(lst[0], tuple):
                    return [(rebarArea,) + item for item in lst]
                elif isinstance(lst[0], list):
                    return [[rebarArea] + item for item in lst]
                else:
                    raise TypeError(
                        "Unsupported data format. Must be list of tuples or lists."
                    )

            def list_to_multiline_string(lst):
                return "\n".join([",".join(map(str, item)) for item in lst])

            total_rebar = len(lst_rebarCoordinates)
            modified_list = add_parameter_to_tuples(lst_rebarCoordinates, rebarArea)
            multiline_string_rebarPts = list_to_multiline_string(modified_list)
            multiline_string_rebarPts = (
                str(total_rebar) + "\n" + multiline_string_rebarPts
            )
            return multiline_string_rebarPts

        lst_offsettedpolyline_points = offset_polyline(
            lst_PierSDShape, pierIndex, offset_distance
        )
        lst_rebarCoordinates = calculate_rebarpoints_for_segments(
            lst_offsettedpolyline_points, spacing
        )

        self.__ReinforcementBars = SPcolumn_RebarFormat(lst_rebarCoordinates, rebarArea)

    def set_reinforcement_bars_cad(self, acadPath: str) -> None:
        acaddoc = read_acad.open_autocad_file(acadPath)
        rebar = read_acad.get_rebarinfo_fromCAD(acaddoc)
        rebar_spColFormat = read_acad.format_rebar_info_for_spcolumn(rebar)
        parts = self.UserOptions.split(",")
        parts[16] = str(len(rebar))
        self.UserOptions = ",".join(parts)
        self.__ReinforcementBars = rebar_spColFormat

    def set_factored_loads(self, forceSet) -> None:
        self.__FactoredLoads = forceSet

    def set_slenderness_column(self) -> None:
        """This section contains 2 lines describing slenderness parameters for column being designed. The
        first line is for X-axis parameters, and the second line is for Y-axis parameters.
        There are 9 values6 separated by commas in each line. These values are described below in the
        order they appear from left to right. (Design Column X Axis and Design Column Y  Axis in
        Slenderness dialog | Columns)"""

        # Typically we set to "No" to slenderness consideration, the following code as below
        # Param1
        columnclearheight = 0
        # Param2: k_nonsway
        k_nonsway_X = 0
        k_nonsway_Y = 0
        # Param2: k_sway
        k_sway_X = 0
        k_sway_Y = 0
        # Param4: 0-Sway frame; 1-Nonsway frame
        param4_X = 0
        param4_Y = 0
        # Param5: 0-Compute ‘k’ factors; 1-Input k factors
        param5 = 0
        # Param6: (ΣPc)/Pc
        param6 = 0
        # Param7: (ΣPu)/Pu
        param7 = 0
        """Param8 :0-Do not ignore moment magnification along column length in sway frames; 
        1-Ignore moment magnification along column length in sway frames. Use for ACI 318-11 and ACI 318-08 only. For all other codes the value must be 0."""
        param8_X = 0
        param8_Y = 0
        # param9. Column end conditions. Values for conditions per SP column manual [0,5]
        param9_X = 0
        param9_Y = 0

        SlendernessColumn_Xaxis = [
            columnclearheight,
            k_nonsway_X,
            k_sway_X,
            param4_X,
            param5,
            param6,
            param7,
            param8_X,
            param9_X,
        ]
        SlendernessColumn_Xaxis_string = ",".join(map(str, SlendernessColumn_Xaxis))
        SlendernessColumn_Yaxis = [
            columnclearheight,
            k_nonsway_Y,
            k_sway_Y,
            param4_Y,
            param5,
            param6,
            param7,
            param8_Y,
            param9_Y,
        ]
        SlendernessColumn_Yaxis_string = ",".join(map(str, SlendernessColumn_Yaxis))
        self.__SlendernessColumn = (
            f"{SlendernessColumn_Xaxis_string}\n{SlendernessColumn_Yaxis_string}"
        )

    def set_slenderness_column_AboveAndBelow(self) -> None:
        """This section contains 2 lines describing slenderness parameters for column above and column
        below. The first line is for column above, and the second line is for column below. (Columns
        Above/Below in Slenderness dialog | Columns)"""

        # Param1: 1. 0-No column specified; 1-Circular column specified; 2-Rectangular column specified; 3-Column above section taken as design column section
        param1_above = 0
        param1_below = 0
        # Param2: Column Height
        param2_above = 0
        param2_below = 0
        # Param2: Column width (along X)
        param3_above = 0
        param3_below = 0
        # Param4: Column depth (along Y)
        param4_above = 0
        param4_below = 0
        # Param5: Concrete compressive strength, f’c
        param5_above = 0
        param5_below = 0
        # Param6: Concrete modulus of elasticity, Ec
        param6_above = 0
        param6_below = 0
        SlendernessColumn_Above = [
            param1_above,
            param2_above,
            param3_above,
            param4_above,
            param5_above,
            param6_above,
        ]
        SlendernessColumn_Above_string = ",".join(map(str, SlendernessColumn_Above))
        SlendernessColumn_Below = [
            param1_below,
            param2_below,
            param3_below,
            param4_below,
            param5_below,
            param6_below,
        ]
        SlendernessColumn_Below_string = ",".join(map(str, SlendernessColumn_Below))
        self.__SlendernessColumnAboveAndBelow = (
            f"{SlendernessColumn_Above_string}\n{SlendernessColumn_Below_string}"
        )

    def set_slenderness_beams(self) -> None:
        # 0-Rectangular Beam specified; 1-No beam specified; 2-Rigid beam specified
        param1_1 = 0
        param1_2 = 0
        param1_3 = 0
        param1_4 = 0
        param1_5 = 0
        param1_6 = 0
        param1_7 = 0
        param1_8 = 0

        # Beam span length (c/c)
        param2_1 = 0
        param2_2 = 0
        param2_3 = 0
        param2_4 = 0
        param2_5 = 0
        param2_6 = 0
        param2_7 = 0
        param2_8 = 0

        # Beam width
        param3_1 = 0
        param3_2 = 0
        param3_3 = 0
        param3_4 = 0
        param3_5 = 0
        param3_6 = 0
        param3_7 = 0
        param3_8 = 0

        # Beam depth
        param4_1 = 0
        param4_2 = 0
        param4_3 = 0
        param4_4 = 0
        param4_5 = 0
        param4_6 = 0
        param4_7 = 0
        param4_8 = 0

        # Beam section moment of inertia
        param5_1 = 0
        param5_2 = 0
        param5_3 = 0
        param5_4 = 0
        param5_5 = 0
        param5_6 = 0
        param5_7 = 0
        param5_8 = 0

        # Concrete compressive strength, f’c
        param6_1 = 0
        param6_2 = 0
        param6_3 = 0
        param6_4 = 0
        param6_5 = 0
        param6_6 = 0
        param6_7 = 0
        param6_8 = 0

        # Concrete modulus of elasticity, Ec
        param7_1 = 0
        param7_2 = 0
        param7_3 = 0
        param7_4 = 0
        param7_5 = 0
        param7_6 = 0
        param7_7 = 0
        param7_8 = 0

        """This section contains 8 lines. Each line describes a beam. 
            Line 1: X-Beam (perpendicular to X), Above Left 
            Line 2: X-Beam (perpendicular to X), Above Right 
            Line 3: X-Beam (perpendicular to X), Below Left 
            Line 4: X-Beam (perpendicular to X), Below Right 
            Line 5: Y-Beam (perpendicular to Y), Above Left 
            Line 6: Y-Beam (perpendicular to Y), Above Right 
            Line 7: Y-Beam (perpendicular to Y), Below Left 
            Line 8: Y-Beam (perpendicular to Y), Below Right """

        beam1 = [param1_1, param2_1, param3_1, param4_1, param5_1, param6_1, param7_1]
        beam2 = [param1_2, param2_2, param3_2, param4_2, param5_2, param6_2, param7_2]
        beam3 = [param1_3, param2_3, param3_3, param4_3, param5_3, param6_3, param7_3]
        beam4 = [param1_4, param2_4, param3_4, param4_4, param5_4, param6_4, param7_4]
        beam5 = [param1_5, param2_5, param3_5, param4_5, param5_5, param6_5, param7_5]
        beam6 = [param1_6, param2_6, param3_6, param4_6, param5_6, param6_6, param7_6]
        beam7 = [param1_7, param2_7, param3_7, param4_7, param5_7, param6_7, param7_7]
        beam8 = [param1_8, param2_8, param3_8, param4_8, param5_8, param6_8, param7_8]

        beam1_string = ",".join(map(str, beam1))
        beam2_string = ",".join(map(str, beam2))
        beam3_string = ",".join(map(str, beam3))
        beam4_string = ",".join(map(str, beam4))
        beam5_string = ",".join(map(str, beam5))
        beam6_string = ",".join(map(str, beam6))
        beam7_string = ",".join(map(str, beam7))
        beam8_string = ",".join(map(str, beam8))

        self.__SlendernessBeams = f"{beam1_string}\n{beam2_string}\n{beam3_string}\n{beam4_string}\n{beam5_string}\n{beam6_string}\n{beam7_string}\n{beam8_string}"

    def set_EI(self) -> None:
        self.__EI = 0.000000

    def set_sldOptFact(self) -> None:
        self.__SldOptFact = 0

    def set_PhiDelta(self) -> None:
        self.__PhiDelta = 0.750000

    def set_crackedI(self) -> None:
        """There are 2 values separated by commas in one line in this section. These values are described
        below in the order they appear from left to right. (Beams and Columns Cracked Section
        Coefficients in Slenderness dialog | Properties | Slenderness Factors)"""
        CrackedI_Beam = 0.35
        CrackedI_Column = 0.7
        CrackedI = [CrackedI_Beam, CrackedI_Column]
        self.__CrackedI = ",".join(map(str, CrackedI))

    def set_service_loads(self) -> None:
        self.__ServiceLoads = 0

    def set_load_combinations(self) -> None:
        self.__LoadCombinations = """13
1.400000,0.000000,0.000000,0.000000,0.000000
1.200000,1.600000,0.000000,0.000000,0.500000
1.200000,1.000000,0.000000,0.000000,1.600000
1.200000,0.000000,0.800000,0.000000,1.600000
1.200000,1.000000,1.600000,0.000000,0.500000
0.900000,0.000000,1.600000,0.000000,0.000000
1.200000,0.000000,-0.800000,0.000000,1.600000
1.200000,1.000000,-1.600000,0.000000,0.500000
0.900000,0.000000,-1.600000,0.000000,0.000000
1.200000,1.000000,0.000000,1.000000,0.200000
0.900000,0.000000,0.000000,1.000000,0.000000
1.200000,1.000000,0.000000,-1.000000,0.200000
0.900000,0.000000,0.000000,-1.000000,0.000000"""

    def set_bar_group_type(self) -> None:
        """There is 1 value in this section. (Bar Set drop-down list on menu Options | Reinforcement…)
        0-User Defined
        1. ASTM615
        2. CSA G30.18
        3. prEN 10080
        4. ASTM615M"""
        self.__BarGroupType = "1"

    def set_user_defined_bars(self) -> None:
        self.__UserDefinedBars = ""

    def set_sustained_load_factors(self) -> None:
        """There are 5 values separated by commas in one line in this section. Each value respectively
        represents percentage of Dead, Live, Wind, EQ, and Snow load case that is considered sustained
        (Load Cases in Definitions dialog | Load Case/Combo.)."""
        DLpercentage = 100.00
        LLpercentage = 0.00
        Wpercentage = 0.00
        EQpercentage = 0.00
        Spercentage = 0.00
        SustainedLoadFactors = [
            DLpercentage,
            LLpercentage,
            Wpercentage,
            EQpercentage,
            Spercentage,
        ]
        self.__SustainedLoadFactors = ",".join(map(str, SustainedLoadFactors))

    def get_irregular_options(self):
        return self.__IrregularOptions

    def set_immutable_CTIfields(self):
        CTIfile.set_irregular_options(self)
        CTIfile.set_ties(self)
        CTIfile.set_investigation_reinforcement(self)
        CTIfile.set_design_reinforcement(self)
        CTIfile.set_investigation_section_dimensions(self)
        CTIfile.set_design_section_dimensions(self)
        CTIfile.set_reduction_factors(self)
        CTIfile.set_design_criteria(self)
        CTIfile.set_internal_points(self)
        CTIfile.set_slenderness_column(self)
        CTIfile.set_slenderness_column_AboveAndBelow(self)
        CTIfile.set_slenderness_beams(self)
        CTIfile.set_EI(self)
        CTIfile.set_sldOptFact(self)
        CTIfile.set_PhiDelta(self)
        CTIfile.set_crackedI(self)
        CTIfile.set_service_loads(self)
        CTIfile.set_load_combinations(self)
        CTIfile.set_bar_group_type(self)
        CTIfile.set_user_defined_bars(self)
        CTIfile.set_sustained_load_factors(self)

    def CTIbuilder(self) -> str:
        """
        Builds the content of the CTI file as a string.

        Returns:
            str: The constructed CTI file content.
        """
        return (
            f"#spColumn Text Input (CTI) File\n"
            f"[spColumn Version]\n{self.__SpColumnVersion}\n"
            f"[Project]\n{self.__ProjectName}\n"
            f"[Column ID]\n{self.__ColumnID}\n"
            f"[Engineer]\n{self.__Engineer}\n"
            f"[Investigation Run Flag]\n{self.__InvestigationRunFlag}\n"
            f"[Design Run Flag]\n{self.__DesignRunFlag}\n"
            f"[Slenderness Flag]\n{self.__SlendernessFlag}\n"
            f"[User Options]\n{self.UserOptions}\n"
            f"[Irregular Options]\n{self.__IrregularOptions}\n"
            f"[Ties]\n{self.__Ties}\n"
            f"[Investigation Reinforcement]\n{self.__InvestigationReinforcement}\n"
            f"[Design Reinforcement]\n{self.__DesignReinforcement}\n"
            f"[Investigation Section Dimensions]\n{self.__InvestigationSectionDimensions}\n"
            f"[Design Section Dimensions]\n{self.__DesignSectionDimensions}\n"
            f"[Material Properties]\n{self.__MaterialProperties}\n"
            f"[Reduction Factors]\n{self.__ReductionFactors}\n"
            f"[Design Criteria]\n{self.__DesignCriteria}\n"
            f"[External Points]\n{self.__ExternalPoints}\n"
            f"[Internal Points]\n{self.__InternalPoints}\n"
            f"[Reinforcement Bars]\n{self.__ReinforcementBars}\n"
            f"[Factored Loads]\n{self.__FactoredLoads}\n"
            f"[Slenderness: Column]\n{self.__SlendernessColumn}\n"
            f"[Slenderness: Column Above And Below]\n{self.__SlendernessColumnAboveAndBelow}\n"
            f"[Slenderness: Beams]\n{self.__SlendernessBeams}\n"
            f"[EI]\n{self.__EI}\n"
            f"[SldOptFact]\n{self.__SldOptFact}\n"
            f"[Phi_Delta]\n{self.__PhiDelta}\n"
            f"[Cracked I]\n{self.__CrackedI}\n"
            f"[Service Loads]\n{self.__ServiceLoads}\n"
            f"[Load Combinations]\n{self.__LoadCombinations}\n"
            f"[BarGroupType]\n{self.__BarGroupType}\n"
            f"[User Defined Bars]\n{self.__UserDefinedBars}\n"
            f"[Sustained Load Factors]\n{self.__SustainedLoadFactors}\n"
        )

    def write_CTIfile_to_file(self, file_path) -> None:
        with open(file_path, "w") as file:
            file.write(self.CTIbuilder())

    def ColumnID_connect_etabs(lst_PierSDShape, pierIndex) -> str:
        ColumnID = connect_etabs.SPcolumnPierLabel(lst_PierSDShape, pierIndex)
        return ColumnID


def main():
    return True


def ab():
    return None


if __name__ == "__main__":
    CTIUserOptions = UserOptions()
    CTIUserOptions.option1 = 1
    newCTIfile = CTIfile()
    print(newCTIfile.UserOptions)
    newCTIfile.UserOptions = CTIUserOptions.set_user_options_CTIformat()
    print(newCTIfile.UserOptions)
