from typing import Tuple
import numpy as np
from flask import Flask, render_template, redirect, url_for, request, jsonify
import GenerateSudoku as Gs
import SolveSudoku as SS
import requests
from requests.exceptions import JSONDecodeError

app = Flask(__name__)

def rowList(item):
    items = item.replace("[", '')
    items = items.replace("]", '')
    items = items.replace("\"", '')
    items = items.split(",")

    row = list(map(int, items))
    return row


def get_repo_stats() -> Tuple[int, int]:
    try:
        response = requests.get('https://api.github.com/repos/UD-SJA/Program02')
        if response.status_code == 200:
            stats = response.json()
            return stats['stargazers_count'], stats['forks_count']
        else:
            print(f"Error: {response.status_code}")
            return 0, 0
    except JSONDecodeError:
        print("Error: JSONDecodeError")
        return 0, 0

@app.route("/", methods=["POST", "GET"])
def Index():
    if request.method == 'POST':
        level = request.form.get('level')
        New_Game = Gs.main(level)
        return jsonify(
            cell_A1=str(New_Game[0, 0]),
            cell_A2=str(New_Game[0, 1]),
            cell_A3=str(New_Game[0, 2]),
            cell_A4=str(New_Game[0, 3]),
            cell_B1=str(New_Game[1, 0]),
            cell_B2=str(New_Game[1, 1]),
            cell_B3=str(New_Game[1, 2]),
            cell_B4=str(New_Game[1, 3]),
            cell_C1=str(New_Game[2, 0]),
            cell_C2=str(New_Game[2, 1]),
            cell_C3=str(New_Game[2, 2]),
            cell_C4=str(New_Game[2, 3]),
            cell_D1=str(New_Game[3, 0]),
            cell_D2=str(New_Game[3, 1]),
            cell_D3=str(New_Game[3, 2]),
            cell_D4=str(New_Game[3, 3]),
        )
    else:
        stars, forks = get_repo_stats()
        return render_template("index.html", stars=stars, forks=forks)

@app.route("/SolveSudoku", methods=['POST'])
def SolveSudoku():
    row1 = rowList(request.form["row1"])
    row2 = rowList(request.form["row2"])
    row3 = rowList(request.form["row3"])
    row4 = rowList(request.form["row4"])
    initial_grid = np.array([row1, row2, row3, row4])
    sudoku_instance = SS.Sudoku(initial_grid)
    solution, _ = sudoku_instance.solve()
    return jsonify(
        cell_A1=str(solution[(0, 0)]),
        cell_A2=str(solution[(0, 1)]),
        cell_A3=str(solution[(0, 2)]),
        cell_A4=str(solution[(0, 3)]),
        cell_B1=str(solution[(1, 0)]),
        cell_B2=str(solution[(1, 1)]),
        cell_B3=str(solution[(1, 2)]),
        cell_B4=str(solution[(1, 3)]),
        cell_C1=str(solution[(2, 0)]),
        cell_C2=str(solution[(2, 1)]),
        cell_C3=str(solution[(2, 2)]),
        cell_C4=str(solution[(2, 3)]),
        cell_D1=str(solution[(3, 0)]),
        cell_D2=str(solution[(3, 1)]),
        cell_D3=str(solution[(3, 2)]),
        cell_D4=str(solution[(3, 3)])
        )



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/PrivacyPolicy")
def privacy():
    return render_template("Privacy.html")


if __name__ == "__main__":
    app.run(debug=True)
