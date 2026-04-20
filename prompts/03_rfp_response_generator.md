# #03 RFP Response Generator

**Use case:** Parallel proposal writing with cross-referenced requirements and consistency checks.

---

Create an agent team to respond to a Request for Proposal.

The RFP document is here:
https://canadabuys.canada.ca/en/tender-opportunities/tender-notice/bc006-2026

**Our company:** We are a 15-person AI consulting firm specializing in building custom automation workflows for mid-market companies. We use tools like Claude Code, n8n, and Supabase. Our average project size is $25K-$75K and we've completed 40+ projects in the last 18 months. Our differentiator is that we build systems clients can maintain themselves after handoff.

Spawn 4 teammates:

1. **RFP Analyst** — Read the full RFP and extract: all explicit requirements (numbered list), evaluation criteria and their weights, submission requirements (format, deadline, page limits), key questions or ambiguities that need clarification. Save analysis to outputs/agent_teams_demo/rfp_response/rfp_analysis.md. **This must complete before Section Writers begin.**

2. **Company Capability Researcher** — Read our company information above and build a capability matrix that maps our strengths to common RFP categories: technical approach, team qualifications, past performance, management approach, pricing strategy. Identify 3-5 differentiators. Save to outputs/agent_teams_demo/rfp_response/capability_matrix.md. **This must complete before Section Writers begin.**

3. **Section Writer A** — Using the RFP analysis and capability matrix, write: Executive Summary (1 page), Technical Approach section, Management Approach section. Save to outputs/agent_teams_demo/rfp_response/proposal_sections_a.md.

4. **Section Writer B** — Using the RFP analysis and capability matrix, write: Team Qualifications section (with placeholder bios), Past Performance section (with placeholder case studies), Pricing Narrative (not actual numbers — the strategic framing). Save to outputs/agent_teams_demo/rfp_response/proposal_sections_b.md.

After both Section Writers finish, review all sections for: consistent tone and terminology, no contradictions between sections, every RFP requirement addressed (cross-reference against the Analyst's checklist), flag any requirements we didn't address.

Save final assembled proposal to outputs/agent_teams_demo/rfp_response/full_proposal.md.
