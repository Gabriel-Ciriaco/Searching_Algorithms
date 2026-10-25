import matplotlib.pyplot as plt
import pytest

from app import RouteApp
from graph_visualizer import GraphVisualizer


ALGORITHMS = ["BFS", "UCS", "DFS", "DLS", "IDS", "Greedy", "A*"]


# All the text written in the bottom info card
def panel_text(app):
    return "\n".join(text.get_text() for text in app.ax_info.texts)


@pytest.fixture
def app():
    return RouteApp()


def test_app_starts_with_a_star(app):
    assert app.cur_algo == "A*"

    text = panel_text(app)

    assert "Algoritmo: A*" in text
    assert "Sucesso" in text
    assert "Presidente Prudente -> Marília -> Bauru" in text


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_app_runs_every_algorithm(app, algo):
    app.run_search(algo)

    text = panel_text(app)

    assert app.cur_algo == algo
    assert f"Algoritmo: {algo}" in text
    assert "Sucesso" in text
    assert algo in app.ax_map.get_title()


def test_app_shows_failure_for_unreachable_destination(app):
    app.on_change_destino("Ilha Solteira")

    text = panel_text(app)

    assert "Falha" in text
    assert "Nenhum caminho possível" in text


def test_app_benchmark_lists_every_algorithm(app):
    app.run_all()

    text = panel_text(app)

    assert app.cur_algo == "BENCHMARK"

    for algo in ["BFS", "UCS", "DFS", f"DLS (l={app.dls_limit})", "IDS", "Greedy", "A*"]:
        assert algo in text


def test_app_keeps_benchmark_when_city_changes(app):
    app.run_all()
    app.on_change_origem("Assis")

    assert app.cur_algo == "BENCHMARK"
    assert app.cur_origem == "Assis"


def test_dls_controls_change_the_limit(app):
    app.on_dls_plus(None)

    assert app.dls_limit == 3
    assert app.dls_label_text.get_text() == "L = 3"
    assert app.cur_algo == "DLS"


def test_dls_controls_stay_between_0_and_10(app):
    app.dls_limit = 0
    app.on_dls_minus(None)

    assert app.dls_limit == 0

    app.dls_limit = 10
    app.on_dls_plus(None)

    assert app.dls_limit == 10


def test_dls_cutoff_message_with_small_limit(app):
    # Presidente Prudente -> Bauru needs 2 hops
    app.dls_limit = 1
    app.run_search("DLS")

    assert "CORTE (CUTOFF)" in panel_text(app)


def test_graph_visualizer_draws_the_path(unesp, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)

    visualizer = GraphVisualizer()

    for city in unesp.values():
        visualizer.add_node(city)

    for city in unesp.values():
        for neighbour, cost in city.neighbours:
            visualizer.add_edge(city, neighbour, cost)

    visualizer.visualize(["Presidente Prudente", "Marília", "Bauru"], title="A*")

    assert visualizer.G.number_of_nodes() == 10
    assert visualizer.G.number_of_edges() == 11
    assert plt.gca().get_title() == "A*"
