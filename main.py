import curses
import subprocess
import sys

OWNER, REPO, WORKFLOW_ID = None, None, None


# Using curses to stop input propagation
def get_clean_input(message):
    user_input = input(message)
    curses.initscr()
    curses.noecho()
    curses.endwin()
    return user_input


def list_workflows():
    try:
        command = f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows | jq '.workflows[] | .name,.id'"  # pylint: disable=line-too-long
        subprocess.run([command], shell=True, check=True)
    except Exception as exception:
        print(f"Got error: {exception}")


def select_workflow():
    global WORKFLOW_ID
    WORKFLOW_ID = get_clean_input("Enter workflow ID: ")


def list_runs():
    if not WORKFLOW_ID:
        print("No workflow selected!")
    else:
        try:
            command = f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs | jq '.workflow_runs[] | .id'"  # pylint: disable=line-too-long
            subprocess.run([command], shell=True, check=True)
        except Exception as exception:
            print(f"Got error: {exception}")


def delete_runs():
    if not WORKFLOW_ID:
        print("No workflow selected!")
    else:
        try:
            command = f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs | jq '.workflow_runs[] | .id' | xargs -I{{}} gh api -X DELETE /repos/{OWNER}/{REPO}/actions/runs/{{}}"  # pylint: disable=line-too-long
            subprocess.run([command], shell=True, check=True)
        except Exception as exception:
            print(f"Got error: {exception}")


def exit_app():
    print("Invalid choice! Exiting...")
    sys.exit()


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
            "5": ("Exit", exit),
        }
        for key in sorted(menu.keys()):
            print(key + ": " + menu[key][0])
        ans = input("Enter your choice: ")
        menu.get(ans, [None, exit_app])[1]()


if __name__ == "__main__":
    main()
