from github import Github
import logging
import dotenv
import os

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

GH_ACCESS_TOKEN = os.getenv("GH_ACCESS_TOKEN")
GH_REPOSITORY = os.getenv("GH_REPOSITORY")

gh = Github(GH_ACCESS_TOKEN)
repo = gh.get_repo(GH_REPOSITORY)


POSSIBLE_PRIORITIES = [
    ["P1", "cc3232", "Issues that are important and urgent"],
    ["P2", "db7b2b", "Issues that are important but are not urgent"],
    ["P3", "2dc937", "Issues that are not important but are urgent"],
    ["P4", "87ceeb", "Issues that are not important and are not urgent"],
    ["P?", "e393ef", "Issues that are yet to be prioritized"],
]
POSSIBLE_PRIORITY_LABELS = [x[0] for x in POSSIBLE_PRIORITIES]

IMPACT_KEY = "### Impact"
URGENCY_KEY = "### Urgency"


def priority(issue_body):
    if issue_body is None:
        return -2

    if IMPACT_KEY not in issue_body and URGENCY_KEY not in issue_body:
        logging.info("Adding form to issue")
        return -2

    important = None
    urgent = None

    impact_line = (
        issue_body[
            issue_body.find(IMPACT_KEY)
            + len(IMPACT_KEY) : issue_body.find(URGENCY_KEY)
        ]
        .strip()
        .lower()
    )
    logging.info("Impact = " + impact_line)

    if "high" in impact_line:
        important = True
    elif "low" in impact_line:
        important = False

    urgency_line = (
        issue_body[
            issue_body.find(URGENCY_KEY)
            + len(URGENCY_KEY) : issue_body.find(URGENCY_KEY)
            + len(URGENCY_KEY)
            + 10
        ]
        .strip()
        .lower()
    )
    logging.info("Urgency = " + urgency_line)
    if "now" in urgency_line:
        urgent = True
    elif "later" in urgency_line:
        urgent = False

    if important is None or urgent is None:
        return -1

    if important and urgent:
        return 1
    if important and not urgent:
        return 2
    if not important and urgent:
        return 3
    if not important and not urgent:
        return 4
    return -1


def priority_label(priority_level):
    if priority_level == 1:
        return POSSIBLE_PRIORITY_LABELS[0]
    if priority_level == 2:
        return POSSIBLE_PRIORITY_LABELS[1]
    if priority_level == 3:
        return POSSIBLE_PRIORITY_LABELS[2]
    if priority_level == 4:
        return POSSIBLE_PRIORITY_LABELS[3]

    return POSSIBLE_PRIORITY_LABELS[4]


def required_labels(current_labels, required_priority):
    if current_labels is None:
        return [required_priority]

    labels_out = []
    for label in current_labels:
        if label not in POSSIBLE_PRIORITY_LABELS:
            labels_out.append(label)
            continue
        if label != required_priority:
            continue
    labels_out.append(required_priority)
    return labels_out


def get_label_names(labels):
    return [label.name for label in labels]


def add_form_to_body(current_body):
    form = "\n\n" "### Impact\n\n" "?\n\n" "### Urgency\n\n" "?"
    if current_body is not None:
        return current_body + form
    return form


def check_labels():
    repo_labels = get_label_names(repo.get_labels())
    for label in POSSIBLE_PRIORITIES:
        if label[0] not in repo_labels:
            logging.info("Creating label " + label[0])
            repo.create_label(name=label[0],
                              color=label[1],
                              description=label[2])
    return 0


def main():
    check_labels()
    open_issues = repo.get_issues(state="open")
    for issue in open_issues:
        logging.info("Checking issue " + str(issue.number))
        if issue.pull_request is not None:
            logging.info("Skipping pull request")
            continue
        body_priority = priority(issue.body)
        if body_priority == -2:
            new_body = add_form_to_body(issue.body)
            issue.edit(body=new_body)
        body_priority_label = priority_label(body_priority)
        logging.info(
            "Issue #" + str(issue.number) + " = " + body_priority_label
        )

        existing_labels = sorted(get_label_names(issue.labels))
        logging.info("Current labels = " + str(existing_labels))

        out_labels = sorted(required_labels(existing_labels, body_priority_label))
        logging.info("Required labels = " + str(out_labels))

        if existing_labels != out_labels:
            logging.info("Updating labels")
            issue.set_labels(*out_labels)
        logging.info("Completed issue #" + str(issue.number))
    return 0


main()
