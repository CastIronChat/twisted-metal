Herein lies all our boring administrivia: how we merge code, how we decide what to work on, naming conventions, etc.

# Trello board columns

- Triage: anything new goes here: musings, ideas, anything.  We may or may not do it.
- To Do: ticket has been approved in grooming session / in a call.  Has
sufficient detail and priority for anyone to self-assign and work on it.
- In Progress: self-explanatory
- Reviewing: ready for code review.  Tickets may ping-pong between Reviewing and In Progress
- Done: Work is done, acceptance criteria met, code is merged.  Or else we've decided we'll never do it.

# Backlog Refinement

Regular meetings to ensure everyone understands tickets, ensure every person is prepared to / capable of picking up a ticket.

- Once per week-ish, as part of our voice calls.
- Use the meeting to move items from Triage into To-Do.
- Tickets should already be on the board going into the meeting.
- Anyone who has something they want done, use the meeting to add it to the agenda.
  - Add ticket to "Triage" column and link to Agenda ticket ahead-of-time.
- Ensure everyone understands tickets
  - Anything moved into To Do should be spec-ed enough for someone to start
  implementing.

# Code Review

Before code can merge to `main` branch, requires:

- At least one approving review on the Github pull request
- Acceptance criteria from the Trello ticket have been met
  - Does the ticket lack acceptance criteria?  Add them.
  - Are they out-of-date?  Update them to match the pull request.
  - As necessary, move unfinished work to a new ticket.
- Feature has been demo'd to a teammate
- (Preferably) video-demo of the feature shared with team on Trello or Discord TBD

# Naming and style conventions

## Git branches

`descriptive-branch-name`

Git branches are all lowercase, with a descriptive name, words separated by
hyphens.

Delete the branch from Github once your PR has been merged.  Github has a button
to do this immediately after you merge.  This is safe; nothing is lost; we can
always re-create as necessary.
