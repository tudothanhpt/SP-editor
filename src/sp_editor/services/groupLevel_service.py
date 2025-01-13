from typing import List

from sp_editor.repositories.etabsStory_repository import EtabsStoryRepository


class GroupLevelService:
    def __init__(self, etabsStory_repository: EtabsStoryRepository):
        self.etabsStory_repository = etabsStory_repository

    def add_tier_to_levels(self, levels: List[str], tier_name: str):
        """
        calling repository function to add tier to related level
        :param levels:
        :param tier_name:
        """
        self.etabsStory_repository.add_tier_to_levels(levels, tier_name)

    def remove_tier_from_levels(self, tier_name: str):
        """
        Removes the specified tier name from all group levels.

        Args:
            tier_name: The tier name to remove.

        Returns:
            The number of GroupLevel objects updated.
        """
        self.etabsStory_repository.remove_tier(tier_name)

    def get_all_levels(self):
        """Retrieves all GroupLevel objects from the repository."""
        return self.etabsStory_repository.get_all_levels()

    def get_levels_with_tiers(self):
        """Retrieves all level from a database without a tier assignment"""
        levels = self.etabsStory_repository.get_levels_with_tiers()
        return list(set(level.story for level in levels if level.story))

    def get_piers_by_levels(self, levels: List[str]) -> List[str]:
        """Retrieve pier labels for the specified levels."""
        return self.etabsStory_repository.get_piers_by_levels(levels)

    def get_all_tier_names(self) -> List[str]:
        """Retrieve all distinct tier names."""
        levels = self.etabsStory_repository.get_all_levels()
        return list(set(level.tier for level in levels if level.tier))
