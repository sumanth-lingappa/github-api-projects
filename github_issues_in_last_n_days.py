import requests
import datetime


def github_issues_in_n_days(url, days):
    owner, repo = url.split("/")[-2:]
    open_issues_in_last_n_days = 0
    closed_issues_in_last_n_days = 0
    updated_issues_in_last_n_days = 0
    ret_updated_issues = []
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    open_issues = requests.get(f"{url}?state=open&per_page=100").json()
    closed_issues = requests.get(f"{url}?state=closed&per_page=100").json()
    total_issues = open_issues + closed_issues
    ret_open_issues = []
    ret_closed_issues = []

    for issue in total_issues:
        created_at = issue["created_at"]  # 2021-06-09T15:00:00Z
        updated_at = issue["updated_at"]  # 2021-06-09T15:00:00Z
        closed_at = issue["closed_at"]  # 2021-06-09T15:00:00Z

        # convert created_at to datetime object
        created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        updated_at = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
        closed_at = (
            datetime.datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
            if closed_at
            else None
        )

        if created_at > datetime.datetime.now() - datetime.timedelta(days=days):
            open_issues_in_last_n_days += 1
            ret_open_issues.append({"title": issue["title"], "url": issue["html_url"]})
        if updated_at > datetime.datetime.now() - datetime.timedelta(days=days):
            updated_issues_in_last_n_days += 1
            ret_updated_issues.append(
                {"title": issue["title"], "url": issue["html_url"]}
            )
        if closed_at and closed_at > datetime.datetime.now() - datetime.timedelta(
            days=days
        ):
            closed_issues_in_last_n_days += 1
            ret_closed_issues.append(
                {"title": issue["title"], "url": issue["html_url"]}
            )

    return {
        "open_issues_in_last_n_days": open_issues_in_last_n_days,
        "closed_issues_in_last_n_days": closed_issues_in_last_n_days,
        "updated_issues_in_last_n_days": updated_issues_in_last_n_days,
        "open_issues": ret_open_issues,
        "closed_issues": ret_closed_issues,
        "updated_issues": ret_updated_issues,
    }


def dict_to_html_table(data, days):
    html = f"<h1>GitHub Issues in last {days} days</h1>"
    html += "<table border='1'>"
    html += "<tr>"
    html += f"<th>Open</th>"
    html += f"<th>Closed</th>"
    html += f"<th>Updated</th>"
    html += "</tr>"
    html += "<tr>"
    html += f"<td align='center'>{data['open_issues_in_last_n_days']}</td>"
    html += f"<td align='center'>{data['closed_issues_in_last_n_days']}</td>"
    html += f"<td align='center'>{data['updated_issues_in_last_n_days']}</td>"
    html += "</tr>"
    html += "</table>"
    html += "<br>"
    html += "<br>"

    html += f"<h2>Open Issues in the last {days} days</h2>"
    html += "<ol>"
    for issue in data["open_issues"]:
        html += f"<li><a href='{issue['url']}'>{issue['title']}</a></li>"
    html += "</ol>"
    html += "<br>"

    html += f"<h2>Updated Issues in the last {days} days</h2>"
    html += "<ol>"
    for issue in data["updated_issues"]:
        html += f"<li><a href='{issue['url']}'>{issue['title']}</a></li>"
    html += "</ol>"
    html += "<br>"

    html += f"<h2>Closed Issues in the last {days} days</h2>"
    html += "<ol>"
    for issue in data["closed_issues"]:
        html += f"<li><a href='{issue['url']}'>{issue['title']}</a></li>"
    html += "</ol>"
    html += "<br>"

    return html


if __name__ == "__main__":
    url = "www.github.com/google/guava"
    days = 7
    ret = github_issues_in_n_days(url, days)
    html = dict_to_html_table(ret, days)
    with open("output.html", "w") as f:
        f.write(html)
