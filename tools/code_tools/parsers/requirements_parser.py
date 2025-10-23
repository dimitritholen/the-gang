"""
Parse requirements markdown files and extract entities/relationships.

Expected structure (based on EXAMPLE-requirements-user-authentication.md):
- Feature metadata (title, status, stakeholders)
- Functional requirements (FR-XXX)
- Non-functional requirements (NFR-XXX)
- Dependencies, constraints, out-of-scope
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from ..graph import (
    Entity, Relationship, Feature, Requirement,
    RequirementType, Priority, RelationshipType
)


class RequirementsParser:
    """Parse requirements markdown into graph entities"""

    def __init__(self, markdown_path: Path):
        self.path = markdown_path
        self.content = markdown_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')

    def parse(self) -> Tuple[List[Entity], List[Relationship]]:
        """Parse markdown and return entities + relationships"""
        entities = []
        relationships = []

        # Parse feature metadata
        feature = self._parse_feature_metadata()
        entities.append(feature)

        # Parse functional requirements
        fr_entities, fr_rels = self._parse_functional_requirements(feature.id)
        entities.extend(fr_entities)
        relationships.extend(fr_rels)

        # Parse non-functional requirements
        nfr_entities, nfr_rels = self._parse_non_functional_requirements(feature.id)
        entities.extend(nfr_entities)
        relationships.extend(nfr_rels)

        # Parse dependencies
        dep_rels = self._parse_dependencies(feature.id)
        relationships.extend(dep_rels)

        return entities, relationships

    def _parse_feature_metadata(self) -> Feature:
        """Extract feature name, status, stakeholders from header"""
        # Extract title (first # heading)
        title = None
        for line in self.lines:
            if line.startswith('# '):
                title = line[2:].strip()
                # Remove "Requirements: " prefix if present
                title = re.sub(r'^Requirements:\s*', '', title)
                break

        if not title:
            title = self.path.stem

        # Extract metadata fields
        status = self._extract_field(r'\*\*Status\*\*:\s*(.+)')
        stakeholders = self._extract_list_field(r'\*\*Stakeholders\*\*:\s*(.+)')
        created = self._extract_field(r'\*\*Created\*\*:\s*(.+)')

        # Extract tags/keywords
        tags = []
        keywords_match = self._extract_field(r'\*\*Keywords\*\*:\s*(.+)')
        if keywords_match:
            tags = [k.strip() for k in keywords_match.split(',')]

        tags_match = self._extract_field(r'\*\*Tags\*\*:\s*(.+)')
        if tags_match:
            tags.extend([t.strip() for t in tags_match.split(',')])

        # Generate feature ID from filename
        feature_id = f"feature:{self.path.stem}"

        return Feature(
            id=feature_id,
            name=title,
            status=status or "unknown",
            priority=None,  # Not in header, extract from requirements if needed
            dependencies=[],  # Parsed separately
            tags=tags,
            source_file=str(self.path),
            metadata={
                'stakeholders': stakeholders,
                'created': created
            }
        )

    def _parse_functional_requirements(self, feature_id: str) -> Tuple[List[Requirement], List[Relationship]]:
        """Parse FR-XXX requirements sections"""
        return self._parse_requirements_section(
            feature_id,
            r'#### (FR-\d+):\s*(.+)',
            RequirementType.FUNCTIONAL
        )

    def _parse_non_functional_requirements(self, feature_id: str) -> Tuple[List[Requirement], List[Relationship]]:
        """Parse NFR-XXX requirements from tables"""
        requirements = []
        relationships = []

        # Find NFR sections (Performance, Security, Availability, Compliance)
        nfr_sections = {
            'Performance': RequirementType.PERFORMANCE,
            'Security': RequirementType.SECURITY,
            'Availability': RequirementType.AVAILABILITY,
            'Compliance': RequirementType.COMPLIANCE
        }

        for section_name, req_type in nfr_sections.items():
            section_reqs, section_rels = self._parse_nfr_table(
                feature_id,
                section_name,
                req_type
            )
            requirements.extend(section_reqs)
            relationships.extend(section_rels)

        return requirements, relationships

    def _parse_requirements_section(self, feature_id: str, pattern: str, req_type: RequirementType) -> Tuple[List[Requirement], List[Relationship]]:
        """Parse requirements with pattern like FR-001: Title"""
        requirements = []
        relationships = []
        current_req = None
        in_acceptance = False
        acceptance_criteria = []

        for i, line in enumerate(self.lines):
            # Match requirement header
            match = re.match(pattern, line)
            if match:
                # Save previous requirement
                if current_req:
                    current_req.acceptance_criteria = acceptance_criteria
                    requirements.append(current_req)
                    relationships.append(Relationship(
                        source_id=feature_id,
                        target_id=current_req.id,
                        type=RelationshipType.REQUIRES
                    ))

                req_id = match.group(1)
                req_name = match.group(2).strip()
                acceptance_criteria = []
                in_acceptance = False

                # Extract description, priority, user story from following lines
                description = None
                priority_str = None
                user_story = None

                for j in range(i + 1, min(i + 30, len(self.lines))):
                    next_line = self.lines[j]

                    # Check for next requirement
                    if re.match(pattern, next_line) or next_line.startswith('---'):
                        break

                    # Extract fields
                    if next_line.startswith('**Description**:'):
                        description = next_line.split(':', 1)[1].strip()
                    elif next_line.startswith('**Priority**:'):
                        priority_str = next_line.split(':', 1)[1].strip().lower()
                    elif next_line.startswith('**User Story**:'):
                        user_story = next_line.split(':', 1)[1].strip()
                    elif next_line.startswith('**Acceptance Criteria**:'):
                        in_acceptance = True
                    elif in_acceptance and next_line.strip().startswith('- [ ]'):
                        acceptance_criteria.append(next_line.strip()[5:].strip())

                # Map priority
                priority = Priority.MEDIUM
                if priority_str:
                    if 'high' in priority_str:
                        priority = Priority.HIGH
                    elif 'low' in priority_str:
                        priority = Priority.LOW

                current_req = Requirement(
                    id=f"req:{req_id}",
                    name=req_name,
                    req_type=req_type,
                    priority=priority,
                    acceptance_criteria=[],
                    parent_feature=feature_id,
                    user_story=user_story,
                    source_file=str(self.path),
                    metadata={'description': description}
                )

        # Save last requirement
        if current_req:
            current_req.acceptance_criteria = acceptance_criteria
            requirements.append(current_req)
            relationships.append(Relationship(
                source_id=feature_id,
                target_id=current_req.id,
                type=RelationshipType.REQUIRES
            ))

        return requirements, relationships

    def _parse_nfr_table(self, feature_id: str, section_name: str, req_type: RequirementType) -> Tuple[List[Requirement], List[Relationship]]:
        """Parse NFR table format: | ID | Requirement | Target Metric | Priority |"""
        requirements = []
        relationships = []

        # Find section header
        section_idx = None
        for i, line in enumerate(self.lines):
            if f"### {section_name}" in line:
                section_idx = i
                break

        if section_idx is None:
            return requirements, relationships

        # Parse table rows
        in_table = False
        for i in range(section_idx, min(section_idx + 50, len(self.lines))):
            line = self.lines[i]

            # Check for table header
            if line.startswith('| ID |'):
                in_table = True
                continue

            # Skip separator row
            if in_table and line.startswith('|---'):
                continue

            # End of table
            if in_table and not line.startswith('|'):
                break

            # Parse row
            if in_table and line.startswith('|'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3:
                    req_id = parts[0]
                    req_name = parts[1]
                    target_metric = parts[2] if len(parts) >= 3 else None
                    priority_str = parts[3].lower() if len(parts) >= 4 else 'medium'

                    # Map priority
                    priority = Priority.MEDIUM
                    if 'high' in priority_str:
                        priority = Priority.HIGH
                    elif 'low' in priority_str:
                        priority = Priority.LOW

                    req = Requirement(
                        id=f"req:{req_id}",
                        name=req_name,
                        req_type=req_type,
                        priority=priority,
                        parent_feature=feature_id,
                        target_metric=target_metric,
                        source_file=str(self.path)
                    )
                    requirements.append(req)
                    relationships.append(Relationship(
                        source_id=feature_id,
                        target_id=req.id,
                        type=RelationshipType.REQUIRES
                    ))

        return requirements, relationships

    def _parse_dependencies(self, feature_id: str) -> List[Relationship]:
        """Parse Dependencies section for system/feature dependencies"""
        relationships = []

        # Find Dependencies section
        dep_idx = None
        for i, line in enumerate(self.lines):
            if line.startswith('## Dependencies'):
                dep_idx = i
                break

        if dep_idx is None:
            return relationships

        # Extract dependency mentions (simple text extraction)
        # More sophisticated: parse "Feature Dependencies" subsection
        for i in range(dep_idx, min(dep_idx + 30, len(self.lines))):
            line = self.lines[i]
            if line.startswith('## '):  # Next section
                break

            # Look for "depends on" patterns
            # Example: "User profile management feature will depend on this authentication system"
            # This is informational but doesn't give us structured dependency IDs
            # In practice, dependencies would be captured via cross-references
            pass

        return relationships

    def _extract_field(self, pattern: str) -> Optional[str]:
        """Extract single field value using regex"""
        for line in self.lines:
            match = re.search(pattern, line)
            if match:
                return match.group(1).strip()
        return None

    def _extract_list_field(self, pattern: str) -> List[str]:
        """Extract comma-separated list field"""
        value = self._extract_field(pattern)
        if value:
            return [item.strip() for item in value.split(',')]
        return []
