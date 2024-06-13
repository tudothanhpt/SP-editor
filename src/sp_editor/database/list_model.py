from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


# Class 3: List model
class ListModel(QAbstractListModel):
    def __init__(self, items=None):
        super().__init__()
        # Initialize the list of items
        self.items = items if items else []
        # Store the original order of items
        self.original_order = {item: index for index, item in enumerate(self.items)}

    def data(self, index, role):
        # Return the data at the given index
        if role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, index = None):
        # Return the number of items in the list
        return len(self.items)

    def add_items(self, items):
        # Begin inserting rows
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()) + len(items) - 1)
        for item, original_index in items:
            self.items.append(item)
            # Update the original order if not already present
            if item not in self.original_order:
                self.original_order[item] = original_index
        # End inserting rows
        self.endInsertRows()

    def remove_item_by_value(self, item):
        # Find the row of the item and remove it
        row = self.items.index(item)
        self.beginRemoveRows(QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def sort_items_by_original_order(self):
        # Sort items based on their original order
        self.items.sort(key=lambda item: self.original_order[item])
        # Emit layout changed signal to update the view
        self.layoutChanged.emit()
    
    def get_items_with_indices(self):
        """Return a list of tuples containing items and their indices."""
        current_item = [(self.data(self.index(row, 0), Qt.DisplayRole), row) for row in range(self.rowCount())]
        return current_item
