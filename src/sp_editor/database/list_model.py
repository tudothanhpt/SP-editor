from typing import *

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


class ListModel(QAbstractListModel):
    def __init__(self, items=None, original_order=None):
        """
        Initialize a ListModel object.

        Args:
            items (list, optional): The initial list of items. Defaults to an empty list.
            original_order (dict, optional): A dictionary mapping items to their original order. 
                                            Defaults to None.
        """
        super().__init__()

        # Initialize the list of items
        self.items = items if items else []

        # Store the original order of items
        # The original order is a dictionary mapping items to their original index in the list.
        # This is used to preserve the ordering of items when sorting.
        self.original_order = original_order if original_order else {}

    def data(
            self,
            index: QModelIndex,
            role: Qt.ItemDataRole
    ) -> str | None:
        """
        Return the data at the given index.

        Args:
            index (QModelIndex): The index of the item to retrieve data for.
            role (Qt.ItemDataRole): The role of the data to retrieve.

        Returns:
            str | None: The data at the given index if the role is DisplayRole, 
                        otherwise None.
        """
        if role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        """
        Return the number of items in the list.

        Args:
            index (QModelIndex): The index of the parent item. Defaults to an empty QModelIndex.

        Returns:
            int: The number of items in the list.
        """
        return len(self.items)

    def add_items(self, items: List[Tuple[str, int]]) -> None:
        """
        Adds a list of items to the model.

        Args:
            items (List[Tuple[str, int]]): A list of tuples containing the item and its original index.

        Returns:
            None
        """
        # Begin inserting rows
        start_row = self.rowCount(QModelIndex())
        end_row = start_row + len(items) - 1
        self.beginInsertRows(QModelIndex(), start_row, end_row)
        for item, original_index in items:
            self.items.append(item)
            # Update the original order if not already present
            if item not in self.original_order:
                self.original_order[item] = original_index
        # End inserting rows
        self.endInsertRows()

    def remove_item_by_value(self, item: str) -> None:
        """
        Remove an item from the model.

        Args:
            item (str): The item to be removed.

        Returns:
            None
        """
        # Find the row of the item and remove it
        row = self.items.index(item)
        self.beginRemoveRows(QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def sort_items_by_original_order(self) -> None:
        """
        Sorts the items in the model based on their original order.

        Returns:
            None
        """
        # Sort items based on their original order
        self.items.sort(key=lambda item: self.original_order[item])
        # Emit layout changed signal to update the view
        self.layoutChanged.emit()

    def get_items_with_indices(self) -> List[Tuple[str, int]]:
        """
        Return a list of tuples containing items and their indices.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing the item (str) and its original index (int).
        """
        current_item: List[Tuple[str, int]] = [(item, self_order[item]) for item, _ in
                                               zip(self.items, self.original_order.values())]
        return current_item
