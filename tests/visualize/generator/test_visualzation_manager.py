from app.visualize.generator.visualization_manager import VisualizationManager


def test_get_code_by_idx():
    code = """a = 3
    for i in range(5):
        print(i)
        if i < 2:
            print(i)
    """
    expected = ["a = 3", "for i in range(5):", "print(i)", "if i < 2:", "print(i)"]
    viz_manager = VisualizationManager(code)

    for i in range(len(expected)):
        assert viz_manager.get_code_by_idx(i + 1) == expected[i]
