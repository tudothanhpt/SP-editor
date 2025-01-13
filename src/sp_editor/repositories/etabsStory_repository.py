from contextlib import AbstractContextManager
from typing import Callable, List, Sequence

import pandas as pd
from sqlmodel import select, Session

from sp_editor.models.models import Level, PierLabel


class EtabsStoryRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, params: list):
        story, height = params
        with self.session_factory() as session:
            level = Level(
                story=story,
                height=height,
            )
            session.add(level)
            session.commit()
            session.refresh(level)
            return level

    def import_stories(self, stories: pd.DataFrame):
        """
        Parses the provided stories dataframe from Etabs and update the database:
            - delete any existing story data
            - Insert new story records from the DataFrame
        :param stories:  stories dataframe
        """
        with self.session_factory() as session:
            # check for existing data
            existing_stories = session.exec(select(Level)).all()

            # if data exists, delete all record
            if existing_stories:
                for story in existing_stories:
                    session.delete(story)
                session.commit()
            # add new records from dataframe
            for _, row in stories.iterrows():
                story = Level(story=row["Story"], height=row["Height"])
                session.add(story)
            session.commit()

    def get_all_levels(self) -> Sequence[Level]:
        """Retrieve all levels."""
        with self.session_factory() as session:
            try:
                stmt = select(Level)
                return session.exec(stmt).all()
            except Exception as e:
                print(f"Error getting all levels: {e}")
                return []

    def get_levels_with_tiers(self) -> Sequence[Level]:
        """Retrieve all levels that have a tier assigned (not NULL or empty)."""
        with self.session_factory() as session:
            try:
                stmt = select(Level).where(
                    (Level.tier.is_not(None)) & (Level.tier != "")
                )
                return session.exec(stmt).all()
            except Exception as e:
                print(f"Error retrieving levels with tiers: {e}")
                return []

    def get_piers_by_levels(self, levels: List[str]) -> List[str]:
        """Retrieve pier labels for the specified levels."""
        if not levels:
            return []

        with self.session_factory() as session:
            try:
                stmt = (
                    select(PierLabel.piername)
                    .join(Level)
                    .where(Level.story.in_(levels))
                    .distinct()
                )
                return [label for label in session.exec(stmt) if label]
            except Exception as e:
                print(f"Error getting pier labels: {e}")
                return []

    def add_tier_to_levels(self, levels: List[str], tier_name: str) -> Sequence[Level]:
        """Adds a tier name to the specified levels."""
        if not levels:
            return []

        with self.session_factory() as session:
            try:
                stmt = select(Level).where(Level.story.in_(levels))
                level_objects = session.exec(stmt).all()

                if not level_objects:
                    return []

                for level in level_objects:
                    level.tier = tier_name

                session.add_all(level_objects)
                session.commit()

                for level in level_objects:
                    session.refresh(level)
                return level_objects
            except Exception as e:
                print(f"Error adding tier to levels: {e}")
                session.rollback()
                return []

    def remove_tier(self, tier_name: str) -> int:
        """Removes a tier from all levels with the specified tier name."""
        with self.session_factory() as session:
            try:
                stmt = select(Level).where(Level.tier == tier_name)
                level_objects = session.exec(stmt).all()

                for level in level_objects:
                    level.tier = None

                session.add_all(level_objects)
                session.commit()
                return len(level_objects)
            except Exception as e:
                print(f"Error removing tier: {e}")
                session.rollback()
                return 0
