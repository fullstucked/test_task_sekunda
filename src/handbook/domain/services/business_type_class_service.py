from __future__ import annotations

from domain.entities.business_type import BusinessType
from domain.exceptions.base import DomainBusinessRuleError


class BusinessTypeClassificationService:
    """
    Read-only domain service for analyzing BusinessType hierarchies.
    Provides advanced tree traversal and analysis methods.
    """

    MAX_HIERARCHY_DEPTH = 3

    @classmethod
    async def validate_hierarchy_depth(cls, node: BusinessType) -> None:
        """
        Validate that the business type hierarchy does not exceed max depth.

        :param node: Business type to validate
        :raises DomainBusinessRuleError: If hierarchy depth exceeds limit
        """

        def get_depth(bt: BusinessType, current_depth: int = 0) -> int:
            if not bt.children:
                return current_depth
            return max(get_depth(child, current_depth + 1) for child in bt.children)

        depth = get_depth(node)
        if depth > cls.MAX_HIERARCHY_DEPTH:
            raise DomainBusinessRuleError(
                f"Business type hierarchy exceeds maximum allowed depth of {cls.MAX_HIERARCHY_DEPTH}",
                context={"max_depth": cls.MAX_HIERARCHY_DEPTH, "current_depth": depth},
            )

    @classmethod
    async def get_all_descendants(cls, root: BusinessType) -> list[BusinessType]:
        """
        Retrieve all descendant business types with depth validation.

        :param root: Root business type
        :return: List of all descendant business types
        """
        await cls.validate_hierarchy_depth(root)

        result: list[BusinessType] = []

        def dfs(node: BusinessType) -> None:
            for child in node.children:
                result.append(child)
                dfs(child)

        dfs(root)
        return result

    @classmethod
    async def get_all_ancestors(cls, node: BusinessType) -> list[BusinessType]:
        """
        Retrieve all ancestor business types.

        :param node: Business type to find ancestors for
        :return: List of ancestor business types
        """
        result: list[BusinessType] = []
        current = node.parent

        while current:
            result.append(current)
            current = current.parent

        return result

    @classmethod
    async def get_leaf_nodes(cls, root: BusinessType) -> list[BusinessType]:
        """
        Find all leaf nodes in the business type hierarchy.

        :param root: Root business type to start search from
        :return: List of leaf business types
        """
        await cls.validate_hierarchy_depth(root)

        leaves: list[BusinessType] = []

        def dfs(node: BusinessType) -> None:
            if not node.children:
                leaves.append(node)
                return
            for child in node.children:
                dfs(child)

        dfs(root)
        return leaves
