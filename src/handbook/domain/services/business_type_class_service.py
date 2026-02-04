from __future__ import annotations

from domain.entities.business_type import BusinessType


class BusinessTypeClassificationService:
    """
    Read-only domain service for analyzing BusinessType hierarchies.
    """

    @staticmethod
    def get_all_descendants(root: BusinessType) -> list[BusinessType]:
        """
        Retrieve all descendant business types.
        """
        result: list[BusinessType] = []
        stack = list(root.children)

        while stack:
            node = stack.pop()
            result.append(node)
            stack.extend(node.children)

        return result

    @staticmethod
    def get_all_ancestors(node: BusinessType) -> list[BusinessType]:
        """
        Retrieve all ancestor business types.
        """
        result: list[BusinessType] = []
        current = node.parent

        while current:
            result.append(current)
            current = current.parent

        return result

    @staticmethod
    def get_leaf_nodes(root: BusinessType) -> list[BusinessType]:
        """
        Find all leaf nodes in the business type hierarchy.
        """
        leaves: list[BusinessType] = []
        stack = [root]

        while stack:
            node = stack.pop()
            if not node.children:
                leaves.append(node)
            else:
                stack.extend(node.children)

        return leaves
