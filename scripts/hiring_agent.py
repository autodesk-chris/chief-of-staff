#!/usr/bin/env python3
"""
Hiring Agent for Julie - handles CV screening, interview prep, and evaluation.
"""

import re
from pathlib import Path
from datetime import datetime

# Base paths
HIRING_PATH = Path(__file__).parent.parent / 'Work' / 'People' / 'Hiring'


def find_role_folder(role_name):
    """
    Find a role folder using fuzzy matching.

    Args:
        role_name: The role to find (e.g., "Community Manager")

    Returns:
        tuple: (folder_path, folder_name) or (None, None) if not found
    """
    if not HIRING_PATH.exists():
        return None, None

    role_lower = role_name.lower().replace(' ', '_').replace('-', '_')

    # Try exact match first
    for folder in HIRING_PATH.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            folder_lower = folder.name.lower().replace(' ', '_').replace('-', '_')
            if folder_lower == role_lower:
                return folder, folder.name

    # Try partial match
    best_match = None
    best_score = 0

    for folder in HIRING_PATH.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            folder_lower = folder.name.lower()
            # Check if all words in role_name appear in folder name
            words = role_name.lower().split()
            matches = sum(1 for word in words if word in folder_lower)
            score = matches / len(words) if words else 0

            if score > best_score:
                best_score = score
                best_match = (folder, folder.name)

    if best_score >= 0.5:
        return best_match

    return None, None


def find_eval_guides(role_folder):
    """Find evaluation guides, outlines, or briefs in a role folder."""
    keywords = ['evaluation_guide', 'outline', 'brief']
    return [f for f in role_folder.iterdir()
            if f.is_file() and f.suffix.lower() in ['.md', '.pdf', '.docx']
            and any(kw in f.stem.lower() for kw in keywords)]


def find_cv(role_folder, candidate_name, include_shortlisted=True):
    """
    Find a CV by candidate name in the role folder.

    Args:
        role_folder: Path to the role folder
        candidate_name: Name to search for
        include_shortlisted: Whether to also search Shortlisted folder

    Returns:
        tuple: (cv_path, location) or (None, None) if not found
    """
    candidate_normalized = candidate_name.lower().replace(' ', '_').replace('-', '_')

    # Search CVs folder
    cvs_folder = role_folder / 'CVs'
    if cvs_folder.exists():
        for cv_file in cvs_folder.iterdir():
            if cv_file.is_file() and cv_file.suffix.lower() in ['.pdf', '.docx', '.doc']:
                stem_normalized = cv_file.stem.lower().replace(' ', '_').replace('-', '_')
                if candidate_normalized in stem_normalized:
                    return cv_file, 'CVs'

    # Search Shortlisted folder
    if include_shortlisted:
        shortlisted_folder = role_folder / 'Shortlisted'
        if shortlisted_folder.exists():
            for cv_file in shortlisted_folder.iterdir():
                if cv_file.is_file() and cv_file.suffix.lower() in ['.pdf', '.docx', '.doc']:
                    stem_normalized = cv_file.stem.lower().replace(' ', '_').replace('-', '_')
                    if candidate_normalized in stem_normalized:
                        return cv_file, 'Shortlisted'

    return None, None


def find_jd(role_folder):
    """
    Find the job description in a role folder.

    Returns:
        Path or None
    """
    # Look for JD files (case-insensitive matching)
    jd_keywords = ['jd', 'job description', 'job_description', 'position', 'role']
    valid_extensions = ['.pdf', '.md', '.docx', '.doc']

    for f in role_folder.iterdir():
        if f.is_file() and f.suffix.lower() in valid_extensions:
            name_lower = f.stem.lower()
            if any(kw in name_lower for kw in jd_keywords):
                return f

    # Also check for any PDF that might be a JD
    for f in role_folder.iterdir():
        if f.is_file() and f.suffix.lower() == '.pdf':
            if 'cv' not in f.name.lower() and 'resume' not in f.name.lower():
                return f

    return None


def list_cvs(role_folder):
    """
    List all CVs in a role folder.

    Returns:
        list of (filename, location) tuples
    """
    cvs = []

    cvs_folder = role_folder / 'CVs'
    if cvs_folder.exists():
        for cv_file in cvs_folder.iterdir():
            if cv_file.is_file() and cv_file.suffix.lower() in ['.pdf', '.docx', '.doc']:
                cvs.append((cv_file.name, 'CVs', cv_file))

    shortlisted_folder = role_folder / 'Shortlisted'
    if shortlisted_folder.exists():
        for cv_file in shortlisted_folder.iterdir():
            if cv_file.is_file() and cv_file.suffix.lower() in ['.pdf', '.docx', '.doc']:
                if 'cv' in cv_file.name.lower() or 'resume' in cv_file.name.lower():
                    cvs.append((cv_file.name, 'Shortlisted', cv_file))

    return cvs


def list_available_roles():
    """List all available role folders."""
    if not HIRING_PATH.exists():
        return []

    roles = []
    for folder in HIRING_PATH.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            roles.append(folder.name)
    return sorted(roles)


def handle_hiring_command(command_text):
    """
    Handle hiring-related commands and return instructions for Claude.

    Args:
        command_text: The full command string

    Returns:
        str: Result message with instructions
    """
    command_lower = command_text.lower()

    # Setup role command
    if command_lower.startswith('setup role:'):
        role_name = command_text[11:].strip()
        return handle_setup_role(role_name)

    # Screen CVs (batch) command
    if command_lower.startswith('screen cvs:'):
        role_name = command_text[11:].strip()
        return handle_screen_cvs(role_name)

    # Review CV (single) command
    if command_lower.startswith('review cv:'):
        args = command_text[10:].strip()
        return handle_review_cv(args)

    # Shortlist command
    if command_lower.startswith('shortlist:'):
        args = command_text[10:].strip()
        return handle_shortlist(args)

    # Interview prep command
    if command_lower.startswith('interview prep:'):
        args = command_text[15:].strip()
        return handle_interview_prep(args)

    # Interview eval command
    if command_lower.startswith('interview eval:'):
        args = command_text[15:].strip()
        return handle_interview_eval(args)

    # Candidate summary command
    if command_lower.startswith('candidate summary:'):
        name = command_text[18:].strip()
        return handle_candidate_summary(name)

    return f"✗ Unknown hiring command: {command_text}"


def parse_name_and_role(args):
    """
    Parse 'name for role' format.

    Args:
        args: String like "Sarah Williamson for Community Manager"

    Returns:
        tuple: (candidate_name, role_name) or (None, None) if invalid
    """
    match = re.match(r'(.+?)\s+for\s+(.+)', args, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None


def handle_setup_role(role_name):
    """Handle setup role command."""
    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        available = list_available_roles()
        return f"""✗ Role folder not found: '{role_name}'

Available roles: {', '.join(available) if available else 'None found'}

Create a folder at: Work/People/Hiring/{role_name.replace(' ', '_')}/
Then add the job description PDF."""

    jd_path = find_jd(role_folder)

    if not jd_path:
        return f"""✗ No job description found in: {role_folder}

Please add a JD file (PDF or markdown) to the role folder."""

    output_path = role_folder / f"{folder_name.replace(' ', '_')}_evaluation_guide.md"

    return f"""✓ Ready to setup role: {folder_name}

**Job description:** {jd_path.name}
**Output:** {output_path}

**Next steps:**
1. Read the JD: {jd_path}
2. Read persona: .claude/personas/AGENT_HIRING.md (Workflow: Setup Role)
3. Generate evaluation guide with 6-8 competencies
4. Save to: {output_path}"""


def handle_screen_cvs(role_name):
    """Handle batch CV screening command."""
    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        available = list_available_roles()
        return f"""✗ Role folder not found: '{role_name}'

Available roles: {', '.join(available) if available else 'None found'}"""

    cvs = list_cvs(role_folder)
    unscreened = [(name, loc, path) for name, loc, path in cvs if loc == 'CVs']

    if not unscreened:
        return f"""✗ No CVs found in: {role_folder}/CVs/

CVs should be placed in the CVs/ subfolder for screening."""

    # Check for evaluation guide
    eval_guide = find_eval_guides(role_folder)

    cv_list = '\n'.join([f"  - {name}" for name, _, _ in unscreened])

    return f"""✓ Ready to screen {len(unscreened)} CVs for: {folder_name}

**CVs to screen:**
{cv_list}

**Evaluation guide:** {eval_guide[0].name if eval_guide else '⚠️ Not found - run setup role first'}

**Next steps:**
1. Read evaluation guide (if available) or JD
2. Read each CV
3. Assess against criteria
4. Generate screening summary with Strong/Moderate/Weak ratings
5. Save to: {role_folder}/cv_screening_{datetime.now().strftime('%Y-%m-%d')}.md"""


def handle_review_cv(args):
    """Handle single CV review command."""
    candidate_name, role_name = parse_name_and_role(args)

    if not candidate_name or not role_name:
        return f"""✗ Invalid format. Use: review CV: [name] for [role]

Example: review CV: Sarah Williamson for Community Manager"""

    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        available = list_available_roles()
        return f"""✗ Role folder not found: '{role_name}'

Available roles: {', '.join(available) if available else 'None found'}"""

    cv_path, location = find_cv(role_folder, candidate_name)

    if not cv_path:
        cvs = list_cvs(role_folder)
        cv_list = '\n'.join([f"  - {name} ({loc})" for name, loc, _ in cvs])
        return f"""✗ CV not found for: '{candidate_name}'

Available CVs in {folder_name}:
{cv_list if cvs else '  None found'}"""

    # Check for evaluation guide
    eval_guide = find_eval_guides(role_folder)
    jd_path = find_jd(role_folder)

    return f"""✓ Ready to review CV: {candidate_name} for {folder_name}

**CV location:** {cv_path}
**Evaluation guide:** {eval_guide[0] if eval_guide else '⚠️ Not found'}
**JD:** {jd_path if jd_path else '⚠️ Not found'}

**Next steps:**
1. Read the CV: {cv_path}
2. Read evaluation guide or JD
3. Assess strengths and gaps
4. Generate screening notes
5. Display results to user"""


def handle_shortlist(args):
    """Handle shortlist candidate command."""
    candidate_name, role_name = parse_name_and_role(args)

    if not candidate_name or not role_name:
        return f"""✗ Invalid format. Use: shortlist: [name] for [role]

Example: shortlist: Sarah Williamson for Community Manager"""

    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        return f"✗ Role folder not found: '{role_name}'"

    cv_path, location = find_cv(role_folder, candidate_name, include_shortlisted=False)

    if not cv_path:
        # Check if already shortlisted
        cv_shortlisted, _ = find_cv(role_folder, candidate_name)
        if cv_shortlisted:
            return f"✓ {candidate_name} is already in Shortlisted folder"
        return f"✗ CV not found for: '{candidate_name}' in CVs folder"

    shortlisted_folder = role_folder / 'Shortlisted'
    dest_path = shortlisted_folder / cv_path.name
    screen_path = shortlisted_folder / f"{candidate_name.replace(' ', '_')}_cv_screen.md"
    prep_path = shortlisted_folder / f"{candidate_name.replace(' ', '_')}_interview_prep.md"

    return f"""✓ Ready to shortlist: {candidate_name} for {folder_name}

**Actions to perform:**
1. Create folder if needed: {shortlisted_folder}
2. Move CV: {cv_path} → {dest_path}
3. Create CV screen notes: {screen_path}
4. Create interview prep: {prep_path}

**After moving, run:**
  interview prep: {candidate_name} for {role_name}"""


def handle_interview_prep(args):
    """Handle interview prep command."""
    candidate_name, role_name = parse_name_and_role(args)

    if not candidate_name or not role_name:
        return f"""✗ Invalid format. Use: interview prep: [name] for [role]

Example: interview prep: Sarah Williamson for Community Manager"""

    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        return f"✗ Role folder not found: '{role_name}'"

    cv_path, location = find_cv(role_folder, candidate_name)

    if not cv_path:
        return f"✗ CV not found for: '{candidate_name}'"

    # Check for existing materials
    eval_guide = find_eval_guides(role_folder)
    screen_notes = list((role_folder / 'Shortlisted').glob(f'*{candidate_name.split()[0].lower()}*screen*')) if (role_folder / 'Shortlisted').exists() else []

    output_path = role_folder / 'Shortlisted' / f"{candidate_name.replace(' ', '_')}_interview_prep.md"

    return f"""✓ Ready to prepare interview: {candidate_name} for {folder_name}

**CV:** {cv_path}
**Evaluation guide:** {eval_guide[0] if eval_guide else '⚠️ Not found'}
**Existing screen notes:** {screen_notes[0] if screen_notes else 'None'}
**Output:** {output_path}

**Process:**
1. Read the CV
2. Extract company names from work history
3. Web search each company for context
4. Read evaluation guide
5. Generate targeted questions:
   - Claims to verify
   - Gaps to probe
   - Competency questions
   - Red flags to watch
6. Save interview prep document"""


def handle_interview_eval(args):
    """Handle interview evaluation command."""
    candidate_name, role_name = parse_name_and_role(args)

    if not candidate_name or not role_name:
        return f"""✗ Invalid format. Use: interview eval: [name] for [role]

Example: interview eval: Tom Hamilton for Community Programme Manager"""

    role_folder, folder_name = find_role_folder(role_name)

    if not role_folder:
        return f"✗ Role folder not found: '{role_name}'"

    cv_path, location = find_cv(role_folder, candidate_name)
    eval_guide = find_eval_guides(role_folder)

    output_path = role_folder / 'Shortlisted' / f"{candidate_name.replace(' ', '_')}_interview_notes.md"

    return f"""✓ Ready to evaluate: {candidate_name} for {folder_name}

**Step 1: Find Granola meetings**
Search for meetings matching "{candidate_name}" and present matches to user for confirmation.

**Step 2: After user confirms meetings, gather:**
- CV: {cv_path if cv_path else '⚠️ Not found'}
- Evaluation guide: {eval_guide[0] if eval_guide else '⚠️ Not found'}
- Interview transcript from confirmed Granola meetings

**Step 3: Evaluate**
- Score each competency from evaluation guide
- Primary evidence: what they said/demonstrated in interview
- Secondary: CV claims vs demonstrated

**Step 4: Output**
- Show evaluation to user
- After approval, save to: {output_path}

**To search Granola, use:**
mcp__granola__query_granola_meetings(query="{candidate_name}")"""


def handle_candidate_summary(name):
    """Handle candidate summary command."""
    # Search all role folders for this candidate
    found_in = []

    if HIRING_PATH.exists():
        for role_folder in HIRING_PATH.iterdir():
            if role_folder.is_dir() and not role_folder.name.startswith('.'):
                shortlisted = role_folder / 'Shortlisted'
                if shortlisted.exists():
                    notes = list(shortlisted.glob(f'*{name.split()[0].lower()}*notes*'))
                    if notes:
                        found_in.append((role_folder.name, notes))

    if not found_in:
        return f"""✗ No interview notes found for: '{name}'

Candidate must have interview notes in a Shortlisted folder.
Run interview eval first, then generate summary."""

    role_name, notes_files = found_in[0]

    return f"""✓ Ready to generate summary for: {name}

**Found in role:** {role_name}
**Interview notes:** {[n.name for n in notes_files]}

**Process:**
1. Read interview notes
2. Generate concise bullet-point summary
3. Include: background, strengths, concerns, recommendation
4. Format for sharing with hiring team"""


if __name__ == '__main__':
    # Test commands
    test_commands = [
        'setup role: Community Programme Manager',
        'screen CVs: Community Programme Manager',
        'review CV: Sarah Williamson for Community Programme Manager',
        'shortlist: Sarah Williamson for Community Programme Manager',
        'interview prep: Tom Hamilton for Community Programme Manager',
        'interview eval: Tom Hamilton for Community Programme Manager',
        'candidate summary: Tom Hamilton',
    ]

    print("Testing hiring agent commands:\n")
    for cmd in test_commands:
        print(f"Command: {cmd}")
        print("-" * 40)
        result = handle_hiring_command(cmd)
        print(result)
        print("\n")
