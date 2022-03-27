# Eisenhower: Assign issue priority labels based on issue content
Eisenhower is a GitHub action that adds Eisenhower matrix priority labels to issues based on the content of the issue.

## What it does

Eisenhower will take the following steps,
- Look through all issues
- Search for required string
- Assign label based on string found. 

Strings Eisenhower looks for are,

IF

> ### Impact
> High
> 
> ### Urgency
> Now

THEN assign label `P1`

IF

> ### Impact
> High
> 
> ### Urgency
> Later

THEN assign label `P2`

IF

> ### Impact
> Low
> 
> ### Urgency
> Now

THEN assign label `P3`

IF

> ### Impact
> Low
> 
> ### Urgency
> Later

THEN assign label `P4`

## Requirements
### Issue templates
In your `repo`/.github/ISSUE_TEMPLATE directory, ensure that your issue templates include the following.
```yml
body:
  - type: dropdown
    id: impact
    attributes:
      label: Impact
      description: How important is this?
      options:
        - High
        - Low
    validations:
      required: true
  - type: dropdown
    id: urgency
    attributes:
      label: Urgency
      description: Should this be fixed now or can it be done later?
      options:
        - Now
        - Later
    validations:
      required: true
```

This ensures that all subsequent issues will have the strings that we need to search for.

### Priority labels
Add the following labels to your repo
- P1
- P2
- P3
- P4

## Thanks
Big thanks to,
- [Jacob Tomlinson](https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/)