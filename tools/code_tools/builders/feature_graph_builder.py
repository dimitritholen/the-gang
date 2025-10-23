"""
Feature graph builder: orchestrate parsing markdown → entities → JSONL
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from ..graph import GraphStore, Entity, Relationship
from ..parsers.requirements_parser import RequirementsParser


class FeatureGraphBuilder:
    """Build feature knowledge graph from markdown files"""

    def __init__(self, memory_dir: Path):
        self.store = GraphStore(memory_dir)

    def build_from_requirements(self, markdown_path: Path, feature_slug: str) -> Dict[str, Any]:
        """
        Parse requirements markdown and build graph.
        Returns: {feature_id, entity_count, relationship_count}
        """
        parser = RequirementsParser(markdown_path)
        entities, relationships = parser.parse()

        # Save to store
        self.store.save_graph(feature_slug, entities, relationships)

        return {
            'feature_id': entities[0].id if entities else None,
            'feature_slug': feature_slug,
            'entity_count': len(entities),
            'relationship_count': len(relationships),
            'source_file': str(markdown_path)
        }

    def build_from_conventions(self, markdown_path: Path, feature_slug: str) -> Dict[str, Any]:
        """
        Parse conventions markdown and build graph.
        Placeholder for future conventions_parser.
        """
        # TODO: Implement conventions parser
        raise NotImplementedError("Conventions parser not yet implemented")

    def build_from_tech_analysis(self, markdown_path: Path, feature_slug: str) -> Dict[str, Any]:
        """
        Parse tech analysis markdown and build graph.
        Placeholder for future tech_analysis_parser.
        """
        # TODO: Implement tech analysis parser
        raise NotImplementedError("Tech analysis parser not yet implemented")

    def rebuild_feature(self, feature_slug: str, memory_dir_search: Path) -> Dict[str, Any]:
        """
        Rebuild graph for feature by discovering all related markdown files.
        Searches for: requirements-{slug}.md, tech-analysis-{slug}.md, etc.
        """
        all_entities: List[Entity] = []
        all_relationships: List[Relationship] = []
        sources = []

        # Find requirements file
        req_pattern = f"*requirements-{feature_slug}.md"
        for req_file in memory_dir_search.glob(req_pattern):
            parser = RequirementsParser(req_file)
            entities, rels = parser.parse()
            all_entities.extend(entities)
            all_relationships.extend(rels)
            sources.append(str(req_file))

        # TODO: Find and parse tech-analysis, conventions, etc.

        # Save consolidated graph
        if all_entities:
            self.store.save_graph(feature_slug, all_entities, all_relationships)

        return {
            'feature_slug': feature_slug,
            'entity_count': len(all_entities),
            'relationship_count': len(all_relationships),
            'sources': sources
        }

    def sync_all(self, memory_dir_search: Path) -> List[Dict[str, Any]]:
        """
        Sync all features by discovering markdown files and rebuilding graphs.
        Returns list of sync results per feature.
        """
        results = []

        # Find all requirements files
        for req_file in memory_dir_search.glob("*requirements-*.md"):
            if req_file.name.startswith('EXAMPLE-') or req_file.name.startswith('TEMPLATE-'):
                continue

            # Extract feature slug from filename
            # Pattern: requirements-{slug}.md or {slug}-requirements.md
            slug = req_file.stem
            if slug.startswith('requirements-'):
                slug = slug[len('requirements-'):]
            elif slug.endswith('-requirements'):
                slug = slug[:-len('-requirements')]

            result = self.build_from_requirements(req_file, slug)
            results.append(result)

        return results

    def get_feature_summary(self, feature_slug: str) -> Dict[str, Any]:
        """Get summary stats for feature graph"""
        entities = self.store.query_entities(feature_slug)
        relationships = self.store.query_relationships(feature_slug)

        entity_counts = {}
        for entity in entities:
            etype = entity['type']
            entity_counts[etype] = entity_counts.get(etype, 0) + 1

        rel_counts = {}
        for rel in relationships:
            rtype = rel['type']
            rel_counts[rtype] = rel_counts.get(rtype, 0) + 1

        return {
            'feature_slug': feature_slug,
            'total_entities': len(entities),
            'total_relationships': len(relationships),
            'entity_counts': entity_counts,
            'relationship_counts': rel_counts
        }
