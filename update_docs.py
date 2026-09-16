def run():
    with open('PROJECT_CONTEXT.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix existing mojibake from someone else
    content = content.replace('ðŸ“ ', '📝 ').replace('âœ…', '✅').replace('ðŸŽ¯', '🎯')

    new_update = '''### Last Updated: September 16, 2026

#### ✅ Dashboard Expansion & Infrastructure Fix (September 16, 2026)

**Status:** ✅ COMPLETED

**Files Created/Modified:**
- ✅ pp/dashboard/pages/graph.py - Refactored completely for better UX, entity exploration, and query limits.
- ✅ pp/dashboard/pages/risk.py - Fully implemented from placeholder status (264 lines).
- ✅ .venv/ - Destroyed broken environment and rebuilt a clean, working virtual environment.

**Features Implemented:**

1. **Risk Analytics Page (isk.py)** - Brand new implementation:
   - Configurable limits via sidebar controls (	op_n).
   - Top-level 5-column **KPI Overview** (Total Entities, Avg/Max Risk, Critical/High sums).
   - Side-by-side **Risk Distribution Charts** using Streamlit st.bar_chart().
   - Comprehensive multi-tab architecture separating DataTables for:
     - 🚨 Highest Risk Entities
     - 🔗 Dependency Risks (Supplier, Country, Tier-1/Tier-2)
     - 🕸️ Centrality Risks (Degree, Betweenness, Closeness)

2. **Graph Analytics Refactoring (graph.py)**:
   - Replaced static limits with sidebar controllers.
   - Refactored layout to use consistent standard columns and typography patterns.
   - Restored missing ender_relationship_distribution components.
   - Fully integrated ender_entity_explorer and raw tabular data functions from backend. 

3. **Development Environment Infrastructure**:
   - Diagnosed and repaired a corrupted .venv resulting from an interrupted local environment build and file locks.
   - Restored missing activation scripts and pip installers.

'''

    if '## Project Status & Changelog' in content:
        content = content.replace('## Project Status & Changelog\n', '## Project Status & Changelog\n\n' + new_update)
    else:
        content += '\n## Project Status & Changelog\n\n' + new_update
        
    content = content.replace('4. Integrate companies page into Streamlit app', '4. ✅ ~~Integrate companies page into Streamlit app~~ **COMPLETED (Sept 16, 2026)**')

    with open('PROJECT_CONTEXT.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    run()