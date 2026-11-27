# Coordinate new-hire tasks across HR and learning systems

**Class:** Microsoft solution idea. **Intent:** Give each new hire a visible checklist and make blocked tasks visible to the people able to resolve them.

## Components and flow

1. An HR-system event or authenticated conversation identifies the hire. Retrieve the approved start date, role and team from the HR information system. Use a stable hire identifier to create or locate the onboarding plan.
2. Copilot Studio answers questions from current SharePoint onboarding guidance. Collect documents through the candidate system, not chat. Map the verified role to required training, then use an authorized learning management system (LMS) connector for enrollment.
3. Record completion when the owning system acknowledges it. A manager uses Power Apps to view milestones, assign a blocker and follow up, without needing access to every candidate document.

**When to choose it:** Useful when onboarding spans systems and has role-specific variations. A checklist workflow alone is enough when there is no need for Q&A or personalization.

**Trust boundary:** Pre-hire and employee identities may differ; verify the mapping before revealing a checklist or connecting documents. A generated learning plan cannot override mandatory training or grant privileged access.

**Failure handling and acceptance:** If LMS enrollment fails, mark just that milestone pending and provide an owner. Reconcile by hire and course before retry. Test a changed start date and a repeated HR event; neither should create duplicate tasks or enrollments.

**Source:** [Microsoft Learn: Improve the new hire experience with a smart onboarding agent](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/onboarding-agent).
