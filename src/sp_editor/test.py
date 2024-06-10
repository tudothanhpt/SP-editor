from sqlmodel import Field, SQLModel, create_engine, Relationship, Session, select
from typing import List, Optional
from natsort import natsorted
from core.connect_etabs import get_story_infor


class Level(SQLModel, table=True):
    name: str = Field(default=None, primary_key=True)
    height: str = Field(default=None)


class Pierlabel(SQLModel, table=True):
    story: str = Field(default=None, primary_key=True, max_length=50)
    label: str = Field(default=None, primary_key=True, max_length=50)
    unique_name: Optional[int] = Field(default=None)
    pier_name: Optional[str] = Field(default=None, max_length=50)

    pierforces: List["Pierforce"] = Relationship(back_populates="pierlabel")
    grouplevels: List["Grouplevel"] = Relationship(back_populates="pierlabel")


class Pierforce(SQLModel, table=True):
    story: str = Field(default=None, foreign_key="pierlabel.story", primary_key=True, max_length=50)
    pier: str = Field(default=None, primary_key=True, max_length=50)
    combo: Optional[str] = Field(default=None, max_length=50)
    location: Optional[str] = Field(default=None, max_length=50)
    p: Optional[float] = Field(default=None)
    v2: Optional[float] = Field(default=None)
    v3: Optional[float] = Field(default=None)
    t: Optional[float] = Field(default=None)
    m2: Optional[float] = Field(default=None)
    m3: Optional[float] = Field(default=None)

    pierlabel: Pierlabel = Relationship(back_populates="pierforces")


class Grouplevel(SQLModel, table=True):
    tier: int = Field(default=None, primary_key=True)
    story: str = Field(default=None, foreign_key="pierlabel.story", primary_key=True, max_length=50)

    pierlabel: Pierlabel = Relationship(back_populates="grouplevels")


# Create the database engine
engine = create_engine("sqlite:///database1.db")

# Create the tables in the database
SQLModel.metadata.create_all(engine)


# Function to insert data
def insert_data():
    pierlabel_data = [
        ('Story10', 'W1', 235, 'P2'),
        ('Story10', 'W27', 306, 'P3'),
        ('Story9', 'W1', 209, 'P2'),
        ('Story9', 'W27', 301, 'P3'),
        ('Story8', 'W1', 183, 'P2'),
        ('Story8', 'W27', 296, 'P3'),
        ('Story7', 'W1', 157, 'P2'),
        ('Story7', 'W27', 291, 'P3'),
        ('Story6', 'W1', 131, 'P2'),
        ('Story6', 'W27', 286, 'P3'),
        ('Story5', 'W1', 105, 'P2'),
        ('Story5', 'W27', 281, 'P3'),
        ('Story4', 'W1', 79, 'P2'),
        ('Story4', 'W27', 276, 'P3'),
        ('Story3', 'W1', 53, 'P2'),
        ('Story3', 'W27', 271, 'P3'),
        ('Story2', 'W1', 27, 'P2'),
        ('Story2', 'W27', 266, 'P3'),
        ('Story1', 'W1', 1, 'P2'),
        ('Story1', 'W27', 261, 'P3')
    ]

    pierforce_data = [
        ('Story10', 'P2', 'DWalS1-1', 'Bottom', -300.287, 14.004, -46.481, -57.2077, -150.3493, 186.9327),
        ('Story10', 'P3', 'DWalS1-1', 'Bottom', -304.022, 51.796, 13.083, -361.0938, -143.8063, -361.9353),
        ('Story9', 'P2', 'DWalS1-1', 'Bottom', -633.274, 10.042, -66.695, -45.2754, -150.1865, 296.2948),
        ('Story9', 'P3', 'DWalS1-1', 'Bottom', -612.544, 65.787, 11.782, -330.1051, -197.1488, -550.6412),
        ('Story8', 'P2', 'DWalS1-1', 'Bottom', -960.955, 8.55, -64.106, -20.0934, -159.7155, 351.3244),
        ('Story8', 'P3', 'DWalS1-1', 'Bottom', -912.862, 65.849, 8.547, -192.5389, -293.9429, -663.8083),
        ('Story7', 'P2', 'DWalS1-1', 'Bottom', -1282.923, 3.42, -56.74, -1.7765, -145.3329, 368.7717),
        ('Story7', 'P3', 'DWalS1-1', 'Bottom', -1201.067, 56.034, 4.489, -57.4006, -301.8745, -788.1996),
        ('Story6', 'P2', 'DWalS1-1', 'Bottom', -1587.707, 0.829, -44.868, 19.4377, -186.1316, 384.2991),
        ('Story6', 'P3', 'DWalS1-1', 'Bottom', -1476.647, 44.337, 2.255, 19.2037, -212.0839, -943.6035),
        ('Story5', 'P2', 'DWalS1-1', 'Bottom', -1877.592, 0.106, -33.888, 34.9366, -244.6487, 393.632),
        ('Story5', 'P3', 'DWalS1-1', 'Bottom', -1740.822, 33.766, -0.851, 41.361, -146.6601, -1137.3223),
        ('Story4', 'P2', 'DWalS1-1', 'Bottom', -2157.993, -0.768, -25.591, 35.7568, -291.478, 395.1268),
        ('Story4', 'P3', 'DWalS1-1', 'Bottom', -1992.933, 24.369, -0.627, 48.0712, -115.7591, -1349.3117),
        ('Story3', 'P2', 'DWalS1-1', 'Bottom', -2430.062, -1.169, -18.123, 33.5044, -314.0193, 402.5578),
        ('Story3', 'P3', 'DWalS1-1', 'Bottom', -2220.944, 17.507, -1.056, 62.7924, -11.2398, -1443.295),
        ('Story2', 'P2', 'DWalS1-1', 'Bottom', -2689.559, -2.337, -12.83, 21.9896, -370.9106, 381.3587),
        ('Story2', 'P3', 'DWalS1-1', 'Bottom', -2436.022, 12.006, -2.588, 30.8556, 39.5745, -1526.1079),
        ('Story1', 'P2', 'DWalS1-1', 'Bottom', -2934.959, -0.728, -13.262, 16.5461, -541.4748, 374.6771),
        ('Story1', 'P3', 'DWalS1-1', 'Bottom', -2638.105, 12.846, -0.795, 52.821, 90.5172, -1544.2652)
    ]

    grouplevel_data = [
        (1, 'Story1'),
        (1, 'Story2'),
        (1, 'Story3'),
        (1, 'Story4'),
        (1, 'Story5'),
        (2, 'Story6'),
        (2, 'Story7'),
        (2, 'Story8'),
        (2, 'Story9'),
        (2, 'Story10')
    ]

    with Session(engine) as session:
        for data in pierlabel_data:
            session.add(Pierlabel(story=data[0], label=data[1], unique_name=data[2], pier_name=data[3]))

        for data in pierforce_data:
            session.add(Pierforce(story=data[0], pier=data[1], combo=data[2], location=data[3], p=data[4], v2=data[5],
                                  v3=data[6], t=data[7], m2=data[8], m3=data[9]))

        for data in grouplevel_data:
            session.add(Grouplevel(tier=data[0], story=data[1]))

        session.commit()


# Insert the data into the database
insert_data()


# Function to execute the query
def execute_query():
    with Session(engine) as session:
        # Define the query
        statement = (
            select(Pierforce)
            .join(Pierlabel, Pierforce.story == Pierlabel.story)
            .where(Pierforce.pier == Pierlabel.pier_name)
            .join(Grouplevel, Pierlabel.story == Grouplevel.story)
            .where(Grouplevel.tier == 2)
            .where(Pierforce.pier == 'P2')
        )

        # Execute the query and fetch results
        results = session.exec(statement).all()

        # Print the results
        for result in results:
            print(result)


# Execute the query
execute_query()
