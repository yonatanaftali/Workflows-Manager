import subprocess
import curses

WORKFLOW_ID = None


# Using curses to stop input propagation
def get_clean_input(message):
    INPUT = input(message)
    stdscr = curses.initscr()
    curses.noecho()
    curses.endwin()
    return INPUT


def list_workflows():
    subprocess.run(
        [f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows | jq '.workflows[] | .name,.id'"],
        shell=True,
    )


def select_workflow():
    global WORKFLOW_ID
    WORKFLOW_ID = get_clean_input("Enter workflow ID: ")


def list_runs():
    if not WORKFLOW_ID:
        print("No workflow selected!")
    else:
        subprocess.run(
            [
                f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs | jq '.workflow_runs[] | .id'"
            ],
            shell=True,
        )


def delete_runs():
    if not WORKFLOW_ID:
        print("No workflow selected!")
    else:
        subprocess.run(
            [
                f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs | jq '.workflow_runs[] | .id' | xargs -I{{}} gh api -X DELETE /repos/{OWNER}/{REPO}/actions/runs/{{}}"
            ],
            shell=True,
        )


def exit():
    print("Invalid choice! Exiting...")
    quit()


def main():
    global OWNER, REPO
    OWNER = get_clean_input("Enter your username/organization name: ")
    REPO = get_clean_input("Enter your repository name: ")
    while True:
        menu = {
            "1": ("List all workflows", list_workflows),
            "2": ("Select workflow", select_workflow),
            "3": ("List selected workflow runs", list_runs),
            "4": ("Delete selected workflow runs", delete_runs),
            "5": ("Quit", quit),
        }
        for key in sorted(menu.keys()):
            print(key + ": " + menu[key][0])
        ans = input("Enter your choice: ")
        menu.get(ans, [None, exit])[1]()


if __name__ == "__main__":
    main()
